import logging as logger
import datetime
import os
import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow


def main(argv):

    # Create logger directory
    logDir = os.path.abspath('../temp')
    if not os.path.exists(logDir):
        os.mkdir(logDir)

    # Setup logger, configure verbosity.
    # Possible values are:
    # INFO, DEBUG, WARN, WARNING,
    # CRITICAL, FATAL, ERROR
    logger.basicConfig(level=logger.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='../temp/'+datetime.datetime.now().strftime("%m%d%Y-%H%M%S")+'.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logger.StreamHandler()
    console.setLevel(logger.INFO)
    # set a format which is simpler for console use
    formatter = logger.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.getLogger('').addHandler(console)

    # Setup and run application
    app = QApplication(argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
