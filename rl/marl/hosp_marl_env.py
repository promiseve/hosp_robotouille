from enum import Enum
import gym
from gym import spaces
from rl.marl.marl_env import MARLEnv
import utils.pddlgym_utils as pddlgym_utils
import utils.robotouille_utils as robotouille_utils
from gym.spaces import Box
import numpy as np


class HospitalMARLEnv(MARLEnv):
    """
    This is a converter class that simplifies the environment for the RL agent by converting the state and action space to a format that is easier for the RL agent to learn.
    """

    class observation_size(Enum):
        SMALL = 1
        MEDIUM = 2
        LARGE = 3

    def __init__(
        self, n_agents, expanded_truths, expanded_states, valid_actions, all_actions
    ):
        """
        Initializes the converter based on expanded_truths, expanded_states, valid_actions, and all_actions.

        Args:
            expanded_truths (list): List of expanded truths of the current state.
            expanded_states (list): List of expanded states that correspond to each truth in expanded_truths.
            valid_actions (list): List of valid actions
            all_actions (list): List of all actions
        """

        super().__init__(
            n_agents, expanded_truths, expanded_states, valid_actions, all_actions
        )

    def step(self, expanded_truths, valid_actions):
        """
        Updates the environment based on the action taken by the agent.

        Args:
            expanded_truths (list): List of expanded truths of the state after the update.
            valid_actions (list): List of valid actions after the update
        """
        super().step(expanded_truths, valid_actions)

    def _get_observation_space(self, mode=observation_size.LARGE):
        """
        Returns the shortened observation space based on the expanded truths and expanded states. If the observation size is SMALL, the observation space will only include the iscut and iscooked predicates. If the observation size is MEDIUM, the observation space will also include the location of the robot, the held item of the robot and the order of the ingredients. If the observation size is LARGE, the observation space will also include the location of the ingredients.

        Args:
            mode (observation_size): The size of the observation space.

        Returns:
            shortened_expanded_truths (list): List of truth values for each predicate in the shortened observation space.
            shortened_expanded_states (list): List of states in the shortened observation space.
        """

        desired_truths = [
            "ischestcompressed",
            "isrescuebreathed",
            "isshocked",
            "istreated",
            "has",
            "loc",
        ]
        desired_items = ["patient", "patient", "patient", "patient", "robot", "robot"]

        shortened_expanded_truths = []
        shortened_expanded_states = []
        print("expanded_states", self.expanded_states)
        for truth, state in zip(self.expanded_truths, self.expanded_states):
            predicate = state.predicate.name
            item = state.variables[0].name

            for i in range(len(desired_items)):
                if predicate in desired_truths[i] and desired_items[i] in item:
                    shortened_expanded_truths.append(truth)
                    shortened_expanded_states.append(state)
                    break

            if predicate == "at" and mode == self.observation_size.LARGE:
                shortened_expanded_truths.append(truth)
                shortened_expanded_states.append(state)

        return shortened_expanded_truths, shortened_expanded_states

    def _get_action_space(self):
        """
        Returns the shortened action space based on the valid actions. The shortened action space includes the following actions: moving to each location, cook, cut, pick-up, place, stack, unstack. We take advantage of the fact that at any point in time, these actions are deterministic.

        Returns:
            shortened_action_truths (list): List of truth values for each action in the shortened action space.
            shortened_action_names (list): List of action names in the shortened action space.
        """

        return super()._get_action_space()

    def unwrap_move(self, agent_index, action):
        """
        Returns the action that corresponds to the shortened action space. If it is an invalid action, return "invalid". Otherwise, it returns the pddlgym action that corresponds to the shortened action space.

        Args:
            action (int): The index of the action in the shortened action space.

        """
        return super().unwrap_move(agent_index, action)

    def print_state(self):
        """
        Prints the state of the environment.
        """

        output = []
        for truth, state in zip(self.state, self.state_names):
            if truth == 1.0:
                output.append(state)

        print(output)
