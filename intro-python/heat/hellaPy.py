from matplotlib import use, rcParams, cm, colors,font_manager
#use('Agg')
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

default_style = hellaPy('serif')

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

def mycontourf(*args,edgecolor='face',**kwargs):
  cf = pylab.contourf(*args,**kwargs)
  for c in cf.collections:
    c.set_edgecolor(edgecolor)
  return None
