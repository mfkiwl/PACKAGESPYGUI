#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


"""
http://doc-snapshot.qt-project.org/4.8/widgets-icons.html
warning: Must construct a QApplication before a QPaintDevice icon
"""

import os
import sys
import glob
from PyQt5 import QtGui
from pprint import pprint, pformat

# from ribbonpy.ribbonTrace import Trace as RT
from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()

verbose = False

#indirection for user name to file name...
IconsUser={
  "castem" : "castemMod64x64", #"earthquake100x100",
  "castemDgibiFile" : "castemMod64x64", #"earthquake100x100",
  "castemSauvFile" : "castemMod64x64",
  "medFile" : "salomeLampe180x180",
  "csvFile" : "butblue",
  "inpFile" : "butgreen",
  "pngFile" : "butpurple",
  "test" : "working64x64",
  "tests" : "working64x64",
  "noIcon" : "noIcon64x64",
  "help" : "help64x64",
  "editor" : "kate",
  "run" : "run",
  "browsefile" : "browsefile",
  "open" : "open",
  "save" : "save",
  "openxml" : "openxml",
  "savexml" : "savexml",
  "opencsv" : "opencsv",
  "savecsv" : "savecsv",
  "refresh" : "refresh",
  "clearModel" : "clearModel",
  #plot
  "plot" : "plot",
  "plot2" : "plot2",
  "plotn" : "plotn",
  "plotd" : "plotd",
  "plotEllipse" : "working64x64",
  "addColumn" : "addColumn",
  "todo" : "toDo",
  }



IconsUserloaded = {} #load only one time, in memory
IconPath = os.path.join(os.path.dirname(__file__), "images")

RT.debug("iconRibbon path '%s'" % IconPath)

def _getIcon(name):
  #find as name=path/name(+".png")
  if ".png" not in name:
    aname = name + ".png"
  else:
    aname = name
  res = None
  if os.path.exists(aname):
    if aname in list(IconsUserloaded.keys()):
      return IconsUserloaded[aname]
    try:
      res = QtGui.QIcon(aname)
      IconsUserloaded[aname] = res
    except:
      res=None
      #could be an icon but empty if file not found
  else:
    RT.warning("_getIcon: No file icon for '%s'" % aname)
  
  if res==None:
    RT.warning("_getIcon No icon for '%s'" % aname)
    aname = os.path.join(os.path.dirname(__file__),"images","noIcon64x64.png")
    if aname in IconsUserloaded:
      res = IconsUserloaded[aname]
    else:
      res = QtGui.QIcon(aname)
      IconsUserloaded[aname] = res
  return res

def findFilesFromGnomeIconTheme(text):
  """find "*text*.png in local gnome-icon-theme-3.12.0, return list or empty list"""

  sp = os.path.join(IconPath, "gnome-icon-theme-3.12.0", "gnome", "48x48", "*", "*%s*.png" % text)
  files = glob.glob(sp)
  if len(files) > 1:  #  select exact choice
    res = [i for i in files if os.path.basename(i) == "%s.png" % text]
    if len(res) == 1:
      return res
  return files

def getIconFromName(text):
  """
  load only one time, store in IconsUserloaded,
  and resend same instance (same id)
  """
  if text in list(IconsUser.keys()):
    afile = os.path.join(IconPath,IconsUser[text])
    res = _getIcon(afile)
    return res
  files = findFilesFromGnomeIconTheme(text)
  # look for gnome-icon-theme-3.12.0/gnome/48x48/*/*text*.png
  if len(files) > 1:
    RT.warning("Find multiples icon for '%s'\n%s" % (text, pformat(files)))
  elif len(files) < 1:
    RT.warning("Find no icon for '%s'" % (text))
  else:
    res = _getIcon(files[0])
    return res
  # noIcon
  afile = os.path.join(IconPath, IconsUser["noIcon"])
  RT.warning("getIconFromName No icon for '%s'" % text)
  res = _getIcon(afile)
  return res
  
def getIconFileName(text):
  if text in list(IconsUser.keys()):
    res = IconsUser[text] + ".png"
  else:
    res = IconsUser["noIcon"] + ".png"
  return res




