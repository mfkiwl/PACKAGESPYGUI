#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END

"""\
ribbonpy, contains python package for define pyqt ribbon widgets
"""

#print "__init__", __file__
import os
_aDir = os.path.split(__file__)[0]
__all__ = [o for o in os.listdir(_aDir) if os.path.isdir(os.path.join(_aDir, o))]
del _aDir


