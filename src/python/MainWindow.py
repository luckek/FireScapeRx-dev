from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, qApp
from gui.Ui_MainWindow import Ui_MainWindow
from UserSettingsForm import UserSettingsForm
from UserSettings import UserSettings
from AboutDialog import AboutDialog
from SimulationSettings import SimulationSettings
import os
import Utility as util
import sys
import logging as logger


class MainWindow(QMainWindow, Ui_MainWindow):

    # Path to pre-packaged fds executable
    fds_exec = os.path.abspath(os.pardir) + os.sep + 'fds_gnu_linux_64'

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Reset progress bar
        self.progressBar.setValue(0)

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

        dialog = None

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
            # FIXME: could probably wrap this if-else in it's own function
            # TODO: run simulation num_sims number of times
            if self.environment_present():
                logger.log(logger.INFO, 'Run simulation...')

                self.run_wfds()

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
            # TODO: Log unrecognized identifiers?
            print('UNRECOGNIZED IDENTIFIER:', identifier)
            return

        if dialog is not None:
            # TODO: Log null dialog?
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Ensure resources are freed when dlg closes
            dialog.exec_()  # Executes dialog

    # FIXME: make better name for this function
    @QtCore.pyqtSlot(str)
    def handle_file_button(self, identifier):

        if identifier == 'action_import_environment':
            # TODO: Could probably wrap this in its own function
            user_settings = UserSettings()

            # Open FileDialog in user's current working directory, with fds file filter
            file, file_filter = QFileDialog.getOpenFileName(self, 'Import Environment', user_settings.working_dir, filter="fds (*.fds *.txt)")

            if file:
                self.fds_file = file
                # TODO: actually import FDS file
                # TODO: if FDS file import is successful, modify current_env_label

            return

        else:
            # TODO: Log unrecognized identifiers?
            # FIXME: ignore identifiers that will not be handled
            print('UNRECOGNIZED IDENTIFIER:', identifier)

    def environment_present(self):
        return self.fds_file is not None

    def run_wfds(self):
        """This function runs wfds with the currently loaded environment"""

        user_settings = UserSettings()

        # Get user's output directory
        out_dir = os.path.abspath(user_settings.output_dir)

        # TODO: add ability to name simulation output directory?
        # TODO: if so, could make this(current) scheme default
        # eg, auto populate prompt w/ this directory

        fds_fname = util.get_filename(self.fds_file)

        # Create directory with same name as simulation
        out_dir += os.sep + fds_fname

        # TODO: see if this is necessary
        out_dir = util.make_unique_directory(out_dir)

        # Make another directory for simulation output files
        os.mkdir(out_dir)

        # FIXME
        fds_out_file = ''  # = open(out_dir + '/' + fds_fname + '.err', 'w', buffering=1)

        logger.log(logger.INFO, 'Running simulation')
        self.execute_and_update(cmd=[self.fds_exec, self.fds_file], cwd=out_dir, out_file=fds_out_file)

    # out_file not currently used, but may be later. So it is left in signature
    def execute_and_update(self, cmd, cwd=None, out_file=sys.stdout):

        """Execute the given command and update the progress bar"""

        # FIXME: this should come from fds_file
        t_end = 5.0

        # TODO: May be able to grab first few lines and update version info etc
        # could also use modified version of WFDS that does not hang upon execution
        for path in util.execute(cmd=cmd, cwd=cwd):

            path = path.replace(' ', '').replace('\n', '')

            if path.startswith('TimeStep'):

                timestep_kv, sim_time_kv = path.split(',')

                # Not currently used, could be later?
                timestep_int = timestep_kv.split(':')[1]
                sim_time_float = float(sim_time_kv.split(':')[1].replace('s', ''))

                # Figure out percentage and update progress bar
                loading = (sim_time_float / t_end) * 100
                self.progressBar.setValue(loading)

            # This may help to keep the gui responsive
            qApp.processEvents()
