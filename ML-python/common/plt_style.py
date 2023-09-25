from matplotlib import rcParams,rc,font_manager as fm
from pathlib import Path
import glob
import pylab as plt

gld = '#FFC627'
mrn = '#8C1D40'
dpu = '#0C0C12'
gry = '#77777777'

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

def no_ax_fax(k=1,Gamma=1,fs_base=6):
  fig = plt.figure(k,figsize=(fs_base*Gamma,fs_base))
  ax  = plt.Axes(fig,[0,0,1,1])
  ax.set_axis_off()
  fig.clf()
  fig.add_axes(ax)
  for a in fig.axes:
    a.get_xaxis().set_visible(False)
    a.get_yaxis().set_visible(False)
  return fig,ax

mycm15 = plt.mpl.colors.LinearSegmentedColormap.from_list('mycm15',[
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

#home_dir  = str(Path.home())
#font_dirs = [ '/packages/public/fonts' ]
#font_recs = fm.findSystemFonts(fontpaths=font_dirs)
#font_list = fm.createFontList(font_recs)
#fm.fontManager.ttflist.extend(font_list)
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
# 'font.family'      : 'sans-serif',
# 'font.sans-serif'  : ['Roboto'],
# 'mathtext.fontset' : 'stixsans',
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
