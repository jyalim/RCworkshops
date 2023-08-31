#!/usr/bin/env python
# Author: Jason Yalim
# email:  yalim@asu.edu
import numpy as np

def cheb(N):
  """
  ======================================================================
  cheb
  ----------------------------------------------------------------------
    Computes Gauss Lobatto Chebyshev derivative matrix and domain for
    polynomial of order `N`
  ----------------------------------------------------------------------

  Parameters
  ----------
  N : int
    Order of the Chebyshev polynomial 
    
  Returns
  -------
  D2: array_like, float, shape (N+1,N+1)
    Gauss Lobatto Chebyshev Second-Derivative matrix 
  D : array_like, float, shape (N+1,N+1)
    Gauss Lobatto Chebyshev Derivative matrix 
  x : array_like, float, shape (N+1,)
    Gauss Lobatto Chebyshev domain

  References
  ----------

  [1] Trefethen, L.N., 2000. Spectral methods in MATLAB. SIAM.
      https://doi.org/10.1137/1.9780898719598

  """
  D,x = 0.,1.
  if N==0:
    return D,x
  x = np.cos(np.pi*np.arange(N+1)/N).reshape(-1,1)
  c = (np.array([ 2, *np.ones(N-1), 2 ]) * (-1)**(np.arange(N+1))).reshape(-1,1)
  dx= x - x.T
  D = (c @ ( 1/c.T )) / (dx + np.eye(N+1))
  D-= np.diag(np.sum(D,1))
  D2 = D@D
  D2 = 0.5 * (D2 + D2[::-1,::-1])
  D2-= np.diag(np.sum(D2,1))
  return D2,D,x.flatten()

