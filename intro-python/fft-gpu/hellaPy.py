from matplotlib import use, rcParams, cm, colors,font_manager
use('Agg')
import numpy, pylab
import ctypes
from sys import path
from pathlib import Path

home_dir  = str(Path.home())
font_dirs = ['{:s}/.local/etc/fonts'.format(home_dir),]
font_recs = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_recs)
font_manager.fontManager.ttflist.extend(font_list)

rcParams.update({
  'figure.autolayout'  : False,
  'figure.figsize'     : (8,6),
  'figure.facecolor'   : [1,1,1,0],
  'figure.edgecolor'   : [0,0,0,1],
  'figure.dpi'         : 100,
  'text.usetex'        : True,
  'text.latex.preamble': [
    r'\usepackage{amsmath,amssymb,bm}',
#   r'\usepackage{siunitx}',
  ],
  # Plot boundary properties
  'axes.linewidth'     : 1.75,
  'axes.edgecolor'     : [0,0,0,1],
  'axes.facecolor'     : [1,1,1,1],
  # Axes/Font spacing and size
  'font.size'            : 28,
  'axes.labelsize'       : 28,
  'axes.titlesize'       : 28,
  'xtick.major.pad'      : 10,
  'xtick.minor.pad'      : 10,
  'xtick.major.size'     : 8,
  'xtick.minor.size'     : 4,
  'xtick.major.width'    : 1.25,
  'xtick.minor.width'    : 1.25,
  'xtick.minor.visible'  : True,
  'xtick.direction'      : 'in',
  'xtick.bottom'         : True,
  'xtick.top'            : True,
  'ytick.major.pad'      : 10,
  'ytick.minor.pad'      : 10,
  'ytick.major.size'     : 8,
  'ytick.minor.size'     : 4,
  'ytick.major.width'    : 1.25,
  'ytick.minor.width'    : 1.25,
  'ytick.minor.visible'  : True,
  'ytick.direction'      : 'in',
  'ytick.left'           : True,
  'ytick.right'          : True,
  'legend.numpoints'     :  1,
  'legend.fontsize'      : 18,
  # Line and marker styles
  'lines.linewidth'       : 1,
  'lines.linestyle'       : '-',
  'lines.color'           : 'k',
  'lines.marker'          : None,
  'lines.markeredgewidth' : 1,
  'lines.markersize'      : 5,
  # Colormap
  'image.cmap'            : 'viridis',
  # Fonts
  'font.serif'            : [ 
      'Latin Modern Roman',
      'Computer Modern Roman',
      'Times',
      'Times New Roman',
      'Bitstream Vera Serif',
  ], 
  'font.sans-serif'       : [
      'Open Sans',
      'Computer Modern Sans',
      'Bitstream Vera Sans'
  ],
  'font.monospace'        : [
      'Anonymous Pro', 
      'Bitstream Vera Sans Mono'
  ],
  ### Saving Figures
# 'savefig.transparent'   : True,
})

class ColorBasis:
  # Default Colors
  r = numpy.array([ 1.,0.,0.,0. ])
  g = numpy.array([ 0.,1.,0.,0. ])
  b = numpy.array([ 0.,0.,1.,0. ])
  a = numpy.array([ 0.,0.,0.,1. ])
  # Initial Call
  def __init__(self, red=r,green=g,blue=b,alpha=a ):
    self.r    = red    # red
    self.g    = green  # green
    self.b    = blue   # blue
    self.a    = alpha  # alpha
    self.rgba = numpy.vstack([ red, green, blue, alpha ])
    return None

  def dot(self,choice):
    return numpy.dot(self.rgba,choice)

class hellaPy:
  def __init__(self,*args):
    self.autolayout = True
    self.fontfamily = 'serif'
    self.font       = 'Latin Modern Roman'
    self.usetex     = True
    self.square     = (8,8)
    self.rectangle  = (8,6)
    self.figsize    = self.rectangle
    self.cmap       = 'viridis'
    for arg in args:
      if arg == 'sans':
        self.fontfamily = 'sans-serif'
    rcParams.update({
      'font.family' : self.fontfamily,  
    }) 
    return None

  def set_autolayout(self,autolayout_flag):
    self.autolayout = autolayout_flag
    rcParams.update({
      'figure.autolayout' : self.autolayout,
    })
    return None

  def set_fontfamily(self,family):
    self.fontfamily = family
    rcParams.update({
      'font.family' : self.fontfamily,
    })
    return None

  def set_font(self,font):
    self.font = font
    rcParams.update({
      'font.{}'.format(self.fontfamily) : self.font,
    })
    return None

  def set_tex(self,boolean=False):
    self.usetex = boolean
    rcParams.update({
      'text.usetex' : self.usetex 
    })
    return None
  
  def set_figsize(self,figsize):
    self.figsize = figsize
    rcParams.update({
      'figure.figsize' : self.figsize  
    })
    return None

  def set_cmap(self,cmap):
    self.cmap = cmap
    rcParams.update({
      'image.cmap' : self.cmap
    })
    return None
# End Class

# Colors
yellow = numpy.array([1.0,1.0,0.0,0.8])
red    = numpy.array([1.0,0.0,0.0,0.8])
black  = numpy.array([0.0,0.0,0.0,1.0])
blue   = numpy.array([0.0,0.7,0.8,0.8])
teal   = numpy.array([0.0,0.8,0.6,0.8])
gray   = numpy.array([0.3,0.3,0.3,0.5])

dyellow = numpy.array([0.7,0.7,0.0,0.6])
dred    = numpy.array([0.7,0.0,0.0,0.6])

greycm  = cm.get_cmap(name='Greys_r')
graycm  = cm.get_cmap(name='gray')
GRAYcm  = colors.ListedColormap( numpy.array([k//32/7*numpy.ones(3) for k in range(256)]))
GRAYCM  = colors.ListedColormap( numpy.array([k//4/63*numpy.ones(3) for k in range(256)]))

mysimpcm = colors.LinearSegmentedColormap.from_list('simple',[
 ( 0   ,'#FFFFFF'),
 ( 1   ,'#000000')
],N=2)

myRCS  = colors.LinearSegmentedColormap.from_list('myRCS',[
  ( 0.    ,'#FFFFFF'),
  ( 0.01  ,'#FFFF00'),
  ( 0.50  ,'#FFA500'),
  ( 1.    ,'#FF0000'),
])

mycm19 = colors.LinearSegmentedColormap.from_list('mycm19',[
 ( 0.   ,'#0000AF'),
 ( 1./18,'#0000CC'),
 ( 2./18,'#0000FF'),
 ( 3./18,'#0E62F2'),
 ( 4./18,'#0099FF'),
 ( 5./18,'#00B7FF'),
 ( 6./18,'#00DBFF'),
 ( 7./18,'#5AE8FF'),
 ( 8./18,'#AFF4FF'),
 ( .5   ,'#FFFFFF'),
 (10./18,'#FFFF00'),
 (11./18,'#FFE300'),
 (12./18,'#FFC500'),
 (13./18,'#FFAD00'),
 (14./18,'#F98B04'),
 (15./18,'#F94F04'),
 (16./18,'#FF0000'),
 (17./18,'#CD0000'),
 ( 1    ,'#AF0000')
])

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

myBlues = colors.LinearSegmentedColormap.from_list('myBlues',[
   ( 0.   ,'#0000AF'),
   ( 0.5  ,'#0000CC'),
   ( 1.   ,'#0000FF'),
])

myReds  = colors.LinearSegmentedColormap.from_list('myReds',[
  ( 0.   ,'#FF0000'),
  ( 0.5  ,'#CD0000'),
  ( 1.   ,'#AF0000'),
])

myBlWh = colors.LinearSegmentedColormap.from_list('myBlWh',[
  (  0./14,'#0000FF'),
  (  2./14,'#0E62F2'),
  (  4./14,'#0099FF'),
  (  6./14,'#00B7FF'),
  (  8./14,'#00DBFF'),
  ( 10./14,'#5AE8FF'),
  ( 12./14,'#AFF4FF'),
  ( 14./14,'#FFFFFF'),
])

myWhRd = colors.LinearSegmentedColormap.from_list('myWhRd',[
  ( 0./14,'#FFFFFF'),
  ( 2./14,'#FFFF00'),
  ( 4./14,'#FFE300'),
  ( 6./14,'#FFC500'),
  ( 8./14,'#FFAD00'),
  (10./14,'#F98B04'),
  (12./14,'#F94F04'),
  (14./14,'#FF0000'),
])

myKWh = colors.LinearSegmentedColormap.from_list('myKWh',[
  (  0./14,'#000000'),
  (  2./14,'#0E62F2'),
  (  4./14,'#0099FF'),
  (  6./14,'#00B7FF'),
  (  8./14,'#00DBFF'),
  ( 10./14,'#5AE8FF'),
  ( 12./14,'#AFF4FF'),
  ( 14./14,'#FFFFFF'),
])

default_style = hellaPy('serif')

# axes style with auto layout and no labels
#re = [.1408,.128,.79,.8115]

def basic_plotting_help():
  print('                                                            \n\
data_array   = loadtxt(datafilename)                                 \n\
xdata, ydata = data_array[:,0], data_array[:,1]                      \n\
                                                                     \n\
figure(figsize=(l,w),dpi=r) # l,w are floats that represent inches   \n\
clf()                                                                \n\
plot(xdata,ydata,style)     # style default is "-b" (blue solid line)\n\
xlabel(x_string)                                                     \n\
ylabel(y_string)                                                     \n\
legend(array_of_strings)    # Does not have to be an array           \n\
title(title_string)                                                  \n\
savefig("fig.eps")                                                   \n\
  ')
  return None

def normalize(x,y0=0.,y1=1.):
  x0, x1 = x.min(), x.max()
  fp0    = ( y1 - y0 ) / ( x1 - x0 )
  return y0 + ( x - x0 ) * fp0

def moving_average(x,N):
  cs = numpy.cumsum(numpy.r_[0,x])
  return (cs[N:]-cs[:-N])/N

ma = moving_average

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
  print('MKL ERROR -- ',ex)

#mkl_set_num_threads(1)

def no_ax_fax(k=1,Gamma=1,fs_base=6):
  fig = pylab.figure(k,figsize=(fs_base*Gamma,fs_base))
  ax  = pylab.Axes(fig,[0,0,1,1])
  ax.set_axis_off()
  fig.clf()
  fig.add_axes(ax)
  for a in fig.axes:
    a.get_xaxis().set_visible(False)
    a.get_yaxis().set_visible(False)
  return fig,ax

def mycontourf(*args,lc='face',lw=0,**kwargs):
  cf = pylab.contourf(*args,**kwargs)
  for c in cf.collections:
    c.set_edgecolor(lc)
    c.set_linewidth(lw)
  return None
