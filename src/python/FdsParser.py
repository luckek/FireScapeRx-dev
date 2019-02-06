class FdsParser:

    def __init__(self):
        self._lines = list()

    def parse(self, fds_file):
        """Function to parse contents of an fds file, most things are parsed at a fairly high level.
        Returns true if parsing is successful"""

        with open(fds_file) as f:
            for line in f.readlines():

                self._lines.append(line)
                print(line)

    def save_file(self, fds_file):
        """Function to save contents of an fds file"""

        with open(fds_file, 'w') as f:
            for line in self._lines:
                f.write(line)
