# -*- coding: utf-8 -*-
"""Management of the importable functions of pdfo.

Authors
-------
Tom M. RAGONNEAU (tom.ragonneau@connect.polyu.hk)
and Zaikun ZHANG (zaikun.zhang@polyu.edu.hk)
Department of Applied Mathematics,
The Hong Kong Polytechnic University.

Dedicated to late Professor M. J. D. Powell FRS (1936--2015).
"""


# start delvewheel patch
def _delvewheel_init_patch_0_0_21():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pdfo.libs'))
    if sys.version_info[:2] >= (3, 8):
        conda_workaround = sys.version_info[:3] < (3, 9, 9) and os.path.exists(os.path.join(sys.base_prefix, 'conda-meta'))
        if conda_workaround:
            # backup the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            conda_dll_search_modification_enable = os.environ.get('CONDA_DLL_SEARCH_MODIFICATION_ENABLE')
            os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = '1'
        os.add_dll_directory(libs_dir)
        if conda_workaround:
            # restore the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            if conda_dll_search_modification_enable is None:
                os.environ.pop('CONDA_DLL_SEARCH_MODIFICATION_ENABLE', None)
            else:
                os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = conda_dll_search_modification_enable
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-pdfo-1.2')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_21()
del _delvewheel_init_patch_0_0_21
# end delvewheel patch


from datetime import datetime

try:
    # Enable subpackage importing when binaries are not yet built.
    __PDFO_SETUP__  # noqa
except NameError:
    __PDFO_SETUP__ = False

# Definition of the metadata of PDFO for Python. It is accessible via:
# >>> import pdfo
# >>> print(pdfo.__author__)
# >>> ...
__author__ = 'Tom M. Ragonneau and Zaikun Zhang'
__copyright__ = f'Copyright 2020--{datetime.now().year}, ' \
                f'Tom M. Ragonneau and Zaikun Zhang'
__credits__ = ['Tom M. Ragonneau', 'Zaikun Zhang', 'Antoine Dechaume']
__license__ = 'LGPLv3+'
__version__ = '1.2'
__date__ = 'October, 2021'
__maintainer__ = 'Tom M. Ragonneau and Zaikun Zhang'
__email__ = 'tom.ragonneau@connect.polyu.hk and zaikun.zhang@polyu.edu.hk'
__status__ = 'Production'

if not __PDFO_SETUP__:

    from ._dependencies import OptimizeResult, Bounds, LinearConstraint, \
        NonlinearConstraint

    from ._bobyqa import bobyqa
    from ._cobyla import cobyla
    from ._lincoa import lincoa
    from ._newuoa import newuoa
    from ._uobyqa import uobyqa
    from ._pdfo import pdfo
    from . import tests
    from .tests import test_pdfo as testpdfo
    __all__ = ['OptimizeResult', 'Bounds', 'LinearConstraint',
               'NonlinearConstraint', 'bobyqa', 'cobyla', 'lincoa', 'newuoa',
               'uobyqa', 'pdfo', 'tests', 'testpdfo']