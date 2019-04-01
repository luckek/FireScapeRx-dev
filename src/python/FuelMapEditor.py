from AsciiGridEditor import *
from gui.FuelMapRect import *
from Utility import linspace


class FuelMapEditor(AsciiGridEditor):

    def __init__(self, parent, ascii_fname):

        super().__init__(parent, ascii_fname)

        self._ascii_parser.data_table = self._ascii_parser.data_table.astype(int)
        dat_table = self._ascii_parser.data_table

        # Create grid of buttons
        for i in range(1, self._nrows + 1):
            row = []
            for j in range(2, self._ncols + 2):

                init_color = dat_table[i - 1][j - 2]

                if init_color == self._ascii_parser.no_data_val:
                    init_color = -1

                rect = self.draw_add_rect(i, j, init_color)
                row.append(rect)

            self.rects.append(row)

    def draw_add_rect(self, row, col, init_color):

        rect = FuelMapRect(row, col, 50, init_color)
        self.addItem(rect)
        return rect

    def modify_range(self, x_min, x_max, y_min, y_max, value):

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
        rect_grid = self.rects

        # Modify the fuel map grip
        for point in points_list:
            i, j = t_map[point]
            rect_grid[i][j].color_idx = value
            rect_grid[i][j].set_color()

    def parser(self):
        self.update_vals()
        return self._ascii_parser

    def get_rects(self):
        self.update_vals()
        return self._ascii_parser
