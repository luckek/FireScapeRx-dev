# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from TestDialog import *

class TestMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionUser_Settings = QtWidgets.QAction(MainWindow)
        self.actionUser_Settings.setObjectName("actionUser_Settings")
        self.menuSettings.addAction(self.actionUser_Settings)
        self.menubar.addAction(self.menuSettings.menuAction())
        # ---- End generated code

        self.mapper = QtCore.QSignalMapper(MainWindow)

        # button.clicked.connect(lambda state, x=idx: self.button_pushed(x))
        identifier = 'User Settings'
        self.actionUser_Settings.triggered.connect(lambda state, x=identifier: self.handle_button(x))

        # self.mapper.setMapping(self.actionUser_Settings, 'User Settings')
        # self.actionUser_Settings.triggered.connect(self.mapper.map)

        # Call on_button_clicked when anything connected to the mapper is pressed
        # self.mapper.mapped[str].connect(self.handle_button)

        # Call on_button_clicked when user_settings is pressed
        # self.actionUser_Settings.triggered.connect(self.on_button_clicked)

        # ---- Begin generated code
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # ---- End generated code

    # ---- Generated function
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionUser_Settings.setText(_translate("MainWindow", "User Settings"))

    #@QtCore.pyqtSlot(str)
    def handle_button(self, identifier):
        dialog = QDialog()

        if identifier == 'User Settings':
            dialog.ui = TestDialog()
        else:
            print(identifier)

        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()
