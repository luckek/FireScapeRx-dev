from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import QRect
import numpy as np

class AsciiViewer(QGraphicsView):

    def __init__(self, parent):

        super().__init__(parent=parent)
        self._ascii_parser = None
        self.setGeometry(QRect(10, 60, 822, 800))

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

        y_start = self.grid_y_min()
        y_end = self.grid_y_max() - self.resolution() // 2

        return set(np.linspace(y_start, y_end, self._ascii_parser.nrows).astype(int).tolist())

    def column_numbers(self):

        x_start = self.grid_x_min()
        x_end = self.grid_x_max() - self.resolution() // 2

        return set(np.linspace(x_start, x_end, self._ascii_parser.ncols).astype(int).tolist())

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
