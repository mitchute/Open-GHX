from collections import deque

import numpy as np

from ghx.constants import ConstantClass


class AggregatedLoadFixed:
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


class AggregatedLoadShifting:
    """
    Class that contains a block of aggregated loads
    """

    def __init__(self, max_loads=0):
        """
        Constructor for the class
        """

        # class data

        self.is_full = False
        self.num_loads = 0
        self.max_num_loads = max_loads
        self.energy = 0
        self.energy_to_shift_out = 0
        self.g_func = 0
        self.q = 0

    def shift_energy(self, energy_in):

        if not self.is_full:
            self.num_loads += 1
            self.energy += energy_in
            if self.num_loads == self.max_num_loads:
                self.is_full = True
            return True

        self.energy_to_shift_out = self.energy/self.num_loads
        self.energy -= self.energy_to_shift_out
        self.energy += energy_in

    def calc_q(self):
        self.q = self.energy/(self.num_loads * ConstantClass.sec_in_hour)
