# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow

from PyQt5 import QtCore, QtGui, QtWidgets

class TestDialog(object):
    def setupUi(self, testDialog):
        testDialog.setObjectName("testDialog")
        testDialog.resize(400, 299)
        self.buttonBox = QtWidgets.QDialogButtonBox(testDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.testlineEdit = QtWidgets.QLineEdit(testDialog)
        self.testlineEdit.setGeometry(QtCore.QRect(130, 100, 191, 31))
        self.testlineEdit.setObjectName("testlineEdit")
        self.pushButton = QtWidgets.QPushButton(testDialog)
        self.pushButton.setGeometry(QtCore.QRect(240, 140, 80, 23))
        self.pushButton.setObjectName("pushButton")

        # When button is pushed, on_button_clicked is called
        self.pushButton.clicked.connect(on_button_clicked)

        # Whenever 'testlineEdit' is edited, a signal is emitted (regardless whether it is bound to a slot).
        # By connecting to self.print_edited, this function will be called whenever this signal is emitted
        # NOTE: this uses newer, alternative syntax. The [str] specifies we want to connect to
        # the text edited signal that emits a string.
        self.testlineEdit.textEdited[str].connect(print_edited)

        self.retranslateUi(testDialog)
        self.buttonBox.accepted.connect(testDialog.accept)
        self.buttonBox.rejected.connect(testDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(testDialog)

    def retranslateUi(self, testDialog):
        _translate = QtCore.QCoreApplication.translate
        testDialog.setWindowTitle(_translate("testDialog", "Dialog"))
        self.pushButton.setText(_translate("testDialog", "PushButton"))


# Mark method with decorator
# so it is explicitly a slot.
# While slightly more verbose, it is much
# safer and faster. This way, PyQt KNOWS it is definitely a slot.
@QtCore.pyqtSlot(bool)
def on_button_clicked(checked=None):

    """Small example slot"""

    if checked is None:
        return

    dialog = QDialog()
    dialog.ui = TestDialog()
    dialog.ui.setupUi(dialog)
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    dialog.exec_()


@QtCore.pyqtSlot(str)
def print_edited(text):
    print('Current text:', text)
