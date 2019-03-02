import Utility as util


class FdsParser:

    file_ext = '.fds'

    def __init__(self):
        self._lines = list()

        self._head = ''
        self._title = ''
        self._misc = ''

        self._cell_size = 0

        # FIXME: could let user pick these
        self._dump_dt = 180
        self._3d_smoke = False

        self._radi_radiation = False

        self._x_start = 0
        self._x_end = 0

        self._y_start = 0
        self._y_end = 0

        self._z_start = 0
        self._z_end = 0

        self._mult = ''
        self._mesh = ''
        self._surf = []
        self._vent = []
        self._obst_dict = {}
        self._dump = ''
        self._slcf = []
        self._isof = []
        self._bndf = []

        self._time = ''

    def parse(self, fds_file):
        """Function to parse contents of an fds file, most things are parsed at a fairly high level.
        Returns true if parsing is successful"""

        with open(fds_file) as f:
            for line in f.readlines():

                line = line.replace('\n', '')

                self._lines.append(line)

                title_idx = line.find('TITLE')

                if title_idx != -1:
                    sub_str = line[title_idx:].replace('/', '').replace("'", '').strip()

                    self._title = sub_str.split("=")[1]

                if len(line) == 0 or line[0] == '-' or line[0] == 'c' or line[0] == ' ':
                    continue

                if line.startswith('&HEAD'):

                    self._head = line

                if line.startswith('&TIME'):
                    self._time = line.split('=')[1].replace('/', '').strip(' ')

            if not self._title:
                self._title = util.get_filename(fds_file)

    def save_file(self, fds_file):
        """Function to save contents of an fds file"""

        # FIXME: This could be made more general... currently hard coded from JFSP run 1
        misc_str = "&MISC   TERRAIN_CASE=.TRUE.,\n        VEG_LEVEL_SET_UNCOUPLED=.TRUE.," \
                   "\n        VEG_LEVEL_SET_COUPLED=.FALSE./\n\n"

        # FIXME: This could be made more general... currently hard coded from JFSP run 1
        untrt_str = "&SURF ID ='untrt'\nFREE_SLIP=.TRUE.\nVEG_LEVEL_SET_SPREAD =.TRUE.\nVEG_LSET_ELLIPSE=.TRUE.\n" \
                    "VEG_LSET_SURFACE_FIRE_HEAD_ROS_MODEL='ROTHERMEL'\nVEG_LSET_CROWN_FIRE_HEAD_ROS_MODEL= 'SR'\n" \
                    "VEG_LSET_MODEL_FOR_PASSIVE_ROS = 'SR'\nVEG_LSET_ROTH_ZEROWINDSLOPE_ROS = 0.007118\n" \
                    "VEG_LSET_HEAT_OF_COMBUSTION=18000\nVEG_LSET_BETA = 0.0173\nVEG_LSET_SIGMA = 5788\n" \
                    "VEG_LSET_SURF_HEIGHT = 0.254\nVEG_LSET_SURF_LOAD = 2.24592\nVEG_LSET_CHAR_FRACTION = 0.2\n" \
                    "VEG_LSET_CANOPY_FMC=1\nVEG_LSET_WAF_SHELTERED = 0.09\nVEG_LSET_CANOPY_BULK_DENSITY= 0.089\n" \
                    "VEG_LSET_CANOPY_HEIGHT= 23\nVEG_LSET_CANOPY_BASE_HEIGHT = 0\n" \
                    "VEG_LSET_ROTHFM10_ZEROWINDSLOPE_ROS = 0.007118\nPART_ID='TE'\nNPPC = 1\nVEL = -0.01" \
                    "\nRGB=122,117,48 /\n\n"

        # FIXME: This could be made more general... currently hard coded from JFSP run 1
        trt_str = "&SURF ID ='trt'\nFREE_SLIP=.TRUE.\nVEG_LEVEL_SET_SPREAD =.TRUE.\nVEG_LSET_ELLIPSE=.TRUE.\n" \
                  "VEG_LSET_SURFACE_FIRE_HEAD_ROS_MODEL='ROTHERMEL'\nVEG_LSET_CROWN_FIRE_HEAD_ROS_MODEL= 'SR'\n" \
                  "VEG_LSET_MODEL_FOR_PASSIVE_ROS = 'SR'\nVEG_LSET_ROTH_ZEROWINDSLOPE_ROS = 0.007118\n" \
                  "VEG_LSET_HEAT_OF_COMBUSTION=18000\nVEG_LSET_BETA = 0.0173\nVEG_LSET_SIGMA = 5788\n" \
                  "VEG_LSET_SURF_HEIGHT = 0.254\nVEG_LSET_SURF_LOAD = 2.24592\nVEG_LSET_CHAR_FRACTION = 0.2\n" \
                  "VEG_LSET_CANOPY_FMC=1\nVEG_LSET_WAF_SHELTERED = 0.18\nVEG_LSET_CANOPY_BULK_DENSITY= 0.037\n" \
                  "VEG_LSET_CANOPY_HEIGHT= 23\nVEG_LSET_CANOPY_BASE_HEIGHT = 11\n" \
                  "VEG_LSET_ROTHFM10_ZEROWINDSLOPE_ROS = 0.007118\nPART_ID='TE'\nNPPC = 1\nVEL = -0.01" \
                  "\nRGB=0,0,0 /\n\n"

        # FIXME: This could be made more general... currently hard coded from JFSP run 1
        part_id_str = "-- Thermal Elements\n&PART ID='TE',\nAGE=9999,\nTE_BURNTIME=2.5,\nMASSLESS=.TRUE.," \
                      "\nSAMPLING_FACTOR=30,\nCOLOR='BLACK' /\n\n"

        fds_fname = util.get_filename(fds_file)

        # FIXME: this could be a little different / more general?
        self._head = fds_fname
        self._title = fds_fname

        with open(fds_file, 'w') as f:

            f.write("&HEAD CHID='" + self._head + "',TITLE='" + self._title + "' /\n\n")

            # Calculate mesh size
            mesh_i = self._x_end // self._cell_size
            mesh_j = self._y_end // self._cell_size
            mesh_k = self._z_end // self._cell_size

            ijk_str = ','.join([str(int(mesh_i)), str(int(mesh_j)), str(int(mesh_k))])
            xb_str = ','.join([str(int(self._x_start)), str(int(self._x_end)), str(int(self._y_start)),
                               str(int(self._y_end)), str(int(self._z_start)), str(int(self._z_end))])

            f.write("&MESH IJK=" + ijk_str + ", XB=" + xb_str + ' /\n\n')

            f.write("&TIME T_END=" + str(self.time) + ',LOCK_TIME_STEP=.TRUE./\n\n')
            f.write(misc_str)
            f.write("&RADI RADIATION=." + str(self._radi_radiation).upper() + '. /\n\n')

            # NOTE: untrt rgb = trt rgb?
            f.write('-- Unique FVS stands\n')
            f.write(untrt_str)
            f.write(trt_str)
            f.write(part_id_str)

            f.write("-- Ignitor fire\n")
            for i, ign_cell in enumerate(self._vent):

                p1, p2, ign_time = ign_cell

                x1 = p1.x
                y1 = p1.y
                z1 = p1.z

                x2 = p2.x
                y2 = p2.y
                z2 = p2.z

                ign_id = 'P' + str(i)
                xb_str = ','.join([str(int(x1)), str(int(x2)), str(int(y1)), str(int(y2)), str(int(z1)), str(z2)])

                f.write("&SURF ID='" + ign_id + "',VEG_LSET_IGNITE_TIME=" + str(ign_time) + ",RGB=255,0,0 /\n")
                f.write("&VENT XB=" + xb_str + ",SURF_ID='" + ign_id + "' /\n")

            f.write("\n-- Vegetation\n")
            for surf_id in self._obst_dict:
                for veg in self._obst_dict[surf_id]:

                    p1, p2 = veg

                    x1 = p1.x
                    y1 = p1.y
                    z1 = p1.z

                    x2 = p2.x
                    y2 = p2.y
                    z2 = p2.z

                    xb_str = ','.join([str(int(x1)), str(int(x2)), str(int(y1)), str(int(y2)), str(int(z1)), str(z2)])
                    f.write("&OBST XB=" + xb_str + ", SURF_ID='" + surf_id + "' /\n")

            f.write('\n')

            f.write("-- Outputs\n")
            f.write("&DUMP DT_OUTPUT_LS=180,SMOKE3D=." + str(self._3d_smoke).upper() + ". /\n\n")

            f.write("-- END of Input file\n")
            f.write("&TAIL /")

        return True

    # TODO: create setters for these values
    @property
    def time(self):
        return self._time

    @property
    def title(self):
        return self._title

    @property
    def head(self):
        head_str = self._head.split('=')[1].replace('/', '').replace("'", '').strip(' ')
        return head_str

    def add_ign_cell(self, p1, p2, time):
        self._vent.append((p1, p2, time))

    def _add_obst(self, p1, p2, surf_id):

        if surf_id not in self._obst_dict:
            self._obst_dict[surf_id] = []

        self._obst_dict[surf_id].append((p1, p2))

    def add_veg_cell(self, p1, p2, fuel_type):

        fuel_str = ''

        if fuel_type == 1:
            fuel_str = 'untrt'

        elif fuel_type == 2:
            fuel_str = 'trt'

        self._add_obst(p1, p2, fuel_str)

    @property
    def cell_size(self):
        return self._cell_size

    @cell_size.setter
    def cell_size(self, new_size):
        self._cell_size = new_size

    @property
    def x_start(self):
        return self._x_start

    @x_start.setter
    def x_start(self, new_x):
        self._x_start = new_x

    @property
    def x_end(self):
        return self._x_end

    @x_end.setter
    def x_end(self, new_x):
        self._x_end = new_x

    @property
    def y_start(self):
        return self._y_start

    @y_start.setter
    def y_start(self, new_y):
        self._y_start = new_y

    @property
    def y_end(self):
        return self._y_end

    @y_end.setter
    def y_end(self, new_y):
        self._y_end = new_y

    @property
    def z_start(self):
        return self._z_start

    @z_start.setter
    def z_start(self, new_z):
        self._z_start = new_z

    @property
    def z_end(self):
        return self._z_end

    @z_end.setter
    def z_end(self, new_z):
        self._z_end = new_z
