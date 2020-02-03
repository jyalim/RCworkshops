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
  return D,x.flatten()

def cheb_card(xc,xp,TOL=1e-10):
  """
  ======================================================================
  cheb_card
  ----------------------------------------------------------------------
    Computes Cardinal function for Gauss Lobatto Chebyshev grid onto
    onto an arbitrary domain
  ----------------------------------------------------------------------

  Parameters
  ----------
  xc : array_like, shape (N,) or (N,1)
    `M` Gauss Lobatto Chebyshev coordinates
  xp : array_like, shape (K,) or (K,1)
    `K` coordinates to be interpolated onto 
  TOL: float, optional
    Tolerance for machine zero, default is 10^{-10}.

  Returns
  -------
  C : array_like, float, shape (N,K)
    Cardinal operator for the interpolant.

  Notes
  -----
  Uses the Chebyshev Gauss Lobatto Cardinal functions such that the
  interpolation is given by matrix multiplication.

      C_{n}(xp_k) =
        (-1)^{n+1} \frac{1-xp_k**2}{c_n M**2 (xp_k-xc_n)} \frac{dT_M(xp_k)}{dx},

  where `M = N-1`. But note that,

      \frac{dT_M(xp_k)}{dx} = M U_{M-1} = M \frac{\sin(M \theta)}{\sin(\theta)},

  which implies,

      C_{n}(xp_k) =
        (-1)^{n+1} \frac{1-xp_k**2}{c_n M (xp_k-xc_n)} U_{M-1}.

  See reference [1] for more details.

  References
  ----------

  [1] Boyd, John P., 2000, `Chebyshev and Fourier Spectral Methods`,
      Dover. 
  """
  N,K  = len(xc),len(xp)
  M    = N - 1
  c    = np.ones(N); c[[0,-1]] = .5
  C    = np.ones((N,K))
  th   = np.arccos(xp[1:-1])
  card_dTdx = (np.sin(M*th)/np.sin(th))*(1-xp[1:-1]**2)/float(M)
  card_dTdx = np.r_[ 0, card_dTdx, 0 ]

  for n in range(N):
    for k in range(K):
      dx = xp[k] - xc[n] 
      if np.abs(dx) >= TOL:
        C[n,k] = (-1)**(n+1) * c[n] * card_dTdx[k] / dx
  return C

def cheb_interp(xc,zc,xp,zp,cheb_fields):
  """
  ======================================================================
  cheb_interp
  ----------------------------------------------------------------------
    Performs two dimensional Gauss Lobatto Chebyshev interpolation
    onto an arbitrary two dimensional grid for passed fields
  ----------------------------------------------------------------------

  Parameters
  ----------
  xc : array_like, shape (M,) or (M,1)
    `M` Gauss Lobatto Chebyshev x-coordinates
  zc : array_like, shape (N,) or (N,1)
    `N` Gauss Lobatto Chebyshev x-coordinates
  xp : array_like, shape (K,) or (K,1)
    `L` x-coordinates to be interpolated onto 
  zp : array_like, shape (L,) or (L,1)
    `L` z-coordinates to be interpolated onto 
  cheb_fields : dictionary, shape (j,(M,N))
    List of `j` data fields to be interpolated onto the specified domain

  Returns
  -------
  int_fields  : dictionary, shape (j,(K,L))
    List of `j` interpolated data fields

  Notes
  -----
  Uses the Chebyshev Gauss Lobatto Cardinal functions such that the
  interpolation is given by matrix multiplication.

  References
  ----------

  [1] Boyd, John P., 2000, `Chebyshev and Fourier Spectral Methods`,
      Dover

  """
  M,N = len(xc),len(zc)
  K,L = len(xp),len(zp)
  Cx = cheb_card(xc,xp)
  Cz = cheb_card(zc,zp)
  int_fields = {}
  for field in cheb_fields:
    int_fields[field] = Cx.T @ cheb_fields[field] @ Cz
  return int_fields

def clenshaw_curtis_quad(L):
  """
  ======================================================================
  clenshaw_curtis_quad
  ----------------------------------------------------------------------
    Performs two dimensional Gauss Lobatto Chebyshev interpolation
    onto an arbitrary two dimensional grid for passed fields
  ----------------------------------------------------------------------

  Parameters
  ----------
  L  : integer
    Lth degree polynomial quadrature.

  Returns
  -------
  w  : array_like, shape(L)
    array of weights

  Notes
  -----
  For Even degreed polys

  References
  ----------
  """
  w = np.zeros(L+1)
  w[[0,-1]] = 1./(L**2 - 1.)
  pi = np.pi
  for k in range(1,L):
    for j in range(1,L//2):
      w[k] += 2./(1.-4.*j**2)*np.cos(2.*k*j*pi/L)
    w[k] += 1. + np.cos(k*pi) / (1.-L**2)
    w[k] *= 2. / L
  return w

def cheb_1st_roots(N):
  """
  ======================================================================
  cheb_1st_roots
  ----------------------------------------------------------------------
    Returns roots of the Chebyshev Polynomial of the First Kind order N
  ----------------------------------------------------------------------

  Parameters
  ----------
  N : int
    Order of the First Chebyshev polynomial 
    
  Returns
  -------
  x : array_like, float, shape (N,)
    Roots of First Kind Chebyshev Polynomial of Order N

  References
  ----------

  [1] 
     

  """
  M = N+1
  pi= np.pi
  k = np.arange(1,M)
  x = np.cos((2*k-1)/(2*N)*pi)
  return x
