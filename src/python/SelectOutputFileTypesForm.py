from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from gui.Ui_SelectOutputFileTypes import Ui_SelectOutputFileTypes
from UserSettings import *
import os.path as osp


class SelectOutputFileTypesForm(QDialog, Ui_SelectOutputFileTypes):

    FILE_TYPES = ['txt', 'fds', 'slc', 'iso', 'bf', 'sf', ]

    def __init__(self):
        super(SelectOutputFileTypesForm, self).__init__()

        self.setupUi(self)

        self._check_box_list = list()
        for file_type in self.FILE_TYPES:
            check_box = QtWidgets.QCheckBox(file_type, parent=self.verticalLayoutWidget)
            check_box.setObjectName(file_type)
            self.verticalLayout.addWidget(check_box)
            self._check_box_list.append(check_box)

    def get_file_types(self):
        out_list = []
        if self.exec_() == QDialog.Accepted:
            # Get the selected output file types
            for box in self.verticalLayout.children():
                if type(box) is QtWidgets.QCheckBox and box.isChecked():
                    out_list.append(box.text())

        return out_list
