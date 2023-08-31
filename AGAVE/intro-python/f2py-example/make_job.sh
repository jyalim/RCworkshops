#!/bin/bash
#SBATCH --job-name="f2py compile" 
#SBATCH --ntasks=1                # Number of cores requested
#SBATCH --qos=wildfire            # The queue (line) we are in
#SBATCH --partition=debug         # The compute node set to submit to
#SBATCH --output=sbatch_compile_%j.out
#SBATCH --error=sbatch_compile_%j.err
#SBATCH --time=0-0:05:00 
#SBATCH --mail-type=ALL
##SBATCH --mail-user=asurite@asu.edu

module load intel/2019.4 anaconda/py3
source activate pyintel
bash make.sh
