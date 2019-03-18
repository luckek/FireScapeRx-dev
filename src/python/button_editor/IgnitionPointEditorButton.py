from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from gui.Ui_AsciiGridEditorButton import Ui_AsciiGridEditorButton


class IgnitionPointEditorButton(Ui_AsciiGridEditorButton):

    colors = [QColor(Qt.white), QColor(Qt.red)]

    no_data_color = [QColor(Qt.black)]

    def __init__(self, parent, bttn_size, init_color=0, name=None):

        super().__init__(parent, bttn_size, init_color, name)

        # Disconnect so user can't 'edit' button color
        self.clicked.disconnect(self.button_click)

    # This disables the 'click' animation
    # Could install event filter, but this was quick / easy
    def mousePressEvent(self, e):
        pass
