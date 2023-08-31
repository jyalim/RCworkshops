print('RUNNING test_mod_build')
try:
  from numpy import *
  import d2reader as dr
  wobl = dr.reader.read_wobl_file('o141e-2_a1e-2_Th30e0_m72_np1e3.000009')
  x,D  = dr.cheb(dr.reader.m,dr.reader.asp)
  print('SUCCESS -- test_mod_build')
except Exception as ex:
  print('FAILED -- test_mod_build -- EXCEPTION ENCOUNTERED: ', ex)

