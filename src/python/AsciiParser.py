import numpy as np


class AsciiParser:

    FILE_EXT = '.asc'

    def __init__(self, fname):

        self._fname = fname

        self._ncols = 0
        self._nrows = 0
        self._xllcorner = 0.0
        self._yllcorner = 0.0
        self._cell_size = 0
        self._NODATA_value = 0
        self._data_table = []

        self._orig_xllcorner = 0
        self._orig_yllcorner = 0

        self.read()

    def read(self, fname=None):

        read_fname = self._fname

        if fname:
            read_fname = fname

        with open(read_fname) as f:
            self._data_table = []

            for line in f:

                line = line.replace('\n', '').strip()

                if len(line) == 0:
                    continue

                if line.startswith('ncols'):
                    self._ncols = int(line.split(' ')[-1])

                elif line.startswith('nrows'):
                    self._nrows = int(line.split(' ')[-1])

                elif line.startswith('xllcorner'):
                    self._xllcorner = float(line.split(' ')[-1])

                elif line.startswith('yllcorner'):
                    self._yllcorner = float(line.split(' ')[-1])

                elif line.startswith('cellsize'):
                    self._cell_size = int(float(line.split(' ')[-1]))

                elif line.startswith('NODATA_value'):
                    cols_str = line.split(' ')[-1]
                    self._NODATA_value = int(cols_str.replace(' ', ''))

                else:
                    self._data_table.append([float(x)for x in line.split(' ')])

        self._data_table = np.asarray(self._data_table)

        self._orig_xllcorner = self.xllcorner
        self._orig_yllcorner = self.yllcorner

        self._xllcorner = 0
        self._yllcorner = 0

    def save(self, new_fname=None):

        save_fname = self._fname

        if new_fname:
            save_fname = new_fname

        self._xllcorner = self._orig_xllcorner
        self._yllcorner = self._orig_yllcorner

        with open(save_fname, 'w') as f:
            f.write(self.__str__())

    @property
    def fname(self):
        return self._fname

    @fname.setter
    def fname(self, new_fname):
        self._fname = new_fname

    @property
    def ncols(self):
        return self._ncols

    @ncols.setter
    def ncols(self, new_ncols):
        self._ncols = new_ncols

    @property
    def nrows(self):
        return self._nrows

    @nrows.setter
    def nrows(self, new_nrows):
        self._nrows = new_nrows

    @property
    def xllcorner(self):
        return self._xllcorner

    @xllcorner.setter
    def xllcorner(self, new_xllcorner):
        self._xllcorner = new_xllcorner

    @property
    def yllcorner(self):
        return self._yllcorner

    @yllcorner.setter
    def yllcorner(self, new_yllcorner):
        self._yllcorner = new_yllcorner

    @property
    def cell_size(self):
        return self._cell_size

    @cell_size.setter
    def cell_size(self, new_cell_size):
        self._cell_size = new_cell_size

    @property
    def no_data_val(self):
        return self._NODATA_value

    @no_data_val.setter
    def no_data_val(self, new_no_data_val):
        self._NODATA_value = new_no_data_val

    @property
    def data_table(self):
        return self._data_table

    @data_table.setter
    def data_table(self, new_data_table):
        self._data_table = new_data_table

    def x_max(self):
        return self.cell_size * self._ncols

    def x_min(self):
        return self._xllcorner + self._cell_size // 2

    def x_min_val(self):
        return self._xllcorner

    def y_max(self):
        return self.cell_size * self._nrows

    def y_min(self):
        return self._yllcorner + self._cell_size // 2

    def y_min_val(self):
        return self._yllcorner

    def has_file(self):
        return self._fname is not None

    def __str__(self):
        header = ''.join(['ncols ', str(self._ncols), '\nnrows ', str(self._nrows), '\nxllcorner ', str(self._xllcorner),
                          '\nyllcorner ', str(self._yllcorner), '\ncellsize ', str(self._cell_size), '\nNODATA_value ',
                          str(self._NODATA_value)])

        header += '\n'
        for row in self._data_table:
            row_str = str(row.tolist())
            row_str = row_str.replace('[', '').replace(']', '').replace(',', '')
            header += row_str + '\n'

        return header
