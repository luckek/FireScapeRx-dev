# NOTE:
# dem = digital elevation model
# fl = fuel
# smv = smokeview

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, qApp, QLabel, QGraphicsView, QWidget, QGridLayout, QDesktopWidget
from gui.Ui_MainWindow import Ui_MainWindow
from UserSettingsForm import UserSettingsForm, UserSettings
from AboutDialog import AboutDialog
from SimulationSettings import SimulationSettings
from SelectOutputFileTypesForm import SelectOutputFileTypesForm
from AsciiParser import AsciiParser
from FuelMapEditor import FuelMapEditor
from IgnitionPointEditor import IgnitionPointEditor
from Fds import Fds
from AsciiToFds import AsciiToFds
import os
import os.path as osp
import Utility as util
import sys
import logging as logger
import time


class MainWindow(QMainWindow, Ui_MainWindow):

    # Path to pre-packaged smv executable
    smv_exec = osp.join(osp.abspath(os.pardir), 'smokeview_linux_64')

    def __init__(self):

        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Center main application window
        util.center_window(self)

        # TODO: init editor with no file here
        # Create the fuel map editor variable
        self._fl_map_editor = None
        self._ign_pt_editor = None

        # Disable export of files until one is loaded
        self.action_export_fuel_map.setEnabled(False)
        self.action_export_dem.setEnabled(False)
        self.action_export_summary_file.setEnabled(False)
        self.action_export_environment.setEnabled(False)
        self.action_ascii_to_fds.setEnabled(False)

        self._fl_type_lgnd_tab.setEnabled(False)
        self.ignition_point_legend_tab.setEnabled(False)
        self._sim_settings_tab.setEnabled(False)

        self._tab_widget.currentChanged.connect(self.__tab_changed)

        # FIXME: re-enable when this gets implemented:
        self.action_import_summary_file.setEnabled(False)
        self.add_type_button.setEnabled(False)
        self.remove_type_button.setEnabled(False)
        self.action_create_environment.setEnabled(False)

        # Hide and reset progress bar
        self.__hide_and_reset_progress()

        # Setup validation for fuel map editor inputs
        self._x_rng_ign_pt_max_line_edit.returnPressed.connect(self.__x_rng_ret_pressed)
        self._x_rng_ign_pt_min_line_edit.returnPressed.connect(self.__x_rng_ret_pressed)

        self._y_rng_ign_pt_max_line_edit.returnPressed.connect(self.__y_rng_ret_pressed)
        self._y_rng_ign_pt_min_line_edit.returnPressed.connect(self.__y_rng_ret_pressed)

        self.modify_fuel_map_button.clicked.connect(self.__modify_fuel_map)
        self.modify_ign_points_button.clicked.connect(self.__modify_ignition_map)

        # Initialize fds object
        self._fds = Fds()
        self._fds_exec = self._fds.fds_exec

        # Setup and hide the fuel type legend grid
        self._fl_type_grid_layout_widget = QWidget(self)
        self._fl_type_grid_layout = QGridLayout(self._fl_type_grid_layout_widget)

        # HIDE THIS or it will cause problems with GUI (cant click on part of menu bar)
        self._fl_type_grid_layout_widget.hide()

        # Setup and hide the ignition point type legend grid
        self._ign_pt_type_grid_layout_widget = QWidget(self)
        self._ign_pt_type_grid_layout = QGridLayout(self._ign_pt_type_grid_layout_widget)
        self._ign_pt_type_grid_layout_widget.hide()

        # TODO: make use of this variable
        # Initialize selected output file types
        self._output_file_types = []

        # Initialize fds_file to be None
        self._smv_file = None

        sim_settings = SimulationSettings('default.sim_settings')

        # Initialize fields with simulation settings values
        self._num_sim_line_edit.setText(str(sim_settings.num_sims))
        self._sim_duration_line_edit.setText(str(sim_settings.sim_duration))
        self._wind_speed_line_edit.setText(str(sim_settings.wind_speed))
        self._wind_direction_line_edit.setText(str(sim_settings.wind_direction))

        for child in self._menu_bar.children():
            if type(child) is QtWidgets.QMenu:
                for action in child.actions():
                    # Use objectName as identifier so as to ensure uniqueness of identifier
                    identifier = action.objectName()
                    action.triggered.connect(lambda state, x=identifier: self.__handle_button(x))

    # FIXME: make static or remove from class altogether if we do not need to access anything in main window
    @QtCore.pyqtSlot(str)
    def __handle_button(self, identifier):

        dialog = None

        # FIXME: ignore identifiers that will not be handled

        if identifier == 'action_create_environment':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_ascii_to_fds':

            self.__ascii_to_fds()

        elif identifier == 'action_import_environment':
            self.__import_environment()
            return

        elif identifier == 'action_import_simulation':
            print(identifier, 'not implemented')
            return

        elif identifier == 'action_import_fuel_map':
            self.__import_fuel_map()
            return

        elif identifier == 'action_import_dem':
            self.__import_dem()
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
            self.__export_dem()
            return

        elif identifier == 'action_run_sim':
            # TODO: run simulation num_sims number of times
            self.__run_simulation()

        elif identifier == 'action_view_sim':

            user_settings = UserSettings()

            # Open FileDialog in user's current working directory, with smv file filter
            file, file_filter = QFileDialog.getOpenFileName(self, 'View Simulation', user_settings.working_dir,
                                                            filter="smv (*.smv)")

            if file:
                self._smv_file = file

            if self._smv_file is not None:
                logger.log(logger.INFO, 'Launching smokeview')
                self.__run_smv()

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

        x_min_str = self._x_rng_min_fl_line_edit.text()
        x_max_str = self._x_rng_max_fl_line_edit.text()

        y_min_str = self._y_rng_min_fl_line_edit.text()
        y_max_str = self._y_rng_max_fl_line_edit.text()

        # Ensure x and y range are valid
        if self.__check_fl_map_x_rng(x_min_str, x_max_str):
            if self.__check_fl_map_y_rng(y_min_str, y_max_str):
                print('valid coordinate range')

                x_min = int(x_min_str)
                x_max = int(x_max_str)

                y_min = int(y_min_str)
                y_max = int(y_max_str)

                fuel_type = self._fl_type_combo_box.currentIndex() + 1

                # Modify the fuel map
                self._fl_map_editor.modify_range(x_min, x_max, y_min, y_max, fuel_type)

    def __modify_ignition_map(self):

        x_min_str = self._x_rng_ign_pt_min_line_edit.text()
        x_max_str = self._x_rng_ign_pt_max_line_edit.text()

        y_min_str = self._y_rng_ign_pt_min_line_edit.text()
        y_max_str = self._y_rng_ign_pt_max_line_edit.text()

        # Ensure x and y range are valid
        if self.__check_ign_pt_x_rng(x_min_str, x_max_str):
            if self.__check_ign_pt_y_rng(y_min_str, y_max_str):
                print('valid coordinate range')

                x_min = int(x_min_str)
                x_max = int(x_max_str)

                y_min = int(y_min_str)
                y_max = int(y_max_str)

                ignition_type = self._ign_pt_combo_box.currentIndex()

                # Modify the fuel map
                self._ign_pt_editor.modify_range(x_min, x_max, y_min, y_max, ignition_type)

    def __import_fuel_map(self):

        user_settings = UserSettings()
        file_filter = 'Ascii file (*' + AsciiParser.FILE_EXT + ')'
        file, filt = QFileDialog.getOpenFileName(self, 'Open File', user_settings.working_dir, file_filter)

        if file:
            # FIXME: make two fixed size widgets or something for fuel map and ignition point editor, they now have own scroll area
            # FIXME: increase SIZE when there are lots of cells in fuel map and ignition

            if self._fl_map_editor:
                self._fl_map_editor.deleteLater()
                # self._fl_map_editor.hide()

            self._fl_map_editor = FuelMapEditor(self, file)
            self._fl_map_editor.setEnabled(True)

            self.__setup_fl_map_lgnd()

            # Enable relevant widgets
            self.action_export_fuel_map.setEnabled(True)

            # This means that a DEM has already been loaded,
            # so the user can now convert to FDS file
            if self._ign_pt_editor:
                self._sim_settings_tab.setEnabled(True)
                self.action_ascii_to_fds.setEnabled(True)

            # Set current tab to fuel type legend
            self._tab_widget.setCurrentIndex(1)

            # Tab index might not change, so __tab_changed will never get called
            self._fl_map_editor.show()

    def __export_fuel_map(self):

        user_settings = UserSettings()
        file_filter = 'Ascii file (*' + AsciiParser.FILE_EXT + ')'
        file, filt = QFileDialog.getSaveFileName(self, 'Save File', user_settings.working_dir, file_filter)

        if file:

            if not file.endswith('.asc'):
                file += AsciiParser.FILE_EXT

            self._fl_map_editor.save(file)
            QMessageBox.information(self, "Export successful", "Fuel map successfully exported")

    def __import_dem(self):

        user_settings = UserSettings()
        file_filter = 'Ascii file (*' + AsciiParser.FILE_EXT + ')'
        file, filt = QFileDialog.getOpenFileName(self, 'Open File', user_settings.working_dir, file_filter)

        if file:

            if self._ign_pt_editor:
                self._ign_pt_editor.deleteLater()

            self._ign_pt_editor = IgnitionPointEditor(self, file)
            self._ign_pt_editor.setEnabled(True)

            self._setup_ign_pt_map_lgnd()

            # Enable relevant widgets
            self.action_export_dem.setEnabled(True)

            # This means that a fuel map has already been loaded,
            # so the user can now convert to FDS file
            if self._fl_map_editor:
                self._sim_settings_tab.setEnabled(True)
                self.action_ascii_to_fds.setEnabled(True)

            # Set current tab to fuel type legend
            self._tab_widget.setCurrentIndex(2)
            self._ign_pt_editor.show()

    def __export_dem(self):

        user_settings = UserSettings()
        file_filter = 'Ascii file (*' + AsciiParser.FILE_EXT + ')'
        file, filt = QFileDialog.getSaveFileName(self, 'Save File', user_settings.working_dir, file_filter)

        if file:

            if not file.endswith('.asc'):
                file += AsciiParser.FILE_EXT

            self._ign_pt_editor.save(file)
            QMessageBox.information(self, "Export successful", "Digital elevation model successfully exported")

    @QtCore.pyqtSlot(int, name='__tab_changed')
    def __tab_changed(self, new_tab_index):

        if new_tab_index == 1 and self._tab_widget.widget(new_tab_index).isEnabled():

            if self._ign_pt_editor is not None:
                self._ign_pt_editor.hide()

            if self._fl_map_editor is not None:
                self._fl_map_editor.show()

        elif new_tab_index == 2 and self._tab_widget.widget(new_tab_index).isEnabled():

            if self._ign_pt_editor is not None:
                self._ign_pt_editor.show()

            if self._fl_map_editor is not None:
                self._fl_map_editor.hide()

    def __import_environment(self):

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

            self._sim_title_label.setText('Simulation Title: ' + self._fds.job_name())
            self._sim_settings_tab.setEnabled(True)
            QMessageBox.information(self, 'Import successful', 'Environment imported successfully.')

    def __run_simulation(self):

        if self.__environment_present():
            logger.log(logger.INFO, 'Run simulation...')

            self.__run_wfds()

        else:

            # FIXME: decide if should be warning, information or critical
            # NOTE: Since QMessageBox displays rich text, we can use markup and html to format output
            # NOTE: QMessageBox displays itself
            QMessageBox.information(self, 'No Environment Present',
                                    '<html>No Environment Present!<br>Please create or import an environment.</html>')

            # We do not care about return value of QMessageBox
            return

    def __environment_present(self):
        return self._fds.file_present()

    def __run_wfds(self):
        """This function runs wfds with the currently loaded environment"""

        # Get user's output directory
        user_settings = UserSettings()
        out_dir = osp.abspath(user_settings.output_dir)

        # Get path to current fds file
        fds_filepath = self._fds.fds_file
        fds_fname = util.get_filename(fds_filepath)

        # Create a unique directory with same name as simulation
        out_dir = osp.join(out_dir, fds_fname)
        out_dir = util.make_unique_directory(out_dir)

        os.mkdir(out_dir)

        # Save the input file that was used to run the simulation
        save_fname = osp.join(out_dir, fds_fname + Fds.file_ext())
        self._fds.save(save_fname)

        logger.log(logger.INFO, 'Running simulation')

        # Clean up the output directory that was made if exception occurs
        try:

            self.__execute_and_update(cmd=[self._fds_exec, fds_filepath], out_dir=out_dir)

        except Exception as e:
            logger.log(logger.ERROR, str(e))
            logger.log(logger.INFO, 'Cleaning up...')

            QMessageBox.warning(self, 'A problem occurred',
                                'There was a problem while running the simulation(s), please try again')

            # Remove files from directory
            for file in os.listdir(out_dir):
                os.remove(osp.join(out_dir, file))

            os.rmdir(out_dir)

            # Hide and reset progress bar
            self.__hide_and_reset_progress()

    def __run_smv(self):
        """This function runs smv with the currently loaded environment"""

        logger.log(logger.INFO, 'Viewing simulation')
        util.execute(cmd=[self.smv_exec, self._smv_file], cwd=None, out_file=None)

    # out_file not currently used, but may be later. So it is left in signature
    def __execute_and_update(self, cmd, out_dir=None, out_file=sys.stdout):
        """Execute the given command and update the progress bar"""

        util.execute(cmd=cmd, cwd=out_dir, out_file=out_file)

        t_end = float(self._fds.sim_time())

        # Make progress bar visible
        self._progress_bar.show()

        # We need to give WFDS some time to create the proper .out so that we may
        # read from it and update the progress bar.
        # Since everyone has different hardware, this seems to be the most sensible solution.
        # Could get caught in an infinite while loop if .out is never made, but we expect this file to be present
        # as part of WFDS' 'interface'

        wait = True
        while wait:

            try:
                out_file = osp.join(out_dir, self._fds.job() + '.out')
                for line in follow(open(out_file, 'r')):

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
                        self._progress_bar.setValue(loading)
                wait = False

            except FileNotFoundError:
                logger.log(logger.INFO, 'Sleep')
                qApp.processEvents()  # Helps keep gui responsive
                time.sleep(0.1)


        # TODO: could get pid from popen and check it or something here.
        # May also be useful to get pid for things such as killing if FireScape Rx is
        # terminated prematurely

        # If we reach here, simulation should be done.
        logger.log(logger.INFO, "Simulation complete")

        self._progress_bar.setValue(100)
        QMessageBox.information(self, 'Simulation Complete', 'Simulation(s) completed.')
        self.hide_and_reset_progress()

    def __hide_and_reset_progress(self):

        # Hide progress bar and reset it
        self._progress_bar.hide()
        self._progress_bar.setValue(0)

    def __setup_fl_map_lgnd(self):

        colors = self._fl_map_editor.colors()
        fuel_types = self._fl_map_editor.fuel_types()

        assert len(colors) == len(fuel_types), "Length of colors != length of fuel_types"

        # Create the fuel map legend
        for i in range(len(colors)):
            legend_label = QLabel()
            legend_label.setText(fuel_types[i])
            self._fl_type_grid_layout.addWidget(legend_label, i, 0)

            legend_label.setFixedSize(65, 20)

            g_view = QGraphicsView()

            pallete = g_view.palette()
            pallete.setColor(g_view.backgroundRole(), colors[i])
            g_view.setPalette(pallete)
            g_view.setMaximumSize(25, 10)

            self._fl_type_grid_layout.addWidget(g_view, i, 1)

        self._fl_type_lgnd_scroll_area.setWidget(self._fl_type_grid_layout_widget)
        self._fl_type_lgnd_tab.setEnabled(True)

    def _setup_ign_pt_map_lgnd(self):

        colors = self._ign_pt_editor.colors()
        fuel_types = self._ign_pt_editor.fuel_types()

        assert len(colors) == len(fuel_types), "Length of colors != length of fuel_types"

        # Create the fuel map legend
        for i in range(len(colors)):
            legend_label = QLabel()
            legend_label.setText(fuel_types[i])
            self._ign_pt_type_grid_layout.addWidget(legend_label, i, 0)

            legend_label.setFixedSize(65, 20)

            g_view = QGraphicsView()

            pallete = g_view.palette()
            pallete.setColor(g_view.backgroundRole(), colors[i])
            g_view.setPalette(pallete)
            g_view.setMaximumSize(25, 10)

            self._ign_pt_type_grid_layout.addWidget(g_view, i, 1)

        self.ignition_point_map_legend_scroll_area.setWidget(self._ign_pt_type_grid_layout_widget)
        self.ignition_point_legend_tab.setEnabled(True)

    def __x_rng_ret_pressed(self):
        self.__check_fl_map_x_rng()

    def __y_rng_ret_pressed(self):
        self.__check_fl_map_y_rng()

    def __check_fl_map_x_rng(self, usr_x_min, usr_x_max):

        f_map_x_max = self._fl_map_editor.grid_x_max()
        f_map_x_min = self._fl_map_editor.grid_x_min()

        # TODO: Move this into fuel map editor / ascii grid editor??
        # Ensure the coordinates are within a valid range
        valid_range = self.__check_rng_input(usr_x_min, usr_x_max, f_map_x_min, f_map_x_max)

        if valid_range:

            column_numbers = self._fl_map_editor.column_numbers()
            usr_x_min = int(usr_x_min)
            usr_x_max = int(usr_x_max)

            # Ensure the coordinates correspond to proper fuel map coordinates
            if usr_x_min not in column_numbers or usr_x_max not in column_numbers:
                QMessageBox.information(self, 'Non numeric range', 'At least one of the x range inputs not a valid fuel '
                                                                   'map coordinate<br>Please input a valid coordinate.')
                return False

            return True

        return False

    def __check_fl_map_y_rng(self, usr_y_min, usr_y_max):

        f_map_y_max = self._fl_map_editor.grid_y_max()
        f_map_y_min = self._fl_map_editor.grid_y_min()

        # Ensure the coordinates are within a valid range
        valid_range = self.__check_rng_input(usr_y_min, usr_y_max, f_map_y_min, f_map_y_max)

        if valid_range:

            row_numbers = self._fl_map_editor.row_numbers()
            usr_y_min = int(usr_y_min)
            usr_y_max = int(usr_y_max)

            # Ensure the coordinates correspond to proper fuel map coordinates
            if usr_y_min not in row_numbers or usr_y_max not in row_numbers:
                QMessageBox.information(self, 'Non numeric range', 'At least one of the y range inputs not a valid fuel '
                                                                   'map coordinate<br>Please input a valid coordinate.')
                return False

            return True

        return False

    def __check_ign_pt_x_rng(self, usr_x_min, usr_x_max):

        ign_pt_x_min = self._ign_pt_editor.grid_x_min()
        ign_pt_x_max = self._ign_pt_editor.grid_x_max()

        # TODO: Move this into fuel map editor / ascii grid editor??
        # Ensure the coordinates are within a valid range
        valid_range = self.__check_rng_input(usr_x_min, usr_x_max, ign_pt_x_min, ign_pt_x_max)

        if valid_range:

            column_numbers = self._ign_pt_editor.column_numbers()
            usr_x_min = int(usr_x_min)
            usr_x_max = int(usr_x_max)

            # Ensure the coordinates correspond to proper fuel map coordinates
            if usr_x_min not in column_numbers or usr_x_max not in column_numbers:
                QMessageBox.information(self, 'Non numeric range',
                                        'At least one of the x range inputs not a valid fuel '
                                        'map coordinate<br>Please input a valid coordinate.')
                return False

            return True

        return False

    def __check_ign_pt_y_rng(self, usr_y_min, usr_y_max):

        ign_pt_y_min = self._ign_pt_editor.grid_y_min()
        ign_pt_y_max = self._ign_pt_editor.grid_y_max()

        # Ensure the coordinates are within a valid range
        valid_range = self.__check_rng_input(usr_y_min, usr_y_max, ign_pt_y_min, ign_pt_y_max)

        if valid_range:

            row_numbers = self._ign_pt_editor.row_numbers()
            usr_y_min = int(usr_y_min)
            usr_y_max = int(usr_y_max)

            # Ensure the coordinates correspond to proper fuel map coordinates
            if usr_y_min not in row_numbers or usr_y_max not in row_numbers:
                QMessageBox.information(self, 'Non numeric range',
                                        'At least one of the y range inputs not a valid fuel '
                                        'map coordinate<br>Please input a valid coordinate.')
                return False

            return True

        return False

    def __check_rng_input(self, usr_min, usr_max, f_map_min, f_map_max):

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

    def __ascii_to_fds(self):

        # Note: normally, this would be dangerous as
        # either of these could be None, but since the user
        # cannot access this function until both are loaded

        # TODO: ensure that DEM and fuel map are both same size
        # idea: user cannot load fuel map that is not same size as DEM and vice versa
        fl_map_parser = self._fl_map_editor.parser()
        dem_parser = self._ign_pt_editor.parser()

        sim_settings = SimulationSettings('default.sim_settings')

        ascii_fds_converter = AsciiToFds(fl_map_parser, dem_parser, sim_settings)
        ascii_fds_converter.save(self._fl_map_editor.button_values_grid())


def follow(thefile):

    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            qApp.processEvents()  # Helps keep gui responsive
            time.sleep(0.1)
            continue
        yield line
