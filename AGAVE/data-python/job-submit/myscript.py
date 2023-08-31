import numpy as np
import pylab as plt
from plt_style import *
from scipy.stats import norm
import sys

def parse_token(string,token,delim='_'):
  return string.split(token)[-1].split(delim)[0]

def main(f):
  pr = f.split('/')[-1]
  mu    = parse_token(f,'mu')
  sigma = parse_token(f,'sigma')
  print(mu,sigma)
  d = np.loadtxt(f).T
  t = d[0]
  X = d[1:]
  order = X[np.arange(len(X)),X.argmax(axis=1)].argsort()
  plt.figure(1,figsize=(10,6))
  for x in X[order]:
    plt.plot(t,x,'-')
  plt.xlim(*t[[0,-1]])
  plt.ylim(-5,5)
  plt.xlabel(r'$t$')
  plt.ylabel(r'$x_t$')
  plt.title(rf'$\mu=$ {mu} $\sigma=$ {sigma}')
  plt.savefig(f'fig/out_{pr}.png',bbox_inches='tight')
  plt.close()
  return None


if __name__ == '__main__':
  try:
    f = sys.argv[1]
    main(f)
  except Exception as ex:
    print('EXCEPTION: ',ex)
    sys.exit(1)

