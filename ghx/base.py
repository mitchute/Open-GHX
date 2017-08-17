import os
import timeit
from collections import deque

import numpy as np
import simplejson as json

from ghx.borehole import BoreholeClass
from ghx.my_print import PrintClass


class BaseGHXClass:
    """
    Base class for GHXArray
    """

    def __init__(self, json_data, loads_path, output_path, print_output=True):

        """
        Class constructor
        """
        self.timer_start = timeit.default_timer()
        errors_found = False
        self.output_path = output_path

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        with open(os.path.join(self.output_path, 'in.json'), 'w') as outfile:
            json.dump(json_data, outfile, indent=4, sort_keys=True)

        # load data into data structs
        PrintClass.my_print("....Loading GHX data")

        try:
            self.name = json_data['Name']
        except:  # pragma: no cover
            PrintClass.my_print("....'Name' key not found", 'warn')
            errors_found = True

        try:
            self.sim_years = json_data['Simulation Configuration']['Simulation Years']
        except:  # pragma: no cover
            PrintClass.my_print("....'Simulation Years' key not found", 'warn')
            errors_found = True

        try:
            self.aggregation_type = json_data['Simulation Configuration']['Aggregation Type']
        except:  # pragma: no cover
            PrintClass.my_print("....'Aggregation Type' key not found", 'warn')
            errors_found = True

        try:
            self.min_hourly_history = json_data['Simulation Configuration']['Min Hourly History']
        except:  # pragma: no cover
            PrintClass.my_print("....'Min Hourly History' key not found", 'warn')
            errors_found = True

        try:
            self.agg_load_intervals = json_data['Simulation Configuration']['Intervals']
        except:  # pragma: no cover
            PrintClass.my_print("....'Intervals' key not found", 'warn')
            errors_found = True

        try:
            self.g_func_lntts = []
            self.g_func_val = []
            for pair in json_data['G-func Pairs']:
                self.g_func_lntts.append(pair[0])
                self.g_func_val.append(pair[1])
            self.g_func_present = True
        except:  # pragma: no cover
            PrintClass.my_print("....'G-func Pairs' key not found", 'warn')
            self.g_func_present = False

        self.total_bh_length = 0

        self.ghx_list = []
        ghx_dict_list = []

        for json_data_bh in json_data['GHXs']:
            ghx_dict_list.append(json_data_bh)
            this_bh = BoreholeClass(json_data_bh, print_output)
            self.total_bh_length += this_bh.depth
            self.ghx_list.append(this_bh)

        self.borehole = BoreholeClass(self.merge_dicts(ghx_dict_list), print_output)

        try:
            PrintClass.my_print("....Importing flow rates and loads")
            load_pairs = np.genfromtxt(loads_path, delimiter=',', skip_header=1)
            self.sim_hours = []
            self.sim_loads = []
            self.total_flow_rate = []
            for pair in load_pairs:
                self.sim_hours.append(pair[0])
                self.sim_loads.append(pair[1])
                self.total_flow_rate.append(pair[2])
        except:  # pragma: no cover
            PrintClass.fatal_error(message="Error importing loads")

        if not errors_found:
            # success
            PrintClass.my_print("Simulation successfully initialized")
        else:  # pragma: no cover
            PrintClass.fatal_error(message="Error initializing BaseGHXClass")

        self.ts = self.calc_ts()
        self.temp_bh = deque()
        self.temp_mft = deque()

        self.agg_load_objects = []

        self.g_func_hourly = deque()
        self.hourly_loads = deque()

        self.agg_loads_flag = True

    def merge_dicts(self, list_of_dicts):

        """
        Merges two-level dictionaries into a single identical dictionary.
        For non-int/floats arguments, the first item in the list will remain in place.
        For int/float arguments, the mean value of the parent dictionaries will calculated.
        """

        z = {}

        for this_dict in list_of_dicts:
            for key in this_dict.keys():
                if key not in z:
                    z[key] = this_dict[key]
                    continue
                try:
                    for sub_key in this_dict[key].keys():
                        if isinstance(this_dict[key][sub_key], (float, int)):
                            z[key][sub_key] += this_dict[key][sub_key]
                        else:
                            z[key][sub_key] = this_dict[key][sub_key]
                except:
                    if isinstance(this_dict[key], (float, int)):
                        z[key] += this_dict[key]

        num_dicts = len(list_of_dicts)

        for key in z.keys():
            try:
                for sub_key in z[key].keys():
                    if isinstance(z[key][sub_key], (float, int)):
                        z[key][sub_key] /= num_dicts
            except:
                if isinstance(z[key], int) or isinstance(z[key], float):
                    z[key] /= num_dicts
        return z

    def calc_ts(self):

        """
        Calculates non-dimensional time.
        """

        try:
            ts = self.borehole.depth ** 2 / (9 * self.borehole.soil.thermal_diffusivity)
            return ts
        except:  # pragma: no cover
            PrintClass.fatal_error(message="Error calculating simulation time scale \"ts\"")

    def calc_g_func(self):

        """
        Calculate g-functions for given ground heat exchangers.
        """

        try:
            PrintClass.my_print("Calculating g-functions")
            self.g_func_present = True
            PrintClass.my_print("....Success")
        except:  # pragma: no cover
            PrintClass.fatal_error(message="Error calculating g-functions")

    def g_func(self, ln_t_ts):
        """
        Interpolates to the correct g-function value
        """

        num = len(self.g_func_lntts)
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
            PrintClass.my_print("Writing output results")
            cwd = os.getcwd()
            path_to_output_dir = os.path.join(cwd, self.output_path)

            if not os.path.exists(path_to_output_dir):
                os.makedirs(path_to_output_dir)

            # open files
            out_file = open(os.path.join(path_to_output_dir, "GHX.csv"), 'w')

            # write headers
            out_file.write("Hour, BH Temp [C], MFT [C]\n")

            for i in range(len(self.temp_bh)):
                out_file.write("%d, %0.4f, %0.4f\n" % (i + 1,
                                                       self.temp_bh[i],
                                                       self.temp_mft[i]))

            # close file
            out_file.close()

            PrintClass.my_print("....Success")

        except:  # pragma: no cover
            PrintClass.fatal_error(message="Error writing output results")
