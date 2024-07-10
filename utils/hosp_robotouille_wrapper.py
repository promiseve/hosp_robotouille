import gym
import pddlgym
import utils.robotouille_utils as robotouille_utils
import utils.pddlgym_utils as pddlgym_utils
from environments.env_generator.hosp_object_enums import Item


class HospRobotouilleWrapper(gym.Wrapper):
    """
    This wrapper wraps around the Hospital Robotouille environment from PDDLGym.

    This wrapper is necessary because while the PDDL language is powerful, it can be
    cumbersome to implement data-driven state such as treating patients, performing CPR,
    using AED, and providing ventilation. This does not mean it is impossible but rather 
    than littering the observation space with a bunch of predicates to represent time and 
    actions, we offload this to the wrapper's metadata.
    """

    def __init__(self, env, config, renderer):
        """
        Initialize the Hospital Robotouille wrapper.

        Args:
            env (PDDLGym Environment): The environment to wrap.
            config (dict): A configuration JSON with custom values.
        """
        super(HospRobotouilleWrapper, self).__init__(env)
        # The PDDLGym environment.
        self.env = env
        # The previous step of the environment.
        self.prev_step = None
        # The number of timesteps that have passed.
        self.timesteps = 0
        # The state of the environment (for non-PDDL states like actions on patients)
        self.state = {}
        # The configuration for this environment.
        self.config = config
        self.num_players = None
        self.planning_algorithm = []
        self.renderer = renderer

    def _interactive_starter_prints(self, expanded_truths):
        """
        This function prints the initial state of the environment and the valid actions.

        Args:
            expanded_truths (np.array): Array of 0s and 1s where 1 indicates the literal is true
        """
        print("\n" * 10)
        if self.timesteps % 10 == 0:
            print(f"You have made {self.timesteps} steps.")
        robotouille_utils.print_states(self.prev_step[0])
        print("\n")
        robotouille_utils.print_actions(self.env, self.prev_step[0], self.renderer)
        print(f"True Predicates: {expanded_truths.sum()}")

    def _handle_action(self, action):
        """
        This function handles the action taken by the environment.

        Args: action (str): The action to take.
        """
        if action == "noop":
            return self.prev_step
        action_name = action.predicate.name
        if action_name in ["givemedicine", "giveCPR", "giveAED", "giveVentilation"]:
            item = next(
                filter(
                    lambda typed_entity: typed_entity.var_type == "item",
                    action.variables,
                )
            )
            patient = next(
                filter(
                    lambda typed_entity: typed_entity.var_type == "station",
                    action.variables,
                )
            )
            if action_name == "givemedicine":
                self.state[patient.name] = {"treated": True}
            elif action_name == "giveCPR":
                self.state[patient.name] = {"resuscitated": True}
            elif action_name == "giveAED":
                self.state[patient.name] = {"defibrillated": True}
            elif action_name == "giveVentilation":
                self.state[patient.name] = {"ventilated": True}
            return self.prev_step
        return self.env.step(action)

    def _state_update(self):
        """
        This function updates the custom non-PDDL state of the environment.

        This function is called after every step in the environment. It can either update
        the custom state (e.g. incrementing the action time of a treatment) or directly
        modify the PDDL state (e.g. adding the isaeddefibrillated predicate to a patient that has been
        fully treated).

        Returns:
            new_env_state (PDDLGym State): The new state of the environment.
        """
        state_updates = []
        for patient, status_dict in self.state.items():
            for status, state in status_dict.items():
                if status == "treated" and state:
                    literal = pddlgym_utils.str_to_literal(f"istreated({patient}:station)")
                    state_updates.append(literal)
                elif status == "resuscitated" and state:
                    literal = pddlgym_utils.str_to_literal(f"iscprresuscitated({patient}:station)")
                    state_updates.append(literal)
                elif status == "defibrillated" and state:
                    literal = pddlgym_utils.str_to_literal(f"isaeddefibrillated({patient}:station)")
                    state_updates.append(literal)
                elif status == "ventilated" and state:
                    literal = pddlgym_utils.str_to_literal(f"isventilated({patient}:station)")
                    state_updates.append(literal)
        env_state = self.env.get_state()
        new_literals = env_state.literals.union(state_updates)
        new_env_state = pddlgym.structs.State(
            new_literals, env_state.objects, env_state.goal
        )
        self.env.set_state(new_env_state)
        return new_env_state

    def _count_players(self, obs):
        """
        This function counts the number of players in the environment.

        Args:
            obs (PDDLGym State): The current state of the environment.

        Returns:
            num_players (int): The number of players in the environment.
        """
        num_players = 0
        for literal in obs.literals:
            if "isrobot" in literal.predicate.name:
                num_players += 1
        return num_players

    def _current_selected_player(self, obs):
        """
        This function returns the current selected player in the environment.

        Returns:
            selected_player (str): The name of the selected player.
        """
        for literal in obs.literals:
            if "selected" == literal.predicate.name:
                return literal.variables[0].name

    def _change_selected_player(self, obs):
        """
        This function changes the player in the environment.

        Returns:
            new_env_state (PDDLGym State): The new state of the environment.
        """

        current_player = self._current_selected_player(obs)
        current_player_index = int(current_player[5:])
        next_player = current_player_index % self.num_players + 1
        next_player = f"robot{next_player}"
        action = f"select({current_player}:player,{next_player}:player)"
        try:
            action = robotouille_utils.create_action(
                self.env, obs, action, self.renderer
            )
        except Exception:
            print("Error in changing player")
            return self.prev_step
        return self.env.step(action)

    def _heuristic_function(self, obs):
        """
        This function is a heuristic function that is used to generate a plan.

        Args:
            obs (PDDLGym State): The current state of the environment.

        Returns: The measure of "goodness" of the state.
        """

        treated = False
        resuscitated = False
        defibrillated = False
        ventilated = False

        # See if goals (treatment, CPR, AED, ventilation) are met
        score = 0
        for clause in obs.goal.literals:
            for goal in clause.literals:
                for literal in obs.literals:
                    if goal == literal:
                        if goal.predicate == "istreated":
                            treated = True
                        if goal.predicate == "iscprresuscitated":
                            resuscitated = True
                        if goal.predicate == "isaeddefibrillated":
                            defibrillated = True
                        if goal.predicate == "isventilated":
                            ventilated = True

        if treated:
            score += 25
        if resuscitated:
            score += 25
        if defibrillated:
            score += 25
        if ventilated:
            score += 25

        return score

    def get_latest_info(self):
        """
        Get the latest info dictionary from the environment.

        Returns:
            dict: The latest info dictionary.
        """
        return self.prev_step[3] if self.prev_step else None

    def generate_plan(self, obs):
        goal = []
        return goal

    def test_step(self, action):
        obs, reward, done, info = self._handle_action(action)
        _, reward, done, info = self.prev_step
        self.prev_step = (obs, reward, done, info)
        return obs, reward, done, info

    def step(self, action=None, interactive=False):
        """
        This function steps the environment forward.

        Most of the output of this function comes from PDDLGym. The observation is a frozenset of
        PDDLGym literals (predicates), objects, and the goal. The reward is 1 if the goal is met and
        0 otherwise. The done flag is True if the goal is met and False otherwise.

        The info metadata is where the wrapper adds the interesting things. The info metadata consists of
        the following:
            - timesteps (int): The number of timesteps that have passed. Currently every action takes
                1 timestep.
            - expanded_truths (np.array): Array of 0s and 1s where 1 indicates the literal is true. PDDLGym
                only provides us with the predicates that are true, but we also need to know which predicates
                are false. This array includes the true and false predicates as a 1D array of 0s and 1s.
            - expanded_states (np.array): Array of literals corresponding to the expanded truths. This is a 1D
                array of the same shape as the expanded truths array. This array's indices map a literal to its
                corresponding truth value in the expanded truths array.
            - toggle_array (np.array): Array of 0s and 1s where 1 indicates the literal changed from time step t
                to t+1. This array is similar to the expanded truths array and it is useful for quickly determining
                how many predicates changed.
            - state (dict): The custom non-PDDL state of the environment. See the state_update function for more
                information.

        Args:
            action (str): The action to take. If None, then it is assumed that interactive is True.
            interactive (bool): Whether or not to use interactive mode.

        Returns:
            obs (PDDLGym State): The new state of the environment.
            reward (float): The reward for the action.
            done (bool): Whether or not the episode is done.
            info (dict): A dictionary of metadata about the step.
        """
        expanded_truths = self.prev_step[3]["expanded_truths"]
        expanded_states = self.prev_step[3]["expanded_states"]

        if interactive:
            self._interactive_starter_prints(expanded_truths)
            action = robotouille_utils.create_action_repl(
                self.env, self.prev_step[0], self.renderer
            )
        else:
            action = robotouille_utils.create_action(
                self.env, self.prev_step[0], action, self.renderer
            )

        prev_heuristic = self._heuristic_function(self.prev_step[0])

        obs, reward, done, info = self._handle_action(action)
        obs, reward, _, info = self._change_selected_player(obs)
        obs = self._state_update()

        toggle_array = pddlgym_utils.create_toggle_array(
            expanded_truths, expanded_states, obs.literals
        )
        if interactive:
            print(f"Predicates Changed: {toggle_array.sum()}")

        expanded_truths, expanded_states = pddlgym_utils.expand_state(
            obs.literals, obs.objects
        )

        if self._current_selected_player(obs) == "robot1":
            self.timesteps += 1

        info = {
            "timesteps": self.timesteps,
            "expanded_truths": expanded_truths,
            "expanded_states": expanded_states,
            "toggle_array": toggle_array,
            "state": self.state,
        }

        reward = self._heuristic_function(obs) - prev_heuristic

        self.prev_step = (obs, reward, done, info)

        if done:
            print("Goal Reached!")

        return obs, reward, done, info

    def reset(self):
        """
        This function resets the environment.

        Returns:
            obs (PDDLGym State): The initial state of the environment.
            info (dict): A dictionary of metadata about the step.
        """
        obs, _ = self.env.reset()
        expanded_truths, expanded_states = pddlgym_utils.expand_state(
            obs.literals, obs.objects
        )
        info = {
            "timesteps": self.timesteps,
            "expanded_truths": expanded_truths,
            "expanded_states": expanded_states,
            "toggle_array": None,
            "state": {},
        }
        self.prev_step = (obs, 0, False, info)
        self.timesteps = 0
        self.state = {}
        self.num_players = self._count_players(obs)
        self.planning = self.generate_plan(obs)
        return obs, info
