#!/bin/bash
#SBATCH -p htc
#SBATCH -q public
#SBATCH -t 5
#SBATCH -c 2
#SBATCH -o log/slurm.%A.%a.%j.out
#SBATCH --array=1-100
#SBATCH --export=NONE

module load mamba/latest
source activate scicomp

python heatnb.py $SLURM_ARRAY_TASK_ID
