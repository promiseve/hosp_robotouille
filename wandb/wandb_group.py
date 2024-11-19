import wandb


run_path = "airlabmarl/6756-rl-experiments/2x4p8b5g"
api = wandb.Api()


def set_group():
    run = api.run(run_path)
    run.group = "equalskilled_givemedicine"
    run.update()


def scale_timestep():
    run_id = "y2kwkwfo"
    run = api.run(f"airlabmarl/6756-rl-experiments/{run_id}")
    history = run.history(keys=["reward per episode"])
    filtered_rewards = history["reward per episode"].iloc[::10].reset_index(drop=True)
    wandb.init(project="6756-rl-experiments")
    # print wandb run
    print(wandb.run)
    for idx, reward in enumerate(filtered_rewards):
        wandb.log({"scaled reward per episode": reward})


if __name__ == "__main__":
    scale_timestep()
