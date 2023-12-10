import gym
import pddlgym
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

    def __init__(self, env, config):
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
        robotouille_utils.print_actions(self.env, self.prev_step[0])
        print(f"True Predicates: {expanded_truths.sum()}")

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

    def _handle_action(self, action):
        if action == "noop":
            return self.prev_step

        # Update state based on the action
        self._update_state_based_on_action(action)

        # Perform the environment step
        obs, _, done, info = self.env.step(action)

        # Calculate reward
        reward = self.handle_reward(action, obs)

        # Accumulate reward
        accumulated_reward = self.prev_step[1] + reward

        # Update the previous step
        self.prev_step = (obs, accumulated_reward, done, info)
        return obs, accumulated_reward, done, info


    def _update_state_based_on_action(self, action):
        """
        Update the state of the environment based on the action taken.
        """
        action_name = action.predicate.name
        item = next(filter(lambda typed_entity: typed_entity.var_type == "item", action.variables), None)

        if item:
            item_status = self.state.get(item.name, {})
            if action_name == "cut":
                item_status["cut"] = item_status.get("cut", 0) + 1
            elif action_name in ["cook", "fry"]:
                cooking_status = item_status.get(action_name, {"cooking": False, "cook_time": 0, "fry_time": 0})
                cooking_status["cooking"] = True
                item_status[action_name] = cooking_status
            elif action_name == "pick-up":
                if "cook" in item_status:
                    item_status["cook"]["cooking"] = False
                if "fry" in item_status:
                    item_status["fry"]["frying"] = False

            self.state[item.name] = item_status

    def handle_reward(self, action, obs):
        reward = 0
        action_name = action.predicate.name


        # Reward/Penalty for cutting
        if action_name == "cut":
            item = next(filter(lambda typed_entity: typed_entity.var_type == "item", action.variables), None)
            if item:
                item_status = self.state.get(item.name, {})
                num_cuts = item_status.get("cut", 0)
                reward += 5 if num_cuts == 1 else -0.1

        # Reward/Penalty for cooking and frying
        elif action_name in ["cook", "fry"]:
            item = next(filter(lambda typed_entity: typed_entity.var_type == "item", action.variables), None)
            if item:
                item_status = self.state.get(item.name, {})
                if action_name == "fry":
                    num_fries = item_status.get("fry", {}).get("fry_time", 0)
                    reward += 5 if num_fries < 1 else -0.1
                elif action_name == "cook":
                    num_cooks = item_status.get("cook", {}).get("cook_time", 0)
                    reward += 5 if num_cooks < 1 else -0.1

        # Partial rewards for partial goals in burger assembly
        print(self._is_burger_partially_correct())
        if self._is_burger_partially_correct():
            print("Currest")
            reward += 5
        elif self._is_burger_assembled_incorrectly():
            print("wrongs")
            reward -= 5

        # Reward for correct assembly (non-continuous)
        if self._is_burger_assembled_correctly() and not self.prev_step[3].get("correctly_assembled", False):
             reward += 10
             self.prev_step[3]["correctly_assembled"] = True

        return reward

    
    def _is_burger_partially_correct(self):
        info = self.get_latest_info()
        if not info:
            return False

        state_truth_map = self.map_state_to_truth(info)
        string_state_truth_map = {str(key): value for key, value in state_truth_map.items()}

        # Case 1: Patty on bottom bun
        patty_on_bottom_bun = state_truth_map.get("atop(bottombun1:item,patty1:item)", 1.0)
        if patty_on_bottom_bun:
            return True

        # # Case 2: Lettuce on patty, but no top bun
        # lettuce_on_patty = state_truth_map.get('atop(patty1:item,lettuce1:item)', 1.0)
        # top_bun_not_present = not state_truth_map.get('atop(lettuce1:item,topbun1:item)', 0.0)
        # if lettuce_on_patty and top_bun_not_present:
        #     return True

        # # Case 3: Bottom bun and patty present, but no lettuce or top bun
        # no_lettuce = not state_truth_map.get('atop(patty1:item,lettuce1:item)', 1.0)
        # no_top_bun = not state_truth_map.get('atop(lettuce1:item,topbun1:item)', 1.0)
        # if patty_on_bottom_bun and no_lettuce and no_top_bun:
        #     return True

        return False



    def _is_burger_assembled_correctly(self):
        info = self.get_latest_info()
        if not info:
            return False

        state_truth_map = self.map_state_to_truth(info)
        string_state_truth_map = {str(key): value for key, value in state_truth_map.items()}
        correct_order = [
            'atop(table1:station,bottombun1:item)', 
            'atop(bottombun1:item,patty1:item)', 
            'atop(patty1:item,lettuce1:item)', 
            'atop(lettuce1:item,topbun1:item)'
        ]
        return all(string_state_truth_map.get(order, 1.0) for order in correct_order)



    def _is_burger_assembled_incorrectly(self):
        info = self.get_latest_info()
        if not info:
            return False

        state_truth_map = self.map_state_to_truth(info)
        string_state_truth_map = {str(key): value for key, value in state_truth_map.items()}
        incorrect_order = [
            "atop(lettuce1:item,bottombun1:item)", 
            "atop(topbun1:item,lettuce1:item)", 
            "atop(topbun1:item,patty1:item)", 
            "atop(bottombun1:item,topbun1:item)",
            "atop(patty1:item,topbun1:item)", 
            "atop(lettuce1:item,patty1:item)"
        ]
        for val in incorrect_order:
            if string_state_truth_map.get(val) > 0.0:
                return True
        return False


    def map_state_to_truth(self, info):
        if not info or 'expanded_states' not in info or 'expanded_truths' not in info:
            print("Error: Info is incomplete or missing")
            return {}

        expanded_states = info['expanded_states']
        expanded_truths = info['expanded_truths']

        if expanded_truths is None or len(expanded_truths) != len(expanded_states):
            print("Error: Mismatch in lengths or None input")
            return {}

        return {state: truth for state, truth in zip(expanded_states, expanded_truths) if truth is not None}


    def get_latest_info(self):
        """
        Get the latest info dictionary from the environment.

        Returns:
            dict: The latest info dictionary.
        """
        return self.prev_step[3] if self.prev_step else None



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
        expanded_truths, expanded_states = pddlgym_utils.expand_state(
            self.prev_step[0].literals, self.prev_step[0].objects
        )

        if interactive:
            self._interactive_starter_prints(expanded_truths)
            action = robotouille_utils.create_action_repl(self.env, self.prev_step[0])
        else:
            action = robotouille_utils.create_action(
                self.env, self.prev_step[0], action
            )
        obs, reward, done, _ = self._handle_action(action)
        print("reward from handle action", reward)
        obs = self._state_update()
        toggle_array = pddlgym_utils.create_toggle_array(
            expanded_truths, expanded_states, obs.literals
        )
        if interactive:
            print(f"Predicates Changed: {toggle_array.sum()}")
        info = {
            "timesteps": self.timesteps,
            "expanded_truths": expanded_truths,
            "expanded_states": expanded_states,
            "toggle_array": toggle_array,
            "state": self.state,
        }

        self.prev_step = (obs, reward, done, info)
        self.timesteps += 1
        return obs, reward, done, info

    def reset(self):
        """
        This function resets the environment.

        Returns:
            obs (PDDLGym State): The initial state of the environment.
            info (dict): A dictionary of metadata about the step.
        """
        obs, _ = self.env.reset()
        info = {
            "timesteps": self.timesteps,
            "expanded_truths": None,
            "expanded_states": None,
            "toggle_array": None,
            "state": {},
        }
        self.prev_step = (obs, 0, False, info)
        self.timesteps = 0
        self.state = {}
        return obs, info
