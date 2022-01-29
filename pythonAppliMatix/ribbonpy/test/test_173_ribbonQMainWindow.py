#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


import unittest
from PyQt5 import QtCore, QtWidgets as QTW
import ribbonpy.ribbonClassFactory as RCF

setTimer = True
deltaTime = 2000
withShow = True
verbose = False

class TestCase(unittest.TestCase):

  def launchTimer(self, wid):
    import salomepy.onceQApplication as OQA
    app = OQA.OnceQApplication()
    timer = QtCore.QTimer();
    timer.timeout.connect(wid.close)
    if setTimer: timer.start(deltaTime)
    app.exec_()

  def test_000(self):
    #avoid QWidget: Must construct a QApplication before a QWidget
    import ribbonpy.ribbonTrace as RT
    RT.pushLevel("CRITICAL")
    import salomepy.onceQApplication as OQA
    app = OQA.OnceQApplication()

  def test_999(self):
    #avoid QWidget: Must construct a QApplication before a QWidget
    import ribbonpy.ribbonTrace as RT
    RT.popLevel()

  def test_010(self):
    import ribbonpy.ribbonQMainWindow as RQM
    import ribbonpy.ribbonClassFactory as RCF
    aJsonValue = RCF.getExampleJsonRibbon()
    fen = RQM.QMainWindowForRibbon(setFromJson=aJsonValue)
    fen.show()
    self.launchTimer(fen)


if __name__ == '__main__':
  verbose = False
  setTimer = False
  unittest.main()
  pass
