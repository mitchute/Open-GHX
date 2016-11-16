from __future__ import division

import sys
import os
import simplejson as json

from collections import deque
from ghx_constants import *
from ghx_print import *
from ghx_fluids import *
from ghx_borehole import *
from ghx_soil import *


class BaseGHX(PrintClass, ConstantClass):

    """
    Base class for GHXArray
    """

    def __init__(self, json_data, loads_path, print_output=True):

        """
        Class constructor
        """

        # init inherited classes
        PrintClass.__init__(self, print_output)
        ConstantClass.__init__(self)

        errors_found = False

        # load data into data structs
        self.my_print("Loading GHX data")

        try:
            self.name = json_data['Name']
        except:  # pragma: no cover
            self.my_print("\t'Name' key not found", self._color_warn)
            errors_found = True

        try:
            self.sim_years = json_data['Simulation Configuration']['Simulation Years']
        except:  # pragma: no cover
            self.my_print("\t'Simulation Years' key not found", self._color_warn)
            errors_found = True

        try:
            self.sim_years = json_data['Simulation Configuration']['Aggregation Type']
        except:  # pragma: no cover
            self.my_print("\t'Aggregation Type' key not found", self._color_warn)
            errors_found = True

        try:
            self.min_hourly_history = json_data['Simulation Configuration']['Min Hourly History']
        except:  # pragma: no cover
            self.my_print("\t'Min Hourly History' key not found", self._color_warn)
            errors_found = True

        try:
            self.g_func_lntts = []
            self.g_func_val = []
            for pair in json_data['G-func Pairs']:
                self.g_func_lntts.append(pair[0])
                self.g_func_val.append(pair[1])
            self.g_func_present = True
        except:  # pragma: no cover
            self.my_print("....'G-func Pairs' key not found", self._color_warn)
            self.g_func_present = False

        self.ghx_list = []

        for json_data_bh in json_data['GHXs']:
            this_bh = BoreholeClass(json_data_bh, print_output)
            self.ghx_list.append(this_bh)

        try:
            self.my_print("Importing flow rates and loads")
            load_pairs = np.genfromtxt(loads_path, delimiter=',', skip_header=1)
            self.sim_hours = []
            self.sim_loads = []
            self.total_flow_rate = []
            for pair in load_pairs:
                self.sim_hours.append(pair[0])
                self.sim_loads.append(pair[1])
                self.total_flow_rate.append(pair[2])
            self.my_print("....Success")
        except:  # pragma: no cover
            self.fatal_error(message="Error importing loads")

        if not errors_found:
            # success
            self.my_print("....Success")
        else:  # pragma: no cover
            self.fatal_error(message="Error initializing BaseGHX")

        self.sim_years = None
        self.aggregation_type = None
        self.min_hourly_history = None

        self.ts = None
        self.temp_bh = deque()
        self.temp_mft = deque()

        self.agg_load_objects = []

        self.g_func_hourly = deque()
        self.hourly_loads = deque()

        self.agg_loads_flag = True
        self.agg_load_intervals = []
        self.agg_hour = None
        self.sim_hour = None

        self.total_bh_length = None

        # calc ts
        self.calc_ts()

    def calc_ts(self):

        """
        Calculates non-dimensional time. Selects length scale based on deepest GHX
        """

        try:
            max_h = 0.0
            ground_thermal_diffusivity = 0.0

            for ghx in self.ghx_list:
                if max_h < ghx.depth:
                    max_h = ghx.depth
                ground_thermal_diffusivity += ghx.soil.thermal_diffusivity

            self.ts = max_h ** 2 / (9 * ground_thermal_diffusivity)

        except:  # pragma: no cover
            self.fatal_error(message="Error calculating simulation time scale \"ts\"")

    def calc_g_func(self):

        """
        Attempts to calculate g-functions for given ground heat exchangers. If not successful, program exits.

        More documentation to come...
        """

        try:
            self.my_print("Calculating g-functions")
            self.g_func_present = True
            self.update_g_func_interp_lists()
            self.my_print("....Success")
        except:  # pragma: no cover
            self.fatal_error(message="Error calculating g-functions")

    def g_func(self, ln_t_ts):
        """
        Interpolates to the correct g-function value
        """

        num = len(self.g_func_pairs)
        lower_index = 0
        upper_index = num - 1

        if ln_t_ts < self.g_func_lntts[lower_index]:
            # if value is below range, extrapolate down
            return ((ln_t_ts - self.g_func_lntts[lower_index]) / (
                self.g_func_lntts[lower_index + 1] - self.g_func_lntts[lower_index])) * (
                self.g_func_val[lower_index + 1] - self.g_func_val[lower_index]) + self.g_func_val[lower_index]
        elif ln_t_ts > self.g_func_lntts[upper_index]:
            # if value is above range, extrapolate up
            return ((ln_t_ts - self.g_func_lntts[upper_index]) / (
                self.g_func_lntts[upper_index - 1] - self.g_func_lntts[upper_index])) * (
                self.g_func_val[upper_index - 1] - self.g_func_val[upper_index]) + self.g_func_val[upper_index]
        else:
            # value is in range
            return np.interp(ln_t_ts, self.g_func_lntts, self.g_func_val)

    def generate_output_reports(self):  # pragma: no cover

        """
        Generates output results
        """

        try:
            self.my_print("Writing output results")
            cwd = os.getcwd()
            path_to_run_dir = os.path.join(cwd, "run")

            if not os.path.exists(path_to_run_dir):
                os.makedirs(path_to_run_dir)

            # open files
            out_file = open(os.path.join(path_to_run_dir, "GHX.csv"), 'w')

            # write headers
            out_file.write("Hour, BH Temp [C], MFT [C]\n")

            for i in range(len(self.temp_bh)):
                out_file.write("%d, %0.4f, %0.4f\n" % (i+1,
                                                       self.temp_bh[i],
                                                       self.temp_mft[i]))

            # close file
            out_file.close()

            self.my_print("....Success")

        except:
            self.fatal_error(message="Error writing output results")

