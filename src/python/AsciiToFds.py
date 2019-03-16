from Fds import *
from Point import Point
import numpy as np


class AsciiToFds:

    ls_template_file = os.path.abspath('../../files/test_files/fds_input/LS_template.txt')

    def __init__(self, fuel_map, dem, simulation_settings):

        self._fuel_map = fuel_map
        self._dem = dem
        self._sim_settings = simulation_settings

        self._nrows = fuel_map.nrows
        self._ncols = fuel_map.ncols

        no_data = self._dem.no_data_val

        dat_table = self._dem.data_table

        # TODO: ###handle 'no data' values###

        # NOTE: we replace NO_DATA values with inf here so that we may properly calculate the table minimum
        dat_table[dat_table == no_data] = np.inf

        # One liner to get max and min of data table
        tbl_min = dat_table.min()

        # Re assign no data values
        dat_table[dat_table == np.inf] = no_data

        # This 'zeroes out' elevation so the lowest elevation is 0 m.
        # NOTE: We do this even when tbl_min = 0.0 so that the elevation values are rounded
        # TODO: can't round inf...
        dat_table -= tbl_min
        np.round(dat_table)

        # Round to nearest tens
        self._tbl_max = round(dat_table.max(), -1)

        # FIXME:
        #self._spatial_translator = SpatialTranslator(fuel_map)

        # These are used for caching point conversions
        self._i_cache = {}
        self._j_cache = {}

    def __convert(self, fuel_map_grid):
        """ Converts manipulated ascii grid info into fds structures"""

        return self.__convert_rows_diff_elevation(fuel_map_grid)

    def __convert_same_elevation(self, fuel_map_grid):
        """ Converts manipulated ascii grid info into fds structures"""

        map_list = self.__convert_rows_same_elevation(fuel_map_grid)

        return self.__create_area_map(map_list)

    def save(self, fuel_map_grid, fire_lines, save_fname):
        """Creates FDS object that is equivalent to current fuel map, elevation model, and simulation settings"""

        # idea: populate save file dialog with .asc filename(as suggested / default filename)

        cells_above_max_z = 10

        # Calculate area mapping
        area_map = self.__convert(fuel_map_grid)

        # Grab levelset template:
        new_fds_file = FdsParser()

        fuel_map = self._fuel_map

        # Give FDS file information it needs to
        # properly create FDS file
        new_fds_file.time = self._sim_settings.sim_duration
        new_fds_file.ambient_temp = self._sim_settings.ambient_temp

        u0, v0 = self._sim_settings.wind_vector()
        new_fds_file.u0 = u0
        new_fds_file.v0 = v0

        new_fds_file.cell_size = fuel_map.cell_size

        new_fds_file.x_start = fuel_map.x_min_val()
        new_fds_file.x_end = fuel_map.x_max()

        new_fds_file.y_start = fuel_map.y_min_val()
        new_fds_file.y_end = fuel_map.y_max()

        new_fds_file.z_start = 0  # This should always be true, because we subtract min from DEM table
        new_fds_file.z_end = self._tbl_max + (cells_above_max_z * self._fuel_map.cell_size)

        ign_pts_and_times = self.convert_fire_lines(fire_lines)

        for item in ign_pts_and_times:

            p1, p2, ign_time = item

            new_fds_file.add_ign_cell(p1, p2, ign_time)

        for key in area_map:
            for point_pair in area_map[key]:

                p1, p2 = point_pair

                new_fds_file.add_veg_cell(p1, p2, key)

        # new_fds_file should now have all relevant info
        return new_fds_file.save_file(save_fname)

    # FIXME: put this kind of stuff into own class?
    # could be 'spatial translator' or something cool
    # like that. Could incorporate DEM into it as well
    # NOTE: while this is not currently used, it may be in the future.
    # It was made as part of the first iteration of the AsciiToFds routine / class
    def index_to_point(self, i, j, ofs):

        cell_size = self._fuel_map.cell_size

        if i not in self._i_cache:
            self._i_cache[i] = self._fuel_map.yllcorner + self._nrows * cell_size - i * cell_size - ofs

        if j not in self._j_cache:
            self._j_cache[j] = self._fuel_map.xllcorner + ofs + j * cell_size

        x = self._j_cache[j]
        y = self._i_cache[i]

        return Point(x, y, 0)

    # FIXME: put this kind of stuff into own class?
    # could be 'spatial translator' or something cool
    # like that. Could incorporate DEM into it as well
    def index_to_value(self, i, j):

        cell_size = self._fuel_map.cell_size

        if i not in self._i_cache:
            self._i_cache[i] = self._fuel_map.yllcorner + self._nrows * cell_size - i * cell_size

        if j not in self._j_cache:
            self._j_cache[j] = self._fuel_map.xllcorner + j * cell_size

        x = self._j_cache[j]
        y = self._i_cache[i]

        return Point(x, y, 0)

    # FIXME: this does not work
    def value_to_index(self, y, x):

        cell_size = self._fuel_map.cell_size

        j = (x - self._fuel_map.xllcorner) / cell_size
        i = ((y + self._fuel_map.yllcorner) + (self._nrows * cell_size)) / cell_size

        return Point(j, i, 0)

    # TODO: figure out something a little better
    def index_to_point_map(self):

        t_map = dict()

        cell_size = self._dem.cell_size
        init_x = self._dem.xllcorner + int(cell_size / 2)
        init_y = self._dem.yllcorner + (int((cell_size * self._nrows) - int(cell_size / 2.0)))

        current_y = init_y
        for i in range(self._nrows):
            current_x = init_x
            for j in range(self._ncols):
                t_map[(i, j)] = (int(current_x), int(current_y))
                current_x += cell_size
            current_y -= cell_size

        return t_map

    def point_to_index_map(self):

        t_map = self.index_to_point_map()

        return {b: a for a, b in t_map.items()}

    def __convert_rows_same_elevation(self, fuel_map_grid):

        untreated_conversion_dict = {}
        treated_conversion_dict = {}

        untrt_value = 1
        trt_value = 2

        i = 0
        while i < self._nrows:
            untreated_conversion_dict[i] = []
            treated_conversion_dict[i] = []

            j = 0
            while j < self._ncols:

                if fuel_map_grid[i][j] == untrt_value:

                    value_start, value_end = self.__calculate_range(i, j, fuel_map_grid, untrt_value)
                    j = value_end

                    untreated_conversion_dict[i].append((value_start, value_end))

                elif fuel_map_grid[i][j] == trt_value:

                    value_start, value_end = self.__calculate_range(i, j, fuel_map_grid, trt_value)
                    j = value_end

                    treated_conversion_dict[i].append((value_start, value_end))

                j += 1
            i += 1

        return [untreated_conversion_dict, treated_conversion_dict]

    def __convert_rows_diff_elevation(self, fuel_map_grid):

        no_dat_value = -1
        untrt_value = 1
        trt_value = 2

        area_map = {untrt_value: [], trt_value: []}
        cell_size = self._fuel_map.cell_size
        dem_grid = self._dem.data_table

        area_map[untrt_value] = []
        area_map[trt_value] = []
        area_map[no_dat_value] = []

        for i, row in enumerate(fuel_map_grid):
            for j, cell in enumerate(row):

                # Create p1 and p2
                p1 = self.index_to_value(i, j)
                p2 = self.index_to_value(i, j)

                # Add cell value to get other edge of cell
                p2.x += cell_size

                p1.y -= cell_size

                p2.z = dem_grid[i][j]

                # Append to list, mapped by fuel type
                area_map[cell].append((p1, p2))

        return area_map

    def __calculate_range(self, i, j, fuel_map, value):

        value_start = j
        value_end = j
        in_value = True

        while in_value and j < len(fuel_map[i]):

            if fuel_map[i][j] == value:
                j += 1

            else:
                in_value = False

                j -= 1
                value_end = j

        if j == self._ncols and in_value:
            value_end = j - 1

        return value_start, value_end

    def __create_area_map(self, map_list):

        area_map = {}
        offset = self._fuel_map.cell_size / 2.0

        for i, current_map in enumerate(map_list):

            area_map[i] = []
            for key in current_map:
                for item in current_map[key]:

                    # Create p1 and p2
                    p1 = self.index_to_point(key, item[0], offset)
                    p2 = self.index_to_point(key, item[1], offset)

                    # Offset b/c FDS wants start
                    # to end
                    p1.x -= offset
                    p1.y += offset

                    p2.x += offset
                    p2.y -= offset

                    # Append to list, mapped by fuel type
                    area_map[i].append((p1, p2))

        return area_map

    def convert_fire_lines(self, fire_lines):

        points_and_time = []

        offset = self._fuel_map.cell_size / 2.0

        t_map = self.point_to_index_map()

        for f_line in fire_lines:

            for l, point in enumerate(f_line.points_list()):

                i, j = t_map[point]
                x, y = point

                # Create p1 and p2
                p1 = Point(x, y, self._dem.data_table[i][j])
                p2 = Point(x, y, self._dem.data_table[i][j])

                # Offset b/c FDS wants start
                # to end
                p1.x -= offset
                p1.y -= offset

                p2.x += offset
                p2.y += offset

                # Append to list, mapped by fuel type
                points_and_time.append((p1, p2, f_line.times_list()[l]))

        return points_and_time
