from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from AsciiParser import AsciiParser
from Utility import linspace
from gui.Ui_AsciIGridEditor import Ui_AsciiGridEditor


class AsciiGridEditor(Ui_AsciiGridEditor):

    def __init__(self, parent, ascii_fname):

        Ui_AsciiGridEditor.__init__(self, parent)

        self._ascii_parser = AsciiParser(ascii_fname)
        self._ascii_parser.read()

        self._nrows = self._ascii_parser.nrows
        self._ncols = self._ascii_parser.ncols

        cell_size = self._ascii_parser.cell_size

        # Record set of column coordinates
        self._row_set = set()

        # Columns start at max coordinate value
        init_y_val = int(self._ascii_parser.yllcorner) + cell_size * self._nrows - cell_size // 2
        current_y_val = init_y_val

        # Setup row labels for editor
        for i in range(1, self._nrows + 1):

            self._row_set.add(current_y_val)

            label = QLabel(parent=self._grid_layout_widget, text=str(current_y_val))
            label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            label.setAlignment(Qt.AlignCenter)
            self._grid_layout.addWidget(label, i, 0)

            current_y_val -= cell_size

        # Record set of column coordinates
        self._col_set = set()

        # Rows start at min coordinate value
        init_x_val = int(self._ascii_parser.xllcorner) + cell_size // 2
        current_x_val = init_x_val

        # Setup column labels for editor
        for i in range(1, self._ncols + 1):

            self._col_set.add(current_x_val)

            label = QLabel(parent=self._grid_layout_widget, text=str(current_x_val))
            label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            label.setAlignment(Qt.AlignCenter)
            self._grid_layout.addWidget(label, 0, i)

            current_x_val += cell_size

        self._ascii_button_grid = []
        self.setWidget(self._grid_layout_widget)

    def button_values_grid(self):

        fuel_map_grid = []
        for button_row in self._ascii_button_grid:
            fuel_map_row = []
            for button in button_row:
                fuel_map_row.append(button.color)
            fuel_map_grid.append(fuel_map_row)

        return fuel_map_grid

    def save(self, save_fname, update=True):
        if update:
            self._ascii_parser.data_table = self.button_values_grid()

        self._ascii_parser.save(save_fname)

    def grid_x_max(self):
        return self._ascii_parser.x_max()

    def grid_x_min(self):
        return self._ascii_parser.x_min()

    def grid_y_max(self):
        return self._ascii_parser.y_max()

    def grid_y_min(self):
        return self._ascii_parser.y_min()

    def resolution(self):
        return self._ascii_parser.cell_size

    def row_numbers(self):
        return self._row_set

    def column_numbers(self):
        return self._col_set

    def index_to_point_map(self):

        t_map = dict()

        cell_size = self._ascii_parser.cell_size
        init_x = self._ascii_parser.xllcorner + int(cell_size / 2)
        init_y = self._ascii_parser.yllcorner + (int((cell_size * self._nrows) - int(cell_size / 2.0)))

        current_y = init_y
        for i in range(self._nrows):
            current_x = init_x
            for j in range(self._ncols):
                t_map[(i, j)] = (int(current_x), int(current_y))
                current_x += cell_size
            current_y -= cell_size

        return t_map

    def point_to_index_map(self):

        t_map = self.index_to_point_map()

        return {b: a for a, b in t_map.items()}

    def parser(self):
        return self._ascii_parser
