#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


"""
ribbon singleton manager to store an retrieve instances of all
ribbon action(s) and widget(s)
(actions and widgets created in other user widget classes etc...)
retrive actions and widgets (by unique name in __actionsAndWidgets__ dict)
used for ribbon

usage:

>>> import ribbonpy.ribbonItemManager as RIM
>>> RIM.addItem(anItem, "anItemName")
>>> something = RIM.getItemFromName("anItemName")
"""

#FAQ 3210 ribbon named instances manager (for actions and widgets...)

import os
import sys
import pprint as PP

# from ribbonpy.ribbonTrace import Trace as RT
from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()

verbose = True
__actionsAndWidgets__={} # mix actions and widgets, never mind


def addItem(item, aName=None):
  name = aName
  if name == None: name = item.objectName()
  if name in list(__actionsAndWidgets__.keys()):
    RT.warning("existing yet item: '%s'" % name)
    return
  else:
    __actionsAndWidgets__[name] = item
    return

def getItemFromName(name, verbose=True):
  if "example0" not in list(__actionsAndWidgets__.keys()):
    _createExampleActions()
  if name in list(__actionsAndWidgets__.keys()):
    return __actionsAndWidgets__[name]
  else:
    if verbose: RT.error("getItemFromName: Item '%s' unknown. Names are:\n%s" % (name, PP.pformat(sorted(__actionsAndWidgets__.keys()))))
    return None


def createRibbonAction(theWidget, Name, Shortcut=None, ToolTip=None, Slot=None, Icon=None, addGlobal=False):
  """
  to set created action in global __actionsAndWidgets___ dictionary
  user have to call 'addItem()' if needed... or set addGlobal=True
  see http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
  """
  #FAQ 1160 create named QAction in manager
  from PyQt5 import QtWidgets as QTW
  import ribbonpy.ribbonIcons as IUSR #here to fix QWidget: Must construct a QApplication before a QWidget
  
  action = QTW.QAction(Name, theWidget)
  if Shortcut != None:
    action.setShortcut(Shortcut)
  if ToolTip != None:
    action.setToolTip(ToolTip)
  if Icon != None:
    action.setIcon(IUSR.getIconFromName(Icon))
  if Slot != None: 
    action.triggered.connect(Slot)
  if addGlobal == True:
    addItem(action, Name)
  return action


def _createExampleActions():
  """is here for prototypage and EZ demo"""
  from PyQt5 import QtWidgets as QTW
  import ribbonpy.ribbonIcons as IUSR #here to fix QWidget: Must construct a QApplication before a QWidget
  
  class ExampleAction(QTW.QAction):
    """for example, only print message slot"""
    def exampleSlot(self):
      RT.info("ExampleAction.exampleSlot: hello '%s'" % self.toolTip())

  theWidget = QTW.QWidget() #create parent of examples actions
  addItem(theWidget, "_parentExamplesActions") #so no garbage collecting
  #FilesIcon = IUSR.findFilesFromGnomeIconTheme("face-") #it is more funny than document-
  FilesIcon = IUSR.findFilesFromGnomeIconTheme("document-") #it is more serious than face-
  for i in range(0,10):
    prefix, _ = os.path.splitext(os.path.basename(FilesIcon[i]).replace("document-",""))
    Name = "example%i" % i
    ToolTip = "%s %i" % (prefix, i)
    #FileIcon = "exx%i" % i
    action = ExampleAction(Name, theWidget)
    action.setToolTip(ToolTip)
    action.setIcon(IUSR._getIcon(FilesIcon[i]))
    action.triggered.connect(action.exampleSlot)
    addItem(action, Name)
  return
