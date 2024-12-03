from rl.marl.multiagent_hospital_env import MAHospital_robotouille
from robotouille.robotouille_env import create_robotouille_env


env, json, renderer = create_robotouille_env(
    "multiagent_givemedicine_spec", None, False
)
obs, info = env.reset()

ENVIRONMENT = MAHospital_robotouille(env, json, renderer)
