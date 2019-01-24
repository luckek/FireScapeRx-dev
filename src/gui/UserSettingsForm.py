# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_settings_form.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class UserSettingsForm(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 226)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 170, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 128))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.outputDirectoryLineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.outputDirectoryLineEdit_2.setObjectName("outputDirectoryLineEdit_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.outputDirectoryLineEdit_2)
        self.outputDirectoryLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.outputDirectoryLabel.setObjectName("outputDirectoryLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.outputDirectoryLabel)
        self.outputDirectoryLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.outputDirectoryLineEdit.setObjectName("outputDirectoryLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.outputDirectoryLineEdit)
        self.simulationDurationLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.simulationDurationLineEdit.setObjectName("simulationDurationLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.simulationDurationLineEdit)
        self.simulationRunsLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.simulationRunsLabel.setObjectName("simulationRunsLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.simulationRunsLabel)
        self.simulationRunsLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.simulationRunsLineEdit.setObjectName("simulationRunsLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.simulationRunsLineEdit)
        self.simulationDurationLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.simulationDurationLabel.setObjectName("simulationDurationLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.simulationDurationLabel)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(330, 10, 39, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButton = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 0, 1, 1)
        self.toolButton_3 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_3.setObjectName("toolButton_3")
        self.gridLayout.addWidget(self.toolButton_3, 3, 0, 1, 1)
        self.toolButton_4 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_4.setObjectName("toolButton_4")
        self.gridLayout.addWidget(self.toolButton_4, 4, 0, 1, 1)
        self.toolButton_2 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout.addWidget(self.toolButton_2, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Working Directory"))
        self.outputDirectoryLabel.setText(_translate("Dialog", "Output Directory"))
        self.simulationRunsLabel.setText(_translate("Dialog", "Simulation Runs"))
        self.simulationDurationLabel.setText(_translate("Dialog", "Simulation Duration"))
        self.toolButton.setText(_translate("Dialog", "WD"))
        self.toolButton_3.setText(_translate("Dialog", "SD"))
        self.toolButton_4.setText(_translate("Dialog", "SR"))
        self.toolButton_2.setText(_translate("Dialog", "OD"))

