#!/packages/envs/scicomp/bin/python
import numpy as np
def wiener(t,x0=0,mu=0,sigma=1):
  # Euler-Maruyama 
  h_ = np.sqrt(t[1]-t[0])
  Nt = h_*(sigma*np.random.randn(len(t))+mu*h_)
  Nt[0] = x0
  x = np.cumsum(Nt)
  return x
    
if __name__ == '__main__':
  np.random.seed(42)
  t = np.linspace(0,1,1001)
  for m in np.arange(10):
    for s in np.arange(1,11):
      x = np.array([ wiener(t,x0=0,mu=m,sigma=s) for k in range(3) ])
      np.savetxt(f'mu{m}_sigma{s}_wiener.txt',np.c_[t,x.T],fmt="%+14.7e")
      print(m,s)
      
