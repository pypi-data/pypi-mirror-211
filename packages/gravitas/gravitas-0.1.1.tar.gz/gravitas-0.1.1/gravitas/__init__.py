import sys
import os
import inspect

# COMPILER SETUP
if sys.platform == "linux" or sys.platform == "linux2":
    try:
        os.system('module load gcc') 
        # If we're on a compute cluster, intel compilers might be loaded
    except:
        print("Module load errored, compilation may fail")
        pass


os.environ['GRAVITAS_ROOT'] = os.path.dirname(
    os.path.abspath(inspect.getsourcefile(lambda: 0))
)
sys.path.insert(0, os.environ['GRAVITAS_ROOT'])


from .lib import *
from ._grav import _grav