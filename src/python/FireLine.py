class FireLine:

    def __init__(self, points_list, times):

        assert(len(points_list) == len(times))

        self._points_list = points_list

        self._times_list = times

    def points_list(self):
        return self._points_list

    def points_set(self):
        return set(self._points_list)

    def times_list(self):
        return self._times_list

    def times_set(self):
        return set(self._times_list)

    def overlap(self, rhs):
        """
        Simple function to test if two firelines overlap
        :param rhs: the fireline we wish to check for intersection with
        :return: true if there is no overlap between the respective firelines(i.e. a non-empty intersection)
        """

        return bool(self.points_set().intersection(rhs.points_set()))

    def same(self, rhs):
        return self.points_set() == rhs.points_set()

    def start_coor(self):
        return self._points_list[0]

    def end_coor(self):
        return self._points_list[-1]

    def start_time(self):
        return self._times_list[0]

    def end_time(self):
        return self._times_list[-1]

    def __getitem__(self, i):

        return self._points_list[i], self._times_list[i]

    def __str__(self):
        return str(self._points_list) + '\n' + str(self._times_list)
