#!/bin/bash
# ======================================================================
# Wraps fortran 90 code for python
# 
# Environment Requires:
#   module load intel/2019.4
#   and appropriate python env
# ======================================================================
prefix=d3zslat_reader
opts=(
  ${prefix}.F90     # Fortran file to compile
  -m ${prefix}      # Resultant module file
  -c                # Allow f2py to accept compiler options
  # Specify compilier family (intel)
  --fcompiler=intel 
  # Specify optimization level, allow vectorization and parallel mkl
  # NOTE: MKL_NUM_THREADS env variable will limit parallel execution
  --opt="-O3 -xCORE-AVX2 -axCORE-AVX512,MIC-AVX512 -mkl=parallel"
)
f2py "${opts[@]}"
