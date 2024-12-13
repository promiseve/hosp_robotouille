from argparse import Namespace
from typing import List, Optional, Union
import gym
import pddlgym
from rl.marl.hosp_marl_env import HospitalMARLEnv
from rl.marl.marl_env import MARLEnv
from utils.robotouille_utils import get_valid_moves
import utils.pddlgym_utils as pddlgym_utils
import utils.robotouille_wrapper as robotouille_wrapper
import wandb
from communication.gnn import GCNComm
import numpy as np
import torch


class MARLWrapper(robotouille_wrapper.RobotouilleWrapper):
    """
    This class is a wrapper around the Robotouille environment to make it compatible with stable-baselines3. It simplifies the environment for the RL agent by converting the state and action space to a format that is easier for the RL agent to learn.
    """

    def __init__(self, env, renderer, n_agents):
        wandb.login()
        # Default configuration
        self.config2 = {
            "msg_hidden_dim": 64,
            "num_layers": 3,
            "msg_out_size": 32,
            "comm_dist": 2,  # Default communication distance
        }

        self.env = env  # gym environment
        self.pddl_env = env  # robotouille wrapper environment
        self.n_agents = n_agents
        self.renderer = renderer
        self.max_steps = 50
        self.episode_reward = 0

        # Initialize GNN with the merged configuration
        self.gnn = GCNComm(
            input_shape=2, 
            args=Namespace(**self.config2)  # Convert dict to Namespace
        )

        # Metrics configuration for tracking performance
        self.metrics_config = {
            "ep_rew_mean": None,  # Mean episode reward
            "total_timesteps": 0,  # Total number of timesteps
            "iterations": 0,  # Number of iterations
            "ep_len_mean": None,  # Mean episode length
            "loss": None,  # Loss
            "entropy_loss": None,  # Entropy loss
        }

        self._wrap_env()

        # Initialize WandB with metrics configuration
        wandb.init(
            project="6756-rl-experiments",
            config=self.metrics_config,
            notes="equalskilled_givemedicine_mappo",
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

        valid_actions = get_valid_moves(
            self.pddl_env, self.pddl_env.prev_step[0], self.renderer
        )
        all_actions = list(
            self.pddl_env.action_space.all_ground_literals(
                self.pddl_env.prev_step[0], valid_only=True
            )
        )

        # if the environment is a RobotouilleWrapper, we need to change it to MARLEnv. Otherwise, just step the MARLEnv
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
        """
        rewards = []
        all_adj_matrices = []
        done_flags = []
        info_list = []
        
        for i, action in enumerate(actions):
            # Unwrap and execute action
            action_str = self.env.unwrap_move(i, action)
            if debug:
                print(f"Agent {i} Action: {action_str}")

            if action_str == "invalid":
                result = self.pddl_env.prev_step
                if len(result) == 4:
                    obs, reward, done, info = result
                elif len(result) > 4:
                    obs, reward, done, info, *_ = result
                else:
                    raise ValueError(f"Unexpected step result: {result}")

                reward = 0  # Assign zero reward for invalid actions
            else:
                result = self.pddl_env.step(action_str, interactive)
                if len(result) == 4:
                    obs, reward, done, info = result
                elif len(result) > 4:
                    obs, reward, done, info, *_ = result
                else:
                    raise ValueError(f"Unexpected step result: {result}")

                # Normalize reward
                reward = (reward + 0.01) / 194

            # Append results
            rewards.append(reward)
            done_flags.append(done)
            info_list.append(info)

            # Update previous step for this agent
            self.pddl_env.prev_step = (obs, reward, done, info)

            # Fetch dynamic positions of players and patient
            self.pddl_env.renderer.canvas.update_all_player_pos(obs.literals)
            player_positions = [
                player["position"] for player in self.pddl_env.renderer.canvas.players_pose
            ]
            print(player_positions)
            patient_position = self.pddl_env.renderer.canvas._get_station_position("patient_bed_station1")
            print(f"Patient position: {patient_position}")
            # Compute adjacency matrix
            adj_matrix = self.compute_adjacency_matrix(player_positions, patient_position, self.config2)
            all_adj_matrices.append(adj_matrix)

            # Convert adjacency matrix to tensor
            # Pass adjacency matrix and features to the GNN
            adj_tensor = torch.tensor(adj_matrix, dtype=torch.float32)

            #features_tensor = torch.tensor(self.get_agent_features(self.config), dtype=torch.float32)
            #gnn_output = self.gnn(features_tensor, adj_tensor)

            # Log GNN outputs
            #wandb.log({
            #    "gnn_output_mean": gnn_output.mean().item(),
            #    f"adj_matrix_agent_{i}": wandb.Image(adj_matrix),
            #})

        # Combine done flags to decide overall episode termination
        overall_done = any(done_flags)  # Adjust based on environment semantics

        # Log cumulative rewards and adjacency matrices
        wandb.log({
            "reward_per_step": sum(rewards),
            "adjacency_matrices": all_adj_matrices,
        })

        self.episode_reward += sum(rewards)
        if self.pddl_env.timesteps >= self.max_steps or overall_done:
            wandb.log({
                "reward_per_episode": self.episode_reward,
                "timesteps": self.pddl_env.timesteps,
            })

        return self.env.state, rewards, overall_done, {"info_per_agent": info_list}




    def reset(self, seed=42, options=None):
        """
        Reset the environment to its initial state.

        Returns:
            state (list): The initial state of the environment.
            info (dict): A dictionary containing information about the environment.
        """
        obs, info = self.pddl_env.reset()
        self.episode_reward = 0
        self._wrap_env()
        # print("self.env.state", self.env.state)
        return self.env.state, info

    def render(self, *args, **kwargs):
        self.pddl_env.render()

