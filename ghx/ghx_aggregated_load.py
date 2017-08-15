import numpy as np
from collections import deque


class AggregatedLoad:

    """
    Class that contains a block of aggregated loads
    """

    def __init__(self, loads, first_sim_hour, max_length, init=False):

        """
        Constructor for the class
        """

        # class data

        self.max_length = max_length
        self.loads = deque(loads, maxlen=max_length)
        self.q = self.calc_q()
        self.first_sim_hour = first_sim_hour
        self.keep_q_values = False

        if init:
            self.last_sim_hour = 0
        else:
            self.last_sim_hour = len(loads) + first_sim_hour
            self.calc_q()

    def time(self):

        """
        :returns absolute time (in hours) when load occurred
        """

        return self.first_sim_hour

    def calc_q(self):

        """
        Calculates the mean q value for the aggregation period
        """

        return np.mean(self.loads)
