from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import QRect
from gui.FuelMapButton import FuelMapButton


class FuelMapEditor(QWidget):

    BUTTON_SIZE = 25

    def __init__(self, rows, cols):

        QWidget.__init__(self)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 162, 71))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        # self.gridLayout.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
        self.setFixedSize(self.BUTTON_SIZE * rows, self.BUTTON_SIZE * cols)
        self.gridLayoutWidget.setFixedSize(self.BUTTON_SIZE * rows, self.BUTTON_SIZE * cols)

        self._fuel_map_button_grid = []
        for i in range(rows):
            button_row = []
            for j in range(cols):
                button = FuelMapButton(self.gridLayoutWidget, self.BUTTON_SIZE)
                self.gridLayout.addWidget(button, i, j)
                button_row.append(button)

            self._fuel_map_button_grid.append(button_row)

    def get_fuel_map(self):

        fuel_map_grid = []
        for button_row in self._fuel_map_button_grid:
            fuel_map_row = []
            for button in button_row:
                fuel_map_row.append(button.color)

            fuel_map_grid.append(fuel_map_row)
