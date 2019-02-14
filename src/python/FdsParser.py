class FdsParser:

    # TODO: figure out what is optional, create mechanism to deal with that
    def __init__(self):
        self._lines = list()

        self._head = ''
        self._title = ''
        self._misc = []

        self._mult = ''
        self._mesh = ''
        self._surf = []
        self._vent = []
        self._dump = ''
        self._slcf = []
        self._isof = []
        self._bndf = []

        self._time = ''

    # TODO: add ability to carry comments through
    def parse(self, fds_file):
        """Function to parse contents of an fds file, most things are parsed at a fairly high level.
        Returns true if parsing is successful"""

        with open(fds_file) as f:
            for line in f.readlines():

                line = line.replace('\n', '')

                self._lines.append(line)

                # FIXME: remove, when this is finished
                # print(line,)

                if len(line) == 0 or line[0] == '-' or line[0] == 'c' or line[0] == ' ':
                    continue

                elif line.startswith('&HEAD'):
                    self._head = line

                elif line.startswith('TITLE'):
                    self._title = line

                elif line.startswith('&TIME'):
                    self._time = line

                # FIXME: Once misc is taken care of, can just pass rest
                # of file through to lines, for now.
                # else:
                #     self._lines.append(line)

    def save_file(self, fds_file):
        """Function to save contents of an fds file"""

        # TODO: save modified values
        with open(fds_file, 'w') as f:
            for line in self._lines:
                f.write(line + '\n')

    @property
    def time(self):

        t_end_str = self._time.split('=')[1].replace('/', '').strip(' ')
        return t_end_str

    @property
    def title(self):

        title_str = self._title.split('=')[1].replace('/', '').replace("'", '').strip(' ')
        return title_str

    @property
    def head(self):

        head_str = self._head.split('=')[1].replace('/', '').replace("'", '').strip(' ')
        return head_str
