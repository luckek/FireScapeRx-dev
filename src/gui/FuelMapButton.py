from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSlot


class FuelMapButton(QPushButton):

    colors = QColor(Qt.white), QColor(Qt.green)

    def __init__(self, parent, bttn_size, name=None):

        QPushButton.__init__(self, parent)

        self.color = 0
        self.setObjectName(name)
        self.setFixedSize(bttn_size, bttn_size)

        pallete = self.palette()
        pallete.setColor(self.backgroundRole(), self.colors[self.color])
        self.setPalette(pallete)

        self.clicked.connect(self.button_click)

    @pyqtSlot(bool, name='button_clicked')
    def button_click(self):

        if self.color == 0:
            self.color = 1

        else:
            self.color = 0

        color_index = self.color
        color = self.colors[color_index].lighter(150)

        pallete = self.palette()
        pallete.setColor(self.backgroundRole(), color)
        self.setPalette(pallete)
