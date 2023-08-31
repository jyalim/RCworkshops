# coding: utf-8
from numpy import *
def wiener(t,x0=0,mu=0,sigma=1):
  h = t[1]-t[0]
  h_= sqrt(h)
  x = 0 * t
  Nt= sigma*random.randn(len(t))+mu
  Nt[0]+= x0
  x = h_*cumsum(Nt)
  return x
    
t = linspace(0,1,1001)
for m in arange(9):
  for s in arange(1,10):
    x = array([ wiener(t,x0=0) for k in range(3) ])
    savetxt(f'mu{m}_sigma{s}_wiener.dat',c_[t,x.T])
    print(m,s)
    
