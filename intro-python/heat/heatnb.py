import timeit
import sys
from hellaPy import *
import pylab as plt
import scipy.integrate as si
from numpy import *
from numpy.linalg import *
import nucheb as cheb
import numpy 

print('Running heat.py with numpy (CPU-MKL)')
SKIP = 200

def get_corner_elements(A):
  corner_ind = ix_((0,-1),(0,-1))
  return A[corner_ind]

def mybacksolve(A,b):
  # Solves A.T x.T = b.T and returns x = b A^{-1}
  x = solve(A.T,b.T)
  return x.T

def rk4(f,time,u):
  def method(h,f,t,u):
    k1 = h*f(t      ,u       )
    k2 = h*f(t+0.5*h,u+0.5*k1)
    k3 = h*f(t+0.5*h,u+0.5*k2)
    k4 = h*f(t+    h,u+    k3)
    return u + (k1+2*(k2+k3)+k4)/6
  U = zeros((len(time),len(u)))
  U[0] = u
  dt= diff(time)
  for k,t in enumerate(time):
    if k == 0:
      continue
    U[k] = method(dt[k-1],f,t,U[k-1])
    v = norm(U[k])
  return U

def main(N,tspan,h,gBC=r_[1,1]):
  # u_t = u_xx -1<x<1, with Neumann boundary conditions
  D2,D,x = cheb.cheb(N) 
  x = -x    # Reverse order of x so x(1) = -1.
  D = -D    # D is affected by reorder.
  u0 = cos(pi*x)+0.2*cos(5*pi*x)+1; # initial distribution.
# gBC= r_[1,1]                # Von Neumann Boundary Conditions
  B  = D2[1:-1,[0,-1]]        # u0 and uN still want to party,
  D2i= D2[1:-1,1:-1];         # but they werent invited to D2.
  A  = get_corner_elements(D) # Dem no flux conditions
  C  = D[[0,-1], 1:-1]        # allow us to rewrite B*[u0;uN]
  # Solving on interior of field:
  #    RHS = lambda t,u: D2@u + B@inv(A)@(gBC - C*u)
  # These are constant matrices! Compute them ONLY once.
  BiA   = mybacksolve(A,B)  # B A^{-1}
  Q     = D2i - BiA@C  
  b     = BiA@gBC 
  RHS   = lambda t,u: Q@u+b; 
  t     = arange(*tspan+r_[[0,h]],h)
  tic = timeit.default_timer()
  Ui  = rk4(RHS,t,u0[1:-1])
  toc = timeit.default_timer();
  # Build full solution
  M = len(t[::SKIP])
  U = zeros((M,len(x)))
  iAgBC = solve(A,gBC) # A^{-1} gBC compute once
  iAC   = solve(A,C  ) # A^{-1} C   compute once
  for k,uk in enumerate(Ui[::SKIP]):
    u0,uN = iAgBC-iAC@uk;
    U[k] = r_[u0,uk,uN]
  T,X = meshgrid(t[::SKIP],x,indexing='ij')
  # float is necessary to prevent 0-d array bug
  err = float(norm(D@U[-1]-1)/sqrt(N))
  return T,X,U,toc-tic,err

if __name__ == '__main__':
  mul = 1
  if len(sys.argv) > 1:
    mul = float(sys.argv[1])
  gBC = mul * r_[1.,1]
  N = 32
  tspan = [0,3]
  h = 1e-4
  print('Running heat equation solver with')
  print(f'       N = {N}')
  print(f'   tspan = [{tspan[0]},{tspan[1]}]')
  print(f'timestep = {h}')
  print(f'    flux = {gBC[0]}')
  T,X,U,ctime,err = main(N,tspan,h,gBC)
  print(f'Finished (wall time): {ctime}')
  plt.figure(1,figsize=(10,7))
  mycontourf(T,X,U,numpy.linspace(-1,1)*numpy.abs(U).max(),cmap=mycm15,edgecolor='#999999')
  plt.xticks(fontsize=25)
  plt.yticks(fontsize=25)
  plt.xlabel('time',fontsize=30)
  plt.ylabel('space',fontsize=30)
  plt.title(f'Solution case: {int(mul):3d}',fontsize=36)
  plt.savefig(f'figs/out_{int(mul):03d}.png')
