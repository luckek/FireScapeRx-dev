from AsciiGridEditor import AsciiGridEditor
from IgnitionPointEditorButton import IgnitionPointEditorButton


class IgnitionPointEditor(AsciiGridEditor):

    def __init__(self, ascii_fname):

        super().__init__(ascii_fname)

        # Create grid of buttons
        for i in range(1, self._nrows + 1):
            button_row = []
            for j in range(1, self._ncols + 1):
                button = IgnitionPointEditorButton(self._grid_layout_widget, self.BUTTON_SIZE)

                self._grid_layout.addWidget(button, i, j)
                button_row.append(button)

            self._ascii_button_grid.append(button_row)

        for i in range(self._nrows):
            for j in range(self._ncols):

                current_button = self._ascii_button_grid[i][j]
                current_data = self._ascii_parser.data_table[i][j]

                if current_data == self._ascii_parser.no_data_val:
                    current_button.color = -1

    @staticmethod
    def colors():
        return IgnitionPointEditorButton.colors + list(IgnitionPointEditorButton.no_data_color)

    @staticmethod
    def fuel_types():
        return ['No Ignition', 'Ignition', 'No data']
