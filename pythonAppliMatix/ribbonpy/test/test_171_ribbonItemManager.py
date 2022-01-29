#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


import unittest
from PyQt5 import QtCore, QtWidgets as QTW

verbose = False

class TestCase(unittest.TestCase):

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
    import ribbonpy.ribbonItemManager as RIM
    a = QtCore.QObject()
    name = "aName"
    RIM.addItem(a, name)
    b = RIM.getItemFromName(name)
    self.assertEqual(id(a), id(b))
    c = RIM.getItemFromName("oops", verbose=False)
    self.assertEqual(c, None)

  def test_030(self):
    import ribbonpy.ribbonItemManager as RIM
    a = QtCore.QObject()
    name = "__hello"
    b = RIM.createRibbonAction(a, name, Shortcut="1", ToolTip="abc", Slot=None, Icon = "noIcon", addGlobal=False)
    self.assertEqual(b.__class__, QTW.QAction)
    c = RIM.getItemFromName(name, verbose=False)
    self.assertEqual(c, None)


if __name__ == '__main__':
  verbose = False
  unittest.main()
  pass
