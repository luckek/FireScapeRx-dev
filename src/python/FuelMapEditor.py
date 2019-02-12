from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from gui.Ui_FuelMapEditor import Ui_FuelMapEditor
from gui.Ui_FuelMapButton import Ui_FuelMapButton
from AsciiParser import AsciiParser


class FuelMapEditor(Ui_FuelMapEditor):

    def __init__(self, ascii_fname):

        Ui_FuelMapEditor.__init__(self)

        self._ascii_parser = AsciiParser(ascii_fname)
        self._ascii_parser.read()

        self._nrows = self._ascii_parser.nrows
        self._ncols = self._ascii_parser.ncols

        cell_size = int(self._ascii_parser.cell_size)
        # TODO: add some labels?
        init_val = int((cell_size * self._nrows) - int(cell_size / 2.0))
        for i in range(1, self._nrows + 1):

            label = QLabel(parent=self.gridLayoutWidget, text=str(init_val))
            init_val -= cell_size
            label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            label.setAlignment(Qt.AlignCenter)
            self.gridLayout.addWidget(label, i, 0)

        init_val = int(cell_size / 2)
        for i in range(1, self._ncols + 1):

            label = QLabel(parent=self.gridLayoutWidget, text=str(init_val))
            init_val += cell_size

            label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            label.setAlignment(Qt.AlignCenter)
            self.gridLayout.addWidget(label, 0, i)

        self._fuel_map_button_grid = []
        for i in range(1, self._nrows + 1):
            button_row = []
            for j in range(1, self._ncols + 1):
                button = Ui_FuelMapButton(self.gridLayoutWidget, self.BUTTON_SIZE)

                current_data = self._ascii_parser.data_table[i - 1][j - 1]

                # FIXME: throw, log, or handle? (currently silently handled)
                if current_data > len(Ui_FuelMapButton.colors):
                    current_data = len(Ui_FuelMapButton.colors) - 1

                if current_data == self._ascii_parser.no_data_val:
                    button.color = -1

                else:

                    button.color = self._ascii_parser.data_table[i - 1][j - 1]  # Initialize grid to match ascii data table
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

        return fuel_map_grid

    def save(self, save_fname):

        self._ascii_parser.data_table = self.get_fuel_map()
        self._ascii_parser.save(save_fname)

    def colors(self):
        return Ui_FuelMapButton.colors + list(Ui_FuelMapButton.no_data_color)

    def fuel_types(self):
        return ['Untreated', 'Treated', 'No data']

    def get_point_translation_map(self):

        t_map = dict()

        cell_size = self._ascii_parser.cell_size
        init_x = int(cell_size / 2)
        current_y = int((cell_size * self._nrows) - int(cell_size / 2.0))

        for i in range(self._nrows):
            current_x = init_x
            for j in range(self._ncols):
                t_map[(i, j)] = (current_x, current_y)
                current_x += cell_size
            current_y -= cell_size

        return t_map