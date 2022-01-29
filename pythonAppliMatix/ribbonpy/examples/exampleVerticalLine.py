#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import json
from PyQt5 import QtCore, QtWidgets as QTW


def exampleVerticalLine():

    app = QTW.QApplication(sys.argv)
    
    window = QTW.QMainWindow()
    window.setWindowTitle("Example QFrame Vertical Splitter")
    window.resize(330, 220) 
    
    centralWidget   =  QTW.QWidget(window)
    layout    =  QTW.QGridLayout()  
    verticalLine  =  QTW.QFrame()
    
    buttons = [QTW.QPushButton("Button %i" % i) for i in range(4)]
    
    centralWidget.setLayout(layout)
    
    verticalLine.setFrameStyle(QTW.QFrame.VLine)
    verticalLine.setSizePolicy(QTW.QSizePolicy.Minimum,QTW.QSizePolicy.Expanding)
    verticalLine.setFrameShadow(QTW.QFrame.Sunken)
    
    for b in buttons:
      b.setSizePolicy(QTW.QSizePolicy.Expanding,QTW.QSizePolicy.Expanding)

    layout.addWidget(buttons[0],0,0)
    layout.addWidget(buttons[1],2,0)     
    layout.addWidget(verticalLine,0,1,3,1)  
    layout.addWidget(buttons[2],0,2)   
    layout.addWidget(buttons[3],2,2)   
    
    window.setCentralWidget(centralWidget)

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
  exampleVerticalLine()

