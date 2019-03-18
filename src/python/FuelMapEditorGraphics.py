from AsciiGridEditorGraphics import *
from gui.FuelMapRect import *


class FuelMapEditorGraphics(AsciiGridEditorGraphics):

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
