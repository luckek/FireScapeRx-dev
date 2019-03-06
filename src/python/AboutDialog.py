from PyQt5.QtWidgets import QDialog

from gui.Ui_AboutDialog import Ui_About


class AboutDialog(QDialog, Ui_About):

    def __init__(self):
        super(AboutDialog, self).__init__()

        self.setupUi(self)
        self.textEdit.setReadOnly(True)
