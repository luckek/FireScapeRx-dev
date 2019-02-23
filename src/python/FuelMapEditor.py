from AsciiGridEditor import AsciiGridEditor
from FuelMapEditorButton import FuelMapEditorButton
from PyQt5.QtWidgets import qApp


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
