from AsciiGridEditor import AsciiGridEditor
from FuelMapEditorButton import FuelMapEditorButton


class FuelMapEditor(AsciiGridEditor):

    def __init__(self, ascii_fname):

        super().__init__(ascii_fname)

        # Create grid of buttons
        for i in range(1, self._nrows + 1):
            button_row = []
            for j in range(1, self._ncols + 1):
                button = FuelMapEditorButton(self.gridLayoutWidget, self.BUTTON_SIZE)

                self.gridLayout.addWidget(button, i, j)
                button_row.append(button)

            self._ascii_button_grid.append(button_row)

        for i in range(self._nrows):
            for j in range(self._ncols):

                current_button = self._ascii_button_grid[i][j]
                current_data = self._ascii_parser.data_table[i][j]

                if current_data == self._ascii_parser.no_data_val:
                    current_button.color = -1

                # FIXME: throw, log, or handle? (currently silently handled)
                # if current_data > len(Ui_AsciiGridEditorButton.colors):
                #     current_data = len(Ui_AsciiGridEditorButton.colors) - 1

                else:
                    current_button.color = self._ascii_parser.data_table[i][j]  # Initialize grid to match ascii data table


    def colors(self):
        return FuelMapEditorButton.colors + list(FuelMapEditorButton.no_data_color)

    def fuel_types(self):
        return ['Untreated', 'Treated', 'No data']