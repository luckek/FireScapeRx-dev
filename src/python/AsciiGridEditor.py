from PyQt5.QtWidgets import QGraphicsTextItem
from numpy import asarray

from AsciiParser import AsciiParser
from Utility import center_num
from gui.CustomRectangle import *


class AsciiGridEditorGraphics(QtWidgets.QGraphicsScene):

    def __init__(self, parent, ascii_fname):

        super().__init__(parent)

        self.lines = []
        self.rects = []

        self._ascii_parser = AsciiParser(ascii_fname)

        self._nrows = self._ascii_parser.nrows
        self._ncols = self._ascii_parser.ncols

        # Record set of column coordinates
        self._row_set = set()

        self.draw_grid()

    def draw_grid(self):


        WIDTH = 51
        HEIGHT = 51

        size = 50

        width = (self._nrows + 1) * WIDTH
        height = (self._ncols + 1) * HEIGHT

        self.setSceneRect(0, 0, width, height)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        # FIXME:
        cell_size = self._ascii_parser.cell_size
        # cell_size = self._ascii_parser.cell_size + 500

        # Rows start at min coordinate value
        init_x_val = int(self._ascii_parser.xllcorner) + cell_size // 2

        # FIXME:
        current_x_val = init_x_val
        # current_x_val = init_x_val + 1000

        # Setup row labels for editor
        for i in range(2, self._ncols + 2):

            current_x_str = center_num(current_x_val)

            label = QGraphicsTextItem(current_x_str)
            label.setPos((i * size), 0)

            self.addItem(label)

            current_x_val += cell_size

        # Columns start at max coordinate value
        init_y_val = int(self._ascii_parser.yllcorner) + cell_size * self._nrows - cell_size // 2
        current_y_val = init_y_val

        # Setup row labels for editor
        for i in range(1, self._nrows + 1):

            current_y_str = center_num(current_y_val)

            label = QGraphicsTextItem(current_y_str)
            label.setPos(0, i * size)
            self.addItem(label)

            current_y_val -= cell_size

    def values_grid(self):

        fuel_map_grid = []
        for row in self.rects:
            fuel_map_row = []
            for rect in row:
                fuel_map_row.append(rect.color_idx)
            fuel_map_grid.append(fuel_map_row)

        return asarray(fuel_map_grid, dtype=int)

    def save(self, save_fname, update=True):
        if update:
            self._ascii_parser.data_table = self.values_grid()

        self._ascii_parser.save(save_fname)

    def update_vals(self):
        self._ascii_parser.data_table = self.values_grid()

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
        return self._row_set

    def column_numbers(self):
        return self._col_set

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
