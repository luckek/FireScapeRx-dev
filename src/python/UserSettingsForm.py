from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

from UserSettings import *
from Utility import get_directory
from gui.Ui_UserSettingsForm import Ui_UserSettingsForm
from PyQt5.QtWidgets import QFileDialog


class UserSettingsForm(QDialog, Ui_UserSettingsForm):

    def __init__(self):
        super(UserSettingsForm, self).__init__()

        self.setupUi(self)

        self.user_settings = UserSettings()

        # Initialize fields with user settings values
        self._output_dir_line_edit.setText(osp.abspath(str(self.user_settings.output_dir)))
        self._working_dir_line_edit.setText(osp.abspath(str(self.user_settings.working_dir)))
        self._sim_duration_line_edit.setText(str(self.user_settings.sim_duration))
        self._wfds_exec_line_edit.setText(str(self.user_settings.wfds_exec))
        self._smv_exec_line_edit.setText(str(self.user_settings.smv_exec))

        # Set line edits to read only
        self._output_dir_line_edit.setReadOnly(True)
        self._working_dir_line_edit.setReadOnly(True)
        self._wfds_exec_line_edit.setReadOnly(True)
        self._smv_exec_line_edit.setReadOnly(True)

        # Clicked signal emits a bool that is passed with the lambda,
        # Which is why the dummy variable checked is there.
        self.output_dir_button.clicked.connect(lambda checked, x=True, state=self: button_clicked((x, state)))
        self.working_dir_button.clicked.connect(lambda checked, x=False, state=self: button_clicked((x, state)))

        self.wfds_exec_bttn.clicked.connect(lambda checked, x=True, state=self: button_clicked_exec((x, state)))
        self.smv_exec_bttn.clicked.connect(lambda checked, x=False, state=self: button_clicked_exec((x, state)))

        self.button_box.accepted.connect(self.save_user_settings)

    @QtCore.pyqtSlot(name='save_user_settings')
    def save_user_settings(self):

        # Modify user settings to whatever the user has modified them to be
        self.user_settings.output_dir = self._output_dir_line_edit.text()
        self.user_settings.working_dir = self._working_dir_line_edit.text()
        self.user_settings.sim_duration = self._sim_duration_line_edit.text()

        self.user_settings.wfds_exec = self._wfds_exec_line_edit.text()
        self.user_settings.smv_exec = self._smv_exec_line_edit.text()

        self.user_settings.save_user_settings()

    def output_dir_line_edit(self):
        return self._output_dir_line_edit

    def working_dir_line_edit(self):
        return self._working_dir_line_edit

    def wfds_exec_line_edit(self):
        return self._wfds_exec_line_edit

    def smv_exec_line_edit(self):
        return self._smv_exec_line_edit


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


@QtCore.pyqtSlot(tuple, name='button_clicked_exec')
def button_clicked_exec(args):

    wfds_pressed, state = args

    # NOTE: we do not have to worry about validating
    # new_directory. If anything != None is returned, it
    # is guaranteed to be a valid directory.

    new_exec, filt = QFileDialog.getOpenFileName(state, "Select executable", state.user_settings.working_dir)

# Make sure user chose a directory
    if new_exec:
        if wfds_pressed:
            state.wfds_exec_line_edit().setText(new_exec)

        else:
            state.smv_exec_line_edit().setText(new_exec)