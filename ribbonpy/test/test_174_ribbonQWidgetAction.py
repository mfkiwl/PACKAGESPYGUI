#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% LICENSE_SALOME_CEA_BEGIN
# see PACKAGESPY/LICENCE file
# %% LICENSE_END

"""
Launch this test:
./AllTestLauncher.sh pythonAppliMatix/ribbonpy  "test_174_*.py"
"""

import unittest
import datetime
from PyQt5 import QtCore, QtWidgets as QTW
from functools import partial

import ribbonpy.ribbonClassFactory as RCF
import ribbonpy.ribbonQMainWindow as RQM

from ribbonpy.ribbonTrace import getLoggerRibbon
RT = getLoggerRibbon()


setTimer = True
deltaTime = 2000
withShow = True
verbose = False


#############################################
class MyQWidgetAction(QTW.QWidgetAction):
  def __init__(self, *args, **kwargs):
    QTW.QWidgetAction.__init__(self, args[0])
    self.setObjectName(args[1])
    self.setToolTip = "tooltip '%s'" % self.objectName()


#############################################
class MyQWidgetAction_more(QTW.QWidgetAction):

  index = [0] # for unique createWidget naming

  def __init__(self, *args, **kwargs):
    QTW.QWidgetAction.__init__(self, args[0])
    self.setObjectName(args[1])
    self.setToolTip = "tooltip '%s'" % self.objectName()

  def createWidget(self, parent):
    RT.warning("%s.createWidget [%i]" % (self.objectName(), self.index[0]))
    wid = QTW.QWidget(parent)
    wid.setObjectName("%s widget [%i]" % (self.objectName(), self.index[0]))
    lay = QTW.QHBoxLayout()
    lay.addWidget(QTW.QLabel("a implicit widgetaction [%i]" % self.index[0]))
    lay.addWidget(QTW.QLineEdit("line edit [%i]" % self.index[0]))
    wid.setLayout(lay)
    self.index[0] += 1
    RT.warning("TODO MyQWidgetAction_more connect slots if useful")
    return wid


#############################################
class MyMenu(QTW.QMenu):
  def __init__(self, *args, **kwargs):
    QTW.QMenu.__init__(self, *args)
    self.setToolTip = "tooltip '%s'" % self.objectName()
    for i in range(5):
      name = "MyMenu_Action_[%i]" % i
      action = self.addAction(name)
      action.setObjectName(name)
      action.setToolTip = "tooltip '%s'" % action.objectName()  # useless
      action.triggered.connect(partial(hello, action.objectName()))


#############################################
class MyQCombobox(QTW.QComboBox):
  def __init__(self, *args, **kwargs):
    QTW.QComboBox.__init__(self)
    self.setObjectName(args[0])
    self.setToolTip = "tooltip '%s'" % self.objectName()
    self.setMinimumSize(20, 10)
    for i in range(5):
      name = "%s_Item_[%i]" % (self.objectName(), i)
      self.addItem(name)
      #action.triggered.connect(partial(hello, action.objectName()))



#############################################
class MyCustomDateEdit(QTW.QWidget):
  """
  example from ert-master/python/python/ert_gui/tools/plot/custom_date_edit.py
  """
  def __init__(self):
    QTW.QWidget.__init__(self)
    self._line_edit = QTW.QLineEdit()

    self._calendar_button = QTW.QToolButton()
    self._calendar_button.setPopupMode(QTW.QToolButton.InstantPopup)
    # self._calendar_button.setFixedSize(26, 26)
    self._calendar_button.setText("calendar")
    # self._calendar_button.setAutoRaise(True)
    # self._calendar_button.setIcon(resourceIcon("calendar.png"))
    self._calendar_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")

    tool_menu = QTW.QMenu(self._calendar_button)
    self._calendar_widget = QTW.QCalendarWidget(tool_menu)
    action = QTW.QWidgetAction(tool_menu)
    action.setDefaultWidget(self._calendar_widget)
    tool_menu.addAction(action)
    self._calendar_button.setMenu(tool_menu)

    layout = QTW.QHBoxLayout()
    # layout.setMargin(0)
    layout.addWidget(self._calendar_button)
    layout.addWidget(self._line_edit)
    self.setLayout(layout)
    self._calendar_widget.activated.connect(self.setDate)

  def setDate(self, date):
    if isinstance(date, datetime.date):
      date = QDate(date.year, date.month, date.day)

    if date is not None and date.isValid():
      self._line_edit.setText(str(date.toString("yyyy-MM-dd")))
    else:
      self._line_edit.setText("")

  def date(self):
    date_string = self._line_edit.text()
    if len(str(date_string).strip()) > 0:
      date = QDate.fromString(date_string, "yyyy-MM-dd")
      if date.isValid():
        return datetime.date(date.year(), date.month(), date.day())
    return None


#############################################
def hello(msg):
  RT.warning("**** Hello %s" % msg)


#############################################
class TestCase(unittest.TestCase):

  def launchTimer(self, wid):
    timer = QtCore.QTimer()
    timer.timeout.connect(wid.close)
    if setTimer: timer.start(deltaTime)
    self.app.exec_()

  def test_000(self):
    # avoid message QWidget: Must construct a QApplication before a QWidgetimport salomepy.onceQApplication as OQA
    import salomepy.onceQApplication as OQA
    self.app = OQA.OnceQApplication()
    # print(RT.__dict__.keys())
    if verbose:
      RT.setLevel("DEBUG")
    else:
      RT.setLevel("ERROR")

  def test_999(self):
    # RT.popLevel()
    pass

  def xtest_010(self):
    fen = QTW.QMainWindow()
    fen.setWindowTitle(self._testMethodName)
    fen.resize(500, 200)
    mba = fen.menuBar()
    men1 = MyMenu("menu_1")
    mba.addMenu(men1)
    mba.addSeparator()  # useless
    men2 = MyMenu("menu_2")
    mba.addMenu(men2)
    fen.show()
    self.launchTimer(fen)

  def xtest_020(self):
    fen = QTW.QMainWindow()
    fen.setWindowTitle(self._testMethodName)
    fen.resize(500, 200)
    mba = fen.menuBar()
    tba = fen.addToolBar("toolbar_1")
    men = MyMenu("menu_1")
    com1 = MyQCombobox("MyQCombobox_1")
    com2 = MyQCombobox("MyQCombobox_2")

    mba.addMenu(men)
    tba.addWidget(com1)
    tba.addSeparator()
    tba.addWidget(com2)
    fen.show()
    self.launchTimer(fen)

  def xtest_025(self):
    fen = QTW.QMainWindow()
    fen.setWindowTitle(self._testMethodName)
    fen.resize(500, 200)
    tba = fen.addToolBar("toolbar_1")
    tba.addWidget(MyCustomDateEdit())
    fen.show()
    self.launchTimer(fen)


  def xtest_030(self):
    fen = QTW.QMainWindow()
    fen.setWindowTitle(self._testMethodName)
    fen.resize(800, 200)
    mba = fen.menuBar()
    tba = fen.addToolBar("toolbar_1")
    men = MyMenu("menu_1")
    com = MyQCombobox("MyQCombobox")

    wid = QTW.QWidget()
    lay = QTW.QHBoxLayout()
    lay.addWidget(QTW.QLabel("a first widgetaction"))
    lay.addWidget(QTW.QLineEdit("line edit"))
    wid.setLayout(lay)

    wac = MyQWidgetAction(tba, "MyQWidgetAction")
    wac.setDefaultWidget(wid)

    mba.addMenu(men)
    tba.addWidget(com)
    tba.addSeparator()
    tba.addAction(wac)

    tba2 = fen.addToolBar("toolbar_2")
    tba2.addWidget(QTW.QLabel("a second widgetaction"))
    tba2.addAction(wac)  # useless only one time

    fen.show()
    self.launchTimer(fen)


  def xtest_040(self):
    fen = QTW.QMainWindow()
    fen.setWindowTitle(self._testMethodName)
    fen.resize(800, 200)
    mba = fen.menuBar()
    tba = fen.addToolBar("toolbar_1")
    men = MyMenu("menu_1")
    com = MyQCombobox("MyQCombobox")

    wac1 = MyQWidgetAction_more(tba, "MyQWidgetAction_more_1")

    mba.addMenu(men)
    tba.addWidget(com)
    tba.addSeparator()
    RT.warning('tba.addAction(wac1) so createWidget')
    tba.addAction(wac1)

    tba2 = fen.addToolBar("toolbar_2")
    wac2 = MyQWidgetAction_more(tba2, "MyQWidgetAction_more_2")
    RT.warning('tba.addAction(wac2) so createWidget')
    tba2.addAction(wac2)

    fen.show()
    self.launchTimer(fen)


  def xtest_100(self):
    aJsonValue = RCF.getExampleJsonRibbon()
    fen = RQM.QMainWindowForRibbon(setFromJson=aJsonValue)
    fen.setWindowTitle(self._testMethodName)
    ribbon = fen.ribbon[0]
    RT.warning("ribbon %s" % ribbon)

    mba = fen.menuBar().addMenu(MyMenu("menu_1"))

    for i in range(4):
      tbr = fen.addToolBar("Toolbar %i" % i)
      wac = MyQWidgetAction_more(tbr, "MyQWidgetAction %i" % i)
      tbr.addAction(wac)

    fen.show()
    self.launchTimer(fen)


if __name__ == '__main__':
  verbose = False
  setTimer = False
  unittest.main()
  pass
