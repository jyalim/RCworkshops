from matplotlib import rcParams, colors
import pylab
import ctypes

gld = '#FFC627'
mrn = '#8C1D40'
dpu = '#0C0C12'

rcParams.update({
  'axes.facecolor'   : '#111111',
  'axes.edgecolor'   : 'w',
  'figure.facecolor' : '#111111',
  'xtick.color'      : 'w',
  'ytick.color'      : 'w',
  'text.color'       : 'w',
  'font.size'        : 20,
  'axes.labelsize'   : 20,
  'axes.titlesize'   : 24,
})

def no_ax_fax(k=1,HGamma=1,Gamma=1,fs_base=6):
  fig = pylab.figure(k,figsize=(fs_base*Gamma,fs_base*HGamma))
  ax  = pylab.Axes(fig,[0,0,1,1])
  ax.set_axis_off()
  fig.clf()
  fig.add_axes(ax)
  for a in fig.axes:
    a.get_xaxis().set_visible(False)
    a.get_yaxis().set_visible(False)
  return fig,ax

mycm15 = colors.LinearSegmentedColormap.from_list('mycm15',[
  ( 0./14,'#0000FF'),
  ( 1./14,'#0E62F2'),
  ( 2./14,'#0099FF'),
  ( 3./14,'#00B7FF'),
  ( 4./14,'#00DBFF'),
  ( 5./14,'#5AE8FF'),
  ( 6./14,'#AFF4FF'),
  ( 7./14,'#FFFFFF'),
  ( 8./14,'#FFFF00'),
  ( 9./14,'#FFE300'),
  (10./14,'#FFC500'),
  (11./14,'#FFAD00'),
  (12./14,'#F98B04'),
  (13./14,'#F94F04'),
  (14./14,'#FF0000'),
])

def mycontourf(*args,lc='face',lw=0,**kwargs):
  cf = pylab.contourf(*args,**kwargs)
  for c in cf.collections:
    c.set_edgecolor(lc)
    c.set_linewidth(lw)
  return c

try: 
  mkl_rt = ctypes.CDLL('libmkl_rt.so')
  mkl_max_threads = mkl_rt.mkl_get_max_threads()

  def mkl_set_num_threads(threads):
    th = threads
    if th > mkl_max_threads:
      print('Threads: {:d} > {:d} Max Threads'.format(threads,mkl_max_threads))
      th = 1
    mkl_rt.mkl_set_num_threads(ctypes.byref(ctypes.c_int(th)))
    print('MKL THREADS SET: {:d}'.format(th))
    return None
except Exception as ex:
  pass