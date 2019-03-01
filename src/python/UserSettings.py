import os.path as osp


class UserSettings:

    FNAME = 'FireScape_Rx.ini'
    USER_SETTINGS_LOC = '../../' + FNAME
    FILE_EXT = '.ini'
    KV_SEP = ':'

    DEF_OUTPUT_DIR = '../../'
    DEF_WORKING_DIR = ''
    DEF_DEFAULT_ENVIRONMENT = 'No environment set'
    DEF_SIM_DURATION = 100.0

    def __init__(self):

        self._output_dir = self.DEF_OUTPUT_DIR
        self._working_dir = self.DEF_WORKING_DIR
        self._default_environment = self.DEF_DEFAULT_ENVIRONMENT
        self._sim_duration = self.DEF_SIM_DURATION
        self._file_exists = False

        # Check if user settings file already exists
        if osp.isfile(self.USER_SETTINGS_LOC):
            self.read()
            self._file_exists = True

        else:
            self.create_user_settings()

    def read(self):

        print('Reading settings')
        with open(self.USER_SETTINGS_LOC) as f:
            for line in f.readlines():

                if line[0] == '#':
                    continue

                # Remove newline and spaces
                line = line.strip(' ')[:-1]
                key, value = line.split(self.KV_SEP)

                # TODO: ensure directory is valid
                if key.startswith('OUTPUT_DIRECTORY'):
                    self._output_dir = value

                # TODO: ensure directory is valid
                elif key.startswith('WORKING_DIRECTORY'):
                    self._working_dir = value

                # TODO: ensure environment is valid
                elif key.startswith('DEFAULT ENVIRONMENT'):
                    self._default_environment = value

                # TODO: ensure duration is valid( < SimulationSettings.MAX_SIM_DURATION)
                elif key.startswith('SIM_DURATION'):
                    self._sim_duration = value

    def create_user_settings(self):

        print('creating user settings')
        with open(self.USER_SETTINGS_LOC, 'w') as f:

            f.write('OUTPUT_DIRECTORY' + self.KV_SEP + self._output_dir + '\n')
            f.write('WORKING_DIRECTORY' + self.KV_SEP + self._working_dir + '\n')
            f.write('DEFAULT ENVIRONMENT' + self.KV_SEP + self._default_environment + '\n')
            f.write('SIM_DURATION' + self.KV_SEP + str(self._sim_duration) + '\n')

    # TODO:
    # Can make saving user settings more fancy
    # Keep comments etc
    def save_user_settings(self):
        print('saving user settings')
        self.create_user_settings()

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir):
        self._output_dir = output_dir

    @property
    def working_dir(self):
        return self._working_dir

    @working_dir.setter
    def working_dir(self, working_dir):
        self._working_dir = working_dir

    @property
    def default_environment(self):
        return self._default_environment

    @default_environment.setter
    def default_environment(self, default_environment):
        self._default_environment = default_environment

    @property
    def sim_duration(self):
        return self._sim_duration

    #TODO: validate sim_duration?
    @sim_duration.setter
    def sim_duration(self, sim_duration):
        self._sim_duration = sim_duration

    @property
    def file_exists(self):
        return self._file_exists
