import numpy as np
import random


class TimeSeries:

    def __init__(self, time, magnitude, id_):
        self.time = time
        self.magnitude = magnitude
        self._id = id_


class TimeSeriesOriginal(TimeSeries):

    def __init__(self, time, magnitude, id_, standarize=True):
        super().__init__(time, magnitude, id_)
        if standarize:
            self.standardize_magnitude()

    def standardize_magnitude(self):
        mean = self.magnitude.mean()
        std = self.magnitude.std()
        self.magnitude -= mean
        self.magnitude /= std

    def run_sliding_window(self, time_window=250, time_step=10):
        t = self.time
        t_0 = t[0]
        t_last = t[-1]
        start_time = t_0
        end_time = start_time + time_window
        result = []
        i = 0
        while True:
            indices = np.where(np.logical_and(t >= start_time, t < end_time))[0]
            if len(indices) > 0:
                x = self.time[indices]
                y = self.magnitude[indices]
                subsequence_id = '{0}.{1}'.format(self._id, i)
                subsequence = TimeSeriesSubsequence(x, y, subsequence_id,
                                                    self._id)
                subsequence.zeroify_time()
                result.append(subsequence)
            if end_time > t_last:
                break
            start_time += time_step
            end_time += time_step
            i += 1
        return result

    def get_random_subsequences(self, n, time_window=250, time_step=10):
        subsequences = self.run_sliding_window(time_window, time_step)
        return random.sample(subsequences, n)


class TimeSeriesSubsequence(TimeSeries):

    def __init__(self, time, magnitude, id_, original_id):
        super().__init__(time, magnitude, id_)
        self.original_id = original_id

    def zeroify_time(self):
        t0 = self.time[0]
        self.time -= t0