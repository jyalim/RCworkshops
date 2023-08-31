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
compilers. To successfully generate this module, the intel parallel
studio provided "Intel Python" environment may be used, otherwise, a
`mamba` environment must be created. From this directory (or with the
`environment.yml` in this directory handy), conduct the following
interactive session:

```bash
# request 1 core of the debug partition for max time (15m) 
aux-interactive 
# Once the debug core is allocated, load the intel compiler from 
# 2020 into the environment, and load the latest mamba module
module load intel/parallel-studio-2020.4 mamba/latest
## OPTIONAL
# Create the intel python environment
mamba env create -f environment.yml
```

Compiling interactively
-----------------------

From a login node (assuming no custom `mamba` environment):

```bash
# request an interactive session on the lightwork partition
aux-interactive
# Once the debug core is allocated, load the intel compiler from 
# 2020 into the environment
module load intel/parallel-studio-2020.4 
# compile the fortran code with f2py
bash make.sh
# verify the existence of the module and check it by running test
python test_mod_build.py
```

Compiling with sbatch 
---------------------

From a login node:

```bash
sbatch make_job.sh
```

Verify the `slurm` out file that the `test_mod_build.py` run was
successful




<img 
  src="https://github.com/ASU-KE/rc-assets/blob/main/logos/ASURC_color_600.png?raw=true" 
  width="240" >
