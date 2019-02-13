from PyQt5.QtWidgets import QWidget, QGridLayout


class Ui_AsciiGridEditor(QWidget):

    BUTTON_SIZE = 25

    def __init__(self):

        QWidget.__init__(self)

        # Create and configure grid layout
        self.gridLayoutWidget = QWidget(self)
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
