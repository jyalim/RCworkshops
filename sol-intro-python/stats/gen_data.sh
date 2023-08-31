#!/bin/sh
# Used to generate the data for the statistics exercise
##

gen_data() {
  seed="$1"
  /packages/envs/scicomp/python << __EOF
import numpy as np
seed = $seed
np.random.seed(seed=seed)
N = 501
x = 2*np.pi*np.linspace(0,1,N)[:-1]
y = np.sin(x)
z = np.random.normal(0,0.1,len(y))
np.savetxt(f"dat/seed_{seed:03d}.txt",np.c_[x,y+z],header='',comments='')
__EOF
  echo $seed
}

! [[ -d dat/ ]] && mkdir dat/ || :

export -f gen_data

N=$(nproc)
parallel -kvj$N gen_data ::: $(seq 0 999)
