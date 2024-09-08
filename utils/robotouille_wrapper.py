import gym
import pddlgym
from utils.robotouille_reward_handler import RobotouilleRewardHandler
import utils.robotouille_utils as robotouille_utils
import utils.pddlgym_utils as pddlgym_utils
from environments.env_generator.object_enums import Item


class RobotouilleWrapper(gym.Wrapper):
    """
    This wrapper wraps around the Robotouille environment from PDDLGym.

    This wrapper is necessary because while the PDDL language is powerful, it can be
    cumbersome to implement data-driven state such as cutting X times or cooking something
    for Y timesteps. This does not mean it is impossible but rather than littering the
    observation space with a bunch of predicates to represent time and number of cuts, we
    offload this to the wrapper's metadata.
    """

    def __init__(self, env, config, renderer):
        """
        Initialize the Robotouille wrapper.

        Args:
            env (PDDLGym Environment): The environment to wrap.
            config (dict): A configuration JSON with custom values
        """
        super(RobotouilleWrapper, self).__init__(env)
        # The PDDLGym environment.
        self.env = env
        # The previous step of the environment.
        # This is useful for the interactive mode and for cases where nothing changes (e.g. noop)
        self.prev_step = None
        # The number of timesteps that have passed.
        self.timesteps = 0
        # The state of the environment (for non-PDDL states like cut and cook)
        self.state = {}
        # The configuration for this environment.
        # This is used to specify things such as cooking times and cutting amounts
        self.config = config
        self.num_players = None
        self.taken_actions = []
        self.renderer = renderer
        self.reward_handler = RobotouilleRewardHandler()

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
        if action_name == "cut":
            item = next(
                filter(
                    lambda typed_entity: typed_entity.var_type == "item",
                    action.variables,
                )
            )
            item_status = self.state.get(item.name)
            if item_status is None:
                self.state[item.name] = {"cut": 1}
            elif item_status.get("cut") is None:
                item_status["cut"] = 1
            else:
                item_status["cut"] += 1

                if item_status["cut"] == 3:
                    item_status["picked-up"] = False
            return self.prev_step
        elif action_name == "cook":
            item = next(
                filter(
                    lambda typed_entity: typed_entity.var_type == "item",
                    action.variables,
                )
            )
            item_status = self.state.get(item.name)
            if item_status is None:
                self.state[item.name] = {"cook": {"cook_time": -1, "cooking": True}}
            elif item_status.get("cook") is None:
                item_status["cook"] = {"cook_time": -1, "cooking": True}
            else:
                item_status["cook"]["cooking"] = True
            return self.prev_step
        elif action_name == "fry" or action_name == "fry_cut_item":
            item = next(
                filter(
                    lambda typed_entity: typed_entity.var_type == "item",
                    action.variables,
                )
            )
            item_status = self.state.get(item.name)
            if item_status is None:
                self.state[item.name] = {"fry": {"fry_time": -1, "frying": True}}
            elif item_status.get("fry") is None:
                item_status["fry"] = {"fry_time": -1, "frying": True}
            else:
                item_status["fry"]["frying"] = True
            return self.prev_step
        elif action_name == "pick-up":
            item = next(
                filter(
                    lambda typed_entity: typed_entity.var_type == "item",
                    action.variables,
                )
            )
            item_status = self.state.get(item.name)
            if item_status is not None and item_status.get("cook") is not None:
                item_status["cook"]["cooking"] = False
            if item_status is not None and item_status.get("fry") is not None:
                item_status["fry"]["frying"] = False

            # Spaghetti code to handle the fact that the patty is not stacked after cooking
            item_status = self.state.get("patty1")
            cooked = self._check_cooked(self.prev_step[0])

            # initialize state["patty1"]["picked-up"] if it doesn't exist
            if item_status is None:
                self.state[item.name] = {"picked-up": False}
                item_status = self.state.get(item.name)
            elif item_status.get("picked-up") is None:
                item_status["picked-up"] = False

            if cooked:
                item_status["picked-up"] = True
        # TODO: Probably stop cooking if something is stacked on top of meat
        return self.env.step(action)

    def _state_update(self):
        """
        This function updates the custom non-PDDL state of the environment.

        This function is called after every step in the environment. It can either update
        the custom state (e.g. incrementing the cook time of a cooking item) or directly
        modify the PDDL state (e.g. adding the iscut predicate to an item that has been
        fully cut).

        Returns:
            new_env_state (PDDLGym State): The new state of the environment.
        """
        state_updates = []
        for item, status_dict in self.state.items():
            for status, state in status_dict.items():
                if status == "cut":
                    item_name, _ = robotouille_utils.trim_item_ID(item)
                    # TODO: Might need to trim item name
                    num_cuts = self.config["num_cuts"]
                    max_num_cuts = num_cuts.get(item_name, num_cuts["default"])
                    if state >= max_num_cuts:
                        literal = pddlgym_utils.str_to_literal(f"iscut({item}:item)")
                        state_updates.append(literal)
                elif status == "cook":
                    item_name, _ = robotouille_utils.trim_item_ID(item)
                    cook_time = self.config["cook_time"]
                    max_cook_time = cook_time.get(item_name, cook_time["default"])
                    if state["cooking"]:
                        state["cook_time"] += 1
                        if state["cook_time"] == max_cook_time:
                            status_dict["picked-up"] = False
                    if state["cook_time"] >= max_cook_time:
                        literal = pddlgym_utils.str_to_literal(f"iscooked({item}:item)")
                        state_updates.append(literal)
                elif status == "fry":
                    item_name, _ = robotouille_utils.trim_item_ID(item)
                    fry_time = self.config["fry_time"]
                    max_fry_time = fry_time.get(item_name, fry_time["default"])
                    if state["frying"]:
                        state["fry_time"] += 1
                    if state["fry_time"] >= max_fry_time:
                        literal = pddlgym_utils.str_to_literal(f"isfried({item}:item)")
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

    def _check_cooked(self, obs):
        for literal in obs.literals:
            if "iscooked" == literal.predicate.name:
                return True
        return False

    def get_latest_info(self):
        """
        Get the latest info dictionary from the environment.

        Returns:
            dict: The latest info dictionary.
        """
        return self.prev_step[3] if self.prev_step else None

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

        self.taken_actions.append(action)
        if interactive:
            self._interactive_starter_prints(expanded_truths)
            action = robotouille_utils.create_action_repl(
                self.env, self.prev_step[0], self.renderer
            )
        else:
            action = robotouille_utils.create_action(
                self.env, self.prev_step[0], action, self.renderer
            )

        prev_heuristic = self.reward_handler.heuristic_reward(
            self.prev_step[0], self.state
        )

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
        curr_heuristic = self.reward_handler.heuristic_reward(obs, self.state)
        reward = curr_heuristic - prev_heuristic
        reward /= self.timesteps + 1
        self.prev_step = (obs, reward, done, info)

        if done:
            print("Goal Reached!")
        # print("prev_heuristic: ", prev_heuristic)
        # print("current_heuristic: ", curr_heuristic)
        print("reward: ", reward)
        return obs, reward, done, info

    def save_episode(self, filename):
        with open(filename, "w") as f:
            for action in self.taken_actions:
                f.write(action + "\n")

    def get_episode_actions(self):
        return self.taken_actions

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
        self.taken_actions = []
        self.num_players = self._count_players(obs)
        return obs, info
