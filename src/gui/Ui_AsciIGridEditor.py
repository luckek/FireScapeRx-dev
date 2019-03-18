from PyQt5 import QtCore
from PyQt5.QtWidgets import QScrollArea, QGridLayout, QWidget


class Ui_AsciiGridEditor(QScrollArea):

    BUTTON_SIZE = 25

    def __init__(self, parent):

        QScrollArea.__init__(self, parent=parent)

        # Create and configure grid layout
        self._grid_layout_widget = QWidget(self)
        self._grid_layout = QGridLayout(self._grid_layout_widget)
        self._grid_layout.setContentsMargins(0, 0, 0, 0)
        self._grid_layout.setSpacing(0)
        self.setGeometry(QtCore.QRect(10, 60, 800, 822))
