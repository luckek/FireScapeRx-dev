import os.path as osp
from UserSettings import UserSettings


class SimulationSettings:

    FILE_EXT = '.sim_settings'
    KV_SEP = ':'

    DEF_NUM_RUNS = 5  # FIXME: figure out reasonable default
    DEF_NUM_SIMS = 5  # FIXME: figure out reasonable default
    DEF_SIM_DURATION = 60.0  # FIXME: figure out reasonable default
    DEF_WIND_SPEED = 0.0  # FIXME: figure out reasonable default
    DEF_WIND_DIR = 45.0  # FIXME: figure out reasonable default
    DEF_INIT_INTENSITY = 300.0  # FIXME: figure out reasonable default
    DEF_IGNITION_START = 5.0  # FIXME: figure out reasonable default

    MAX_SIMS = 20  # FIXME: figure out reasonable maximum
    MAX_RUNS = 20  # FIXME: figure out reasonable maximum
    MAX_DURATION = 20  # FIXME: figure out reasonable maximum

    MAX_WIND_DIR = 360.0  # FIXME: could try to bring number back to w/in 0-360?

    def __init__(self, fname):

        self._num_runs = self.DEF_NUM_RUNS
        self._num_sims = self.DEF_NUM_SIMS
        self._sim_duration = self.DEF_SIM_DURATION
        self._wind_speed = self.DEF_WIND_SPEED
        self._wind_dir = self.DEF_WIND_DIR
        self._init_intensity = self.DEF_INIT_INTENSITY
        self._ignition_start = self.DEF_IGNITION_START

        user_settings = UserSettings()
        self._user_settings = user_settings

        # Check if sim settings file already exists
        if osp.isfile(fname):
            self.read(fname)

        else:

            # This should attempt to put sim settings into
            # currently set output_dir if it is a valid path
            if osp.isfile(user_settings.output_dir + fname):
                fname = user_settings.output_dir + fname

            self.create_sim_settings(fname)

    #  According to the documentation found at https://docs.python.org/3/library/exceptions.html,
    #  we should raise TypeErrors when an unintended value is passed i.e float when it should be an int.
    # Conversely, if a value is outside of the appropriate range, a ValueError should be raised
    def read(self, fname):

        # Open file
        with open(fname) as f:

            for line in f.readlines():

                # Check for comments, serves no functional purpose, could be useful for debugging
                if line[0] == '#':
                    continue

                # Split into key value pair
                key, value = line.replace('\n', '').split(':')

                try:

                    if not self.is_number(value):
                        raise TypeError('TypeError: ' + key + ' should be a valid number')

                    # Check for negative numbers(none of the sim parameters are allowed to be negative
                    # A little hackish, but it prevents the need for several 'if value < 0' statements further down.
                    # And, it seems reasonable that if the value is indeed a number and negative, it will begin with a '-'
                    if value[0] == '-':
                        raise ValueError('ValueError: ' + key + ' should be positive. Reverting to default value')

                    if key == 'NUM_RUNS':

                        # Make sure value is valid(integer and less than max runs)
                        # In the case that the value is not valid, an error is raised and the default value is kept
                        float_value = float(value)

                        if not float_value.is_integer():
                            raise TypeError('TypeError: ' + key + ' should be an integer. Reverting to default value')

                        int_value = int(float_value)

                        if int_value > self.MAX_RUNS:
                            self._num_runs = self.MAX_RUNS
                            # FIXME: print max value?
                            raise ValueError('ValueError: ' + key + ' is too large. Reverting to maximum value')

                        # elif int_value < 0:
                        #     raise ValueError('ValueError: ' + key + ' should be positive. Reverting to default value')

                        self._num_runs = int_value

                    # FIXME: could refactor this into own method?
                    elif key == 'NUM_SIMS':

                        float_value = float(value)

                        if not float_value.is_integer():
                            raise TypeError('TypeError: ' + key + ' should be an integer. Reverting to default value')

                        int_value = int(float_value)

                        if int_value > self.MAX_SIMS:
                            self._num_sims = self.MAX_SIMS
                            raise ValueError('ValueError: ' + key + ' should be less than' + str(self.MAX_SIMS) + '. Reverting to maximum value')

                        # elif int_value < 0:
                        #     raise ValueError('ValueError: ' + key + ' should be positive. Reverting to default value')

                        self._num_sims = int_value

                    elif key == 'SIM_DURATION':
                        float_value = float(value)

                        if float_value > self.MAX_DURATION: #or float_value < 0.0:
                            raise ValueError('ValueError: ' + key + ' should be less than' + str(self.MAX_DURATION) + '. Reverting to maximum value')

                        self._sim_duration = float_value

                    elif key == 'WIND_SPEED':

                        float_value = float(value)

                        # TODO: Bound wind speed?
                        # if float_value < 0.0:
                        #     raise ValueError('ValueError: ' + key + ' is outside the appropriate range. Reverting to default value')

                        self._wind_speed = float_value

                    elif key == 'WIND_DIR':
                        float_value = float(value)

                        if float_value > self.MAX_WIND_DIR: #or float_value < 0.0: # FIXME: shouldnt need to check for negative, but if do should be seperate check
                            self._wind_dir = self.MAX_WIND_DIR
                            raise ValueError('ValueError: ' + key + ' should be between less than ' + str(self.MAX_WIND_DIR) + ' degrees. Reverting to maximum value')

                        self._wind_dir = float_value

                    # TODO: bound intensity?
                    elif key == 'INIT_INTENSITY':
                        float_value = float(value)
                        self._init_intensity = float_value

                    # FIXME: figure out way to ensure ignition start < sim duration
                    elif key == 'IGNITION_START':
                        float_value = float(value)
                        self._ignition_start = float_value

                    else:
                        raise KeyError('KeyError: ' + key + '. Key will be ignored.')

                except (ValueError, TypeError, KeyError) as vtke:
                    print(vtke)

    def create_sim_settings(self, fname):
        with open(fname, 'w') as f:
            for key, value in self.get_default_settings_dict():
                f.write(key + ':' + value + '\n')

    def save(self, fname):

        if not fname.endswith(self.FILE_EXT):
            fname += self.FILE_EXT

        with open(fname, 'w') as f:
            for key, value in self.get_settings_dict():
                f.write(key + self.KV_SEP + value + '\n')

    def get_settings_dict(self):
        return {'NUM_RUNS': self._num_runs, 'NUM_SIMS': self._num_sims, 'SIM_DURATION': self._sim_duration,
                'WIND_SPEED': self._wind_speed, 'WIND_DIR': self._wind_dir, 'INIT_INTENSITY': self._init_intensity,
                'IGNITION_START': self._ignition_start}

    def get_default_settings_dict(self):
        return {'NUM_RUNS': self.DEF_NUM_SIMS, 'NUM_SIMS': self.DEF_NUM_SIMS, 'SIM_DURATION': self.DEF_SIM_DURATION,
                'WIND_SPEED': self.DEF_WIND_SPEED, 'WIND_DIR': self.DEF_WIND_DIR, 'INIT_INTENSITY': self.DEF_INIT_INTENSITY,
                'IGNITION_START': self.DEF_IGNITION_START}

    def update_settings(self, settings_dict):

        # FIXME: make sure values are valid here? this will probably only be called by the interface so
        # we may reasonably assume the values will already be valid, numerical, and that the key is also valid(incoming dict will likely be build by system)
        for key, value in settings_dict.items():

            # FIXME: incoming 'value' may already be numerical type, esp. if coming from interface.
            # So, may not need to cast to numerical type
            if key == 'NUM_RUNS':
                self._num_runs = int(value)

            elif key == 'NUM_SIMS':
                self._num_sims = int(value)

            elif key == 'SIM_DURATION':
                self._sim_duration = float(value)

            elif key == 'WIND_SPEED':
                self._wind_speed = float(value)

            elif key == 'WIND_DIR':
                self._wind_dir = float(value)

            elif key == 'INIT_INTENSITY':
                self._init_intensity = float(value)

            elif key == 'IGNITION_START':
                self._ignition_start = float(value)

    # FIXME: possible soln for checking wether or not value is number
    # TODO: Move this into utility class?
    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @property
    def num_sims(self):
        return self._num_sims

    @num_sims.setter
    def num_sims(self, num_sims):
        self._num_sims = num_sims

    @property
    def sim_duration(self):
        return self._sim_duration

    @sim_duration.setter
    def sim_duration(self, sim_duration):
        self._sim_duration = sim_duration

    @property
    def wind_speed(self):
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, wind_speed):
        self._wind_speed = wind_speed

    @property
    def wind_dir(self):
        return self._wind_dir

    @wind_dir.setter
    def wind_dir(self, wind_dir):
        self._wind_dir = wind_dir
