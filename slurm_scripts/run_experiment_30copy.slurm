#!/bin/bash
#SBATCH -J exp_30_ippo_100M                        # Job name
#SBATCH -o exp_30_ippo_100M%j.out                 # Output file (%j expands to jobID)
#SBATCH -e exp_30_ippo_100M%j.err                 # Error log file (%j expands to jobID)
#SBATCH --mail-type=END,FAIL                  # Mail events (BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=poe6@cornell.edu          # Where to send mail
#SBATCH -N 1                                  # Run on a single node
#SBATCH -n 1                                  # Run a single task
#SBATCH --cpus-per-task=64                     # Use 1 CPU core
#SBATCH --mem=128GB                             # Memory limit
#SBATCH -t 120:00:00                         # Time limit hrs:min:sec (1444 hours)
#SBATCH --partition=default_partition         # Partition to submit to

# Activate the virtual environment
source "/home/poe6/hosp_rob_env/bin/activate"

# Change to the project directory
cd /home/poe6/hosp_robotouille

# Run the Python script
python epymarl/main.py --config=ippo --env-config=gymma with env_args.time_limit=50
