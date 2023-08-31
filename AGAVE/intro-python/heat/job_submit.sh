#!/bin/bash
#SBATCH -p htc
#SBATCH -q normal
#SBATCH -t 5
#SBATCH -c 2
#SBATCH -o log/slurm.%A.%a.%j.out
#SBATCH --array=1-100
#SBATCH --export=NONE

module load anaconda/py3
source activate pyintel

python heatnb.py $SLURM_ARRAY_TASK_ID
