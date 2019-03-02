from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from gui.Ui_AsciiGridEditorButton import Ui_AsciiGridEditorButton


class FuelMapEditorButton(Ui_AsciiGridEditorButton):

    colors = [QColor(Qt.white), QColor(Qt.green)]

    no_data_color = [QColor(Qt.black)]

    def __init__(self, parent, bttn_size, init_color=1, name=None):

        super().__init__(parent, bttn_size, init_color, name)

        # Disallow user to edit 'no value' cells
        if init_color == -1:
            self.clicked.disconnect(self.button_click)
