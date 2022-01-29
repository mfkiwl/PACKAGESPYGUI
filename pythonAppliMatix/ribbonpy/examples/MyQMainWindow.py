#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtGui, QtCore, QtWidgets

verbose = False
verboseEvent = False

class MyQMainWindow(QtWidgets.QMainWindow):  

  def event(self, event):
    print("MyQMainWindow event %s" % event)
    return super(MyQMainWindow, self).event(event)

if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  fen = MyQMainWindow()
  fen.show()
  app.exec_()
  #avoid Erreur de segmentation (core dumped)
  del(fen)
  del(app)
  sys.exit()
