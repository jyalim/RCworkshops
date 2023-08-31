#!/bin/bash
# ======================================================================
# Wraps fortran 90 code for python
# 
# Environment Requires:
#   module load intel/parallel-studio-2020.4 
#   and, if necessary, appropriate python env
# ======================================================================
prefix=d3zslat_reader
opts=(
  ${prefix}.F90     # Fortran file to compile
  -m ${prefix}      # Resultant module file
  -c                # Allow f2py to accept compiler options
  # Specify compilier family (intel)
  --fcompiler=intelem
  # Specify optimization level, allow vectorization and parallel mkl
  # NOTE: MKL_NUM_THREADS env variable will limit parallel execution
  --opt="-O3 -x core-avx2 -march=core-avx2 -mkl=parallel -qopenmp"
)
f2py "${opts[@]}"
