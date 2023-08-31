from matplotlib import rcParams,rc,font_manager as fm
from pathlib import Path
import glob
import pylab as plt

home_dir  = str(Path.home())
font_dirs = ['{:s}/.local/etc/fonts'.format(home_dir),]
font_recs = fm.findSystemFonts(fontpaths=font_dirs)
font_list = fm.createFontList(font_recs)
fm.fontManager.ttflist.extend(font_list)

gld = '#FFC627'
mrn = '#8C1D40'
dpu = '#0C0C12'
gry = '#77777777'

#rcParams['axes.facecolor']    = '#111111'
#rcParams['axes.edgecolor']    = 'w'
#rcParams['figure.facecolor']  = '#111111'
#rcParams['xtick.color']       = 'w'
#rcParams['ytick.color']       = 'w'
#rcParams['text.color']        = 'w'

style_dict = {
  'axes.facecolor'   : '#111111',
  'axes.edgecolor'   : 'w',
  'figure.facecolor' : '#111111',
  'xtick.color'      : 'w',
  'ytick.color'      : 'w',
  'text.color'       : 'w',
  'font.weight'      : 'bold',
  'font.size'        : 24,
  'axes.labelsize'   : 24,
  'axes.titlesize'   : 24,
  'font.family'      : 'sans-serif',
  'font.sans-serif'  : ['Roboto'],
  'mathtext.fontset' : 'stixsans',
  'text.usetex'      : False,
}

lblprops = {
  'color':'w',
  'fontsize':24,
}

for k,v in style_dict.items():
  rcParams[k] = v

def my_plot(x,y,*args,**kwargs):
  for k,v in style_dict.items():
    rcParams[k] = v
  plt.plot(x,y,*args,**kwargs)

def my_scatter(x,y,*args,**kwargs):
  for k,v in style_dict.items():
    rcParams[k] = v
  plt.scatter(x,y,*args,**kwargs)
