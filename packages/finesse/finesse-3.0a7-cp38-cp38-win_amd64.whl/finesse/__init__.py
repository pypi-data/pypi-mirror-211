# flake8: noqa

"""Finesse is a Python package for simulating interferometers in the frequency
domain."""


# start delvewheel patch
def _delvewheel_init_patch_1_3_7():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'finesse.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-finesse-3.0a7')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-finesse-3.0a7')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not ctypes.windll.kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError()))


_delvewheel_init_patch_1_3_7()
del _delvewheel_init_patch_1_3_7
# end delvewheel patch



import sys
import locale


PROGRAM = __name__
DESCRIPTION = "Simulation program for laser interferometers."

# Set the Finesse version.
try:
    from .version import version as __version__
except ImportError:
    raise Exception("Could not find version.py. Ensure you have run setup.")

# Set up some sensible default runtime options.
from .config import configure, autoconfigure

autoconfigure()

# Import a bunch of useful functions and classes into the top-level package.
from .env import (
    is_interactive,
    show_tracebacks,
    tb,
    session_instance as _session_instance,
)
from .constants import values as constants
from .parameter import Parameter, float_parameter
from .gaussian import BeamParam
from .model import Model
from .plotting import init as init_plotting
from .script import syntax, help_ as help
from .script import syntax

# Set up the user session.
session = _session_instance()

from .utilities.storage import save, load