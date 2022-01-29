#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END

"""
goal is windows where echoes text files
"""

import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets as QTW
from datetime import datetime
import subprocess as SP

# from ribbonpy.ribbonTrace import Trace as RT
from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()

import ribbonpy.ribbonIcons as IUSR

verbose = False
verboseEvent = verbose

class QTextEditSimple(QTW.QPlainTextEdit):
  """
  implements a simple widget QPlainTextEdit, 
  """
  index = [0] #need unambigous name...
  
  def __init__(self):
    super(QTextEditSimple, self).__init__()
    self.nameFile = None
    self.setObjectName("QTextEditSimple_%i" % self.index[0])
    self.setWindowTitle(self.objectName())
    self.index[0] += 1
    self.saveFileExt = ".tmp"
    
    self.fontName = "Monospace"
    self.fontColor = "black"
    self.fontSize = "9"
    self.fontStyle = "normal"
    font = QtGui.QFont(self.fontName)
    #print font.family(), font.fixedPitch() #is monospaced?
    self.setFont(font);
    self.workDir = "/tmp"
    self.currentDir = self.workDir

    self.setLineWrapMode(self.NoWrap)
    self.withEditor="gedit"

    clearAction = QTW.QAction("Clear All", self)
    clearAction.triggered.connect(self.clear)
    
    editAction = QTW.QAction("Edit with "+self.withEditor, self)
    editAction.setIcon(IUSR.getIconFromName("editor"))
    editAction.triggered.connect(self.bestEdit)

    saveAction = QTW.QAction('Save', self)
    saveAction.setShortcut('Ctrl+S')
    saveAction.setStatusTip('Save current file')
    saveAction.triggered.connect(self.saveFile)
    
    openAction = QTW.QAction('Open', self)
    openAction.setShortcut('Ctrl+O')
    openAction.setStatusTip('Open a file')
    openAction.triggered.connect(self.openKnownFile)

    editContextMenu = self.createStandardContextMenu()
    
    editContextMenu.addAction(clearAction)
    #self.editContextMenu.addSeparator()
    action0=editContextMenu.actions()[0]
    editContextMenu.insertAction(action0, openAction)
    editContextMenu.insertAction(action0, saveAction)
    editContextMenu.insertAction(action0, editAction)
    editContextMenu.insertSeparator(action0)
    
    for a in editContextMenu.actions(): a.setEnabled(True)
    
    self.editContextMenu = editContextMenu
    #Erreur de segmentation: need setparent
    editContextMenu.setParent(self)
 
    pal=self.palette()
    pal.setColor(pal.Base, QtGui.QColor(230,230,230))
    pal.setColor(pal.Text, QtGui.QColor(0,0,0))   
    self.setPalette(pal)
    pass


  def closeEvent(self, event):
    if verboseEvent: print("%s.closeEvent" % self.objectName())
    return super(QTextEditSimple, self).closeEvent(event)
    
  def fromUtf8(self,  value):
    #return QtCore.QString.fromUtf8(value)
    try:
      return str(value)
    except:
      RT.warning("check codec in:\n'%s'" % value)
      return value
    
  def getCurrentFontFamilies(self):
    res = []
    fontDatabase = QtGui.QFontDatabase()
    for family in fontDatabase.families():
      RT.debug("font family '%s'" % str(family))
      #res.append(family.toUtf8())
      res.append(family)
    return res

  def contextMenuEvent(self, event):
    if verboseEvent: self.objectName+".contextMenuEvent"
    self.editContextMenu.exec_(event.globalPos())

  def bestEdit(self):
    if self.nameFile==None:
      self.nameFile=self.getDefaultNameFile()
      self.saveFile()
    #2> /dev/null because sometimes warnings editors: Can't load fallback CSS etc...
    cmd = self.withEditor + " " + self.nameFile + " 2> /dev/null &"
    if self.withEditor=="gedit":
      cmd = self.withEditor + " " + self.nameFile + " 2> /dev/null &"
    if self.withEditor=="kate":
      # do not work on centos6.4 cmd = self.withEditor + " --start cassis --use " + self.nameFile + " &"
      cmd = self.withEditor + " " + self.nameFile + " 2> /dev/null &"
    proc = SP.Popen(str(cmd), shell=True)

  def saveFile(self):
    if self.nameFile==None:
      #http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html#qfiledialog
      nameFile = QTW.QFileDialog.getSaveFileName(self, 'Save File', self.currentDir)[0]
    else:
      nameFile = self.nameFile
    if nameFile=="": return #cancel
    RT.info("saveFile '%s'" % str(nameFile))
    realPath = os.path.realpath(nameFile)
    dirName = os.path.dirname(realPath)
    if not os.path.exists(dirName): os.makedirs(dirName)
    f = open(realPath, 'w')
    filedata = self.document().toPlainText()
    f.write(filedata.encode('utf-8'))
    f.close()
    self.nameFile = nameFile

  def getDefaultNameFile(self):
    ext = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    return os.path.join(self.workDir, "log_" + ext + self.saveFileExt)    
 
  def setNameFile(self, nameFile):
    """needs nameFile with path"""
    self.nameFile = os.path.realpath(nameFile)
 
  def setCurrentDir(self, currentDir):
    """needs arg currentDir for path of log file"""
    self.currentDir = currentDir
    RT.debug("currentDir of open/save file '%s'" % self.currentDir)
 
  def openKnownFile(self):
    if self.nameFile==None:
      nameFile = QTW.QFileDialog.getOpenFileName(self, 'Open File', self.currentDir)[0]
      if nameFile=="": return #cancel
    else:
      nameFile = self.nameFile
    self.openFile(nameFile)

  def openFile(self, nameFile):
    if nameFile == "": return #cancel
    if '.png' in nameFile:
      QTW.QMessageBox.warning(self, "warning", "Not a text file: '%s'" % nameFile)
      return
    if True: #try:
      if os.path.exists(nameFile):
        #source accent is code python with #coding=utf-8
        self.clear()
        self.setPlainText(self.fromUtf8(open(nameFile, 'r').read()))
        self.nameFile = nameFile
        self.setCurrentDir(os.path.dirname(os.path.realpath(nameFile)))
      else:
        self.insertLine("Problem inexisting file:\n"+nameFile, "Red")
    else: #except: 
      QTW.QMessageBox.warning(self,"warning","Problem reading file: '%s'" % nameFile)
  
  def moveCursor(self, operation, mode=QtGui.QTextCursor.MoveAnchor):
     """
     TODO do not work...
      move the cursor. operation could be:
      
      - QtGui.QTextCursor.End
      - QtGui.QTextCursor.Left
      - QtGui.QTextCursor.Right
      - QtGui.QTextCursor.EndOfLine
      - QtGui.QTextCursor.LineUnderCursor
     """
     logger.warning("TODO moveCursor do not work, have to debug")
     cursor = self.textCursor()
     cursor.movePosition(operation, mode)
     self.setTextCursor(cursor)

  def insertLine(self, line, color=None, fontName=None, fontSize=None, fontStyle=None):
     """insert one standard line without forbidden tag xml <>"""
     
     """
     see http://en.wikipedia.org/wiki/Font_family_%28HTML%29
     #example of format:
     <pre style="font-family: times, serif; font-size:14pt; font-style:italic; color:red">
     Sample text formatted with inline CSS.
     </pre>
     warning <p> strip multiples whitespaces
             <pre> do not strip multiples whitespaces
     """
     
     if line[-1] == "\n": line = line[:-1] #appendHtml do one lf
     
     col, nam, siz, sty = (self.fontColor, self.fontName, self.fontSize, self.fontStyle)
     if color != None: col = self.fromUtf8(color)
     if fontName != None: nam = self.fromUtf8(fontName)
     if fontSize != None: siz = self.fromUtf8(fontSize)
     if fontStyle != None: sty = self.fromUtf8(fontStyle)
     
     #http://www-sul.stanford.edu/tools/tutorials/html2.0/whitespace.html
     aTag='<pre style="font-family: %s; font-size:%spt; font-style:%s; color:%s">%s</p>'
     #source accent is code python with #coding=utf-8
     a=aTag % (nam, siz, sty,  color, self.fromUtf8(line) )
     self.appendHtml( a )
     self.ensureCursorVisible()
     
  def insertText(self, aText):
     """
     insert text as it
     """
     self.appendPlainText( aText )
     self.ensureCursorVisible()
     
  def insertTextColor(self, aText, color="Black"):
     """could be risky if text have <xml tags> expressions"""
     if "<" in aText:
       self.insertText(aText)
     else:
       self.insertLine(aText, color)


if __name__ == "__main__":
  #FAQ 4020 construct simple file viewers-editor in QPlainTextEdit
  app = QTW.QApplication(sys.argv)
  edit = QTextEditSimple()
  edit.show()
  for i in edit.getCurrentFontFamilies():
    #first arrived, first shown
    edit.insertLine(i, fontName=i)
  app.exec_()
  #avoid Erreur de segmentation (core dumped)
  del(edit)
  del(app)
  sys.exit()


