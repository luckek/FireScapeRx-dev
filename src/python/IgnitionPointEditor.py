from AsciiGridEditor import AsciiGridEditor
from IgnitionPointEditorButton import IgnitionPointEditorButton
from Utility import linspace
from FireLine import FireLine


class IgnitionPointEditor(AsciiGridEditor):

    def __init__(self, parent, ascii_fname):

        super().__init__(parent, ascii_fname)

        self._fire_lines = []

        # Create grid of buttons
        for i in range(1, self._nrows + 1):
            button_row = []
            for j in range(1, self._ncols + 1):
                button = IgnitionPointEditorButton(self._grid_layout_widget, self.BUTTON_SIZE, init_color=1)

                self._grid_layout.addWidget(button, i, j)
                button_row.append(button)

            self._ascii_button_grid.append(button_row)

        for i in range(self._nrows):
            for j in range(self._ncols):

                if self._ascii_parser.data_table[i][j] == self._ascii_parser.no_data_val:
                    self._ascii_button_grid[i][j].color = -1

    @staticmethod
    def colors():
        return IgnitionPointEditorButton.colors + list(IgnitionPointEditorButton.no_data_color)

    @staticmethod
    def fuel_types():
        return ['No Ignition', 'Ignition', 'No data']

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
            button_grid = self._ascii_button_grid

            # Modify the fuel map grip
            for point in points_list:
                i, j = t_map[point]
                button_grid[i][j].color = value

        # Remove
        else:

            for f_line in self._fire_lines:
                if f_line.same(curr_f_line):
                    self._fire_lines.remove(f_line)

                    # Get dictionary to translate from (x,y) -> (i,j)
                    t_map = self.point_to_index_map()
                    button_grid = self._ascii_button_grid

                    # Modify the fuel map grip
                    for point in points_list:
                        i, j = t_map[point]
                        button_grid[i][j].color = value
                        break
