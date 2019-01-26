from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from gui.Ui_MainWindow import Ui_MainWindow
from UserSettingsForm import UserSettingsForm


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # # Connect up the buttons.
        # self.okButton.clicked.connect(self.accept)
        # self.cancelButton.clicked.connect(self.reject)

        # Create mapper
        self.mapper = QtCore.QSignalMapper(self)

        # NOTE: this has to be done after retranslateUi otherwise the text is not set
        for child in self.menubar.children():
            if type(child) is QtWidgets.QMenu:
                for action in child.actions():
                    # This line maps an action to a string
                    self.mapper.setMapping(action, action.text())
                    identifier = action.text()
                    action.triggered.connect(lambda state, x=identifier: self.handle_button(x))

                    # Connect the action's signal to the mapper
                    # action.triggered.connect(self.mapper.map)

        # Connect the mapper to the button
        # self.mapper.connect(self.handle_button)
        # self.mapper.mapped['QString'].connect(self.handle_button)
        # self.mapper.mapped['QString'].connect(self.handle_file_button)

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