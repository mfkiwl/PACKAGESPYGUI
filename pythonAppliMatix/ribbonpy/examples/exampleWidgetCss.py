#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END


import sys
import traceback
from PyQt5 import QtCore, QtWidgets as QTW

verbose = False
verboseEvent = False
setcss = True


############################################
class MyQVBoxLayout(QTW.QWidget):
  
  index = [0]
  css = """\
QWidget{
    Background: #AACCAA;
    color:blue;
    font:12px bold;
    font-weight:bold;
    border-radius: 1px;
    height: 11px;
}
QDialog{
    Background-image:url('img/titlebar bg.png');
    font-size:12px;
    color: black;

}
QToolButton{
    Background:#CCCCCC;
    font-size:15px;
    color: black;
}
QToolButton:hover{
    Background:n #EE2222;
    font-size:10px;
}"""

  def __init__(self, *args):
    super(MyQVBoxLayout, self).__init__(*args)
    self.className = self.__class__.__name__
    self.setObjectName("%s%s" % (self.className, str(self.index)))
    self.index[0] += 1 #unambigous objectName
    self.setWindowTitle(self.objectName())
    self.setWindowModality(QtCore.Qt.NonModal)
    self.box = QTW.QVBoxLayout()
    self.setLayout(self.box)
    if setcss: 
      self.setStyleSheet(self.css)
      close=QTW.QToolButton(self)
      close.setText("x")
      frameless=QTW.QToolButton(self)
      frameless.setText("o")
      self.box.addWidget(close)
      self.box.addWidget(frameless)
      self.box.addWidget(QTW.QLabel("!!button 'x' or Alt-F4 to close!!\n!!button 'o' to switch frameless!!\n"))
      close.clicked.connect(self.close)
      frameless.clicked.connect(self.frameless)
      
    #self.setMinimumSize(200, 50)
    edit = QTW.QLabel(self.css)
    self.box.addWidget(edit)
    #use method self.frameless() to get _oldWindowsFlags if not
    self._frameless = False
    self.frameless()
    
  def frameless(self):
    if self._frameless == True:
      self.setWindowFlags(self._oldWindowsFlags)
    else:
      self._oldWindowsFlags = self.windowFlags()
      self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    self._frameless = not self._frameless
    self.show() #seem to be hide on setWindowFlags
    print("frameless",self._frameless)


if __name__ == '__main__':
  app = QTW.QApplication(sys.argv)
  fen = MyQVBoxLayout()
  fen.show()
  app.exec_()
  #avoid Erreur de segmentation (core dumped)
  del(fen)
  del(app)
  sys.exit()


