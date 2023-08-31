#!/packages/apps/intel/intelpython3/bin/python
print('RUNNING test_mod_build')
try:
  from numpy import *
  import d3zslat_reader as dr
  dr.reader.read_file('o71e-2_a15e-2_tr2e2_longbox_ps_00099')
  x,D = dr.cheb(16,2e0)
  print('SUCCESS -- test_mod_build')
except Exception as ex:
  print('FAILED -- test_mod_build -- EXCEPTION ENCOUNTERED: ', ex)

