#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


import sys
from PyQt5 import QtGui, QtCore, QtWidgets as QTW
import traceback
import json

from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()

import ribbonpy.ribbonIcons as IUSR
import ribbonpy.ribbonClassFactory as RCF

from ribbonpy.qTabMultipleText import QTabMultipleText
from ribbonpy.ribbonWidget import RibbonWidget

verbose = True
verboseEvent = False


class QMainWindowForRibbon(QTW.QMainWindow, RCF._ribbonBase):
  """
  example QMainWindow with ribbonWidget
  could be base class
  """
  #FAQ 3005 base class QMainWindow with ribbonWidget, for example
  
  index = [0] #for unique instance naming

  def __init__(self, *args, **kwargs):
    # super(QMainWindowForRibbon, self).__init__(*args)
    QTW.QMainWindow.__init__(self, *args, **kwargs)
    RCF._ribbonBase.__init__(self, *args, **kwargs)

    self.args = args
    self.kwargs = kwargs
    self.setObjectName("QMainWindowForRibbon%s" % str(self.index))
    self.index[0] += 1  # unambigous objectName
    self.setWindowTitle(self.objectName())
    self.setWindowModality(QtCore.Qt.NonModal)
    self.prefixShortcut = "Ctrl+"
    self.ribbon = []  # theorically only one ribbon ... mais sait-on jamais?
    self.central = None
    self.docks = []
    self.toolBars = []
    self.actions = []
    if "setFromJson" in self.kwargs:
      try:
        self.setFromJson(kwargs["setFromJson"])
      except Exception as e:
        trace = traceback.format_exc()  # better explicit verbose problem
        RT.error("%s problem Json setting\n%s" % (self.__class__.__name__, e))
    else:
      self.setFromJson(valuesJson=None)
    
  def setFromJson(self, valuesJson=None):
    """
    virtual, only for example
    """
    RT.info("QMainWindowForRibbon.setFromJson")
    if "setCentral" in self.kwargs: self.__addCentral()
    self.__createActions()
    self.__addToolBars()

    RT.warning("TODO choose only one of RibbonDock or RibbonToolBar")

    if "setRibbonToolBar" in self.kwargs: self.__addRibbonToolBar(valuesJson=valuesJson)

    self.__addRibbonDock(valuesJson=valuesJson)
    if "setDocks" in self.kwargs: self.__addDocks()

    self.setObjectName(self.ribbon[0].objectName())
    self.setWindowTitle(self.ribbon[0].objectName())

    self.statusBar().showMessage('Ready')
    self.statusBar().addPermanentWidget ( QTW.QLabel("QLabel (or else...) for example"), stretch=0 )
    # self.resize(900, 500)

  """
  def close(self):
    #warning: is not usable if salome, only catch hide event, not close
    print "QMainWindowForRibbon %s close",self.objectName()
    return super(QMainWindowForRibbon, self).close()

  def closeEvent(self, event):
    print "QMainWindowForRibbon %s closeEvent",self.objectName()
    #event.ignore()
    return super(QMainWindowForRibbon, self).closeEvent(event)

  def event(self, event):
    print "QMainWindowForRibbon %s event",self.objectName(),strEvent(event)
    return super(QMainWindowForRibbon, self).event(event)

  def __del__(self):
    print "QMainWindowForRibbon %s __del__",self.objectName()
    return super(QMainWindowForRibbon, self).__del__()
  """

  def __addCentral(self, valuesJson=None):
    """
    virtual, only for example
    valuesJson not used, yet
    """
    RT.warning("QMainWindowForRibbon.__addCentral: create centralWidget QTabMultipleText for example")
    self.central = QTabMultipleText()
    self.centralWidget()
    self.setCentralWidget(self.central)
    #self.centralWidget().resize(self.centralWidget().size())
    self.centralWidget().show()

  def __addDocks(self, valuesJson=None):
    """
    virtual, only for example
    valuesJson not used, yet
    """
    RT.warning("QMainWindowForRibbon.__addDocks: create treeView for example")
    self.docks = []
    dock = QTW.QDockWidget("TreeForExample", self)
    self.treeView = QTW.QTreeWidget()
    dock.setWidget(self.treeView)
    pos = QtCore.Qt.LeftDockWidgetArea
    dock.setAllowedAreas(pos)
    self.docks.append(dock)
    for dock in self.docks:
      self.addDockWidget(pos, dock)
    
  def __addRibbonDock(self, valuesJson=None):
    """
    valuesJson not used, yet
    """
    RT.info("QMainWindowForRibbon.__addRibbonDock: create Ribbon in dock")
    # import ribbonpy.ribbonClassFactory as RCF
    self.ribbon.append(RibbonWidget(parent=self, setFromJson=valuesJson))
    dock = QTW.QDockWidget(self.ribbon[-1].objectName()+"_dock", self)
    # dock.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    dock.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    # dock.setFeatures(p.DockWidgetVerticalTitleBar)
    # dock.setWindowFlags(QtCore.Qt.Tool)
    dock.setWidget(self.ribbon[-1])
    pos = QtCore.Qt.TopDockWidgetArea
    dock.setAllowedAreas(pos)
    self.docks.append(dock)
    for dock in self.docks:
      self.addDockWidget(pos, dock)
      # dock.close()
    
  def __addRibbonToolBar(self, valuesJson=None):
    """
    virtual, only for example
    valuesJson not used, yet
    """
    RT.info("QMainWindowForRibbon.__addRibbonToolBar: create Ribbon in ToolBar")
    # import ribbonpy.ribbonClassFactory as RCF
    self.ribbon.append(RibbonWidget(parent=self, setFromJson=valuesJson))
    tb = self.addToolBar(self.ribbon[-1].objectName() + "_toolbar")
    tb.addWidget(self.ribbon[-1])
    tb.setAllowedAreas(QtCore.Qt.TopToolBarArea | QtCore.Qt.BottomToolBarArea)
    self.toolBars.append(tb)
    
  def __addToolBars(self, valuesJson=None):
    """
    virtual, only for example
    valuesJson not used, yet
    """
    RT.info("TODO QMainWindowForRibbon.__addToolBars: not yet implemented")
    return 
    self.toolBars = []
    tb = self.addToolBar("toolbar1")
    for action in self.actions:
      tb.addAction(action)
    self.toolBars.append(tb)
  
  def __createActions(self, valuesJson=None):
    """
    virtual, only for example
    valuesJson not used, yet
    """
    """create general actions"""
    RT.info("TODO QMainWindowForRibbon.__createActions: not yet implemented")
    return 
    self.actions = []
    self.actions.append(self.__createAction( "Display File", "D", "Display file", self.central.displayFile, "open"))
    
  def __createAction(self, Name, Shortcut, ToolTip, Call, Icon=None):
    """create one actions"""
    #http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
    action = QTW.QAction(Name, self)
    if Shortcut!=None: action.setShortcut(self.prefixShortcut+Shortcut)
    action.setToolTip(ToolTip)
    if Icon!=None:
      action.setIcon(IUSR.getIconFromName(Icon))
    action.triggered.connect(Call)
    return action




if __name__ == '__main__':
  #FAQ 0155 show QMMainWindow with RibbonWidget
  from ribbonpy.onceQApplication import OnceQApplication
  app = OnceQApplication()
  #existing styles ['Windows', 'Motif', 'CDE', 'Plastique', 'GTK+', 'Cleanlooks']
  #app.setStyle("Windows")
  #app.setStyle('Motif')
  #app.setStyle('CDE')
  #app.setStyle('Plastique')
  #app.setStyle('GTK+')
  #app.setStyle('Cleanlooks')
  app.setStyle('Fusion') #qt5
  fen = QMainWindowForRibbon()
  fen.show()
  app.exec_()
  #avoid Erreur de segmentation (core dumped)
  del(fen)
  del(app)
  sys.exit()


