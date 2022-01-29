#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
#########################################################
## customize Title bar
## dotpy.ir
## iraj.jelo@gmail.com
#########################################################
http://stackoverflow.com/questions/9377914/how-to-customize-title-bar-and-window
"""

import sys
from PyQt5 import QtGui, QtCore, QtWidgets as QTW

setcss=False

class TitleBar(QTW.QDialog):
    def __init__(self, parent=None):
        QTW.QWidget.__init__(self, parent)
        css = """
        QWidget{
            #Background: #AA00AA;
            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            #Background-image:url('img/titlebar bg.png');
            font-size:12px;
            color: black;

        }
        QToolButton{
            B#ackground:#AA00AA;
            font-size:11px;
        }
        QToolButton:hover{
            #Background:n #FF00FF;
            font-size:11px;
        }
        """

        if setcss: 
          self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
          self.setStyleSheet(css)
          #self.setAutoFillBackground(True)
          #self.setBackgroundRole(QTW.QPalette.Highlight)
                  
        self.minimize=QTW.QToolButton(self)
        self.minimize.setText("-")
        #self.minimize.setIcon(QTW.QIcon('img/min.png'))
        self.maximize=QTW.QToolButton(self)
        self.maximize.setText("+")
        #self.maximize.setIcon(QTW.QIcon('img/max.png'))
        close=QTW.QToolButton(self)
        close.setText("x")
        #close.setIcon(QTW.QIcon('img/close.png'))
        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10);
        self.maximize.setMinimumHeight(10)
        label=QTW.QLabel(self);
        label.setText("Window Title");
        self.setWindowTitle("Window Title")
        hbox=QTW.QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1,500)
        hbox.setSpacing(0)
        #self.setSizePolicy(QTW.QSizePolicy.Expanding,QTW.QSizePolicy.Fixed)
        self.maxNormal=False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        box.showMinimized()

    def showMaxRestore(self):
        if(self.maxNormal):
            box.showNormal();
            self.maxNormal= False
            self.maximize.setIcon(QTW.QIcon('img/max.png'))
            print('showNormal 1')
        else:
            box.showMaximized()
            self.maxNormal=  True
            print('showMaximized 2')
            self.maximize.setIcon(QTW.QIcon('img/max2.png'))

    def close(self):
        box.close()

    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
           box.moving = True
           box.offset = event.pos()

    def mouseMoveEvent(self,event):
        if box.moving: 
           box.move(event.globalPos()-box.offset)


class Frame(QTW.QFrame):
    def __init__(self, parent=None):
        QTW.QFrame.__init__(self, parent)
        self.m_mouse_down= False;
        self.setFrameShape(QTW.QFrame.StyledPanel)
        css = """
        QFrame{
            Background:  #D700D7;
            color:white;
            font:13px ;
            font-weight:bold;
            }
        """
        if setcss: 
          self.setStyleSheet(css) 
          self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar= TitleBar(self)
        self.m_content= QTW.QWidget(self)
        vbox=QTW.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        #vbox.setMargin(0)
        #vbox.setSpacing(0)
        layout=QTW.QVBoxLayout(self)
        layout.addWidget(self.m_content)
        #layout.setMargin(5)
        #layout.setSpacing(0)
        vbox.addLayout(layout)
        # Allows you to access the content area of the frame
        # where widgets and layouts can be added

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self,event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button()== QtCore.Qt.LeftButton

    def mouseMoveEvent(self,event):
        x=event.x()
        y=event.y()

    def mouseReleaseEvent(self,event):
        m_mouse_down=False

def essai():
    box = Frame()
    #box.move(60,60)
    l=QTW.QVBoxLayout(box.contentWidget())
    #l.setMargin(30)
    edit=QTW.QLabel("""I would've did anything for you 
to show you how much I adored you
But it's over now, it's too late to save our 
loveJust promise me you'll think of me
Every time you look up in the sky and see a 
star 'cuz I'm  your star.""")
    l.addWidget(edit)
    return box

if __name__ == '__main__':
    app = QTW.QApplication(sys.argv)
    fen = essai()
    fen.show()
    app.exec_()
    
    setcss=True
    fen = essai()
    fen.show()
    app.exec_()
    del(fen)
    del(app)
    sys.exit()
    