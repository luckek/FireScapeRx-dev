from AsciiGridEditor import AsciiGridEditor
from FuelMapEditorButton import FuelMapEditorButton
from Utility import linspace


class FuelMapEditor(AsciiGridEditor):

    def __init__(self, parent, ascii_fname):

        # TODO: create enum for fuel type(would make code clearer, easier to read)

        super().__init__(parent, ascii_fname)

        dat_table = self._ascii_parser.data_table
        for i in range(len(dat_table)):
            dat_table[i] = [int(x) for x in dat_table[i]]

        # Create grid of buttons
        for i in range(1, self._nrows + 1):
            button_row = []
            for j in range(1, self._ncols + 1):

                init_color = dat_table[i - 1][j - 1]

                if init_color == self._ascii_parser.no_data_val:
                    init_color = -1

                button = FuelMapEditorButton(self._grid_layout_widget, self.BUTTON_SIZE, init_color=init_color)

                self._grid_layout.addWidget(button, i, j)
                button_row.append(button)

            self._ascii_button_grid.append(button_row)

    @staticmethod
    def colors():
        return FuelMapEditorButton.colors + list(FuelMapEditorButton.no_data_color)

    @staticmethod
    def fuel_types():
        return ['Untreated', 'Treated', 'No data']

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
        button_grid = self._ascii_button_grid

        # Modify the fuel map grip
        for point in points_list:
            i, j = t_map[point]
            button_grid[i][j].color = value
