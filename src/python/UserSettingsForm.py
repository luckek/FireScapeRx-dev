from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from gui.Ui_UserSettings import Ui_Dialog
from UserSettings import *
from SimulationSettings import *
import os.path as osp
from Utility import get_directory


class UserSettingsForm(QDialog, Ui_Dialog):

    def __init__(self):
        super(UserSettingsForm, self).__init__()

        self.setupUi(self)

        self.user_settings = UserSettings()
        self._close_window = True

        # Initalize fields with user settings values
        self._output_dir_line_edit.setText(osp.abspath(str(self.user_settings.output_dir)))
        self._working_dir_line_edit.setText(osp.abspath(str(self.user_settings.working_dir)))
        self._default_environment_line_edit.setText(str(self.user_settings.default_environment))
        self._sim_duration_line_edit.setText(str(self.user_settings.sim_duration))

        # Set line edits to read only
        self._output_dir_line_edit.setReadOnly(True)
        self._working_dir_line_edit.setReadOnly(True)
        self._default_environment_line_edit.setReadOnly(True)

        # Clicked signal emits a bool that is passed with the lambda,
        # Which is why the dummy variable checked is there.
        self.output_dir_button.clicked.connect(lambda checked, x=True, state=self: button_clicked((x, state)))
        self.working_dir_button.clicked.connect(lambda checked, x=False, state=self: button_clicked((x, state)))
        self.default_environment_button.clicked.connect(lambda checked, x=False, state=self: environment_button_clicked((x, state)))

        self._output_dir_line_edit.returnPressed.connect(self.ret_pressed)

    def ret_pressed(self):
        print('Return')

    @QtCore.pyqtSlot(name='save_user_settings')
    def save_user_settings(self):

        # Modify user settings to whatever the user has modified them to be
        self.user_settings.output_dir = self._output_dir_line_edit.text()
        self.user_settings.working_dir = self._working_dir_line_edit.text()
        self.user_settings.default_environment = self._default_environment_line_edit.text()
        # Check validity if sim duration input
        # Check that the value is numeric
        if not(self._sim_duration_line_edit.text().replace('.', '', 1).isdigit()):
            QMessageBox.information(self, "Invalid Input!", "Simulation duration must be numeric.")
            self._close_window = False
        else:
            # Check that the value is in range
            if(float(self._sim_duration_line_edit.text()) <= 0 or float(self._sim_duration_line_edit.text()) > SimulationSettings.MAX_DURATION):
                QMessageBox.information(self, "Invalid Input!", "Simulation duration must be greater than 0 and less than " + str(SimulationSettings.MAX_DURATION))
                self._close_window = False
            else:
                self.user_settings.sim_duration = self._sim_duration_line_edit.text()
                # If everything is valid, set close_window to true
                self._close_window = True

        self.user_settings.save_user_settings()

    def output_dir_line_edit(self):
        return self._output_dir_line_edit

    def working_dir_line_edit(self):
        return self._working_dir_line_edit

    def default_environment_line_edit(self):
        return self._default_environment_line_edit

    # Redefine accept event so values can be checked before closing
    def accept(self):
        # save settings first
        self.save_user_settings()
        # close if new settings are valid
        if self._close_window:
            super(UserSettingsForm, self).accept()


@QtCore.pyqtSlot(tuple, name='button_clicked')
def button_clicked(args):

    output_dir_pressed, state = args

    # NOTE: we do not have to worry about validating
    # new_directory. If anything != None is returned, it
    # is guaranteed to be a valid directory.
    new_directory = get_directory(state)

    # Make sure user chose a directory
    if new_directory:
        if output_dir_pressed:
            state.output_dir_line_edit().setText(new_directory)

        else:
            state.working_dir_line_edit().setText(new_directory)

def environment_button_clicked(args):
    default_environment_pressed, state = args

    #user_settings = UserSettings()

    # Open FileDialog in user's current working directory, with fds file filter
    #file = QFileDialog.getOpenFileName(self=args, 'Open File', user_settings.working_dir, filter="fds (*.fds)")


    #state.default_environment_line_edit().setText(file)