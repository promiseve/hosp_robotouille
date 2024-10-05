#!/bin/bash

# Start a new tmux session
tmux new-session -d -s cluster_jobs

# Submit jobs
tmux new-window -t cluster_jobs:1 -n "submit"
tmux send-keys -t cluster_jobs:1 '
for i in {1..5}
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
