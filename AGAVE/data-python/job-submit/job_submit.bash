#!/bin/bash
#SBATCH --partition debug  # Where to request nodes
#SBATCH --qos wildfire     # Quality of Service
#SBATCH -N 3               # Reserve 3 Nodes
#SBATCH --exclusive        # Full 3 Nodes
#SBATCH -t 00-00:15:00     # Reservation time limit DD-HH:MM:SS
#SBATCH -e log/s.%j.err    # SLURM error log
#SBATCH -o log/s.%j.out    # SLURM output log

module load anaconda/py3
source activate pyintel
echo NPROC: $(nproc)

export MKL_NUM_THREADS=1
mysrun="srun -N 1 -n 1 --exclusive python myscript.py"
parallel -kvj84 --joblog para.log --resume $mysrun {} ::: dat/*.dat
convert -delay 1 fig/*.png out.gif
