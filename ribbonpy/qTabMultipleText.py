#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


import os
import sys
import fnmatch
from PyQt5 import QtGui, QtCore, QtWidgets as QTW

# from ribbonpy.ribbonTrace import Trace as RT
from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()

from ribbonpy.qTextEditSimple import QTextEditSimple

verbose = True
verboseEvent = verbose

"""
widget for a centralWidget Qmainwindow: multiple tab with editors for files xml etc...
"""

class QTabMultipleText(QTW.QTabWidget):
  
  TAB_JSON=0
  TAB_XML=1
  TAB_OTHERTEXTEDIT=2
  TABS = [(TAB_JSON, ".json"), (TAB_XML, ".xml"), (TAB_OTHERTEXTEDIT, ".tmp")]
  index = [0]
  
  def __init__(self):
    super(QTabMultipleText, self).__init__()
    self.setObjectName("QTabMultipleTextCentral"+str(self.index))
    self.setWindowTitle(self.objectName())
    self.index[0] += 1
    self.tabsWidgets = []
    self.currentDir = "/tmp"
    
    for index, ext in self.TABS:
      aTabWidget = QTextEditSimple()
      aTabWidget.saveFileExt = ext
      self.insertTab(index, aTabWidget, "File %s" % ext)
      self.tabsWidgets.append(aTabWidget)
      
    self.__createActions()
    self.resize(600,500)

  def closeEvent(self, event):
    if verboseEvent: print("%s.closeEvent" %self.objectName())
    for aTabWidget in self.tabsWidgets:
      aTabWidget.close()
    return super(QTabMultipleText, self).closeEvent(event)
  
  def __createActions(self):
    import ribbonpy.ribbonItemManager as RIM #here to fix QWidget: Must construct a QApplication before a QWidget
    self.actions = [] #keep in self mind
    action = RIM.createRibbonAction(self, "DisplayFileQTabMultipleText", "D", "Display file", self.displayFile, "open", addGlobal=True)
    self.actions.append(action)

  def showTabWidget(self, anExt):
    for index, ext in self.TABS:
      if ext == anExt:
        self.setCurrentIndex(index)
        return
    RT.warning("QTabMultipleText.showTabWidget: unknown extension '%s'" % anExt)

  def hideTabWidget(self, anExt):
    for index, ext in self.TABS:
      if ext == anExt:
        self.removeTab(index)
        return
    RT.warning("QTabMultipleText.hideTabWidget: unknown extension '%s'" % anExt)

  def hideOtherTexteditWidget(self):
    self.removeTab(self.TAB_OTHERTEXTEDIT)

  def _getIndexFromFilename(self, aFile):
    for index, ext in self.TABS:
      if fnmatch.fnmatch(aFile, "*%s" % ext):
        return index
    return self.TAB_OTHERTEXTEDIT

  def quickEditFiles(self, files):
    RT.debug("quickEditFiles %s" % files)
    indexDone = []
    for aFile in files:
      index = self._getIndexFromFilename(aFile)
      if index not in indexDone:
        self.tabsWidgets[index].openFile(aFile)
        self.setCurrentIndex(index)
        indexDone.append(index)
      else:
        RT.warning("quickEditFiles: pattern '%s' done yet for '%'" % (anExt, aFile))
    
  def displayFile(self, aFile=False): #False from signal/slot
    if not aFile:
      #http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html#qfiledialog
      nameFile = QTW.QFileDialog.getOpenFileName(self, 'Open File', self.currentDir, "*")[0]
    else:
      nameFile = aFile
    if nameFile=="": return #cancel
    RT.debug("displayFile '%s'" % str(nameFile))
    realPath = os.path.realpath(nameFile)
    dirName = os.path.dirname(realPath)
    self.quickEditFiles([nameFile])


if __name__ == '__main__':
  #FAQ 4010 construct multiple file viewers-editors in QTabWidget
  app = QTW.QApplication(sys.argv)
  fen = QTabMultipleText()
  fen.showTabWidget(".xml")
  fen.show()
  app.exec_()
  #avoid Erreur de segmentation (core dumped)
  del(fen)
  del(app)
  sys.exit()


