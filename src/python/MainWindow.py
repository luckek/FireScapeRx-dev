# NOTE:
# dem = digital elevation model
# fl = fuel
# smv = smokeview

import logging as logger
import os
import os.path as osp
import sys
import time

from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, qApp, QLabel, QGraphicsView, QWidget, QGridLayout
from PyQt5.QtCore import Qt

import Utility as util
from AboutDialog import AboutDialog
from AsciiParser import AsciiParser
from AsciiToFds import AsciiToFds
from Fds import Fds
from FuelMapEditor import FuelMapEditor
from IgnitionPointEditor import IgnitionPointEditor
from SelectOutputFileTypesForm import SelectOutputFileTypesForm
from SimulationSettings import SimulationSettings
from UserSettingsForm import UserSettingsForm, UserSettings
from gui.Ui_MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import QWidget, QLabel


class MainWindow(QMainWindow, Ui_MainWindow):

    # Path to pre-packaged smv executable
    smv_exec = osp.join(osp.abspath(os.pardir), 'smokeview_linux_64')

    def __init__(self):

        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Center main application window
        util.center_window(self)

        # TODO: init editor with no file here?
        # Create the fuel map editor variable
        self._fl_map_editor = None
        self._ign_pt_editor = None

        # Disable export of files until one is loaded
        self.action_export_fuel_map.setEnabled(False)
        self.action_export_dem.setEnabled(False)
        self.action_export_summary_file.setEnabled(False)
        self.action_export_environment.setEnabled(False)

        self._fl_type_lgnd_tab.setEnabled(False)
        self.ignition_point_legend_tab.setEnabled(False)
        self._sim_settings_tab.setEnabled(False)

        self._tab_widget.currentChanged.connect(self.__tab_changed)

        # FIXME: re-enable when this gets implemented:
        self.action_import_summary_file.setEnabled(False)
        self.action_create_environment.setEnabled(False)

        # Hide and reset progress bar
        self.__hide_and_reset_progress()

        # TODO: we might not need this since we check on button press
        # Setup validation for fuel map editor inputs
        # self._x_rng_min_fl_line_edit.returnPressed.connect(self.__x_rng_ret_pressed())
        # self._x_rng_max_fl_line_edit.returnPressed.connect(self.__x_rng_ret_pressed())

        # self._y_rng_min_fl_line_edit.returnPressed.connect(self.__y_rng_ret_pressed())
        # self._y_rng_max_fl_line_edit.returnPressed.connect(self.__y_rng_ret_pressed())

        self.modify_fuel_map_button.clicked.connect(self.__modify_fuel_map)
        self.modify_ign_pts_button.clicked.connect(self.__modify_ignition_map)

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

        for child in self._menu_bar.children():
            if type(child) is QtWidgets.QMenu:
                for action in child.actions():
                    # Use objectName as identifier so as to ensure uniqueness of identifier
                    identifier = action.objectName()
                    action.triggered.connect(lambda state, x=identifier: self.__handle_button(x))

    @QtCore.pyqtSlot(str)
    def __handle_button(self, identifier):

        dialog = None

        # FIXME: ignore identifiers that will not be handled

        if identifier == 'action_create_environment':
            self.__ascii_to_fds()
            return

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
            print('UNRECOGNIZED IDENTIFIER:', identifier)
            return

        if dialog is not None:
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

        axis = self._ign_pt_axis_combo_box.currentText()

        usr_min_str = self._ign_pt_rng_min_line_edit.text()
        usr_max_str = self._ign_pt_rng_max_line_edit.text()

        row_col_str = self._ign_pt_row_col_line_edit.text()

        t_start_str = self._ign_pt_t_start_line_edit.text()
        t_end_str = self._ign_pt_t_end_line_edit.text()

        # check time here b/c it is common to both cases
        if self.__validate_ign_pt_t_range(t_start_str, t_end_str):

            t_start = float(t_start_str)
            t_end = float(t_end_str)

            if axis == 'Horizontal':

                if self.__check_ign_pt_x_rng(usr_min_str, usr_max_str):

                    # TODO: make a check row / check col function to speed this up a bit
                    # And give more informative user feedback
                    if self.__check_ign_pt_y_rng(row_col_str, row_col_str):

                        x_min = int(usr_min_str)
                        x_max = int(usr_max_str)

                        y_min = int(row_col_str)
                        y_max = int(row_col_str)

                        ignition_type = self._ign_pt_add_rm_combo_box.currentIndex()

                        # Modify the ignition points
                        if self._ign_pt_editor.modify_range(x_min, x_max, y_min, y_max, t_start, t_end, ignition_type) is 'OVERLAP':
                            QMessageBox.information(self, "Overlapping Fire Lines", "Fire Lines may not overlap. If you "
                                                                                    "prefer this line, please delete the "
                                                                                    "old one")

            elif axis == 'Vertical':

                if self.__check_ign_pt_y_rng(usr_min_str, usr_max_str):

                    # TODO: could probably make a check row / check col function to speed this up a bit
                    if self.__check_ign_pt_x_rng(row_col_str, row_col_str):

                        x_min = int(row_col_str)
                        x_max = int(row_col_str)

                        y_min = int(usr_min_str)
                        y_max = int(usr_max_str)

                        ignition_type = self._ign_pt_add_rm_combo_box.currentIndex()

                        # Modify the ignition points
                        if self._ign_pt_editor.modify_range(x_min, x_max, y_min, y_max, t_start, t_end, ignition_type) is 'OVERLAP':
                            QMessageBox.information(self, "Overlapping Fire Lines",
                                                    "Fire Lines may not overlap. If you "
                                                    "prefer this line, please delete the "
                                                    "old one")

    def __import_fuel_map(self):

        user_settings = UserSettings()
        file_filter = 'Ascii file (*' + AsciiParser.FILE_EXT + ')'
        file, filt = QFileDialog.getOpenFileName(self, 'Open File', user_settings.working_dir, file_filter)

        if file:
            # FIXME: make two fixed size widgets or something for fuel map and ignition point editor, they now have own scroll area
            # FIXME: increase SIZE when there are lots of cells in fuel map and ignition

            qApp.setOverrideCursor(Qt.WaitCursor)

            try:
                new_editor = FuelMapEditor(self, file)

            except IndexError:

                qApp.restoreOverrideCursor()
                QMessageBox.information(self, "Invalid file", "A problem occurred while loading the fuel map. Please "
                                                              "verify that the fuel map does not contain non-integer "
                                                              "numbers")
                return

            if self._fl_map_editor:
                self._fl_map_editor.deleteLater()

            self._fl_map_editor = new_editor

            self._fl_map_editor.setEnabled(True)

            self.__setup_fl_map_lgnd()

            # Enable relevant widgets
            self.action_export_fuel_map.setEnabled(True)

            # This means that a DEM has already been loaded,
            # so the user can now convert to FDS file
            if self._ign_pt_editor:
                self.__init_sim_settings()
                self.action_create_environment.setEnabled(True)

            # Set current tab to fuel type legend
            self._tab_widget.setCurrentIndex(1)

            # Tab index might not change, so __tab_changed will never get called
            self._fl_map_editor.show()
            qApp.restoreOverrideCursor()

            QMessageBox.information(self, "Import successful", "Fuel Map successfully imported.")

    def __export_fuel_map(self):

        user_settings = UserSettings()
        file_filter = 'Ascii file (*' + AsciiParser.FILE_EXT + ')'
        file, filt = QFileDialog.getSaveFileName(self, 'Save File', user_settings.working_dir, file_filter)

        if file:

            qApp.setOverrideCursor(Qt.WaitCursor)

            if not file.endswith(AsciiParser.FILE_EXT):
                file += AsciiParser.FILE_EXT

            self._fl_map_editor.save(file, False)
            qApp.restoreOverrideCursor()

            QMessageBox.information(self, "Export successful", "Fuel map successfully exported")

    def __import_dem(self):

        user_settings = UserSettings()
        file_filter = 'Ascii file (*' + AsciiParser.FILE_EXT + ')'
        file, filt = QFileDialog.getOpenFileName(self, 'Open File', user_settings.working_dir, file_filter)

        if file:

            qApp.setOverrideCursor(Qt.WaitCursor)

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
                self.__init_sim_settings()
                self.action_create_environment.setEnabled(True)

            # Set current tab to fuel type legend
            self._tab_widget.setCurrentIndex(2)

            self._ign_pt_editor.show()
            qApp.restoreOverrideCursor()

            QMessageBox.information(self, "Import successful", "Digital Elevation Model successfully imported.")

    def __export_dem(self):

        user_settings = UserSettings()
        file_filter = 'Ascii file (*' + AsciiParser.FILE_EXT + ')'
        file, filt = QFileDialog.getSaveFileName(self, 'Save File', user_settings.working_dir, file_filter)

        if file:

            qApp.setOverrideCursor(Qt.WaitCursor)

            if not file.endswith(AsciiParser.FILE_EXT):
                file += AsciiParser.FILE_EXT

            self._ign_pt_editor.save(file, False)
            qApp.restoreOverrideCursor()
            QMessageBox.information(self, "Export successful", "Digital elevation model successfully exported")

    def __init_sim_settings(self):

        if not self._sim_settings_tab.isEnabled():

            self._sim_settings_tab.setEnabled(True)

            sim_settings = SimulationSettings('default.sim_settings')

            # Initialize fields with simulation settings values
            self._sim_duration_line_edit.setText(str(sim_settings.sim_duration))
            self._wind_speed_line_edit.setText(str(sim_settings.wind_speed))
            self._wind_direction_line_edit.setText(str(sim_settings.wind_direction))
            self._ambient_temp_line_edit.setText(str(sim_settings.ambient_temp))

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

        if file:
            self._fds.fds_file = file

            # Should not throw because the file is coming from UI,
            # but just in case
            try:

                read_success = self._fds.read()

            except FileNotFoundError as fnfe:
                self._fds.fds_file = None
                logger.log(logger.ERROR, str(fnfe))
                QMessageBox.information(self, "Import Not Successful", "Fds file {0} could not be found".format(file))
                return

            if read_success:

                self._sim_title_label.setText('Simulation Title: ' + self._fds.job_name())
                QMessageBox.information(self, 'Import successful', 'Environment imported successfully.')

            else:
                QMessageBox.information(self, 'Import not successful', 'FDS file is improperly formatted and could not be imported.')
                self._fds.fds_file = None

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

        qApp.setOverrideCursor(Qt.WaitCursor)

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

        #TODO: Determine alternate save method or remove export fds file
        # Save the input file that was used to run the simulation
        #save_fname = osp.join(out_dir, fds_fname + Fds.file_ext())
        #self._fds.save(save_fname)

        logger.log(logger.INFO, 'Running simulation')

        # Clean up the output directory that was made if exception occurs
        try:

            self.__execute_and_update(cmd=[self._fds_exec, fds_filepath], out_dir=out_dir)

        except Exception as e:
            logger.log(logger.ERROR, str(e))
            logger.log(logger.INFO, 'Cleaning up...')

            qApp.restoreOverrideCursor()

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

        # TODO: kill this when done...
        fds_pid = util.execute(cmd=cmd, cwd=out_dir, out_file=out_file)

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

        qApp.restoreOverrideCursor()
        QMessageBox.information(self, 'Simulation Complete', 'Simulation completed.')

        self.__hide_and_reset_progress()

    def __hide_and_reset_progress(self):

        # Hide progress bar and reset it
        self._progress_bar.hide()
        self._progress_bar.setValue(0)

    def __setup_fl_map_lgnd(self):

        colors = self._fl_map_editor.colors()
        fuel_types = self._fl_map_editor.fuel_types()

        assert len(colors) == len(fuel_types), "Length of colors != length of fuel_types"

        # Create the fuel map legend
        res_label = QLabel()
        res_label.setText('Resolution')
        res_label.setFixedSize(65, 20)

        self._fl_type_grid_layout.addWidget(res_label, 0, 0)

        res = QLabel()
        res.setText(str(self._fl_map_editor.resolution()) + 'm')
        res.setMaximumSize(35, 10)

        self._fl_type_grid_layout.addWidget(res, 0, 1)

        for i in range(len(colors)):
            legend_label = QLabel()
            legend_label.setText(fuel_types[i])
            self._fl_type_grid_layout.addWidget(legend_label, i + 1, 0)

            legend_label.setFixedSize(65, 20)

            g_view = QGraphicsView()

            pallete = g_view.palette()
            pallete.setColor(g_view.backgroundRole(), colors[i])
            g_view.setPalette(pallete)
            g_view.setMaximumSize(25, 10)

            self._fl_type_grid_layout.addWidget(g_view, i + 1, 1)

        self._fl_type_lgnd_scroll_area.setWidget(self._fl_type_grid_layout_widget)
        self._fl_type_lgnd_tab.setEnabled(True)

    def _setup_ign_pt_map_lgnd(self):

        colors = self._ign_pt_editor.colors()
        fuel_types = self._ign_pt_editor.fuel_types()

        assert len(colors) == len(fuel_types), "Length of colors != length of fuel_types"

        # Create the ignition point legend
        res_label = QLabel()
        res_label.setText('Resolution')
        res_label.setFixedSize(65, 20)

        self._ign_pt_type_grid_layout.addWidget(res_label, 0, 0)

        res = QLabel()
        res.setText(str(self._ign_pt_editor.resolution()) + 'm')
        res.setMaximumSize(35, 10)

        self._ign_pt_type_grid_layout.addWidget(res, 0, 1)

        for i in range(len(colors)):
            legend_label = QLabel()
            legend_label.setText(fuel_types[i])
            self._ign_pt_type_grid_layout.addWidget(legend_label, i + 1, 0)

            legend_label.setFixedSize(65, 20)

            g_view = QGraphicsView()

            pallete = g_view.palette()
            pallete.setColor(g_view.backgroundRole(), colors[i])
            g_view.setPalette(pallete)
            g_view.setMaximumSize(25, 10)

            self._ign_pt_type_grid_layout.addWidget(g_view, i + 1, 1)

        self.ignition_point_map_legend_scroll_area.setWidget(self._ign_pt_type_grid_layout_widget)
        self.ignition_point_legend_tab.setEnabled(True)

    def __x_rng_ret_pressed(self):

        usr_x_min = self._x_rng_min_fl_line_edit.text()
        usr_x_max = self._x_rng_max_fl_line_edit.text()

        self.__check_fl_map_x_rng(usr_x_min, usr_x_max)

    def __y_rng_ret_pressed(self):

        usr_y_min = self._y_rng_min_fl_line_edit.text()
        usr_y_max = self._y_rng_max_fl_line_edit.text()

        self.__check_fl_map_y_rng(usr_y_min, usr_y_max)

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

    def __validate_ign_pt_t_range(self, t_start, t_end):

        # Check if one of the inputs is empty
        if len(t_start) == 0 or len(t_end) == 0:
            return False

        # Ensure both of the inputs are valid numbers
        if not util.is_number(t_start) or not util.is_number(t_end):
            QMessageBox.information(self, 'Non numeric range', 'At least one of the time range inputs is non-numeric'
                                                               '<br>Please input a numerical range.')
            return False

        usr_min = float(t_start)
        usr_max = float(t_end)

        # Ensure the start of the range is not larger than the end
        if usr_min > usr_max:
            QMessageBox.information(self, 'Invalid range', 'The first time range input cannot be larger than the second.'
                                                           '<br>Please input a valid time range.')
            return False

        if usr_min < 0:
            QMessageBox.information(self, 'Negative Time Value',
                                    'Time Start is negative. Please enter a valid start time')

        return True

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

    def __check_sim_time(self):

        sim_time = self._sim_duration_line_edit.text()

        if not util.is_number(sim_time):
            QMessageBox.information(self, "Invalid number",
                                    "Simulation duration is not a number. Please enter a positive decimal number")

            return False

        sim_time = float(sim_time)

        if sim_time < 0:
            QMessageBox.information(self, "Invalid number",
                                    "Simulation duration must be a positive decimal number.")

            return False

        return True

    def __check_ambient_temp(self):

        ambient_temp = self._ambient_temp_line_edit.text()

        if not util.is_number(ambient_temp):
            QMessageBox.information(self, "Invalid number",
                                    "Ambient temperature is not a number. Please enter a valid temperature")

            return False

        ambient_temp = float(ambient_temp)

        if ambient_temp <= -459.67:

            QMessageBox.information(self, "Invalid number",
                                    "Ambient temperature must be above absolute zero. "
                                    "Please enter a temperature above -457.67F")

            return False

        return True

    def __check_wind(self):

        wind_speed = self._wind_speed_line_edit.text()
        wind_dir = self._wind_direction_line_edit.text()

        if not wind_speed or not wind_dir:
            QMessageBox.information(self, "Blank Field",
                                    "At least one of wind speed or wind direction is empty. "
                                    "Please provide a valid value")

        if not util.is_number(wind_speed) or not util.is_number(wind_dir):
            QMessageBox.information(self, "Invalid number",
                                    "At least one of wind speed or wind direction is not a valid number. "
                                    "Please enter a valid number")

            return False

        wind_speed = float(wind_speed)
        wind_dir = float(wind_dir)

        if wind_dir < 0.0 or wind_dir > 360.0:
            QMessageBox.information(self, "Invalid wind direction",
                                    "Wind direction must be between 0 and 360. "
                                    "Please enter a valid wind direction")

            return False

        if wind_speed < 0.0:
            QMessageBox.information(self, "Invalid wind speed",
                                    "Wind speed must be positive. "
                                    "Please enter a valid wind speed")

            return False

        return True

    def __ascii_to_fds(self):

        if self.__check_wind():
            # Note: normally, this would be dangerous as
            # either of these could be None, but since the user
            # cannot access this function until both are loaded

            # TODO: ensure that DEM and fuel map are both same size
            # idea: user cannot load fuel map that is not same size as DEM and vice versa
            if self.__check_ambient_temp():
                if self.__check_sim_time():

                    # Get user's working directory
                    user_settings = UserSettings()
                    file, filt = QFileDialog.getSaveFileName(self, 'Save File', user_settings.working_dir, "fds (*.fds)")

                    if file:

                        if not file.endswith(Fds.file_ext()):
                            file += Fds.file_ext()

                        # Note: Logically, this is where we would ensure that all of the fire line times
                        # are less than the simulation duration, however WFDS does not care weather or not such
                        # ignition points are present, hence we do not entirely care either.
                        fl_map_parser = self._fl_map_editor.parser()
                        dem_parser = self._ign_pt_editor.parser()

                        orig_xll = fl_map_parser.xllcorner
                        orig_yll = fl_map_parser.yllcorner

                        # TODO: fix this
                        # Hack to ensure WFDS domain starts at zero
                        fl_map_parser.xllcorner = 0
                        fl_map_parser.yllcorner = 0

                        sim_time = float(self._sim_duration_line_edit.text())
                        ambient_temp = util.fahrenheit_to_celsius(float(self._ambient_temp_line_edit.text()))

                        wind_speed = util.mph_to_ms(float(self._wind_speed_line_edit.text()))
                        wind_direction = util.met_to_vect(float(self._wind_direction_line_edit.text()))

                        sim_settings = SimulationSettings('default.sim_settings')

                        sim_settings.sim_duration = sim_time
                        sim_settings.ambient_temp = ambient_temp
                        sim_settings.wind_speed = wind_speed
                        sim_settings.wind_direction = wind_direction

                        ascii_fds_converter = AsciiToFds(fl_map_parser, dem_parser, sim_settings)
                        save_success = ascii_fds_converter.save(self._fl_map_editor.button_values_grid(), self._ign_pt_editor.fire_lines(), file)

                        # Hack to ensure WFDS domain starts at zero
                        fl_map_parser.xllcorner = orig_xll
                        fl_map_parser.yllcorner = orig_yll

                        if save_success:

                            usr_reply = QMessageBox.question(self, "Export successful", "Environment successfully created. "
                                                             "Would you like to set it as the current environment?",
                                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

                            if usr_reply == QMessageBox.Yes:

                                self._fds.fds_file = file
                                self._fds.read()

                                self._sim_title_label.setText('Simulation Title: ' + self._fds.job_name())


def follow(thefile):

    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            qApp.processEvents()  # Helps keep gui responsive
            time.sleep(0.1)
            continue
        yield line
