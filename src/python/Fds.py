import os as os

from FdsParser import FdsParser


class Fds:

    # FIXME: Could make this path an env variable that is passed to execute and upate
    # NOTE: it is not uncommon for wfds to signal IEEE_DENORMAL, this can likely be safely ignored
    # Path to pre-packaged fds executable
    fds_exec = os.path.join(os.path.abspath(os.pardir), 'fds_gnu_linux_64')

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
        return self._parser.parse(self.fds_file)

    def save(self, new_fds_file=None):

        save_fname = self._fds_file

        if new_fds_file is not None:
            save_fname = new_fds_file

        self._parser.save_file(save_fname + '.fds')

    def file_present(self):
        return self._fds_file is not None

    def sim_time(self):
        return self._parser.time

    def job(self):
        return self._parser.head

    def job_name(self):
        return self._parser.title

    @staticmethod
    def file_ext():
        return FdsParser.file_ext
