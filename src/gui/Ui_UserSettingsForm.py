# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_files/UserSettingsForm.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UserSettingsForm(object):
    def setupUi(self, UserSettingsForm):
        UserSettingsForm.setObjectName("UserSettingsForm")
        UserSettingsForm.resize(422, 243)
        self.button_box = QtWidgets.QDialogButtonBox(UserSettingsForm)
        self.button_box.setGeometry(QtCore.QRect(60, 200, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.gridLayoutWidget = QtWidgets.QWidget(UserSettingsForm)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 10, 361, 171))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.grid_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("grid_layout")
        self._working_dir_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._working_dir_line_edit.setObjectName("_working_dir_line_edit")
        self.grid_layout.addWidget(self._working_dir_line_edit, 2, 2, 1, 1)
        self.output_dir_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.output_dir_label.setObjectName("output_dir_label")
        self.grid_layout.addWidget(self.output_dir_label, 1, 1, 1, 1)
        self.working_dir_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.working_dir_button.setObjectName("working_dir_button")
        self.grid_layout.addWidget(self.working_dir_button, 2, 3, 1, 1)
        self._output_dir_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._output_dir_line_edit.setObjectName("_output_dir_line_edit")
        self.grid_layout.addWidget(self._output_dir_line_edit, 1, 2, 1, 1)
        self.working_dir_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.working_dir_label.setObjectName("working_dir_label")
        self.grid_layout.addWidget(self.working_dir_label, 2, 1, 1, 1)
        self._sim_duration_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._sim_duration_line_edit.setObjectName("_sim_duration_line_edit")
        self.grid_layout.addWidget(self._sim_duration_line_edit, 3, 2, 1, 1)
        self.sim_duration_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sim_duration_label.setObjectName("sim_duration_label")
        self.grid_layout.addWidget(self.sim_duration_label, 3, 1, 1, 1)
        self.output_dir_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.output_dir_button.setObjectName("output_dir_button")
        self.grid_layout.addWidget(self.output_dir_button, 1, 3, 1, 1)
        self._wfds_exec_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._wfds_exec_line_edit.setObjectName("_wfds_exec_line_edit")
        self.grid_layout.addWidget(self._wfds_exec_line_edit, 4, 2, 1, 1)
        self.output_dir_label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.output_dir_label_2.setObjectName("output_dir_label_2")
        self.grid_layout.addWidget(self.output_dir_label_2, 4, 1, 1, 1)
        self.wfds_exec_bttn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.wfds_exec_bttn.setObjectName("wfds_exec_bttn")
        self.grid_layout.addWidget(self.wfds_exec_bttn, 4, 3, 1, 1)
        self.output_dir_label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.output_dir_label_3.setObjectName("output_dir_label_3")
        self.grid_layout.addWidget(self.output_dir_label_3, 5, 1, 1, 1)
        self._smv_exec_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self._smv_exec_line_edit.setObjectName("_smv_exec_line_edit")
        self.grid_layout.addWidget(self._smv_exec_line_edit, 5, 2, 1, 1)
        self.smv_exec_bttn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.smv_exec_bttn.setObjectName("smv_exec_bttn")
        self.grid_layout.addWidget(self.smv_exec_bttn, 5, 3, 1, 1)

        self.retranslateUi(UserSettingsForm)
        self.button_box.accepted.connect(UserSettingsForm.accept)
        self.button_box.rejected.connect(UserSettingsForm.reject)
        QtCore.QMetaObject.connectSlotsByName(UserSettingsForm)

    def retranslateUi(self, UserSettingsForm):
        _translate = QtCore.QCoreApplication.translate
        UserSettingsForm.setWindowTitle(_translate("UserSettingsForm", "FireScape Rx - User Settings"))
        self.output_dir_label.setText(_translate("UserSettingsForm", "Output Directory"))
        self.working_dir_button.setToolTip(_translate("UserSettingsForm", "Select a new Working Directory"))
        self.working_dir_button.setText(_translate("UserSettingsForm", "Browse..."))
        self.working_dir_label.setText(_translate("UserSettingsForm", "Working Directory"))
        self.sim_duration_label.setText(_translate("UserSettingsForm", "Simulation Duration"))
        self.output_dir_button.setToolTip(_translate("UserSettingsForm", "Select a new Output Directory"))
        self.output_dir_button.setText(_translate("UserSettingsForm", "Browse..."))
        self.output_dir_label_2.setText(_translate("UserSettingsForm", "WFDS executable"))
        self.wfds_exec_bttn.setToolTip(_translate("UserSettingsForm", "Select a new Output Directory"))
        self.wfds_exec_bttn.setText(_translate("UserSettingsForm", "Browse..."))
        self.output_dir_label_3.setText(_translate("UserSettingsForm", "SMV executable"))
        self.smv_exec_bttn.setToolTip(_translate("UserSettingsForm", "Select a new Output Directory"))
        self.smv_exec_bttn.setText(_translate("UserSettingsForm", "Browse..."))

