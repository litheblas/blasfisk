#!/usr/bin/python
import sys
from subprocess import call

mpc = 'mpc_real2'

if sys.argv[2] == 'playlist':
    call([mpc, 'playlist'])
elif sys.argv[2]:
    pass
else:
    call([mpc])