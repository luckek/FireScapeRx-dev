from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QFileDialog
from gui.Ui_UserSettings import Ui_Dialog
from UserSettings import *
import os.path as osp


class UserSettingsForm(QDialog, Ui_Dialog):

    def __init__(self):
        super(UserSettingsForm, self).__init__()

        self.setupUi(self)

        # Set line edits to read only
        self.output_dir_line_edit.setReadOnly(True)
        self.working_dir_line_edit.setReadOnly(True)

        # Clicked signal emits a bool that is passed with the lambda,
        # Which is why the dummy variable checked is there.
        self.output_dir_button.clicked.connect(lambda checked, x=True, state=self: button_clicked((x, state)))
        self.working_dir_button.clicked.connect(lambda checked, x=False, state=self: button_clicked((x, state)))

        self.button_box.accepted.connect(self.save_user_settings)

        self.output_dir_line_edit.returnPressed.connect(self.ret_pressed)

    def ret_pressed(self):
      print('Return')

    @QtCore.pyqtSlot(name='save_user_settings')
    def save_user_settings(self):

        # Modify user settings to whatever the user has modified them to be
        self.user_settings.output_dir = self.output_dir_line_edit.text()
        self.user_settings.working_dir = self.working_dir_line_edit.text()
        self.user_settings.sim_duration = self.sim_duration_line_edit.text()
        self.user_settings.num_sims = self.num_sims_line_edit.text()

        self.user_settings.save_user_settings()


@QtCore.pyqtSlot(tuple, name='button_clicked')
def button_clicked(args):

    output_dir_pressed, state = args

    file = str(QFileDialog.getExistingDirectory(state, "Select Directory"))

    # Make sure user chose a directory
    if file:
        if output_dir_pressed:
            state.output_dir_line_edit.setText(file)

        else:
            state.working_dir_line_edit.setText(file)
