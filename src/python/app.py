import sys
from MainWindow import MainWindow
from gui.UserSettingsForm import *
from PyQt5.QtWidgets import QMainWindow, QApplication


# class AppWindow(QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#         self.ui = MainWindow()
#         # self.ui.setupUi(self)
#         self.show()


def main(argv):
    app = QApplication(argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
