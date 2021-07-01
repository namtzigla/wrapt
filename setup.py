import os
import platform
import setuptools
from distutils import sysconfig
from distutils.core import setup
import platform

if platform.system() != 'Windows':  # When compilinig con visual no -g is added to params
    cflags = sysconfig.get_config_var('CFLAGS')
    opt = sysconfig.get_config_var('OPT')
    sysconfig._config_vars['CFLAGS'] = cflags.replace(' -g ', ' ')
    sysconfig._config_vars['OPT'] = opt.replace(' -g ', ' ')

if platform.system() == 'Linux':  # In macos there seems not to be -g in LDSHARED
    ldshared = sysconfig.get_config_var('LDSHARED')
    sysconfig._config_vars['LDSHARED'] = ldshared.replace(' -g ', ' ')



# # --- Detect if extensions should be disabled ------------------------------

wrapt_env = os.environ.get('WRAPT_INSTALL_EXTENSIONS')
if wrapt_env is None:
    wrapt_env = os.environ.get('WRAPT_EXTENSIONS')
if wrapt_env is not None:
    disable_extensions = wrapt_env.lower() == 'false'
    force_extensions = wrapt_env.lower() == 'true'
else:
    disable_extensions = False
    force_extensions = False
if platform.python_implementation() != "CPython":
    disable_extensions = True

# --- C extension ------------------------------------------------------------

extensions = [
    setuptools.Extension(
        "wrapt._wrappers",
        sources=[ os.path.realpath(os.path.join(__file__, "..", "src", "wrapt", "_wrappers.c"))],
        optional=not force_extensions,
    )
]


# --- Setup ------------------------------------------------------------------

setuptools.setup(
    ext_modules=[] if disable_extensions else extensions
)
