import os.path as osp
import os

class UserSettings:

    FNAME = 'FireScape_Rx.ini'
    USER_SETTINGS_LOC = '../../' + FNAME
    FILE_EXT = '.ini'
    KV_SEP = ':'

    DEF_OUTPUT_DIR = '../../'
    DEF_WORKING_DIR = ''
    DEF_SIM_DURATION = 100.0

    # DEF_WFDS_EXEC = os.path.join(os.path.abspath(os.pardir), 'fds_gnu_linux_64')
    # DEF_SMV_EXEC = osp.join(osp.abspath(os.pardir), 'smokeview_linux_64')

    def __init__(self):

        self._output_dir = self.DEF_OUTPUT_DIR
        self._working_dir = self.DEF_WORKING_DIR
        self._sim_duration = self.DEF_SIM_DURATION
        self._wfds_exec = ''
        self._smv_exec = ''

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

                # TODO: ensure duration is valid( < SimulationSettings.MAX_SIM_DURATION)
                elif key.startswith('SIM_DURATION'):
                    self._sim_duration = value

                elif key.startswith('WFDS_EXEC'):
                    self._wfds_exec = value

                elif key.startswith('SMV_EXEC'):
                    self._smv_exec = value

    def create_user_settings(self):

        print('creating user settings')
        with open(self.USER_SETTINGS_LOC, 'w') as f:

            f.write('OUTPUT_DIRECTORY' + self.KV_SEP + self._output_dir + '\n')
            f.write('WORKING_DIRECTORY' + self.KV_SEP + self._working_dir + '\n')
            f.write('SIM_DURATION' + self.KV_SEP + str(self._sim_duration) + '\n')
            f.write('WFDS_EXEC' + self.KV_SEP + str(self._wfds_exec) + '\n')
            f.write('SMV_EXEC' + self.KV_SEP + str(self._smv_exec) + '\n')

    # TODO: Can make saving user settings more fancy
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
    def sim_duration(self):
        return self._sim_duration

    # TODO: validate sim_duration?
    @sim_duration.setter
    def sim_duration(self, sim_duration):
        self._sim_duration = sim_duration

    @property
    def wfds_exec(self):
        return self._wfds_exec

    @wfds_exec.setter
    def wfds_exec(self, wfds_exec):
        self._wfds_exec = wfds_exec

    @property
    def smv_exec(self):
        return self._smv_exec

    @smv_exec.setter
    def smv_exec(self, smv_exec):
        self._smv_exec = smv_exec

    @property
    def file_exists(self):
        return self._file_exists
