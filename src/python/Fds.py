import os
from FdsParser import FdsParser


class Fds:

    # Path to pre-packaged fds executable
    fds_exec = os.path.abspath(os.pardir) + os.sep + 'fds_gnu_linux_64'

    def __init__(self, fds_file=None):

        self._fds_file = fds_file
        self._parser = FdsParser()

    @property
    def fds_file(self):
        return self._fds_file

    @fds_file.setter
    def fds_file(self, fds_file):
        self._fds_file = fds_file

    def read(self):
        self._parser.parse(self.fds_file)

    def save(self):
        self._parser.save_file(self.fds_file)

    def file_present(self):
        return self._fds_file is not None
