from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QFileDialog
from gui.Ui_AboutDialog import Ui_About
from UserSettings import *
import os.path as osp


class AboutDialog(QDialog, Ui_About):

    def __init__(self):
        super(AboutDialog, self).__init__()

        self.setupUi(self)