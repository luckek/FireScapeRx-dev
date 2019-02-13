from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from gui.Ui_FuelMapEditor import Ui_FuelMapEditor
from gui.Ui_FuelMapButton import Ui_FuelMapButton
from AsciiParser import AsciiParser
from Utility import linspace


class FuelMapEditor(Ui_FuelMapEditor):

    def __init__(self, ascii_fname):

        Ui_FuelMapEditor.__init__(self)

        self._ascii_parser = AsciiParser(ascii_fname)
        self._ascii_parser.read()

        self._nrows = self._ascii_parser.nrows
        self._ncols = self._ascii_parser.ncols

        cell_size = int(self._ascii_parser.cell_size)

        self._row_set = set()
        init_val = int((cell_size * self._nrows) - int(cell_size / 2.0))
        current_val = init_val

        for i in range(1, self._nrows + 1):

            self._row_set.add(int(current_val))

            label = QLabel(parent=self.gridLayoutWidget, text=str(current_val))
            label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            label.setAlignment(Qt.AlignCenter)
            self.gridLayout.addWidget(label, i, 0)

            current_val -= cell_size

        self._col_set = set()
        init_val = int(cell_size / 2)
        current_val = init_val

        for i in range(1, self._ncols + 1):

            self._col_set.add(current_val)

            label = QLabel(parent=self.gridLayoutWidget, text=str(current_val))
            label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            label.setAlignment(Qt.AlignCenter)
            self.gridLayout.addWidget(label, 0, i)

            current_val += cell_size

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

    def modify_range(self, x_min, x_max, y_min, y_max, fuel_type):

        # Figure out how many points we need
        x_range_length = int((x_max - x_min) / self._ascii_parser.cell_size) + 1
        y_range_length = int((y_max - y_min) / self._ascii_parser.cell_size) + 1

        # Get those points, respectively
        x_points = linspace(x_min, x_max, x_range_length, self._ascii_parser.cell_size)
        y_points = linspace(y_min, y_max, y_range_length, self._ascii_parser.cell_size)

        x_points = [int(x) for x in x_points]
        y_points = [int(y) for y in y_points]

        points_list = []

        # Create full list of points we want to modify
        for x_point in x_points:
            for y_point in y_points:
                points_list.append((x_point, y_point))

        # Get dictionary to translate from (x,y) -> (i,j)
        t_map = self.point_to_index_map()
        fuel_map = self._fuel_map_button_grid

        # Modify the fuel map grip
        for point in points_list:
            i, j = t_map[point]
            fuel_map[i][j].color = fuel_type

    def f_map_x_max(self):
        return self._ascii_parser.x_max()

    def f_map_x_min(self):
        return self._ascii_parser.x_min()

    def f_map_y_max(self):
        return self._ascii_parser.y_max()

    def f_map_y_min(self):
        return self._ascii_parser.y_min()

    def row_numbers(self):
        return self._row_set

    def column_numbers(self):
        return self._col_set

    def colors(self):
        return Ui_FuelMapButton.colors + list(Ui_FuelMapButton.no_data_color)

    def fuel_types(self):
        return ['Untreated', 'Treated', 'No data']

    def index_to_point_map(self):

        t_map = dict()

        cell_size = self._ascii_parser.cell_size
        init_x = int(cell_size / 2)
        current_y = int((cell_size * self._nrows) - int(cell_size / 2.0))

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
