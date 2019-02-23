from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit


class ValidatingLineEdit(QLineEdit):

    colors = QColor(Qt.red), QColor(Qt.yellow), QColor(Qt.green)

    def __init__(self, validate, parent=None, name=None):

        QLineEdit.__init__(self, parent)
        self.setObjectName(name)
        self.validate = validate
        self.editingFinished.connect(self.changed)
        self.color = None
        self.changed()

    def changed(self):

        new_text = self.displayText()
        print('new txt:', new_text)
        colorIndex = self.validate(new_text)

        if colorIndex is None:
            return

        color = self.colors[colorIndex].lighter(150)
        if color != self.color:
            pallete = self.palette()
            pallete.setColor(self.backgroundRole(), color)
            self.setPalette(pallete)
            self.color = color
