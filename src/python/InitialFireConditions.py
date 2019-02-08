class InitialFireConditions:

    DEF_INIT_INTENSITY = 300.0  # FIXME: figure out reasonable default

    # FIXME: figure out reasonable default
    # By default, ignition will start at origin after 1.5s
    DEF_IGN_START_POINTS = [(0, 0, 0)]
    DEF_IGN_POINT_START_TIMES = [1.5]

    def __init__(self):

        self._intial_fire_intensity = self.DEF_INIT_INTENSITY

        # FIXME: figure out way to ensure all ignition point start times < sim duration
        self._ign_start_points = self.DEF_IGN_START_POINTS
        self._ign_point_start_times = self.DEF_IGN_POINT_START_TIMES

        # FIXME: ensure that len(self._ign_start_points) == len(self._ign_point_start_times)

    @property
    def initial_intensity(self):
        return self._intial_fire_intensity

    @initial_intensity.setter
    def initial_intensity(self, initial_fire_intensity):
        self._intial_fire_intensity = initial_fire_intensity

    @property
    def ignition_start_points(self):
        return self._ign_start_points

    @ignition_start_points.setter
    def ignition_start_points(self, ignition_start_points):
        self._ign_start_points = ignition_start_points

    @property
    def ignition_start_times(self):
        return self._ign_point_start_times

    @ignition_start_times.setter
    def ignition_start_times(self, ignition_start_times):
        self._ign_point_start_times = ignition_start_times

    @property
    def points_and_times(self):
        return list(zip(self.ignition_start_points, self.ignition_start_times))
