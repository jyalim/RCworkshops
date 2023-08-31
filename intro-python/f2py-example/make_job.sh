#!/bin/bash
#SBATCH --job-name="f2py compile" 
#SBATCH -c 1                      # Number of cores requested
#SBATCH --qos=public              # The queue (line) we are in
#SBATCH --partition=lightwork     # The partition of compute nodes to run on
#SBATCH --output=sbatch_compile_%j.out
#SBATCH --error=sbatch_compile_%j.err
#SBATCH --time=0-0:05:00 
#SBATCH --mail-type=ALL

module load intel/parallel-studio-2020.4
bash make.sh
