from AsciiViewer import AsciiViewer
from FuelMapEditor import FuelMapEditor
from gui.FuelMapRect import *


class FuelMapViewer(AsciiViewer):

    def __init__(self, parent, fname):

        super().__init__(parent=parent)
        fmeg = FuelMapEditor(self, fname)
        self.editor = fmeg
        self._ascii_parser = fmeg._ascii_parser
        self.setScene(fmeg)

    @staticmethod
    def colors():
        return FuelMapRect.colors + list(FuelMapRect.no_data_color)

    @staticmethod
    def fuel_types():
        return ['Untreated', 'Treated', 'No data']

    def modify_range(self, x_min, x_max, y_min, y_max, value):
        self.editor.modify_range(x_min, x_max, y_min, y_max, value)

    def save(self, save_fname):

        self.editor.save(save_fname)