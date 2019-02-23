import logging as logger
import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow


def main(argv):

    # Setup logger, configure verbosity.
    # Possible values are:
    # INFO, DEBUG, WARN, WARNING,
    # CRITICAL, FATAL, ERROR
    logger.basicConfig(level=logger.INFO)

    # Setup application and run
    app = QApplication(argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
