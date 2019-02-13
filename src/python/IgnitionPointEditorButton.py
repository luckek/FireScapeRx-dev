from gui.Ui_AsciiGridEditorButton import Ui_AsciiGridEditorButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class IgnitionPointEditorButton(Ui_AsciiGridEditorButton):

    colors = [QColor(Qt.white), QColor(Qt.red)]

    no_data_color = [QColor(Qt.black)]

    def __init__(self, parent, bttn_size, init_color=0, name=None):

        super().__init__(parent, bttn_size, init_color, name)
