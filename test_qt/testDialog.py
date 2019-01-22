# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDoubleValidator

class testDialog(object):
    def setupUi(self, testDialog):
        testDialog.setObjectName("testDialog")
        testDialog.resize(400, 299)
        self.buttonBox = QtWidgets.QDialogButtonBox(testDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.testlineEdit = QtWidgets.QLineEdit(testDialog)

        self.deg_validator = QDoubleValidator(bottom=0.0, top=360.0, parent=self.testlineEdit)
        self.testlineEdit.setValidator(self.deg_validator)

        self.testlineEdit.setGeometry(QtCore.QRect(130, 100, 191, 31))
        self.testlineEdit.setObjectName("testlineEdit")

        self.retranslateUi(testDialog)
        self.buttonBox.accepted.connect(testDialog.accept)
        self.buttonBox.rejected.connect(testDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(testDialog)

    def retranslateUi(self, testDialog):
        _translate = QtCore.QCoreApplication.translate
        testDialog.setWindowTitle(_translate("testDialog", "Dialog"))

