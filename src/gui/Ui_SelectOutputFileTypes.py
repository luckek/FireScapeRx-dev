# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_files/SelectOutputFileTypes.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SelectOutputFileTypes(object):
    def setupUi(self, SelectOutputFileTypes):
        SelectOutputFileTypes.setObjectName("SelectOutputFileTypes")
        SelectOutputFileTypes.resize(221, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectOutputFileTypes)
        self.buttonBox.setGeometry(QtCore.QRect(20, 240, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(SelectOutputFileTypes)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 40, 161, 201))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self._file_type_vert_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self._file_type_vert_layout.setContentsMargins(0, 0, 0, 0)
        self._file_type_vert_layout.setObjectName("_file_type_vert_layout")

        self.retranslateUi(SelectOutputFileTypes)
        self.buttonBox.accepted.connect(SelectOutputFileTypes.accept)
        self.buttonBox.rejected.connect(SelectOutputFileTypes.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectOutputFileTypes)

    def retranslateUi(self, SelectOutputFileTypes):
        _translate = QtCore.QCoreApplication.translate
        SelectOutputFileTypes.setWindowTitle(_translate("SelectOutputFileTypes", "Dialog"))

