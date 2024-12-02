import argparse
import wandb


api = wandb.Api()


# Groups the specified run with the specified group name
def set_group(run_path, group):
    if "airlabmarl" not in run_path:
        run_path = "airlabmarl/6756-rl-experiments/" + run_path
    run = api.run(run_path)
    run.group = group
    run.update()


# Scales the timestep of the specified run. Not used as we manually scale MAPPO/IPPO runs
def scale_timestep():
    run_id = "y2kwkwfo"
    run = api.run(f"airlabmarl/6756-rl-experiments/{run_id}")
    history = run.history(keys=["reward per episode"])
    filtered_rewards = history["reward per episode"].iloc[::10].reset_index(drop=True)
    wandb.init(project="6756-rl-experiments")
    for idx, reward in enumerate(filtered_rewards):
        wandb.log({"scaled reward per episode": reward})


if __name__ == "__main__":
    # argparse with the runID and group name
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_path", type=str, help="Run ID")
    parser.add_argument("--group", type=str, help="Group name")
    args = parser.parse_args()
    run_path = args.run_path
    group = args.group
    set_group(run_path, group)
