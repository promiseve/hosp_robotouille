from rl.marl.marl_wrapper import MARLWrapper
from rl.marl.multiagent_hospital_env import MAHospital_robotouille
from robotouille.robotouille_env import RobotouilleRenderer, create_robotouille_env
from robotouille.robotouille_simulator import simulator

config = {
    "num_cuts": {"lettuce": 3, "default": 3},
    "cook_time": {"patty": 3, "default": 3},
    "num_compressions": {"patient": 3, "default": 3},
    "num_breaths": {"patient": 3, "default": 3},
    "num_shocks": {"patient": 1, "default": 1},
    "num_medicine_doses": {"patient": 1, "default": 1},
    "energy_levels": {"compresschest_cost": 5, "recharge_rate": 2, "max": 10},
    "num_players": 2,
}

env, json, renderer = create_robotouille_env("multiagent_givemedicine", None, False)
obs, info = env.reset()

# ENVIRONMENT = MAHospital_robotouille(env, config, renderer)
