from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, qApp, QLabel, QGraphicsView, QWidget, QGridLayout
from gui.Ui_MainWindow import Ui_MainWindow
from UserSettingsForm import UserSettingsForm, UserSettings
from AboutDialog import AboutDialog
from SimulationSettings import SimulationSettings
from SelectOutputFileTypesForm import SelectOutputFileTypesForm
from FuelMapEditor import FuelMapEditor, AsciiParser
from Fds import Fds
import os
import Utility as util
import sys
import logging as logger
import time


class MainWindow(QMainWindow, Ui_MainWindow):

    # Path to pre-packaged smv executable
    smv_exec = os.path.abspath(os.pardir) + os.sep + 'smokeview_linux_64'

    def __init__(self):

        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Create the fuel map editor variable
        self._fuel_map_editor = None

        # Hide scroll area
        self.fuel_map_grid_scroll_area.hide()

        # Disable export of files until one is loaded
        self.action_export_fuel_map.setEnabled(False)
        self.action_export_dem.setEnabled(False)
        self.fuel_type_legend_tab.setEnabled(False)

        # FIXME: re-enable when this gets implemented:
        self.action_import_dem.setEnabled(False)
        self.action_export_summary_file.setEnabled(False)
        self.action_import_summary_file.setEnabled(False)
        self.action_export_environment.setEnabled(False)
        self.add_type_button.setEnabled(False)
        self.remove_type_button.setEnabled(False)

        # Hide and reset progress bar
        self.hide_and_reset_progress()

        # Setup validation for fuel map editor inputs
        self.x_range_max_line_edit.returnPressed.connect(self.x_range_return_pressed)
        self.x_range_min_line_edit.returnPressed.connect(self.x_range_return_pressed)

        self.y_range_max_line_edit.returnPressed.connect(self.y_range_return_pressed)
        self.y_range_min_line_edit.returnPressed.connect(self.y_range_return_pressed)

        self.modify_fuel_map_button.clicked.connect(self.__modify_fuel_map)

        # Initialize fds object
        self._fds = Fds()
        self._fds_exec = self._fds.fds_exec

        self.fuel_type_grid_layout_widget = QWidget(self)
        self.fuel_type_grid_layout = QGridLayout(self.fuel_type_grid_layout_widget)

        # HIDE THIS or it will cause problems with GUI (cant click on part of menubar)
        self.fuel_type_grid_layout_widget.hide()

        # TODO: make use of this variable
        # Initialize selected output file types
        self._output_file_types = []

        # Initialize fds_file to be None
        self.smv_file = None

        sim_settings = SimulationSettings('default.sim_settings')

        # Initialize fields with simulation settings values
        self.num_sim_line_edit.setText(str(sim_settings.num_sims))
        self.sim_duration_line_edit.setText(str(sim_settings.sim_duration))
        self.wind_speed_line_edit.setText(str(sim_settings.wind_speed))
        self.wind_direction_line_edit.setText(str(sim_settings.wind_direction))

        for child in self.menubar.children():
            if type(child) is QtWidgets.QMenu:
                for action in child.actions():
                    # Use objectName as identifier so as to ensure uniqueness of identifier
                    identifier = action.objectName()
                    action.triggered.connect(lambda state, x=identifier: self.handle_button(x))

    # FIXME: make static or remove from class altogether if we do not need to access anything in main window
    @QtCore.pyqtSlot(str)
    def handle_button(self, identifier):

        dialog = None

        # FIXME: ignore identifiers that will not be handled

        if identifier == 'action_create_environment':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_import_environment':
            self.import_environment()
            return

        elif identifier == 'action_import_simulation':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_import_fuel_map':
            self.__import_fuel_map()
            return

        elif identifier == 'action_import_dem':
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

        elif identifier == 'action_export_fuel_map':
            self.__export_fuel_map()

        elif identifier == 'action_export_dem':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_run_sim':
            # TODO: run simulation num_sims number of times
            self.run_simulation()

        elif identifier == 'action_view_sim':

            user_settings = UserSettings()

            # Open FileDialog in user's current working directory, with smv file filter
            file, file_filter = QFileDialog.getOpenFileName(self, 'View Simulation', user_settings.working_dir,
                                                            filter="smv (*.smv)")

            if file:
                self.smv_file = file

            if self.smv_file is not None:
                logger.log(logger.INFO, 'Launching smokeview')
                self.run_smv()

            # We do not care about return value of QMessageBox
            return

        elif identifier == 'action_user_settings':
            dialog = UserSettingsForm()

        elif identifier == 'action_select_output_files':
            dialog = SelectOutputFileTypesForm()
            self._output_file_types = dialog.get_file_types()

            # Dialog will run itself, so we can return.
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

    def __modify_fuel_map(self):

        # Ensure x and y range are valid
        if self.check_x_range():
            if self.check_y_range():
                print('valid coordinate range')

                x_min = int(self.x_range_min_line_edit.text())
                x_max = int(self.x_range_max_line_edit.text())

                y_min = int(self.y_range_min_line_edit.text())
                y_max = int(self.y_range_max_line_edit.text())

                fuel_type = self.fuel_type_combo_box.currentIndex()

                # Modify the fuel map
                self._fuel_map_editor.modify_range(x_min, x_max, y_min, y_max, fuel_type)

    def __import_fuel_map(self):

        user_settings = UserSettings()
        file_filter = 'Ascii GRID file (*' + ' *'.join(AsciiParser.FILE_EXT) + ')'
        file, filt = QFileDialog.getOpenFileName(self, 'Open File', user_settings.working_dir, file_filter)

        if file:
            self._fuel_map_editor = FuelMapEditor(file)
            self.fuel_map_grid_scroll_area.setWidget(self._fuel_map_editor)
            self.setup_fuel_map_legend()

            # Enable relevant widgets
            self.action_export_fuel_map.setEnabled(True)
            self.fuel_type_legend_tab.setEnabled(True)

            # Set current tab to fuel type legend
            self.tab_widget.setCurrentIndex(1)

            # Show relevant scroll area
            self.fuel_map_grid_scroll_area.show()

    def __export_fuel_map(self):

        user_settings = UserSettings()
        file_filter = 'Ascii GRID file (*' + ' *'.join(AsciiParser.FILE_EXT) + ')'
        file, filt = QFileDialog.getSaveFileName(self, 'Save File', user_settings.working_dir, file_filter)

        if file:

            if not file.endswith('.asc') or not file.endswith('.grd'):
                file += AsciiParser.FILE_EXT[0]

            self._fuel_map_editor.save(file)
            QMessageBox.information(self, "Export successful", "Fuel map successfully exported")

        else:
            return

    def import_environment(self):

        user_settings = UserSettings()

        # Open FileDialog in user's current working directory, with fds file filter
        file, file_filter = QFileDialog.getOpenFileName(self, 'Import Environment', user_settings.working_dir,
                                                        filter="fds (*.fds)")

        # TODO: actually import FDS file
        # TODO: if FDS file import is successful, modify current_env_label

        if file:
            self._fds.fds_file = file

            # Should not throw because the file is coming from UI,
            # but just in case
            try:

                self._fds.read()

            except FileNotFoundError as fnfe:
                self._fds.fds_file = None
                logger.log(logger.ERROR, str(fnfe))
                QMessageBox.information(self, "Import Not Successful", "Fds file {0} could not be found".format(file))
                return

            QMessageBox.information(self, 'Import successful', 'Environment imported successfully.')

    def run_simulation(self):

        if self.environment_present():
            logger.log(logger.INFO, 'Run simulation...')

            self.run_wfds()

        else:

            # FIXME: decide if should be warning, information or critical
            # NOTE: Since QMessageBox displays rich text, we can use markup and html to format output
            # NOTE: QMessageBox displays itself
            QMessageBox.information(self, 'No Environment Present',
                                    '<html>No Environment Present!<br>Please create or import an environment.</html>')

            # We do not care about return value of QMessageBox
            return

    def environment_present(self):
        return self._fds.file_present()

    def run_wfds(self):
        """This function runs wfds with the currently loaded environment"""

        # Get user's output directory
        user_settings = UserSettings()
        out_dir = os.path.abspath(user_settings.output_dir)

        # Get path to current fds file
        fds_filepath = self._fds.fds_file
        fds_fname = util.get_filename(fds_filepath)

        # Create a unique directory with same name as simulation
        out_dir += os.sep + fds_fname
        out_dir = util.make_unique_directory(out_dir)

        os.mkdir(out_dir)

        # Save the input file that was used to run the simulation
        save_fname = out_dir + os.sep + fds_fname
        self._fds.save(save_fname)

        logger.log(logger.INFO, 'Running simulation')

        # Clean up the output directory that was made if exception occurs
        try:

            self.execute_and_update(cmd=[self._fds_exec, fds_filepath], out_dir=out_dir)

        except Exception as e:
            logger.log(logger.ERROR, str(e))
            logger.log(logger.INFO, 'Cleaning up...')

            QMessageBox.warning(self, 'A problem occurred',
                                'There was a problem while running the simulation(s), please try again')

            # Remove files from directory
            for file in os.listdir(out_dir):
                os.remove(out_dir + os.sep + file)

            os.rmdir(out_dir)

            # Hide and reset progress bar
            self.hide_and_reset_progress()

    def run_smv(self):
        """This function runs smv with the currently loaded environment"""

        logger.log(logger.INFO, 'Viewing simulation')
        util.execute(cmd=[self.smv_exec, self.smv_file], cwd=None, out_file=None)

    # out_file not currently used, but may be later. So it is left in signature
    def execute_and_update(self, cmd, out_dir=None, out_file=sys.stdout):
        """Execute the given command and update the progress bar"""

        util.execute(cmd=cmd, cwd=out_dir, out_file=out_file)

        t_end = float(self._fds.sim_time())

        # Make progress bar visible
        self.progress_bar.show()

        # TODO: try catch until .out file is found

        # Give Wfds some time to spin up
        time.sleep(3)

        for line in follow(open(out_dir + os.sep + self._fds.job() + '.out', 'r')):

            line = line.replace(' ', '').replace('\n', '')

            # Break if we hit STOP because simulation is over
            if line.startswith('STOP'):
                break

            if line.startswith('Timestep'):
                timestep_kv, sim_time_kv = line.split(',')

                # Not currently used, could be later?
                timestep_int = timestep_kv.split(':')[1]
                sim_time_float = float(sim_time_kv.split(':')[1].replace('s', ''))

                # Figure out percentage and update progress bar
                loading = (sim_time_float / t_end) * 100
                self.progress_bar.setValue(loading)

        # TODO: could get pid from popen and check it or something here.
        # May also be useful to get pid for things such as killing if FireScape Rx is
        # terminated prematurely
        # If we reach here, simulation should be done.
        logger.log(logger.INFO, "Simulation complete")

        self.hide_and_reset_progress()
        QMessageBox.information(self, 'Simulation Complete', 'Simulation(s) completed.')

    def hide_and_reset_progress(self):

        # Hide progress bar and reset it
        self.progress_bar.hide()
        self.progress_bar.setValue(0)

    def setup_fuel_map_legend(self):

        colors = self._fuel_map_editor.colors()
        fuel_types = self._fuel_map_editor.fuel_types()

        assert len(colors) == len(fuel_types), "Length of colors != length of fuel_types"

        # Create the fuel map legend
        for i in range(len(colors)):
            legend_label = QLabel()
            legend_label.setText(fuel_types[i])
            self.fuel_type_grid_layout.addWidget(legend_label, i, 0)

            legend_label.setFixedSize(65, 20)

            g_view = QGraphicsView()

            pallete = g_view.palette()
            pallete.setColor(g_view.backgroundRole(), colors[i])
            g_view.setPalette(pallete)
            g_view.setMaximumSize(25, 10)

            self.fuel_type_grid_layout.addWidget(g_view, i, 1)

        self.scrollArea_3.setWidget(self.fuel_type_grid_layout_widget)

    def x_range_return_pressed(self):
        self.check_x_range()

    def y_range_return_pressed(self):
        self.check_y_range()

    def check_x_range(self):

        x_min = self.x_range_min_line_edit.text()
        x_max = self.x_range_max_line_edit.text()

        f_map_x_max = self._fuel_map_editor.f_map_x_max()
        f_map_x_min = self._fuel_map_editor.f_map_x_min()

        # Ensure the coordinates are within a valid range
        valid_range = self.check_range_input(x_min, x_max, f_map_x_min, f_map_x_max)

        if valid_range:

            column_numbers = self._fuel_map_editor.column_numbers()
            x_min = int(x_min)
            x_max = int(x_max)

            # Ensure the coordinates correspond to proper fuel map coordinates
            if x_min not in column_numbers or x_max not in column_numbers:
                QMessageBox.information(self, 'Non numeric range', 'At least one of the x range inputs not a valid fuel '
                                                                   'map coordinate<br>Please input a valid coordinate.')
                return False

            return True

        return False

    def check_y_range(self):

        y_min = self.y_range_min_line_edit.text()
        y_max = self.y_range_max_line_edit.text()

        f_map_y_max = self._fuel_map_editor.f_map_y_max()
        f_map_y_min = self._fuel_map_editor.f_map_y_min()

        # Ensure the coordinates are within a valid range
        valid_range = self.check_range_input(y_min, y_max, f_map_y_min, f_map_y_max)

        if valid_range:

            row_numbers = self._fuel_map_editor.row_numbers()
            y_min = int(y_min)
            y_max = int(y_max)

            # Ensure the coordinates correspond to proper fuel map coordinates
            if y_min not in row_numbers or y_max not in row_numbers:
                QMessageBox.information(self, 'Non numeric range', 'At least one of the y range inputs not a valid fuel '
                                                                   'map coordinate<br>Please input a valid coordinate.')
                return False

            return True

        return False

    def check_range_input(self, usr_min, usr_max, f_map_min, f_map_max):

        # Check if one of the inputs is empty
        if len(usr_min) == 0 or len(usr_max) == 0:
            return False

        # Ensure both of the inputs are valid numbers
        if not util.is_number(usr_min) or not util.is_number(usr_max):
            QMessageBox.information(self, 'Non numeric range', 'At least one of the range inputs is non-numeric'
                                                               '<br>Please input a numerical range.')
            return False

        usr_min = float(usr_min)
        usr_max = float(usr_max)

        # Ensure both of the inputs are integers(they should essentially be parts of a coordinate)
        if not usr_min.is_integer() or not usr_max.is_integer():
            QMessageBox.information(self, 'Non integer range', 'At least one of the range inputs is not an integer.'
                                                               '<br>Please input an integer range.')
            return False

        # Ensure the start of the range is not larger than the end
        if usr_min > usr_max:
            QMessageBox.information(self, 'Invalid range', 'The first range input cannot be larger than the second.'
                                                           '<br>Please input a valid range.')
            return False

        usr_min = int(usr_min)
        usr_max = int(usr_max)

        if usr_max > f_map_max or usr_min < f_map_min:
            QMessageBox.information(self, 'Invalid range', 'At least one of the range inputs is outside of the fuel map coordinates'
                                                           '<br>Please input a valid range.')
            return False

        return True


def follow(thefile):

    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            qApp.processEvents()  # Helps keep gui responsive
            time.sleep(0.1)
            continue
        yield line
