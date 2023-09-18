from hellaPy import *
import cheb
import qp
from numpy import *
from pylab import *

def qLS(field,cutoff_mode=100):
  M,N = [ k-1 for k in field.shape ]
  Dx,x= cheb.cheb(M)
  Dz,z= cheb.cheb(N)
  wx  = cheb.clenshaw_curtis_quad(M) 
  wz  = cheb.clenshaw_curtis_quad(N)
  x,z,wx,wz = x/2,z/2,wx/2,wz/2
  bl  = qp.get_blayer_thickness(field)
  mx  = max(bl['mhalfx'],bl['mhalfz'])
  clip= abs(x-(x[0]-mx)).argmin()
  print(clip,mx)
  X,Z = meshgrid((x+0.5)*pi,(z+0.5)*pi,indexing='ij')
  C   = zeros((cutoff_mode,cutoff_mode))
  for m in range(1,cutoff_mode):
    for n in range(1,cutoff_mode):
      C[m,n] = LS(field,X,Z,wx,wz,m,n,clip=clip)
  return C

def Th(X,Z,m,n):
  return sin(m*X)*sin(n*Z)

def LS(field,X,Z,wx,wz,m,n,clip=40):
  f = field[clip:-clip,clip:-clip]
  q = Th(X,Z,m,n)[clip:-clip,clip:-clip]
  Wx= wx[clip:-clip]
  Wz= wz[clip:-clip]
  qn= Wx@(f*q)@Wz
  qd= Wx@(q*q)@Wz
  return qn/qd

mkl_set_num_threads(2)
# Structure of Dict:
#   Rn : (Rn,frequency,eta_amplitude)
Q = load('m1n1_eta_amplitude.pykl',allow_pickle=True).item()
C = { Rn : qLS(Q[Rn][-1]) for Rn in Q.keys() }
D = { Rn : diag(C[Rn])[1::2] for Rn in C.keys() }

Rn_labels = { Rn : '$10^{'+Rn.split('e')[-1]+'}$' for Rn in D.keys() }

figure(1,figsize=(10,10))
for Rn in D.keys():
  c = D[Rn]
  loglog(arange(len(c))*2+1,abs(c),'o-',label=Rn_labels[Rn])
legend()
xlabel(r'$m$')
ylabel(r'$\dfrac{\langle A(\eta),\eta_{m:m}\rangle}{\|\eta_{m:m}\|^2}$')
s = sqrt(10)
loglog(r_[   1,  10],r_[1e-2,1e-4],'-',lw=3,c='#77777777')
loglog(r_[  10,s*10],r_[1e-4,5e-6],'-',lw=3,c='#00007777')
loglog(r_[s*10, 100],r_[5e-6,5e-8],'-',lw=3,c='#77000077')
annotate(r'$\Delta=-2$',xy=( 3,2.0e-3),fontsize=18,rotation=-28)
annotate(r'$\Delta=-3$',xy=(15,5.0e-5),fontsize=18,rotation=-37)
annotate(r'$\Delta=-4$',xy=(50,1.5e-6),fontsize=18,rotation=-45)
yticks(10.**arange(-10,-1))
xlim(1,100)
ylim(1e-10,1e-2)
savefig('figs/proj.png',bbox_inches='tight')
