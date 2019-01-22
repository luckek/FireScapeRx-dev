import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from testDialog import *

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = testDialog()
        self.ui.setupUi(self)
        self.show()

def main(argv):
    app = QApplication(argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv[1:])