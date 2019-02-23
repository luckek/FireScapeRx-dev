import os.path as osp

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

from UserSettings import *
from Utility import get_directory
from gui.Ui_UserSettings import Ui_Dialog


class UserSettingsForm(QDialog, Ui_Dialog):

    def __init__(self):
        super(UserSettingsForm, self).__init__()

        self.setupUi(self)

        self.user_settings = UserSettings()

        # Initalize fields with user settings values
        self._output_dir_line_edit.setText(osp.abspath(str(self.user_settings.output_dir)))
        self._working_dir_line_edit.setText(osp.abspath(str(self.user_settings.working_dir)))
        self._sim_duration_line_edit.setText(str(self.user_settings.sim_duration))
        self._num_sims_line_edit.setText(str(self.user_settings.num_sims))

        # Set line edits to read only
        self._output_dir_line_edit.setReadOnly(True)
        self._working_dir_line_edit.setReadOnly(True)

        # Clicked signal emits a bool that is passed with the lambda,
        # Which is why the dummy variable checked is there.
        self.output_dir_button.clicked.connect(lambda checked, x=True, state=self: button_clicked((x, state)))
        self.working_dir_button.clicked.connect(lambda checked, x=False, state=self: button_clicked((x, state)))

        self.button_box.accepted.connect(self.save_user_settings)

        self._output_dir_line_edit.returnPressed.connect(self.ret_pressed)

    def ret_pressed(self):
        print('Return')

    @QtCore.pyqtSlot(name='save_user_settings')
    def save_user_settings(self):

        # Modify user settings to whatever the user has modified them to be
        self.user_settings.output_dir = self._output_dir_line_edit.text()
        self.user_settings.working_dir = self._working_dir_line_edit.text()
        self.user_settings.sim_duration = self._sim_duration_line_edit.text()
        self.user_settings.num_sims = self._num_sims_line_edit.text()

        self.user_settings.save_user_settings()

    def output_dir_line_edit(self):
        return self._output_dir_line_edit

    def working_dir_line_edit(self):
        return self._output_dir_line_edit


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
