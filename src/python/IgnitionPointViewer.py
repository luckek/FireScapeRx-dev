from AsciiViewer import AsciiViewer
from IgnitionPointEditor import IgnitionPointEditor
from gui.IgnitionPointRect import *
from Utility import linspace
from FireLine import FireLine


class IgnitionPointViewer(AsciiViewer):

    def __init__(self, parent, fname):

        super().__init__(parent=parent)
        ipeg = IgnitionPointEditor(self, fname)
        self.editor = ipeg
        self._ascii_parser = ipeg._ascii_parser
        self.setScene(ipeg)

        self._fire_lines = []

    @staticmethod
    def colors():
        return IgnitionPointRect.colors + list(IgnitionPointRect.no_data_color)

    @staticmethod
    def fuel_types():
        return ['No Ignition', 'Ignition', 'No data']

    def modify_range(self, x_min, x_max, y_min, y_max, t_start, t_end, value):
        return self.editor.modify_range(x_min, x_max, y_min, y_max, t_start, t_end, value)

    def fire_lines(self):
        return self.editor.fire_lines()

    def save(self, save_fname, update=False):
        self.editor.save(save_fname, update)
