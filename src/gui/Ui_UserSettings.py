# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_files/UserSettingsForm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(422, 225)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setGeometry(QtCore.QRect(60, 170, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 10, 361, 151))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.grid_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("grid_layout")
        self.sim_duration_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sim_duration_label.setObjectName("sim_duration_label")
        self.grid_layout.addWidget(self.sim_duration_label, 4, 1, 1, 1)
        self.default_environment_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.default_environment_button.setObjectName("default_environment_button")
        self.grid_layout.addWidget(self.default_environment_button, 3, 3, 1, 1)
        self.output_dir_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.output_dir_label.setObjectName("output_dir_label")
        self.grid_layout.addWidget(self.output_dir_label, 1, 1, 1, 1)
        self._output_dir_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._output_dir_line_edit.setObjectName("_output_dir_line_edit")
        self.grid_layout.addWidget(self._output_dir_line_edit, 1, 2, 1, 1)
        self.output_dir_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.output_dir_button.setObjectName("output_dir_button")
        self.grid_layout.addWidget(self.output_dir_button, 1, 3, 1, 1)
        self.working_dir_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.working_dir_button.setObjectName("working_dir_button")
        self.grid_layout.addWidget(self.working_dir_button, 2, 3, 1, 1)
        self._working_dir_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._working_dir_line_edit.setObjectName("_working_dir_line_edit")
        self.grid_layout.addWidget(self._working_dir_line_edit, 2, 2, 1, 1)
        self.working_dir_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.working_dir_label.setObjectName("working_dir_label")
        self.grid_layout.addWidget(self.working_dir_label, 2, 1, 1, 1)
        self._sim_duration_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._sim_duration_line_edit.setObjectName("_sim_duration_line_edit")
        self.grid_layout.addWidget(self._sim_duration_line_edit, 4, 2, 1, 1)
        self.default_environment_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.default_environment_label.setObjectName("default_environment_label")
        self.grid_layout.addWidget(self.default_environment_label, 3, 1, 1, 1)
        self._default_environment_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._default_environment_line_edit.setObjectName("_default_environment_line_edit")
        self.grid_layout.addWidget(self._default_environment_line_edit, 3, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept)
        self.button_box.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.sim_duration_label.setText(_translate("Dialog", "Simulation Duration"))
        self.default_environment_button.setText(_translate("Dialog", "DE"))
        self.output_dir_label.setText(_translate("Dialog", "Output Directory"))
        self.output_dir_button.setText(_translate("Dialog", "OD"))
        self.working_dir_button.setText(_translate("Dialog", "WD"))
        self.working_dir_label.setText(_translate("Dialog", "Working Directory"))
        self.default_environment_label.setText(_translate("Dialog", "Default Environment"))

