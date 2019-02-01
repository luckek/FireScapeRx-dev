from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from gui.Ui_MainWindow import Ui_MainWindow
from UserSettingsForm import UserSettingsForm
from UserSettings import UserSettings
from AboutDialog import AboutDialog
from SimulationSettings import SimulationSettings


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Initialize fds_file to be None
        self.fds_file = None

        # Initialize fields with simulation settings values
        self.num_sim_line_edit.setText(str(SimulationSettings.DEF_NUM_SIMS))
        self.sim_duration_line_edit.setText(str(SimulationSettings.DEF_SIM_DURATION))
        self.wind_speed_line_edit.setText(str(SimulationSettings.DEF_WIND_SPEED))
        self.wind_direction_line_edit.setText(str(SimulationSettings.DEF_WIND_DIR))
        self.initialFireIntensityLineEdit.setText(str(SimulationSettings.DEF_INIT_INTENSITY))
        self.ignitionStartTime_line_edit.setText(str(SimulationSettings.DEF_IGNITION_START))

        for child in self.menubar.children():
            if type(child) is QtWidgets.QMenu:
                for action in child.actions():
                    # Use objectName as identifier so as to ensure uniqueness of identifier
                    identifier = action.objectName()
                    action.triggered.connect(lambda state, x=identifier: self.handle_button(x))
                    action.triggered.connect(lambda state, x=identifier: self.handle_file_button(x))

    # FIXME: make static or remove from class altogether if we do not need to access anything in main window
    @QtCore.pyqtSlot(str)
    def handle_button(self, identifier):

        # FIXME: ignore identifiers that will not be handled

        if identifier == 'action_create_environment':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_import_environment':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_import_simulation':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_export_summary':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_export_environment':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_export_simulation':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_export_summary':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_run_sim':
            # FIXME: could probably wrap this in it's own function
            if self.environment_present():
                print('Run simulation...')
                # FIXME: actually run simulation right here
                # & give user indication of how far along
                # simulation is(if possible)

            else:

                # FIXME: decide if should be warning, information or critical
                # NOTE: Since QMessageBox displays rich text, we can use markup and html to format output
                # NOTE: QMessageBox displays itself
                QMessageBox.information(self, 'No Environment Present', '<html>No Environment Present!<br>Please create or import an environment.</html>')

                # We do not care about return value of QMessageBox
                return

        elif identifier == 'action_view_sim':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_user_settings':
            dialog = UserSettingsForm()

        elif identifier == 'action_select_output_file':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_about':
            dialog = AboutDialog()

        else:
            print(identifier)
            return

        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Ensure resources are freed when dlg closes
        dialog.exec_()  # Executes dialog

    # FIXME: make better name for this function
    @QtCore.pyqtSlot(str)
    def handle_file_button(self, identifier):

        if identifier == 'action_import_environment':
            user_settings = UserSettings()
            file = str(QFileDialog.getOpenFileName(self, 'Import Environment', user_settings.working_dir, filter="fds (*.fds *.txt)"))

            if file:
                self.fds_file = file
                # TODO: actually import FDS file
            return

        else:
            # FIXME: ignore identifiers that will not be handled
            print(identifier, 'Not implemented')

    def environment_present(self):
        return self.fds_file is not None
