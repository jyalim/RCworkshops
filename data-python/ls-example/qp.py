from hellaPy import *
from numpy import *
from pylab import *
import d2reader as dr
import cheb 
import glob,natsort
import sys,os
import pandas as pd

L = linspace(-1,1,16)

def get_token(bn,token):
  bnp = bn
  if '_anim' in bn:
    bns = bnp.split('_anim')
    bnp = bns[0] + bns[-1]
  return bnp.split(token)[-1].split('_')[0]

def r(f,PRINT_MODE=True):
  if PRINT_MODE:
    print(f'READING: {f:s}',file=sys.stderr)
  bn    = os.path.basename(f)
  Rns   = get_token(bn,'Rn')
  oms   = get_token(bn,'o')
  als   = get_token(bn,'a')
  ind   = get_token(bn,'_')
  Rn    = float(Rns)
  om    = float(oms)
  al    = float(als)
  dr.reader.read_wobl_file(f)
  x,y   = dr.reader.x+0,dr.reader.y+0
  Dx,Dy = dr.reader.dx+0,dr.reader.dy+0
  u,v,T = dr.reader.u+0,dr.reader.v+0,dr.reader.t+0
  Darr  = [x,y,Dx,Dy,u,v,T]
  dudx,dudy,dvdx,dvdy,dTdx,dTdy,d2Tdxx,d2Tdyy,eta = dr.partials(*Darr)
  dr.reader.dealloc_arrays()
  X,Z = meshgrid(x,y,indexing='ij')
  Th   = T-Z
  D = {
    'ind'  : ind,
    'Rn'   : Rns,
    'om'   : oms,
    'al'   : als,
    'x'    : x+0,
    'z'    : y+0,
    'X'    : X+0,
    'Z'    : Z+0,
    'u'    : (u+0)/Rn,
    'v'    : (v+0)/Rn,
    'T'    : T+0,
    'Th'   : Th,
    # vorticity is reported as y-component not z-component 
    # (really u_z - w_x, not v_x - u_y)
    'eta'  : -(eta+0)/Rn,
    'dTdx' : dTdx+0,
  }
  D['ens'] = D['eta']**2
  return D

def get_stats(globbed_files,field,N=23):
  bn    = os.path.basename(globbed_files[0])
  print(f'READING: {bn:s}',file=sys.stderr)
  oms   = get_token(bn,'o')
  als   = get_token(bn,'a')
  D  = array([ r(f,PRINT_MODE=False)[field] for f in globbed_files ])
  Dm = D.mean(axis=0)
  Ds = D.std( axis=0)
  DmN= Dm[N:-N,N:-N]
  DsN= Ds[N:-N,N:-N]
  wx= cheb.clenshaw_curtis_quad(len(Dm)-1)/2
  wN= wx[N:-N]
  Mx,Mz = DmN.shape
  DM_ima = abs(D[:,N:-N,N:-N]).max()
  DM_gma = abs(D).max()
  Dm_ima = sqrt(wN@DmN**2@wN)
  Ds_ima = sqrt(wN@DsN**2@wN)
  Dm_gma = sqrt(wx@Dm**2@wx)
  Ds_gma = sqrt(wx@Ds**2@wx)
  K = [
    f'alpha',
    f'omega',
    f'{field}_max_ima',
    f'{field}_max_gma',
    f'{field}_mean_ima',
    f'{field}_mean_gma',
    f'{field}_std_ima',
    f'{field}_std_gma',
  ]
  D = [
    als,
    oms,
    DM_ima,
    DM_gma,
    Dm_ima,
    Dm_gma,
    Ds_ima,
    Ds_gma,
  ]
  return K,D

def get_stats_mean_last(globbed_files,field,N=23):
  bn    = os.path.basename(globbed_files[0])
  print(f'READING: {bn:s}',file=sys.stderr)
  Rns   = get_token(bn,'Rn')
  oms   = get_token(bn,'o')
  als   = get_token(bn,'a')
  D      = array([ r(f,PRINT_MODE=False)[field] for f in globbed_files ])
  DM_ima = abs(D[:,N:-N,N:-N]).max()
  DM_gma = abs(D).max()
  wx= cheb.clenshaw_curtis_quad(len(D[0])-1)/2
  wN= wx[N:-N]
  Dl2= sqrt(array([ wN@d[N:-N,N:-N]**2@wN for d in D ]))
  DL2= sqrt(array([ wx@d**2@wx for d in D ]))
  Dm_gma = DL2.mean()
  Ds_gma = DL2.std()
  Dm_ima = Dl2.mean()
  Ds_ima = Dl2.std()
  K = [
    f'amplitude',
    f'Rn',
    f'omega',
    f'{field}_max_ima',
    f'{field}_max_gma',
    f'{field}_mean_ima',
    f'{field}_mean_gma',
    f'{field}_std_ima',
    f'{field}_std_gma',
  ]
  D = [
    als,
    Rns,
    oms,
    DM_ima,
    DM_gma,
    Dm_ima,
    Dm_gma,
    Ds_ima,
    Ds_gma,
  ]
  return K,D

def get_stats_sqrt_last(globbed_files,field,N=23):
  bn    = os.path.basename(globbed_files[0])
  print(f'READING: {bn:s}',file=sys.stderr)
  Rns   = get_token(bn,'Rn')
  oms   = get_token(bn,'o')
  als   = get_token(bn,'a')
  D      = array([ r(f,PRINT_MODE=False)[field] for f in globbed_files ])
  DM_ima = abs(D[:,N:-N,N:-N]).max()
  DM_gma = abs(D).max()
  wx= cheb.clenshaw_curtis_quad(len(D[0])-1)/2
  wN= wx[N:-N]
  Dl2= array([ wN@d[N:-N,N:-N]**2@wN for d in D ])
  DL2= array([ wx@d**2@wx for d in D ])
  Dm_gma = sqrt(DL2.mean())
  Dm_ima = sqrt(Dl2.mean())
  K = [
    f'amplitude',
    f'Rn',
    f'omega',
    f'{field}_max_ima',
    f'{field}_max_gma',
    f'{field}_mean_ima',
    f'{field}_mean_gma',
  ]
  D = [
    als,
    Rns,
    oms,
    DM_ima,
    DM_gma,
    Dm_ima,
    Dm_gma,
  ]
  return K,D

def get_blayer_thickness(field):
  q    = abs(field)
  m,n  = [ k-1 for k in q.shape ]
  dx,x = cheb.cheb(m)
  dz,z = cheb.cheb(n)
  x /= 2
  z /= 2
  halfx_ind = m//2
  halfz_ind = n//2
  quarx_ind = m//4
  quarz_ind = n//4
  mhalfx = abs(x[0]-x[q[:halfx_ind,halfz_ind].argmin()])
  mhalfz = abs(z[0]-z[q[halfx_ind,:halfz_ind].argmin()])
  mquarx = abs(x[0]-x[q[:halfx_ind,quarz_ind].argmin()])
  mquarz = abs(z[0]-z[q[quarx_ind,:halfz_ind].argmin()])
  Mhalfx = abs(x[0]-x[q[:halfx_ind,halfz_ind].argmax()])
  Mhalfz = abs(z[0]-z[q[halfx_ind,:halfz_ind].argmax()])
  Mquarx = abs(x[0]-x[q[:halfx_ind,quarz_ind].argmax()])
  Mquarz = abs(z[0]-z[q[quarx_ind,:halfz_ind].argmax()])
  mhx = q[:halfx_ind,halfz_ind].min()
  mhz = q[halfx_ind,:halfz_ind].min()
  mqx = q[:halfx_ind,quarz_ind].min()
  mqz = q[quarx_ind,:halfz_ind].min()
  Mhx = q[:halfx_ind,halfz_ind].max()
  Mhz = q[halfx_ind,:halfz_ind].max()
  Mqx = q[:halfx_ind,quarz_ind].max()
  Mqz = q[quarx_ind,:halfz_ind].max()
  Q   = {
    "mhalfx":mhalfx,
    "mhalfz":mhalfz,
    "mquarx":mquarx,
    "mquarz":mquarz,
    "Mhalfx":Mhalfx,
    "Mhalfz":Mhalfz,
    "Mquarx":Mquarx,
    "Mquarz":Mquarz,
    "mhx":   mhx,
    "mhz":   mhz,
    "mqx":   mqx,
    "mqz":   mqz,
    "Mhx":   Mhx,
    "Mhz":   Mhz,
    "Mqx":   Mqx,
    "Mqz":   Mqz,
  }
  return Q

def get_amplitude(globbed_files,field,ima=None,gma=None,N=23):
  bn  = os.path.basename(globbed_files[0])
  print(f'READING: {bn:s}',file=sys.stderr)
  Rns = get_token(bn,'Rn')
  oms = get_token(bn,'o')
  als = get_token(bn,'a')
  D0  = r(globbed_files[0],PRINT_MODE=False)
  X,Z = D0['X'],D0['Z']
  D   = array([ r(f,PRINT_MODE=False)[field] for f in globbed_files ])
  DM  = abs(D).max(axis=0)
  if ima == None:
    ima = abs(DM[N:-N,N:-N]).max()
  if gma == None:
    gma = abs(DM).max()
  p_amplitude(X,Z,DM,Rns,oms,f'{field}',ima=ima,gma=gma)
  return Rns,oms,DM

def p_amplitude(X,Z,q,Rn,om,fn,ima=5e-3,gma=5e-1):
  out = f'out/amps/out_Rn{Rn:s}_o{om:s}_{fn:s}.png'
  print(f'Plotting {out}',file=sys.stderr)
  f,a = no_ax_fax(fs_base=10)
  if gma > ima:
    mycontourf(X,Z,q,linspace(-gma,-ima,3),cmap=myBlues,lw=0.5,lc='#777777')
    mycontourf(X,Z,q,linspace( ima, gma,3),cmap=myReds,lw=0.5,lc='#777777')
  mycontourf(X,Z,q,ima*L,cmap=mycm15,lw=0.5,lc='#777777')
  savefig(out)
  return None

def get_maxes_over_glob(globbed_files,field_list,N=23):
  bn    = os.path.basename(globbed_files[0])
  print(f'READING: {bn:s}',file=sys.stderr)
  oms   = get_token(bn,'o')
  als   = get_token(bn,'a')
  D      = array([ r(f,PRINT_MODE=False) for f in globbed_files ])
  K = [ 'amplitude' , 'omega' ]
  Q = [ als, oms ]
  for field in field_list:
    DD = abs(array([ d[field] for d in D ]))
    DM_ima = DD[:,N:-N,N:-N].max()
    DM_gma = DD.max()
    K.extend((f'{field}_max_ima', f'{field}_max_gma'))
    Q.extend((DM_ima,DM_gma))
  return K,Q

def p(X,Z,q,k,om,fn,ima=5e-3,gma=5e-1):
  print(f'Plotting for {k:s}',file=sys.stderr)
  f,a = no_ax_fax(fs_base=6)
  if gma > ima:
    mycontourf(X,Z,q,linspace(-gma,-ima,3),cmap=myBlues,lw=0.5,lc='#777777')
    mycontourf(X,Z,q,linspace( ima, gma,3),cmap=myReds,lw=0.5,lc='#777777')
  mycontourf(X,Z,q,ima*L,cmap=mycm15,lw=0.5,lc='#777777')
  savefig(f'out/out_om{om:s}_{fn:s}_{k:s}.png')
  return None

def do_plt(f,g,W):
  Q = r(f)
  ind = Q['ind']
  om  = Q['om']
  al  = Q['al']
  q   = {w:Q[w] for w in W}
  x,z = Q['x'],Q['z']
  X,Z = Q['X'],Q['Z']
  # for interp
  xs    = linspace(-1,1,601)
  Xs,Zs = meshgrid(xs,xs,indexing='ij')
  qs = cheb.cheb_interp(x*2,z*2,xs,xs,q)
  Nc = 23
  Ns = abs(xs+.9).argmin()+1
  df = pd.read_csv(g,delim_whitespace=True)
  dfa= df.loc[df.amplitude==float(al)]
  omi= isclose(dfa.omega,float(om),rtol=1e-7)
  ldf= dfa.loc[omi]
  for w in W:
    if w == 'T':
      ima,gma = 0.5,0.5
    else:
      ima = ldf[f'{w}_max_ima'].values[0]
      gma = ldf[f'{w}_max_gma'].values[0]
    p(Xs,Zs,qs[w],ind,om,w,ima=ima,gma=gma)

if __name__ == '__main__':
  f = sys.argv[1]
  w = sys.argv[2]
  k = f.split('_')[-1]
  om= f.split('/')[-1].split('o')[-1].split('_')[0]
  al= f.split('/')[-1].split('a')[-1].split('_')[0]
  Q = r(f)
  q = Q[w]
  x,z = Q['x'],Q['z']
  X,Z = Q['X'],Q['Z']
  # for interp
  xs = linspace(-1,1,601)
  Xs,Zs = meshgrid(xs,xs,indexing='ij')
  qs = cheb.cheb_interp(x*2,z*2,xs,xs,{w:q})[w]
  Nc = 23
  Ns = abs(xs+.9).argmin()+1
  ima,gma = abs(qs[Ns-1:-Ns,Ns-1:-Ns]).max(),abs(qs).max()
  p(Xs,Zs,qs,k,om,w,ima=ima,gma=gma)
  print(ima,gma)
