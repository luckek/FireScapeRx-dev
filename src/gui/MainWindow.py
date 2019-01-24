# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from .UserSettingsForm import *

class MainWindow(object):
    def setupUi(self, MainWindow):

        # ---- Begin generated code
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(932, 600)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 191, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setObjectName("horizontal_layout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacerItem)
        self.current_env_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.current_env_label.setObjectName("current_env_label")
        self.horizontal_layout.addWidget(self.current_env_label)
        self.scroll_area = QtWidgets.QScrollArea(self.central_widget)
        self.scroll_area.setGeometry(QtCore.QRect(590, 0, 341, 561))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_widget_contents = QtWidgets.QWidget()
        self.scroll_area_widget_contents.setGeometry(QtCore.QRect(0, 0, 339, 559))
        self.scroll_area_widget_contents.setObjectName("scroll_area_widget_contents")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scroll_area_widget_contents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 341, 441))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vertical_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setObjectName("vertical_layout")
        self.sim_settings_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.sim_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sim_settings_label.setObjectName("sim_settings_label")
        self.vertical_layout.addWidget(self.sim_settings_label)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.vertical_layout.addWidget(self.line_4)
        self.sim_settings_form_layout = QtWidgets.QFormLayout()
        self.sim_settings_form_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.sim_settings_form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.sim_settings_form_layout.setContentsMargins(10, 5, 10, 5)
        self.sim_settings_form_layout.setVerticalSpacing(10)
        self.sim_settings_form_layout.setObjectName("sim_settings_form_layout")
        self.num_sim_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.num_sim_label.setAlignment(QtCore.Qt.AlignCenter)
        self.num_sim_label.setObjectName("num_sim_label")
        self.sim_settings_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.num_sim_label)
        self.num_sim_line_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.num_sim_line_edit.setObjectName("num_sim_line_edit")
        self.sim_settings_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.num_sim_line_edit)
        self.sim_duration_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.sim_duration_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sim_duration_label.setObjectName("sim_duration_label")
        self.sim_settings_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.sim_duration_label)
        self.sim_duration_line_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.sim_duration_line_edit.setObjectName("sim_duration_line_edit")
        self.sim_settings_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sim_duration_line_edit)
        self.vertical_layout.addLayout(self.sim_settings_form_layout)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.vertical_layout.addWidget(self.line_3)
        self.wind_settings_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.wind_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wind_settings_label.setObjectName("wind_settings_label")
        self.vertical_layout.addWidget(self.wind_settings_label)
        self.line_6 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.vertical_layout.addWidget(self.line_6)
        self.wind_form_layout = QtWidgets.QFormLayout()
        self.wind_form_layout.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.wind_form_layout.setContentsMargins(10, 5, 10, 5)
        self.wind_form_layout.setHorizontalSpacing(60)
        self.wind_form_layout.setVerticalSpacing(10)
        self.wind_form_layout.setObjectName("wind_form_layout")
        self.wind_speed_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.wind_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wind_speed_label.setObjectName("wind_speed_label")
        self.wind_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.wind_speed_label)
        self.wind_speed_line_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.wind_speed_line_edit.setObjectName("wind_speed_line_edit")
        self.wind_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.wind_speed_line_edit)
        self.wind_direction_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.wind_direction_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wind_direction_label.setObjectName("wind_direction_label")
        self.wind_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.wind_direction_label)
        self.wind_direction_line_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.wind_direction_line_edit.setObjectName("wind_direction_line_edit")
        self.wind_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.wind_direction_line_edit)
        self.vertical_layout.addLayout(self.wind_form_layout)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vertical_layout.addWidget(self.line)
        self.init_conditions_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.init_conditions_label.setAlignment(QtCore.Qt.AlignCenter)
        self.init_conditions_label.setObjectName("init_conditions_label")
        self.vertical_layout.addWidget(self.init_conditions_label)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.vertical_layout.addWidget(self.line_5)
        self.form_layout_3 = QtWidgets.QFormLayout()
        self.form_layout_3.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.form_layout_3.setContentsMargins(10, 5, 10, 5)
        self.form_layout_3.setHorizontalSpacing(60)
        self.form_layout_3.setVerticalSpacing(10)
        self.form_layout_3.setObjectName("form_layout_3")
        self.initialFireIntensity_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.initialFireIntensity_label.setAlignment(QtCore.Qt.AlignCenter)
        self.initialFireIntensity_label.setObjectName("initialFireIntensity_label")
        self.form_layout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.initialFireIntensity_label)
        self.initialFireIntensityLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.initialFireIntensityLineEdit.setObjectName("initialFireIntensityLineEdit")
        self.form_layout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.initialFireIntensityLineEdit)
        self.ingnitionStartTime_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ingnitionStartTime_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ingnitionStartTime_label.setObjectName("ingnitionStartTime_label")
        self.form_layout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.ingnitionStartTime_label)
        self.ignitionStartTime_line_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ignitionStartTime_line_edit.setObjectName("ignitionStartTime_line_edit")
        self.form_layout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ignitionStartTime_line_edit)
        self.vertical_layout.addLayout(self.form_layout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vertical_layout.addItem(spacerItem1)
        self.modify_fuel_map = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.modify_fuel_map.setObjectName("modify_fuel_map")
        self.vertical_layout.addWidget(self.modify_fuel_map)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 932, 20))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_import = QtWidgets.QMenu(self.menubar)
        self.menu_import.setObjectName("menu_import")
        self.menu_export = QtWidgets.QMenu(self.menubar)
        self.menu_export.setObjectName("menu_export")
        self.menu_settings = QtWidgets.QMenu(self.menubar)
        self.menu_settings.setObjectName("menu_settings")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        self.menu_simulation = QtWidgets.QMenu(self.menubar)
        self.menu_simulation.setObjectName("menu_simulation")
        MainWindow.setMenuBar(self.menubar)
        self.current_env = QtWidgets.QStatusBar(MainWindow)
        self.current_env.setObjectName("current_env")
        MainWindow.setStatusBar(self.current_env)
        self.action_create_environment = QtWidgets.QAction(MainWindow)
        self.action_create_environment.setObjectName("action_create_environment")
        self.action_import_environment = QtWidgets.QAction(MainWindow)
        self.action_import_environment.setObjectName("action_import_environment")
        self.action_Initial_Conditions = QtWidgets.QAction(MainWindow)
        self.action_Initial_Conditions.setObjectName("action_Initial_Conditions")
        self.actionWind = QtWidgets.QAction(MainWindow)
        self.actionWind.setObjectName("actionWind")
        self.actionFuel_Map = QtWidgets.QAction(MainWindow)
        self.actionFuel_Map.setObjectName("actionFuel_Map")
        self.action_export_simulation = QtWidgets.QAction(MainWindow)
        self.action_export_simulation.setObjectName("action_export_simulation")
        self.action_export_summary_file = QtWidgets.QAction(MainWindow)
        self.action_export_summary_file.setObjectName("action_export_summary_file")
        self.action_export_environment = QtWidgets.QAction(MainWindow)
        self.action_export_environment.setObjectName("action_export_environment")
        self.action_import_simulation = QtWidgets.QAction(MainWindow)
        self.action_import_simulation.setObjectName("action_import_simulation")
        self.action_import_summary_file = QtWidgets.QAction(MainWindow)
        self.action_import_summary_file.setObjectName("action_import_summary_file")
        self.actionWorking_Directory = QtWidgets.QAction(MainWindow)
        self.actionWorking_Directory.setObjectName("actionWorking_Directory")
        self.actionOutput_Directory = QtWidgets.QAction(MainWindow)
        self.actionOutput_Directory.setObjectName("actionOutput_Directory")
        self.actionDefault_Simulation_Duration = QtWidgets.QAction(MainWindow)
        self.actionDefault_Simulation_Duration.setObjectName("actionDefault_Simulation_Duration")
        self.actionSimulation_Runs = QtWidgets.QAction(MainWindow)
        self.actionSimulation_Runs.setObjectName("actionSimulation_Runs")
        self.action_select_output_files = QtWidgets.QAction(MainWindow)
        self.action_select_output_files.setObjectName("action_select_output_files")
        self.action_run_sim = QtWidgets.QAction(MainWindow)
        self.action_run_sim.setObjectName("action_run_sim")
        self.action_view_sim = QtWidgets.QAction(MainWindow)
        self.action_view_sim.setObjectName("action_view_sim")
        self.action_user_settings = QtWidgets.QAction(MainWindow)
        self.action_user_settings.setObjectName("action_user_settings")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menu_file.addAction(self.action_create_environment)
        self.menu_import.addAction(self.action_import_environment)
        self.menu_import.addAction(self.action_import_simulation)
        self.menu_import.addAction(self.action_import_summary_file)
        self.menu_export.addAction(self.action_export_environment)
        self.menu_export.addAction(self.action_export_simulation)
        self.menu_export.addAction(self.action_export_summary_file)
        self.menu_settings.addAction(self.action_user_settings)
        self.menu_settings.addAction(self.action_select_output_files)
        self.menu_help.addAction(self.action_about)
        self.menu_simulation.addAction(self.action_run_sim)
        self.menu_simulation.addAction(self.action_view_sim)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_import.menuAction())
        self.menubar.addAction(self.menu_export.menuAction())
        self.menubar.addAction(self.menu_simulation.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        # ---- End generated code

        # Create mapper
        self.mapper = QtCore.QSignalMapper(MainWindow)

        # NOTE: this has to be done after retranslateUi otherwise the text is not set
        for child in self.menubar.children():
            if type(child) is QtWidgets.QMenu:
                for action in child.actions():
                    # This line maps an action to a string
                    self.mapper.setMapping(action, action.text())

                    # Connect the action's signal to the mapper
                    action.triggered.connect(self.mapper.map)

        # Connect the mapper to the button
        self.mapper.mapped['QString'].connect(self.handle_button)
        self.mapper.mapped['QString'].connect(self.handle_file_button)

        # ---- Begin generated code
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # ---- End generated code

    # ---- Generated function
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.current_env_label.setText(_translate("MainWindow", "Current Environment: "))
        self.sim_settings_label.setText(_translate("MainWindow", "Simulation Settings"))
        self.num_sim_label.setText(_translate("MainWindow", "Number of Simulations"))
        self.sim_duration_label.setText(_translate("MainWindow", "Simulation Duration"))
        self.wind_settings_label.setText(_translate("MainWindow", "Wind Settings"))
        self.wind_speed_label.setText(_translate("MainWindow", "Wind Speed"))
        self.wind_direction_label.setText(_translate("MainWindow", "Wind Direction"))
        self.init_conditions_label.setText(_translate("MainWindow", "Initial conditions"))
        self.initialFireIntensity_label.setText(_translate("MainWindow", "Initial Fire Intensity"))
        self.ingnitionStartTime_label.setText(_translate("MainWindow", "Ignition Start Time"))
        self.modify_fuel_map.setText(_translate("MainWindow", "Modify Fuel Map"))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_import.setTitle(_translate("MainWindow", "Import"))
        self.menu_export.setTitle(_translate("MainWindow", "Export"))
        self.menu_settings.setTitle(_translate("MainWindow", "Settings"))
        self.menu_help.setTitle(_translate("MainWindow", "Help"))
        self.menu_simulation.setTitle(_translate("MainWindow", "Simulation"))
        self.action_create_environment.setText(_translate("MainWindow", "Create Environment"))
        self.action_import_environment.setText(_translate("MainWindow", "Environment"))
        self.action_Initial_Conditions.setText(_translate("MainWindow", "Initial Conditions"))
        self.actionWind.setText(_translate("MainWindow", "Wind"))
        self.actionFuel_Map.setText(_translate("MainWindow", "Fuel Map"))
        self.action_export_simulation.setText(_translate("MainWindow", "Simulation"))
        self.action_export_summary_file.setText(_translate("MainWindow", "Summary File"))
        self.action_export_environment.setText(_translate("MainWindow", "Environment"))
        self.action_import_simulation.setText(_translate("MainWindow", "Simulation"))
        self.action_import_summary_file.setText(_translate("MainWindow", "Summary File"))
        self.actionWorking_Directory.setText(_translate("MainWindow", "Working Directory"))
        self.actionOutput_Directory.setText(_translate("MainWindow", "Output Directory"))
        self.actionDefault_Simulation_Duration.setText(_translate("MainWindow", "Simulation Duration"))
        self.actionSimulation_Runs.setText(_translate("MainWindow", "Simulation Runs"))
        self.action_select_output_files.setText(_translate("MainWindow", "Select Output Files"))
        self.action_run_sim.setText(_translate("MainWindow", "Run"))
        self.action_view_sim.setText(_translate("MainWindow", "View"))
        self.action_user_settings.setText(_translate("MainWindow", "User Settings"))
        self.action_about.setText(_translate("MainWindow", "About"))

    # ---- End generated code

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
            dialog.ui = UserSettingsForm()

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
