import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


def main(argv):
    app = QApplication(argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
