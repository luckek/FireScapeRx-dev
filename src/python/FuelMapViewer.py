from AsciiViewer import AsciiViewer
from FuelMapEditorGraphics import FuelMapEditorGraphics
from gui.FuelMapRect import *


class FuelMapViewer(AsciiViewer):

    def __init__(self, parent, fname):

        super().__init__(parent=parent)
        fmeg = FuelMapEditorGraphics(self, fname)
        self._ascii_parser = fmeg._ascii_parser
        self.setScene(fmeg)

    @staticmethod
    def colors():
        return FuelMapRect.colors + list(FuelMapRect.no_data_color)

    @staticmethod
    def fuel_types():
        return ['Untreated', 'Treated', 'No data']
