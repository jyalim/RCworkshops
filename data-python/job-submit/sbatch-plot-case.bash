#!/bin/bash
#SBATCH --partition=general   # Where to request nodes
#SBATCH --qos=public          # Quality of Service
#SBATCH -c 1                  # single core
#SBATCH -t 2                  # Two minutes allocation time
#SBATCH -o log/s.%A.%a.%j.out # SLURM output log

readonly manifest=${1:?ERROR -- manifest file was not passed}
readonly   taskid=$SLURM_ARRAY_TASK_ID
readonly datafile=$(getline $taskid $manifest)

module load mamba/latest
source activate scicomp

python plot-case.py "$datafile"
