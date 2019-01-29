# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/qt_files/UserSettingsForm.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from python.SimulationSettings import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 225)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setGeometry(QtCore.QRect(30, 170, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 149))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.grid_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("grid_layout")
        self.output_dir_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.output_dir_label.setObjectName("output_dir_label")
        self.grid_layout.addWidget(self.output_dir_label, 1, 1, 1, 1)
        self.output_dir_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.output_dir_line_edit.setObjectName("output_dir_line_edit")
        self.grid_layout.addWidget(self.output_dir_line_edit, 1, 2, 1, 1)
        self.working_dir_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.working_dir_button.setObjectName("working_dir_button")
        self.grid_layout.addWidget(self.working_dir_button, 2, 3, 1, 1)
        self.working_dir_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.working_dir_label.setObjectName("working_dir_label")
        self.grid_layout.addWidget(self.working_dir_label, 2, 1, 1, 1)
        self.working_dir_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.working_dir_line_edit.setObjectName("working_dir_line_edit")
        self.grid_layout.addWidget(self.working_dir_line_edit, 2, 2, 1, 1)
        self.output_dir_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.output_dir_button.setObjectName("output_dir_button")
        self.grid_layout.addWidget(self.output_dir_button, 1, 3, 1, 1)
        self.sim_duration_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sim_duration_label.setObjectName("sim_duration_label")
        self.grid_layout.addWidget(self.sim_duration_label, 3, 1, 1, 1)
        self.sim_duration_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.sim_duration_line_edit.setObjectName("sim_duration_line_edit")
        self.sim_duration_line_edit.setText(str(SimulationSettings.DEF_SIM_DURATION))
        self.grid_layout.addWidget(self.sim_duration_line_edit, 3, 2, 1, 1)
        self.sim_runs_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sim_runs_label.setObjectName("sim_runs_label")
        self.grid_layout.addWidget(self.sim_runs_label, 8, 1, 1, 1)
        self.sim_runs_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.sim_runs_line_edit.setObjectName("sim_runs_line_edit")
        self.sim_runs_line_edit.setText(str(SimulationSettings.DEF_NUM_RUNS))
        self.grid_layout.addWidget(self.sim_runs_line_edit, 8, 2, 1, 1)
        # ---- End generated code

        self.output_dir_button.clicked[bool].connect(button_clicked)
        self.output_dir_line_edit.returnPressed.connect(self.ret_pressed)

        # ---- Begin generated code
        self.retranslateUi(Dialog)
        # self.button_box.
        self.button_box.accepted.connect(Dialog.accept)
        self.button_box.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "User Settings"))
        self.output_dir_label.setText(_translate("Dialog", "Output Directory"))
        self.working_dir_button.setText(_translate("Dialog", "WD"))
        self.working_dir_label.setText(_translate("Dialog", "Working Directory"))
        self.output_dir_button.setText(_translate("Dialog", "OD"))
        self.sim_duration_label.setText(_translate("Dialog", "Simulation Duration"))
        self.sim_runs_label.setText(_translate("Dialog", "Simulation Runs"))


    def ret_pressed(self):
        print('Return')


@QtCore.pyqtSlot(bool, name='button_clicked')
def button_clicked( checked=None):
    file = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
    # fileName, _ = QFileDialog.getSaveFileName(self.button_box.parent(), "QFileDialog.getSaveFileName()", "", "All Files (*);;Text Files (*.txt)")

    if file:
        print('file:', file)