from PyQt5.QtWidgets import QWidget, QGridLayout


class Ui_AsciiGridEditor(QWidget):

    BUTTON_SIZE = 25

    def __init__(self):

        QWidget.__init__(self)

        # Create and configure grid layout
        self._grid_layout_widget = QWidget(self)
        self._grid_layout = QGridLayout(self._grid_layout_widget)
        self._grid_layout.setContentsMargins(0, 0, 0, 0)
        self._grid_layout.setSpacing(0)
