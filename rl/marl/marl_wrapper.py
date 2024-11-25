from typing import List, Optional, Union
import gym
import pddlgym
from rl.marl.hosp_marl_env import HospitalMARLEnv
from rl.marl.marl_env import MARLEnv
from utils.robotouille_utils import get_valid_moves
import utils.pddlgym_utils as pddlgym_utils
import utils.robotouille_wrapper as robotouille_wrapper
import wandb


class MARLWrapper(robotouille_wrapper.RobotouilleWrapper):
    """
    This class is a wrapper around the Robotouille environment to make it compatible with stable-baselines3. It simplifies the environment for the RL agent by converting the state and action space to a format that is easier for the RL agent to learn.
    """

    def __init__(self, env, renderer, n_agents):
        wandb.login()
        self.env = env # gym environment
        self.pddl_env = env # robotouille wrapper environment, not pddl environment just yet
        self.n_agents = n_agents
        self.max_steps = 50
        self.episode_reward = 0
        self.renderer = renderer
        # Configuration dictionary for tracking metrics
        self.metrics_config = {
            "ep_rew_mean": None,  # Mean episode reward
            "total_timesteps": 0,  # Total number of timesteps
            "iterations": 0,  # Number of iterations
            "ep_len_mean": None,  # Mean episode length
            "loss": None,  # Loss,
            "entropy_loss": None,  # Entropy loss
        }

        self._wrap_env()

        # Initialize WandB with the metrics config
        wandb.init(
            project="6756-rl-experiments",
            config=self.metrics_config,
            notes= "specskilled_givemedicine_ippo"
        )

    def log_metrics(self, update_dict):
        """
        Log metrics to the metrics_config and to WandB.
        :param update_dict: A dictionary containing updates to the metrics.
        """
        # Update the metrics configuration with new values
        self.metrics_config.update(update_dict)
        # Log the updated metrics to WandB
        wandb.log(self.metrics_config)

    def _wrap_env(self):
        """
        Wrap the environment to make it compatible with epymarl.
        """
        expanded_truths, expanded_states = pddlgym_utils.expand_state(
            self.pddl_env.prev_step[0].literals, self.pddl_env.prev_step[0].objects
        )

        valid_actions = get_valid_moves( # Potential bug: the valid actions for the a state are the valid actions at the end of previous step - error prone
            self.pddl_env, self.pddl_env.prev_step[0], self.renderer
        )
        all_actions = list(
            self.pddl_env.action_space.all_ground_literals(
                self.pddl_env.prev_step[0], valid_only=False
            )
        )

        # if the environment is a RobotouilleWrapper, we need to change it to MARLEnv. Otherwise, just step the MARLEnv
        # TODO: How to incorporate other information about the state from robotouille wrapper? 
        # What is the required format for HospitalMARLEnv?
        if not isinstance(self.env, HospitalMARLEnv):
            self.env = HospitalMARLEnv(
                self.n_agents,
                expanded_truths,
                expanded_states,
                valid_actions,
                all_actions,
            )
        else:
            self.env.step(expanded_truths, valid_actions)

        self.observation_space = self.env.observation_space

    def step(self, actions=None, interactive=False, debug=False):
        """
        Take a step in the environment.

        Returns:
            state (list): The state of the environment after the step.
            reward (float): The reward obtained from the step.
            done (bool): Whether the episode is done.
            truncated (bool): Whether the episode was truncated.
            info (dict): A dictionary containing information about the environment.
        """

        rewards = []
        for i in range(len(actions)):
            action = self.env.unwrap_move(i, actions[i])
            if debug:
                print(action)
            # if moving, check if action is valid
            if action == "invalid":
                # obs, reward, done, info = self.pddl_env.prev_step
                # # print(f"Invalid action for action {actions[i]}")
                # obs, _, _, _ = self.pddl_env._change_selected_player(obs)
                # self.pddl_env.taken_actions.append("noop")
                # reward = 0 # TODO: no reward punishment yet for invalid action
                # self.pddl_env.prev_step = (obs, reward, done, info)
                # rewards.append(reward)
                # self.pddl_env.move_counter += 1
                # if self.pddl_env._current_selected_player(obs) == "robot1":
                #     self.pddl_env.timesteps += 1
                # info["timesteps"] = self.pddl_env.timesteps
                obs, _, done, info = self.pddl_env.step("noop", interactive)
                reward = -0.1 # TODO: lets not make this hardcoded
            else:
                action = str(action)
                obs, reward, done, info = self.pddl_env.step(action, interactive)
                # Reward .05 for correct action. .05 * 3 agents * 100 timesteps + max 35 reward = 50- cooking setup
                # Reward .01 for correct action. .01 * 4 agents * 100 timesteps + max 50 after normalizing by dividing with timesteps in robotouille wrapper
                #  reward = 50 - For hospital setup
                # - cooking setup
                # Scale between 0 to 1, 
                #/194 for givemedicineequal, /217 for givemedicinespec #already add 4 from the top 
                #/91 for giverescuebreaths, /99 for giverescuebreathsspec#already add 4 from the top

                reward = (reward + 0.01) / 217 # TODO: lets not make this hardcoded

                self.pddl_env.prev_step = (obs, reward, done, info)

                rewards.append(reward)

            # NOTE: We need to do this because when we filter for vaild moves during each step, 
            # we need to have player grid locations maintained in the renderer
            # TODO: Maybe have this inside robotouille_wrapper.py?
            self.pddl_env.renderer.canvas.update_all_player_pos(obs.literals)
            
            self._wrap_env()

        wandb.log({"reward per step": sum(rewards)})

        self.episode_reward += sum(rewards)
        if self.pddl_env.timesteps >= self.max_steps or done:
            wandb.log({"reward per episode": self.episode_reward})
            wandb.log({"timesteps": self.pddl_env.timesteps})

        return (
            self.env.state, # HospitalMARLEnv state
            rewards,
            done,
            info,
        )

    def reset(self, seed=42, options=None):
        """
        Reset the environment to its initial state.

        Returns:
            state (list): The initial state of the environment.
            info (dict): A dictionary containing information about the environment.
        """
        obs, info = self.pddl_env.reset()
        # reset the player grid locations in the renderer
        self.pddl_env.renderer.canvas.reset_player_positions()
        self.episode_reward = 0
        self._wrap_env()
        # print("self.env.state", self.env.state)
        return self.env.state, info

    def render(self, *args, **kwargs):
        self.pddl_env.render()