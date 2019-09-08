f2py example
============

An example of how to wrap existing Fortran subroutines with `f2py` for
python.

The following fortran code, `d3zslat_reader.F90` is a simplified reader
(some subroutines were removed) of a computational fluid dynamics
codebase.

The full code also compute partial derivatives using MKL.

Before Starting
---------------

Note that this exercise involves compiling a fortran module with intel
compiliers. To succesfully generate this module, an anaconda environment
must be created. From this directory (or with the `environment.yml` in
this directory handy), conduct the following interactive session:

```bash
# request 1 core of the debug partition for max time (15m) 
interactive --partition debug --qos debug -t 15 -n 1
# Once the debug core is allocated, load the intel compiler from 
# 2019 into the environment, and load anaconda python 
module load intel/2019.4 anaconda/py3
# Create the intel python environment
conda env create -f environment.yml
```

Compiling interactively
-----------------------

From the headnode:

```bash
# request 1 core of the debug partition for max time (15m) 
interactive --partition debug --qos debug -t 15 -n 1
# Once the debug core is allocated, load the intel compiler from 
# 2019 into the environment, and load anaconda python 
module load intel/2019.4 anaconda/py3
# activate the pyintel conda environment specified in the previous
# section
source activate pyintel
# compile the fortran code with f2py
bash make.sh
# verify the existence of the module and check it by running test
python test_mod_build.py
```

Compiling with sbatch 
---------------------

From the headnode:

```bash
sbatch make_job.sh
```

Verify the `slurm` out file that the `test_mod_build.py` run was
successful




<img src="assets/ASURC_logo.png" width="240">
