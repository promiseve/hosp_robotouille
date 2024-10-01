from enum import Enum
import subprocess
from robotouille import simulator, robotouille_simulator
import argparse

from robotouille.robotouille_simulator import Mode


parser = argparse.ArgumentParser()
parser.add_argument(
    "--environment_name",
    help="The name of the environment to create.",
    default="multiagent",
)
parser.add_argument("--seed", help="The seed to use for the environment.", default=None)
parser.add_argument(
    "--noisy_randomization",
    action="store_true",
    help="Whether to use 'noisy randomization' for procedural generation",
)
parser.add_argument(
    "--mode",
    type=lambda x: Mode[x.upper()],
    choices=list(Mode),
    default=Mode.PLAY,
    help="Whether to play, train, or evaluate the model.",
)
args = parser.parse_args()

simulator(args.environment_name, args.seed, args.noisy_randomization, args.mode)