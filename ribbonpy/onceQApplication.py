#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


"""
singleton on QtGui.QApplication
cause problem if in a __init__ class
"""

from PyQt5 import QtWidgets as QTW

__app__ = []

def OnceQApplication(*args):
  if len(__app__) == 0:
    if args == ():
      app = QTW.QApplication([])
    else:
      app = QTW.QApplication(*args)
    __app__.append(app)
    #qt4 ['Oxygen', 'Windows', 'Motif', 'CDE', 'Plastique', 'GTK+', 'Cleanlooks']
    #qt5 ['Windows', 'GTK+', 'Fusion']
    #app.setStyle("Cleanlooks")
    app.setStyle("Fusion")
  
  else:
    if args!=():
      print("QApplication done yet: args are not considered: '%s'" % args)
  return __app__[0]

# from ribbonpy.ribbonTrace import Trace as RT
from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()
RT.info("OnceQApplication: existing styles %s" % [str(i) for i in list(QTW.QStyleFactory.keys())])

if __name__ == '__main__':
  #FAQ 5010 construct only one QApplication
  import sys
  app1=OnceQApplication(sys.argv)
  app2=OnceQApplication(sys.argv)
  print("OnceQApplication works:",id(app1) == id(app2))
  

