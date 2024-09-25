import subprocess
from robotouille import simulator, robotouille_simulator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--environment_name",
    help="The name of the environment to create.",
    default="multiagent",
)
parser.add_argument(
    "--mode",
    help="Whether to run in play, train, or load mode",
    default="train",
)
parser.add_argument("--seed", help="The seed to use for the environment.", default=None)
parser.add_argument(
    "--noisy_randomization",
    action="store_true",
    help="Whether to use 'noisy randomization' for procedural generation",
)
args = parser.parse_args()

def get_mode(txt):
    match txt.lower():
        case "play":
            return robotouille_simulator.mode.PLAY
        case "train":
            return robotouille_simulator.mode.TRAIN
        case "load":
            return robotouille_simulator.mode.LOAD

simulator(args.environment_name, args.seed, args.noisy_randomization, mode=get_mode(args.mode))
