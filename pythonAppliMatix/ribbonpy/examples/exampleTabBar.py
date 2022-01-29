#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import json
from PyQt5 import QtCore, QtWidgets as QTW


class TabBarPlus(QTW.QTabBar):
    """
    Tab bar that has a plus button floating to the right of the tabs.
    http://stackoverflow.com/questions/19975137/how-can-i-add-a-new-tab-button-next-to-the-tabs-of-a-qmdiarea-in-tabbed-view-m
    """
    #http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
    plusClicked = QtCore.pyqtSignal()

    def __init__(self):
        super(TabBarPlus, self).__init__()

        # Plus Button
        self.plusButton = QTW.QPushButton("+")
        self.plusButton.setParent(self)
        s = 20
        self.plusButton.setMaximumSize(s, s) # Small Fixed size
        self.plusButton.setMinimumSize(s, s) # Small Fixed size
        self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton() # Move to the correct location

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QTW.QTabBar.sizeHint(self) 
        width = sizeHint.width()
        height = sizeHint.height()
        return QtCore.QSize(width+25, height)

    def resizeEvent(self, event):
        """Resize the widget and make sure the plus button is in the correct location."""
        super(TabBarPlus, self).resizeEvent(event)
        self.movePlusButton()

    def tabLayoutChange(self):
        """This virtual handler is called whenever the tab layout changes.
        If anything changes make sure the plus button is in the correct location.
        """
        super(TabBarPlus, self).tabLayoutChange()
        self.movePlusButton()


    def movePlusButton(self):
        """Move the plus button to the correct location."""
        # Find the width of all of the tabs
        size = 0
        for i in range(self.count()):
            size += self.tabRect(i).width()
        # Set the plus button location in a visible area
        h = self.geometry().top()
        w = self.width()
        if size > w: # Show just to the left of the scroll buttons
            x, y = (w-54, h)
        else:
            x, y = (size, h)
        print("movePlusButton x %i y %i" % (x,y))
        if x+y == 0 and self.parent()!=None:
          print("parent:", self.parent().parent())
          #self.plusButton.setParent(self.parent().parent())
          #self.plusClicked.emit()
        self.plusButton.move(x, y)


class CustomTabWidgetPlus(QTW.QTabWidget):
    """Tab Widget that that can have new tabs easily added to it."""
    index=[0]
    
    def __init__(self):
        super(CustomTabWidgetPlus, self).__init__()
        # Tab Bar
        self.tab = TabBarPlus()
        self.setTabBar(self.tab)
        # Properties
        self.setMovable(True)
        self.setTabsClosable(True)
        # Signals
        self.tab.plusClicked.connect(self.addTabPlus)
        #self.tab.tabMoved.connect(self.moveTab)
        self.tabCloseRequested.connect(self.removeTab)
        
    def addTabPlus(self, aWidget=None, aStr=None):
        widget= aWidget
        name = aStr
        if name == None:
          name = "more%s" % self.index
          self.index[0] += 1
        if widget==None:
          widget = QTW.QLabel(name)
        super(CustomTabWidgetPlus, self).addTab(widget, name)



def exampleTabBar():
    window = QTW.QMainWindow()
    window.setWindowTitle("Example TabBar")
    window.resize(330, 220) 

    tab = QTW.QTabWidget()
    tab.addTab(QTW.QLabel("foo"), "foo")
    tab.addTab(QTW.QLabel("bar"), "bar")
    b1 = QTW.QPushButton("<")
    b2 = QTW.QPushButton(">")
    tabbar = tab.tabBar()
    #for i in dir(tabbar): print "tabbar",i
    tabbar.setTabButton(0, tabbar.LeftSide, b1);
    tabbar.setTabButton(1, tabbar.RightSide, b2);

    window.setCentralWidget(tab)
    return window


def exampleTabBarPlus():
    window = QTW.QMainWindow()
    window.setWindowTitle("Example TabBarPlus")
    window.resize(330, 220) 

    tab = CustomTabWidgetPlus()
    tab.addTab(QTW.QLabel("foo"), "foo")
    tab.addTab(QTW.QLabel("bar"), "bar")
    b1 = QTW.QPushButton("<")
    b2 = QTW.QPushButton(">")
    tabbar = tab.tabBar()
    #for i in dir(tabbar): print "tabbar",i
    tabbar.setTabButton(0, tabbar.LeftSide, b1);
    #tabbar.setTabButton(1, tabbar.RightSide, b2);
    tabbar.setTabButton(1, tabbar.LeftSide, b2);
    window.setCentralWidget(tab)
    return window


if __name__ == '__main__':
  app = QTW.QApplication(sys.argv)
  #window = exampleTabBar()
  window = exampleTabBarPlus()
  window.show()
  sys.exit(app.exec_())
