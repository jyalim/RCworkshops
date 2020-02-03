from numpy import *
import d2reader as dr

# Read d2tilt file
dr.reader.read_tilt_file('some-tilt-restart')
# Set values for rdt, omega, and alpha (undef in d2tilt)
dr.reader.rdt   = dr.reader.dt
dr.reader.omega = 0e0
dr.reader.alpha = 0e0
# Write d2wobl restart
dr.reader.write_wobl_file('new-wobl-restart')
