

""""""# start delvewheel patch
def _delvewheel_init_patch_1_3_7():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_3_7()
del _delvewheel_init_patch_1_3_7
# end delvewheel patch

# The _version.py file is managed by setuptools-scm
#   and is not in version control.
from osqp._version import version as __version__  # noqa: F401
from osqp.interface import (  # noqa: F401
    OSQP,
    constant,
    algebra_available,
    algebras_available,
    default_algebra,
)
