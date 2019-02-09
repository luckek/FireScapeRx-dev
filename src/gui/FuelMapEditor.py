from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import QRect, Qt
from gui.FuelMapButton import FuelMapButton


class FuelMapEditor(QWidget):

    BUTTON_SIZE = 25

    def __init__(self, rows, cols):

        QWidget.__init__(self)

        # Create and configure grid layout
        self.gridLayoutWidget = QWidget(self)
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        self.setFixedSize(self.BUTTON_SIZE * (rows + 2), self.BUTTON_SIZE * (cols + 2))
        self.gridLayoutWidget.setFixedSize(self.BUTTON_SIZE * (rows + 2), self.BUTTON_SIZE * (cols + 2))

        # TODO: add some labels?
        for i in range(1, rows + 1):
            label = QLabel(parent=self.gridLayoutWidget, text=str(i))
            label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            label.setAlignment(Qt.AlignCenter)
            self.gridLayout.addWidget(label, i, 0)

        for i in range(1, cols + 1):
            label = QLabel(parent=self.gridLayoutWidget, text=str(i))
            label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            label.setAlignment(Qt.AlignCenter)
            self.gridLayout.addWidget(label, 0, i)

        self._fuel_map_button_grid = []
        for i in range(1, rows + 1):
            button_row = []
            for j in range(1, cols + 1):
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
