#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


import unittest
from PyQt5 import QtCore, QtWidgets as QTW
import ribbonpy.ribbonClassFactory as RCF
import pprint as PP

verbose = False

setTimer = not verbose
deltaTime = 2000
withShow = True

class TestCase(unittest.TestCase):

  def launchTimer(self, wid):
    #FAQ 5100 set timeout on display widget in unittest
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
    #FAQ 0150 create RibbonWidget instance with ribbon class factory
    aJsonValue = RCF.getExampleJsonRibbon()
    a = RCF.getRibbonInstanceClassFromJson(None, aJsonValue) # a ribbon
    paths = a.getAllPathsFromRoot()
    self.assertEqual(paths[0], "test_Ribbon_0")
    if verbose:
      print("test_010 json %s" % PP.pformat(aJsonValue))
      print("test_010 paths %s" % PP.pformat(paths))
    self.assertEqual('test_Ribbon_0//Edit' in paths, True)
    self.assertEqual('test_Ribbon_0//Other' in paths, True)
    self.assertEqual('test_Ribbon_0//Advanced' in paths, True)
    self.assertEqual('test_Ribbon_0//Widgets' in paths, True)
    self.assertEqual('test_Ribbon_0//Widgets//Widget3//LabelEdit8//edit5' in paths, True)

  def test_020(self):
    #FAQ 0152 show RibbonWidget instance
    fen = QTW.QWidget()
    aJsonValue = RCF.getExampleJsonRibbon()
    ribbon = RCF.getRibbonInstanceClassFromJson(None, aJsonValue)
    vbox = QTW.QVBoxLayout()
    vbox.addWidget(ribbon)
    fen.setLayout(vbox)
    fen.show()
    self.launchTimer(fen)


if __name__ == '__main__':
  verbose = True
  setTimer = False
  unittest.main()
  pass
