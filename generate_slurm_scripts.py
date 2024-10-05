import os

# Create a directory to store the scripts
script_dir = "slurm_scripts"
os.makedirs(script_dir, exist_ok=True)

# Base content of the SLURM job script
base_content = """#!/bin/bash
#SBATCH -J exp_{index}                        # Job name
#SBATCH -o exp_{index}_%j.out                 # Output file (%j expands to jobID)
#SBATCH -e exp_{index}_%j.err                 # Error log file (%j expands to jobID)
#SBATCH --mail-type=END,FAIL                  # Mail events (BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=poe6@cornell.edu          # Where to send mail
#SBATCH -N 1                                  # Run on a single node
#SBATCH -n 1                                  # Run a single task
#SBATCH --cpus-per-task=1                     # Use 1 CPU core
#SBATCH --mem=128GB                             # Memory limit
#SBATCH -t 120:00:00                         # Time limit hrs:min:sec (1444 hours)
#SBATCH --partition=default_partition         # Partition to submit to
#SBATCH --gres=gpu:1080ti:1                   # Request 1 GPU

# Load any necessary modules
module load cuda/11.0

# Activate the virtual environment
source "/home/poe6/hosp_rob_env/bin/activate"

# Change to the project directory
cd /home/poe6/hosp_robotouille

# Run the Python script
python epymarl/main.py --config=vdn --env-config=gymma with env_args.time_limit=50
"""

# Create 30 SLURM job scripts
for i in range(1, 31):
    filename = os.path.join(script_dir, f"run_experiment_{i}.slurm")
    with open(filename, "w") as f:
        f.write(base_content.format(index=i))
    os.chmod(filename, 0o755)  # Make the script executable

print(f"Created 30 SLURM job scripts in the '{script_dir}' directory.")

# Create the start_experiments.sh script
start_experiments_content = """#!/bin/bash

# Start a new tmux session
tmux new-session -d -s cluster_jobs

# Submit jobs
tmux new-window -t cluster_jobs:1 -n "submit"
tmux send-keys -t cluster_jobs:1 '
for i in {1..30}
do
    sbatch slurm_scripts/run_experiment_$i.slurm
done
' C-m

# Monitor job queue
tmux new-window -t cluster_jobs:2 -n "queue"
tmux send-keys -t cluster_jobs:2 'watch -n 60 squeue -u $USER' C-m

# Show cluster information
tmux new-window -t cluster_jobs:3 -n "info"
tmux send-keys -t cluster_jobs:3 'watch -n 300 sinfo' C-m

# Show recent job history
tmux new-window -t cluster_jobs:4 -n "history"
tmux send-keys -t cluster_jobs:4 'watch -n 300 sacct -u $USER --starttime $(date -d "24 hours ago" +%Y-%m-%dT%H:%M:%S) -o JobID,JobName,State,ExitCode,Start,End,Elapsed' C-m

# Attach to the tmux session
tmux attach -t cluster_jobs
"""

with open("start_experiments.sh", "w") as f:
    f.write(start_experiments_content)
os.chmod("start_experiments.sh", 0o755)  # Make the script executable

print("Created start_experiments.sh to submit jobs to SLURM and monitor the queue.")