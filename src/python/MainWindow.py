from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from gui.Ui_MainWindow import Ui_MainWindow
from UserSettingsForm import UserSettingsForm


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        for child in self.menubar.children():
            if type(child) is QtWidgets.QMenu:
                for action in child.actions():
                    identifier = action.text()
                    action.triggered.connect(lambda state, x=identifier: self.handle_button(x))

    # FIXME: make static or remove from class altogether if we do not need to access anything in main window
    @QtCore.pyqtSlot(str)
    def handle_button(self, identifier):

        # FIXME: ignore identifiers that will not be handled
        dialog = QDialog()

        if identifier == 'Create Environment':
            print(identifier, 'not implemented')
            return

        elif identifier == 'Environment':
            print(identifier, 'not implemented')
            return

        elif identifier == 'Simulation':
            print(identifier, 'not implemented')
            return

        elif identifier == 'Summary File':
            print(identifier, 'not implemented')
            return

        elif identifier == 'User Settings':
            dialog.ui = Ui_Dialog()

        elif identifier == 'Select Output File':
            print(identifier, 'not implemented')
            return

        elif identifier == 'About':
            print(identifier, 'not implemented')
            return

        elif identifier == 'Run':
            print(identifier, 'not implemented')
            return

        elif identifier == 'View':
            print(identifier, 'not implemented')
            return

        else:
            print(identifier)
            return

        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Ensure resources are freed when dlg closes
        dialog.exec_()  # Executes dialog

    # FIXME: make static or remove from class altogether if we do not need to access anything in main window
    @QtCore.pyqtSlot(str)
    def handle_file_button(self, identifier):
        # FIXME: ignore identifiers that will not be handled
        print(identifier, 'Not implemented')