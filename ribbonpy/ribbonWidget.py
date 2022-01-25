#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END

"""
usage:
import ribbonpy.ribbonWidget as RWT

see ribbonpy.ribbonQMainWindow example
"""

import sys
import traceback
from PyQt5 import QtGui, QtCore, QtWidgets as QTW

import pprint as PP
from functools import partial

# from ribbonpy.ribbonTrace import Trace as RT
from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()

import ribbonpy.ribbonIcons as IUSR
import ribbonpy.ribbonClassFactory as RCF

verbose = False
verboseEvent = True


############################################
class RibbonWidget(QTW.QTabWidget, RCF._ribbonBase):
  """base class RibbonWidget"""

  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QTabWidget.__init__(self, *args, **kwargs)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
    self._smallWidget = None
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc()  # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
      
  def setFromJson(self, valuesJson=None):
    # http://doc.qt.io/qt-5/stylesheet.html
    # FAQ 0250 ever-seen upper right buttons (smallWidget)

    valueSmallWidget = self.ggetFromValuesOrDefault(valuesJson, "smallWidget", None)
    if valueSmallWidget != None:
      self.setSmallWidgetFromJson(valueSmallWidget)
    bk = self.ggetFromValuesOrDefault(valuesJson, "backgroundColor", "grey")
    fs = self.ggetFromValuesOrDefault(valuesJson, "fontSize", "9")

    # self.setStyleSheet("background-color: %s;" % bk)
    css = "Background: %s; font-size:%spx; color: black;" % (bk, fs)
    self.setStyleSheet(css)

    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.setWindowTitle(self.objectName())
    x, y = self.ggetFromValuesOrDefault(valuesJson, "minimumSize", [300, 250])
    self.setMinimumSize(x, y)
    tabpos = self.ggetFromValuesOrDefault(valuesJson, "tabPosition", "North")
    self.setTabPositionFromName(tabpos)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    tabs = self.ggetFromValuesOrDefault(valuesJson, "tabs", [])
    self.setTabsFromJson(tabs)
    return

  def setSmallWidgetFromJson(self, aJsonValue):
    widget = RCF.getRibbonInstanceClassFromJson(self, aJsonValue)
    self.setSmallWidget(widget)
  
  def setSmallWidget(self, widget=None):
    if widget is None:
      sw = self.getDefaultSmallWidget()
    else:
      sw = widget
    self._smallWidget = sw
    sw.setParent(self)
    self.moveSmallWidget()
    
  def moveSmallWidget(self):
    """
    Move the small widget to the correct location.
    """
    # Find the width of all of the tabs
    if self._smallWidget == None: 
      return
    w = self.tabBar().sizeHint().width()
    smw = self._smallWidget.sizeHint().width()
    wmax = self.width()
    x, y = wmax - smw , 1
    RT.debug("moveSmallWidget on %s x %i y %i xmax %i" % (self.objectNameIni,x ,y, wmax))
    if x < w: # no enough place
      y = 30
    self._smallWidget.move(x, y)

  def setTabPositionFromName(self, tabpos):
    try:
      pos = {
        "North": self.North, "South": self.South,
        "West": self.West, "East": self.East}[tabpos]
      self.setTabPosition(pos)
    except:
      self.setTabPosition(self.North)
  
  def setTabsFromJson(self, tabs):
    for index, aJsonValue in enumerate(tabs):
      # something like a QTW.QWidget()
      aWidget = RCF.getRibbonInstanceClassFromJson(self, aJsonValue)
      name = aWidget.ggetFromValuesOrDefault(aJsonValue, "name", "%s_%i" % (self.className, index))
      self.insertTab(index, aWidget, name)
      self.tabsWidgets.append(aWidget)
  
  def addNamedTab(self, aWidget, name):
    """set objectName() of widget as name"""
    aWidget.setObjectName(name)
    self.addTab( aWidget, name)
    self.tabsWidgets.append(aWidget)
    self.moveSmallWidget()
  
  def removeNamedTab(self, name):
    #print len(self.tabsWidgets)
    for i, t in enumerate(self.tabsWidgets):
      if t.objectName() == name:
        self.removeTab(i)
        del(self.tabsWidgets[i]) #remove it in self.tabsWidgets
        self.moveSmallWidget()
        return
    RT.warning("removeNamedTab: tab '%s' not known" % name)

  def tabLayoutChange(self):
    """
    This virtual handler is called whenever the tab layout changes.
    If anything changes make sure the plus button is in the correct location.
    """
    RT.warning("sizeHint on tabLayoutChange %s %s" % (self.objectName(),self.sizeHint()))
    super(RibbonWidget, self).tabLayoutChange()

  def resizeEvent(self, event):
    """
    Resize the widget and make sure the plus button is in the correct location.
    """
    # RT.warning("sizeHint on resizeEvent %s %s" % (self.objectName(),self.tabBar().sizeHint()))
    super(RibbonWidget, self).resizeEvent(event)
    self.moveSmallWidget()



############################################
class RibbonQHBoxLayout(QTW.QWidget, RCF._ribbonBase):

  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QWidget.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
    
    self.box = QTW.QHBoxLayout()
    self.setLayout(self.box)
    self.box.setContentsMargins(1, 1, 1, 1)
    self.lineSplitter = "no"
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc()  # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
      
  def setFromJson(self, valuesJson=None):
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.setWindowTitle(self.objectName())
    x, y = self.ggetFromValuesOrDefault(valuesJson, "minimumSize", [300, 75])
    self.setMinimumSize(x, y)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    tabs = self.ggetFromValuesOrDefault(valuesJson, "tabs", [])
    self.lineSplitter = self.ggetFromValuesOrDefault(valuesJson, "lineSplitter", "no")
    self.setTabsFromJson(tabs)
    return

  def setTabsFromJson(self, tabs):
    for index, aJsonValue in enumerate(tabs):
      # something like a QTW.QWidget()
      aWidget = RCF.getRibbonInstanceClassFromJson(self, aJsonValue)
      name = aWidget.ggetFromValuesOrDefault(aJsonValue, "name", "%s_%i" % (self.className, index))
      self.box.addWidget(aWidget)
      self.tabsWidgets.append(aWidget)
      if self.lineSplitter == "yes":
        line  =  QTW.QFrame()
        line.setFrameShape(QTW.QFrame.VLine)  # Vertical or Horizontal line
        line.setFrameShadow(QTW.QFrame.Sunken)
        line.setLineWidth(1)
        self.box.addWidget(line)  # ,stretch=0)
      
    self.box.addStretch(1)


############################################
class RibbonQVBoxLayout(QTW.QWidget, RCF._ribbonBase):
  
  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QWidget.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
    
    self.box = QTW.QVBoxLayout()
    self.setLayout(self.box)
    self.box.setContentsMargins(1, 1, 1, 1)
    self.lineSplitter = "no"
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc()  # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
      
  def setFromJson(self, valuesJson=None):
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.setWindowTitle(self.objectName())
    x, y = self.ggetFromValuesOrDefault(valuesJson, "minimumSize", [300, 75])
    self.setMinimumSize(x, y)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    tabs = self.ggetFromValuesOrDefault(valuesJson, "tabs", [])
    self.lineSplitter = self.ggetFromValuesOrDefault(valuesJson, "lineSplitter", "no")
    self.setTabsFromJson(tabs)
    return

  def setTabsFromJson(self, tabs):
    for index, aJsonValue in enumerate(tabs):
      # name = self.ggetFromValuesOrDefault(aJsonValue, "name", "%s_%i" % (self.__class__.__name__, index))
      # something like a QTW.QWidget()
      aWidget = RCF.getRibbonInstanceClassFromJson(self, aJsonValue)
      name = aWidget.ggetFromValuesOrDefault(aJsonValue, "name", "%s_%i" % (self.className, index))
      self.box.addWidget(aWidget)
      self.tabsWidgets.append(aWidget)
      if self.lineSplitter == "yes":
        line  =  QTW.QFrame()
        line.setFrameShape(QTW.QFrame.VLine) # Vertical or Horizontal line
        line.setFrameShadow(QTW.QFrame.Sunken)
        line.setLineWidth(1)
        self.box.addWidget(line) #,stretch=0)
      
    self.box.addStretch(1)




############################################
class RibbonQGridLayout(QTW.QWidget, RCF._ribbonBase):
  """gridSize is [row, column]"""

  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QWidget.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
    
    self.box = QTW.QGridLayout()
    self.setLayout(self.box)
    self.box.setContentsMargins(1, 1, 1, 1)
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc() # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
      
  def setFromJson(self, valuesJson=None):
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.setWindowTitle(self.objectName())
    # x, y = self.ggetFromValuesOrDefault(valuesJson, "maximumSize", [1000, 400])
    # self.setMaximumSize(x, y)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    tabs = self.ggetFromValuesOrDefault(valuesJson, "tabs", [])
    self.nx, self.ny = self.ggetFromValuesOrDefault(valuesJson, "gridSize", self.getDefaultSize(len(tabs)))
    self.rowColumnMode = self.ggetFromValuesOrDefault(valuesJson, "rowColumnMode", "ColumnFirst")
    self.checkNxNy(tabs)
    self.setTabsFromJson(tabs)

  def checkNxNy(self, tabs):
    """nx/ny zero as have to set automatically"""
    nb = len(tabs)
    self.nx = max(int(self.nx), 0)  # tricky user defined
    self.ny = max(int(self.ny), 0)  # tricky user defined

    if self.nx == 0 and self.ny == 0:
      self.nx, self.ny = self.getDefaultSize(nb)
    elif self.nx == 0:
      self.nx = nb // self.ny
      if self.nx*self.ny < nb: self.nx += 1
    elif self.ny == 0:
      self.ny = nb // self.nx
      if self.nx*self.ny < nb: self.ny += 1
    # RT.info("check gridSize nb %i -> %s" % (nb, [self.nx, self.ny]))
    return

  def getDefaultSize(self, nb):
    """gridSize is [row, column]"""
    resNb = {1: [1, 1], 2: [1, 2], 3: [1, 3],
             4: [2, 2], 5: [2, 3], 6: [2, 3],
             7: [2, 4], 8: [2, 4], 9: [3, 3]}
    nbc = max(1, nb)
    try:
      res = resNb[nbc]
    except:
      res = [3, (nbc+2)//3]
    # RT.info("getDefaultSize nb %i -> %s" % (nb, res))
    return res
  
  def getRowCol(self, index):
    """gridSize is [row, column]"""
    if self.rowColumnMode == "ColumnFirst":
      row = index // self.ny
      col = index % self.ny
    elif self.rowColumnMode == "RowFirst":
      row = index % self.nx
      col = index // self.nx
    else:  # row first...
      RT.error("unknown rowColumnMode '%s', fix it" % self.rowColumnMode)
      # default row first...
      row = index // self.ny
      col = index % self.ny
    res = [row, col]
    # RT.info("getRowCol i %i -> %s" % (index, res))
    return res

  def setTabsFromJson(self, tabs):
    for index, aJsonValue in enumerate(tabs):
      # name = self.ggetFromValuesOrDefault(aJsonValue, "name", "%s_%i" % (self.__class__.__name__, index))
      # something like a QTW.QWidget()
      aWidget = RCF.getRibbonInstanceClassFromJson(self, aJsonValue)
      name = aWidget.ggetFromValuesOrDefault(aJsonValue, "name", "%s_%i" % (self.className, index))
      row, col = self.getRowCol(index)
      self.box.addWidget(aWidget, row, col)
      self.tabsWidgets.append(aWidget)
    self.box.setColumnStretch(self.nx, 1)



############################################
class RibbonActionButton(QTW.QToolButton, RCF._ribbonBase):

  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QToolButton.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)

    self.setMinimumSize(10, 10)
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc() # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))

  def setFromJson(self, valuesJson=None):
    import ribbonpy.ribbonItemManager as RIM
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.minSize = QtCore.QSize(15, 15)
    self.maxSize = QtCore.QSize(60, 70)
    self.trigSize = QtCore.QSize(40, 40)
    self.setMaximumSize(self.maxSize)
    self.setMinimumSize(self.minSize)
    #https://wiki.qt.io/PushButton_Based_On_Action
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    action = RIM.getItemFromName(name)
    x, y = self.ggetFromValuesOrDefault(valuesJson, "size", [10,10])
    self.resize(x, y)
    if action is None:
      self.setToolTip("%s\n%s" % (self.objectNameIni, "Unknown action '%s'" % name))
      self.setText("?")
      return
    #self.setText(self.objectNameIni)
    self.setIconSize(QtCore.QSize(35, 35))
    self.setToolTip("%s\n%s" % (self.objectNameIni, action.toolTip()))
    self.setIcon(action.icon())
    self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) #Qt.ToolButtonIconOnly.
    self.setText(action.toolTip().replace(" ","\n"))
    #self.setEnabled(action.isEnabled())
    #self.setCheckable(action.isCheckable())
    #self.setChecked(action.Checked())
    self.clicked.connect(action.trigger)
    #self.setWindowTitle(self.objectName())
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    return

  def exampleSlot(self):
    print("exampleSlot: hello %s" % self.objectNameIni)

  def paintEvent(self, event):
    """set only icon or icon plus TextUnderIcon as real current size"""
    verb = False
    wt, ht = self.trigSize.width(), self.trigSize.height() #trigger text and icon
    wc, hc = self.width(), self.height() #real current
    s = "["
    if s in self.objectNameIni:
      #RT.warning("sizeHint on paintEvent %s x %i<->%i y %i<->%i" %(s, wh, wc, hh, hc))
      if hc < ht or wc < wt:
        self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        if verb: RT.warning("icon only paintEvent %s x %i<->%i y %i<->%i" %(s, wt, wc, ht, hc))
      else:
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        if verb: RT.warning("icon plus text on paintEvent %s x %i<->%i y %i<->%i" %(s, wt, wc, ht, hc))
    super(RibbonActionButton, self).paintEvent(event)



############################################
class RibbonQComboBox(QTW.QComboBox, RCF._ribbonBase):
  
  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QComboBox.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
  
    self.setMinimumSize(20, 10)
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc() # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
  
  def setFromJson(self, valuesJson=None):
    import ribbonpy.ribbonItemManager as RIM
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.minSize = QtCore.QSize(15, 15)
    self.maxSize = QtCore.QSize(200, 30)
    self.trigSize = QtCore.QSize(40, 40)
    self.setMaximumSize(self.maxSize)
    self.setMinimumSize(self.minSize)
    #https://wiki.qt.io/PushButton_Based_On_Action
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    x, y = self.ggetFromValuesOrDefault(valuesJson, "size", [10,10])
    self.resize(x, y)
    #self.setIconSize(QtCore.QSize(40, 20))
    tooltip = self.ggetFromValuesOrDefault(valuesJson, "tooltip", None)
    if tooltip != None: self.setToolTip(tooltip)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    items = self.ggetFromValuesOrDefault(valuesJson, "items", ["?"])
    for item in items:
      self.addItem(item)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    if verboseEvent: self.currentIndexChanged.connect(self.exampleSlot)
    return

  def exampleSlot(self, index):
    print("RibbonQComboBox currentIndexChanged exampleSlot: %s %i" % (self.getRibbonPath(), index))

  """def paintEvent(self, event):
    print "RibbonQComboBox paintEvent"
    QTW.QComboBox.paintEvent(self, event)"""



############################################
class RibbonQCheckBox(QTW.QCheckBox, RCF._ribbonBase):
  
  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QCheckBox.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
  
    self.setMinimumSize(20, 10)
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc() # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
  
  def setFromJson(self, valuesJson=None):
    import ribbonpy.ribbonItemManager as RIM
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.minSize = QtCore.QSize(15, 15)
    self.maxSize = QtCore.QSize(200, 30)
    self.trigSize = QtCore.QSize(40, 40)
    self.setMaximumSize(self.maxSize)
    self.setMinimumSize(self.minSize)
    # https://wiki.qt.io/PushButton_Based_On_Action
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    x, y = self.ggetFromValuesOrDefault(valuesJson, "size", [10,10])
    self.resize(x, y)
    # self.setIconSize(QtCore.QSize(40, 20))
    tooltip = self.ggetFromValuesOrDefault(valuesJson, "tooltip", None)
    if tooltip != None: self.setToolTip(tooltip)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    text = self.ggetFromValuesOrDefault(valuesJson, "text", "?")
    self.setText(text)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    if verboseEvent: self.stateChanged.connect(self.exampleSlot)
    return

  def exampleSlot(self, index):
    RT.info("RibbonQCheckBox stateChanged exampleSlot: %s %s" % (self.getRibbonPath(), self.isChecked()))

  """def paintEvent(self, event):
    print "RibbonQComboBox paintEvent"
    QTW.QComboBox.paintEvent(self, event)"""



############################################
class RibbonQLineEdit(QTW.QLineEdit, RCF._ribbonBase):

  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QLineEdit.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
  
    self.setMinimumSize(20, 10)
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc() # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
  
  def setFromJson(self, valuesJson=None):
    import ribbonpy.ribbonItemManager as RIM
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.minSize = QtCore.QSize(15, 15)
    self.maxSize = QtCore.QSize(200, 30)
    self.trigSize = QtCore.QSize(40, 40)
    self.setMaximumSize(self.maxSize)
    self.setMinimumSize(self.minSize)
    # https://wiki.qt.io/PushButton_Based_On_Action
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    x, y = self.ggetFromValuesOrDefault(valuesJson, "size", [10,10])
    self.resize(x, y)
    # self.setIconSize(QtCore.QSize(40, 20))
    tooltip = self.ggetFromValuesOrDefault(valuesJson, "tooltip", None)
    if tooltip != None: self.setToolTip(tooltip)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    text = self.ggetFromValuesOrDefault(valuesJson, "text", "?")
    self.setText(text)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    if verboseEvent: self.textChanged.connect(self.exampleSlot)
    return

  def exampleSlot(self, text):
    RT.info("RibbonQLineEdit textChanged exampleSlot: %s %s" % (self.getRibbonPath(), self.text()))

  """def paintEvent(self, event):
    print "RibbonQComboBox paintEvent"
    QTW.QComboBox.paintEvent(self, event)"""


############################################
class RibbonFormLayoutQLineEdit(QTW.QWidget, RCF._ribbonBase):

  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QWidget.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
    
    self.box = QTW.QFormLayout()
    self.setLayout(self.box)
    self.box.setContentsMargins(1, 1, 1, 1)
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc() # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
      
  def setFromJson(self, valuesJson=None):
    # http://doc.qt.io/qt-4.8/layout.html
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.setWindowTitle(self.objectName())
    # x, y = self.ggetFromValuesOrDefault(valuesJson, "minimumSize", [300, 75])
    # self.setMinimumSize(x, y)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    tabs = self.ggetFromValuesOrDefault(valuesJson, "tabs", [])
    self.nx, self.ny = self.ggetFromValuesOrDefault(valuesJson, "gridSize", self.getDefaultSize(len(tabs)))
    self.setTabsFromJson(tabs)
    return
  
  def getDefaultSize(self, nb):
    resNb = {1:[1,1], 2:[2,1], 3:[3,1],
             4:[2,2], 5:[3,2], 6:[3,2],
             7:[4,2], 8:[4,2], 9:[3,3]}
    nbc = max(1, nb)
    try:
      res = resNb[nbc]
    except:
      res = [(nbc+2)/3, 3]
    # print("getDefaultSize", res, nb)
    return res
  
  def getRowCol(self, index):
    # column first...
    col = index % self.nx
    row = index // self.nx
    # print("getRowCol row %i col %i index %i nx %i ny %i" % (row, col, index, self.nx, self.ny))
    return row, col

  def setTabsFromJson(self, tabs):
    for index, aJsonValue in enumerate(tabs):
      # something like a QTW.QWidget()
      aWidget = RibbonQLineEdit(self, setFromJson=aJsonValue)
      name = aWidget.ggetFromValuesOrDefault(aJsonValue, "name", "%s_%i" % (self.className, index))
      label = aWidget.ggetFromValuesOrDefault(aJsonValue, "label", "")
      text = aWidget.ggetFromValuesOrDefault(aJsonValue, "text", "")
      aWidget.setObjectName(name)
      self.box.addRow(label, aWidget)
      self.tabsWidgets.append(aWidget)



############################################
class RibbonQLabel(QTW.QLabel, RCF._ribbonBase):

  index = [0]

  def __init__(self, *args, **kwargs):
    QTW.QLabel.__init__(self, *args)
    RCF._ribbonBase.__init__(self, *args, **kwargs)
  
    self.setMinimumSize(20, 10)
    try:
      self.setFromJson(kwargs["setFromJson"])
    except Exception as e:
      trace = traceback.format_exc() # better explicit verbose problem
      RT.error("%s problem Json setting\n%s\n\n%s" % (self.__class__.__name__, e, trace))
  
  def setFromJson(self, valuesJson=None):
    import ribbonpy.ribbonItemManager as RIM
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    self.setObjectName(name)
    self.minSize = QtCore.QSize(15, 15)
    self.maxSize = QtCore.QSize(200, 30)
    self.trigSize = QtCore.QSize(40, 40)
    self.setMaximumSize(self.maxSize)
    self.setMinimumSize(self.minSize)
    #https://wiki.qt.io/PushButton_Based_On_Action
    name = self.ggetFromValuesOrDefault(valuesJson, "name", self.objectName())
    x, y = self.ggetFromValuesOrDefault(valuesJson, "size", [10,10])
    self.resize(x, y)
    #self.setIconSize(QtCore.QSize(40, 20))
    tooltip = self.ggetFromValuesOrDefault(valuesJson, "tooltip", None)
    if tooltip != None: self.setToolTip(tooltip)
    typeClass = self.ggetFromValuesOrDefault(valuesJson, "type", self.className)
    text = self.ggetFromValuesOrDefault(valuesJson, "text", "?")
    self.setText(text)
    if self.className != typeClass:
      RT.error("%s.setFromJson: problem class name: expected: '%s'" % (self.className, typeClass))
    return

  def mousePressEvent(self, event):
    print("RibbonQLabel mousePressEvent exampleSlot: %s %s" % (self.getRibbonPath(), self.text()))
    super(QTW.QLabel, self).mousePressEvent(event)

  """def paintEvent(self, event):
    print "RibbonQComboBox paintEvent"
    QTW.QComboBox.paintEvent(self, event)"""



############################################
class RibbonExampleSmallWidget(QTW.QWidget):
  """
  create ever-seen upper right 3 elementaries buttons with action for ribbon smallWidget, define associated actions
  """
  def __init__(self, *args, **kwargs):
    QTW.QWidget.__init__(self, *args)
    self.objectNameIni = "RibbonExampleSmallWidget"
    self.setDefaultSmallWidget()
    self.indexPlus = 0
    RT.warning("RibbonExampleSmallWidget: here only for example ribbon top-right small widget")
  
  def getParentRibbon(self):
    return self.parent() #TODO may be other way... later
  
  def setDefaultSmallWidget(self):
    sw = self
    box = QTW.QHBoxLayout()
    siz = 20
    self.menu = QTW.QMenu(self)
    actions = [("list-add", "add tab", self._exampleAddTab ),
               ("list-remove", "remove tab", self._exampleRemoveTab),
               ("starred", "disable/enable item", self.setMenuInitAndClicked )]  # self.disableFromPath)]
    for name ,tooltip, slot in actions:
      s = QTW.QToolButton()
      s.setIcon(IUSR.getIconFromName(name))
      s.setToolTip(tooltip)
      # s.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
      s.setText(tooltip)
      s.setMaximumSize(siz, siz)
      s.setIconSize(QtCore.QSize(siz-5, siz-5))
      if slot != None:
        s.clicked.connect(slot)
      box.addWidget(s)
      # s.setContentsMargins(2,2,1,1)

    sw.setLayout(box)
    # todo after set parent in setLayout
    box.setContentsMargins(1, 1, 1, 1)
    # sw.setStyleSheet("background-color: %s;" % "#AABBCC")
    RT.debug("sw margins %s" % str(sw.getContentsMargins()))
    RT.debug("box margins %s" % str(box.getContentsMargins()))
    return sw

  def _exampleAddTab(self):
    """
    example slot for add named tab in root ribbonWidget
    """
    # FAQ 0290 add named tab in root ribbonWidget
    RT.debug("_exampleAddTab %s" % self.objectNameIni)
    widget = QTW.QWidget()
    self.indexPlus += 1
    self.getParentRibbon().addNamedTab(widget, "TabPlus%i" % self.indexPlus)

  def _exampleRemoveTab(self):
    """example slot remove named tab in root ribbonWidget"""
    # FAQ 0292 remove named tab in root ribbonWidget
    RT.debug("_exampleRemoveTab %s" % self.objectNameIni)
    self.getParentRibbon().removeNamedTab("TabPlus%i" % self.indexPlus)
    self.indexPlus = max(0, self.indexPlus-1)
    self.getParentRibbon().moveSmallWidget()

  def disableFromPath_combo(self):
    """example slot for disable named [sub]ribbon widget"""
    # FAQ 0294 disable [sub]ribbon widget
    RT.debug("disableFromPath %s" % self.getParentRibbon().objectName())
    parent = self.getParentRibbon()
    paths = parent.getAllPaths()
    # impossible to set nb rows of scrolled combo !
    combo = QTW.QComboBox(self)
    combo.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    combo.addItems(paths[1:])  # no self-disable
    # self.combo.currentIndexChanged.connect(self._disableFromCombo)
    combo.activated.connect(self._disableFromCombo)
    combo.showPopup()
    self.combo = combo

  def setMenuInitAndClicked(self):
    """
    slot for disable/enable named [sub]ribbon widget
    up to date each call as maybe ribbon could change
    """
    RT.debug("setMenuInitAndClicked %s" % self.getParentRibbon().objectName())
    parent = self.getParentRibbon()
    paths = parent.getAllPaths()
    menu = self.menu
    menu.clear()
    current = {}
    # RT.info("paths", paths)
    for i in paths[1:]:
      t1 = i.split('//')[1:]
      if len(t1) == 1:
        t = t1[0]
        current[t] = menu.addMenu(t)

    for i in paths[1:]:
      t1 = i.split('//')[1:]
      if len(t1) >= 2:
        t = t1[0]
        submenu = current[t]
        action = submenu.addAction('//'.join(i.split('//')[2:]))
        action.triggered.connect(partial(self._disableFromMenu, i))

    menu.exec(QtGui.QCursor().pos())


  def _disableFromMenu(self, path):
    """example slot for QMenu with direct popup menu"""
    RT.info("_disableFromMenu %s" % path)
    itemToDisable = self.getParentRibbon().getItemFromRibbonPath(path)
    if itemToDisable.isEnabled():
      itemToDisable.setDisabled(True)
    else:
      itemToDisable.setDisabled(False)


  def _disableFromCombo(self, index):
    """example slot for QComboBox with direct popup menu"""
    self.combo.close()
    path = self.combo.itemText(index)
    print("_disableFromPath", index, path)
    itemToDisable = self.getParentRibbon().getItemFromRibbonPath(path)
    if itemToDisable.isEnabled():
      itemToDisable.setDisabled(True)
    else:
      itemToDisable.setDisabled(False)


  def _exampleDisable(self):
    """example slot for disable widget temporary"""
    RT.debug("_exampleDisable %s" % self.objectNameIni)
    self.getParentRibbon().setDisabled(True)
    #FAQ 4030 use QTimer example
    timer = QtCore.QTimer(self)
    timer.singleShot(3000, self._exampleEnable)

  def _exampleEnable(self):
    """example slot for enable widget"""
    RT.debug("_exampleEnable %s" % self.objectNameIni)
    self.getParentRibbon().setDisabled(False)



#FAQ 0160 make ribbon factory knows classes
RCF.appendAllRibbonClasses( [ 
  RibbonWidget, RibbonQHBoxLayout, RibbonQVBoxLayout, 
  RibbonQGridLayout, RibbonActionButton, 
  RibbonQComboBox, RibbonQCheckBox, 
  RibbonQLineEdit, RibbonFormLayoutQLineEdit, RibbonQLabel, 
  RibbonExampleSmallWidget ] )


if __name__ == '__main__':
  from ribbonpy.onceQApplication import OnceQApplication
  app = OnceQApplication()
  fen = QTW.QWidget()
  aJsonValue = RCF.getExampleJsonRibbon()
  ribbon = RCF.getRibbonInstanceClassFromJson(self, aJsonValue)
  vbox = QTW.QVBoxLayout()
  vbox.addWidget(ribbon)
  fen.setLayout(vbox)
  fen.show()
  app.exec_()
  #FAQ 5030 fix 'Erreur de segmentation (core dumped)' on exit
  del(fen)
  del(app)
  sys.exit()


