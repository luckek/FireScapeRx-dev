from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QPushButton


class Ui_AsciiGridEditorButton(QPushButton):

    # Not necessary, but useful for debugging.
    # Since this is more or less an abstract class, this may
    # have the unintended side effect of also guarding against instantiation
    colors = []
    no_data_color = None

    def __init__(self, parent, bttn_size, init_color, name):

        QPushButton.__init__(self, parent)

        self._color = init_color
        self.setObjectName(name)
        self.setFixedSize(bttn_size, bttn_size)

        self._set_color(init_color)
        self.clicked.connect(self.button_click)

        # Removes blue 'selection' border
        self.setFocusPolicy(Qt.NoFocus)

    @pyqtSlot(bool, name='button_clicked')
    def button_click(self):

        if self.color == len(self.colors):
            self._set_color(1)

        else:
            self._color += 1
            self._set_color(self._color)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._set_color(new_color)

    def _set_color(self, new_color):

        self._color = new_color
        pallete = self.palette()

        if self._color == -1:
            pallete.setColor(self.backgroundRole(), self.no_data_color[0])

        else:
            pallete.setColor(self.backgroundRole(), self.colors[self._color - 1])

        self.setPalette(pallete)
