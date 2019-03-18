from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor


class CustomRectangle(QtWidgets.QGraphicsRectItem):

    colors = []
    no_data_color = [QColor('black')]

    def __init__(self, row, col, size, color_idx):

        super().__init__(col * size, row * size, size, size)

        self.color_idx = color_idx
        self.setPen(Qt.black)
        self.set_color()

    def mousePressEvent(self, e):

        self.update_color()

    def set_color_idx(self, new_idx):

        self.color_idx = new_idx
        self.update_color()

    def update_color(self):

        self.color_idx = (self.color_idx + 1) % len(self.colors)
        self.set_color()

    def set_color(self):

        if self.color_idx == -1:
            self.setBrush(QColor(0, 0, 0))

        else:
            self.setBrush(self.colors[self.color_idx - 1])
