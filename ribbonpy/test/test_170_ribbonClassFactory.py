#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


import unittest
from PyQt5 import QtCore, QtWidgets as QTW
import ribbonpy.ribbonClassFactory as RCF

verbose = False

class TestCase(unittest.TestCase):

  class MyEssai(QtCore.QObject, RCF._ribbonBase):
    index = [0] #for unique instance naming
    pass

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
    a = self.MyEssai(None)
    idx1 = a.index[0]
    self.assertEqual(a.className, "MyEssai")
    self.assertEqual("MyEssai[" in a.objectNameIni, True)
    self.assertEqual("MyEssai[" in a.objectName(), True)
    b = self.MyEssai(None)
    idx2 = a.index[0]
    self.assertEqual(idx1+1, idx2)

  def test_030(self):
    a = self.MyEssai(None, kwarg1=11, kwarg2=22)
    self.assertEqual(a.args, ())
    self.assertEqual(a.kwargs, {'kwarg1': 11, 'kwarg2': 22})
    b = self.MyEssai(a, kwarg1=1, kwarg2=2)
    self.assertEqual(b.args, ())
    self.assertEqual(b.kwargs, {'kwarg1': 1, 'kwarg2': 2})
    self.assertEqual(b.parent(), a)

  def test_050(self):
    jsonDict = {
      "name": "Ribbon1",
      "type": "RibbonWidget",
    }
    a = self.MyEssai(None, setFromJson=jsonDict)
    self.assertEqual(a.kwargs, {'setFromJson': {'type': 'RibbonWidget', 'name': 'Ribbon1'}})
    self.assertEqual(a.getRibbonPath(), a.objectNameIni)
    b = self.MyEssai(a) #a as QObject parent
    self.assertEqual(a.getRibbonPath(), a.objectNameIni)
    bpath = a.objectNameIni + "//" + b.objectNameIni
    self.assertEqual(b.getRibbonPath(), bpath)
    bpath2 = a.splitPath(bpath)[1]
    self.assertEqual(b.objectNameIni, bpath2)
    
    self.assertEqual(b.getRibbonRoot(), a)
    self.assertEqual(a.getItemFromRibbonPath(b.objectNameIni, verbose=False), None) #ok because b is not in a.tabsWidget
    a.tabsWidgets.append(b) #done in use of setFromJson method
    self.assertEqual(a.getItemFromRibbonPath(b.objectNameIni), b) #ok because b is in a.tabsWidget
    
    c = self.MyEssai(b) #a as QObject parent
    b.tabsWidgets.append(c) #done in use of setFromJson method
    bpath = a.objectNameIni + "//" + b.objectNameIni + "//" + c.objectNameIni
    self.assertEqual(c.getRibbonPath(), bpath)
    self.assertEqual(c.getRibbonRoot(), a)
    bpath3 = a.splitPath(bpath)[1]
    self.assertEqual(a.getItemFromRibbonPath(bpath3), c) #ok because c is throught a.tabsWidget & b.tabsWidget

  def test_070(self):
    import ribbonpy.ribbonWidget as RWT
    jsonDict = {
      "name": "Ribbon1",
      "type": "RibbonWidget",
    }
    a = RWT.RibbonWidget(setFromJson=jsonDict)
    pathRoot = a.getRibbonPath()
    self.assertEqual(pathRoot, "Ribbon1")
    self.assertEqual(a.getItemFromRibbonPath(pathRoot), a)
    jsonDict = {
      "name": "Ribbon2",
      "type": "RibbonWidget",
    }
    b = RWT.RibbonWidget(setFromJson=jsonDict)
    self.assertEqual(b.objectName(), "Ribbon2")
    self.assertEqual(b.getRibbonPath(), "Ribbon2")
    a.addNamedTab(b, "Ribbon2New") #modify b.objectName()
    paths = ['Ribbon1', 'Ribbon1//Ribbon2New']
    self.assertEqual(b.objectName(), "Ribbon2New")
    self.assertEqual(b.getRibbonPath(), 'Ribbon1//Ribbon2New')
    self.assertEqual(a.getItemFromRibbonPath(b.getRibbonPath()), b)
    self.assertEqual(a.getItemFromRibbonPath("Ribbon1//Ribbon2New//ooops"), None)
    self.assertEqual(a.getItemFromRibbonPath("Ribbon1////Ribbon2"), None)
    self.assertEqual(a.getItemFromRibbonPath("//Ribbon1////Ribbon2"), None)
    self.assertEqual(b.getItemFromRibbonPath("Ribbon2"), None)
    self.assertEqual(b.getItemFromRibbonPath("Ribbon2New"), b)
    self.assertEqual(b.getRibbonRoot(), a)
    self.assertEqual(a.getAllPathsFromRoot(), paths)
    self.assertEqual(b.getAllPathsFromRoot(), paths)
    self.assertEqual(a.getAllPaths(), paths)
    self.assertEqual(b.getAllPaths(), ["Ribbon1//Ribbon2New"])
    self.assertEqual(b.splitPath("Ribbon1//Ribbon2New"), ("Ribbon1", "Ribbon2New"))
    self.assertEqual(b.splitPath("Ribbon1//Ribbon2New//etc"), ("Ribbon1", "Ribbon2New//etc"))



if __name__ == '__main__':
  verbose = False
  unittest.main()
  pass
