from __future__ import division
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

        self.length = None
        self.max_length = max_length
        self.loads = deque(loads, maxlen=max_length)
        self.q = None
        self.new_q_val = None
        self.q_est = None
        self.first_sim_hour = first_sim_hour

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

        self.q = np.mean(self.loads)

    def estimate_q(self):
        """
        Estimates the average q value for the period using the modified moving average formula
        """
        self.length = len(self.loads)
        self.q_est = ((self.length - 1) * self.q_est + self.new_q_val) / self.length
