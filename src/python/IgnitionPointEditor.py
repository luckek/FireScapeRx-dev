from AsciiGridEditor import *
from gui.IgnitionPointRect import *
from FireLine import *
from Utility import linspace


class IgnitionPointEditor(AsciiGridEditor):

    def __init__(self, parent, ascii_fname):

        super().__init__(parent, ascii_fname)

        self._fire_lines = []

        # Create grid of buttons
        for i in range(1, self._nrows + 1):
            row = []
            for j in range(2, self._ncols + 2):

                init_color = 1

                if init_color == self._ascii_parser.no_data_val:
                    init_color = -1

                rect = self.draw_add_rect(i, j, init_color)
                row.append(rect)

            self.rects.append(row)

    def draw_add_rect(self, row, col, init_color):

        rect = IgnitionPointRect(row, col, 50, init_color)
        self.addItem(rect)
        return rect

    def modify_range(self, x_min, x_max, y_min, y_max, t_start, t_end, value):

        # Figure out how many points we need
        x_range_length = int((x_max - x_min) / self._ascii_parser.cell_size) + 1
        y_range_length = int((y_max - y_min) / self._ascii_parser.cell_size) + 1

        t_length = max(x_range_length, y_range_length)

        # Get those points, respectively
        x_points = linspace(x_min, x_max, x_range_length, self._ascii_parser.cell_size)
        y_points = linspace(y_min, y_max, y_range_length, self._ascii_parser.cell_size)

        t_list = linspace(t_start, t_end, t_length)

        x_points = [int(x) for x in x_points]
        y_points = [int(y) for y in y_points]

        points_list = []

        # Create full list of points we want to modify
        for x_point in x_points:
            for y_point in y_points:
                points_list.append((x_point, y_point))

        curr_f_line = FireLine(points_list, t_list)

        print(curr_f_line)

        # Add
        if value == 0:

            for f_line in self._fire_lines:
                if f_line.overlap(curr_f_line):
                    return 'OVERLAP'

            self._fire_lines.append(curr_f_line)

            # Get dictionary to translate from (x,y) -> (i,j)
            t_map = self.point_to_index_map()
            button_grid = self.rects

            # Modify the fuel map grip
            for point in points_list:
                i, j = t_map[point]
                button_grid[i][j].color_idx = value
                button_grid[i][j].set_color()

        # Remove
        else:

            for f_line in self._fire_lines:
                if f_line.same(curr_f_line):
                    self._fire_lines.remove(f_line)

                    # Get dictionary to translate from (x,y) -> (i,j)
                    t_map = self.point_to_index_map()
                    button_grid = self.rects

                    # Modify the fuel map grip
                    for point in points_list:
                        i, j = t_map[point]
                        button_grid[i][j].color_idx = value
                        button_grid[i][j].set_color()
                    break

    def add_ignition_point(self, i, j, idx_pt_map):

        # Make all points light at 0.2s
        t_list = [0.2]

        # Get (x,y) from (i,j)
        points_list = [idx_pt_map[(i, j)]]

        self._fire_lines.append(FireLine(points_list, t_list))

    def fire_lines(self):

        map = self.index_to_point_map()
        for i, row in enumerate(self.rects):
            for j, rect in enumerate(row):

                if rect.color_idx == 0:
                    self.add_ignition_point(i, j, map)

        return self._fire_lines
