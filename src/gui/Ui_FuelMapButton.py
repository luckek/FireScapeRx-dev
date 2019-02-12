from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot


class Ui_FuelMapButton(QPushButton):

    colors = QColor(Qt.white), QColor(Qt.green)

    def __init__(self, parent, bttn_size, init_color=0, name=None):

        QPushButton.__init__(self, parent)

        self._color = init_color
        self.setObjectName(name)
        self.setFixedSize(bttn_size, bttn_size)

        self._set_color(init_color)
        self.clicked.connect(self.button_click)

    @pyqtSlot(bool, name='button_clicked')
    def button_click(self):

        if self.color == len(self.colors) - 1:
            self._set_color(0)

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
        pallete.setColor(self.backgroundRole(), self.colors[self._color])
        self.setPalette(pallete)
