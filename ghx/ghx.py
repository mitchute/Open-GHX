# imports
import sys
import os
import numpy as np
import simplejson as json
import CoolProp.CoolProp as CP
from collections import deque
import timeit

# *hopefully* small number of globals
months_in_year = 12
hours_in_month = 730
hours_in_year = months_in_year * hours_in_month


def last_day_of_month(month):

    """
    Returns the last day of the given month
    :param month: month of year (0-11)
    :return: last day of given month
    """

    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]


class GHXArray:

    """
    GHXArray is the class object that holds the information that defines a ground heat exchanger array.
    This could be a single borehole, or a field with an arbitrary number of boreholes at arbitrary locations.
    """

    def __init__(self, json_path, loads_path, print_output=True):

        """
        Constructor for the class. Call it with the path to the json input file and the csv loads file.

        Calls get_input and get_loads to load data into structs.

        GHXArray(<json_path>, <loads_path>)
        """

        # class data
        self.timer_start = timeit.default_timer()
        self.name = ""
        self.num_bh = 0
        self.flow_rate = 0.0
        self.ground_cond = 0.0
        self.ground_heat_capacity = 0.0
        self.ground_temp = 0.0
        self.fluid = ""
        self.sim_years = 0
        self.aggregation_type = ""
        self.ghx_list = []
        self.g_func_pairs = []
        self.g_func_present = False
        self.print_output = print_output

        self.g_func_lntts = []
        self.g_func_val = []

        self.load_pairs = []

        self.raw_sim_hours = []
        self.raw_sim_loads = []

        self.ground_thermal_diff = 0.0

        self.ts = 0.0
        self.temp_bh = deque()

        self.agg_load_objects = []

        self.g_func_hourly = deque()
        self.hourly_loads = deque()

        self.agg_load_intervals = []
        self.agg_hour = 0
        self.sim_hour = 0
        self.min_hourly_history = 0

        self.total_bh_length = 0

        # initialize methods

        # get ghx data
        self.get_input(json_path)

        # get loads
        self.get_loads(loads_path)

        # calc ts
        self.calc_ts()

        # set load aggregation intervals
        self.set_load_aggregation()

        # set first aggregated load, which is zero. Need this for later
        self.agg_load_objects.append(AggregatedLoad([0], 0, True))

    def get_input(self, json_path):

        """
        Reads data from the json file using the simplejson python library.
        If the json data is loaded successfully, the GHXArray data structure is populated.
        If data load is not successful, program exits.

        :param json_path: path to the json input file containing information about the GHX array
        """

        # read from JSON file
        try:
            if self.print_output: print("Reading JSON input")

            with open(json_path) as json_file:
                json_data = json.load(json_file)

            if self.print_output: print("....Success")

        except ValueError:  # pragma: no cover
            if self.print_output: print("Error reading JSON data file---check file path")
            if self.print_output: print("Program exiting")
            sys.exit(1)

        # load data into data structs
        try:
            if self.print_output: print("Loading data into structs")

            # load GHX Array level inputs first

            try:
                self.name = json_data['Name']
            except ValueError:  # pragma: no cover
                if self.print_output: print("\t'Name' key not found")
                pass

            try:
                self.num_bh = json_data['Number BH']
            except ValueError:  # pragma: no cover
                if self.print_output: print("\t'Number BH' key not found")
                pass

            try:
                self.flow_rate = json_data['Flow Rate']
            except ValueError:  # pragma: no cover
                if self.print_output: print("\t'Flow Rate' key not found")
                pass

            try:
                self.ground_cond = json_data['Ground Cond']
            except ValueError:  # pragma: no cover
                if self.print_output: print("\t'Ground Cond' key not found")
                pass

            try:
                self.ground_heat_capacity = json_data['Ground Heat Capacity']
            except ValueError:  # pragma: no cover
                if self.print_output: print("\t'Ground Heat Capacity' key not found")
                pass

            try:
                self.ground_temp = json_data['Ground Temp']
            except ValueError:  # pragma: no cover
                if self.print_output: print("\t'Ground Temp' key not found")
                pass

            try:
                self.fluid = json_data['Fluid']
            except ValueError:  # pragma: no cover
                if self.print_output: print("\t'Fluid' key not found")
                pass

            try:
                self.sim_years = json_data['Simulation Years']
            except ValueError:  # pragma: no cover
                if self.print_output: print("\t'Simulation Years' key not found")
                pass

            try:
                self.aggregation_type = json_data['Aggregation Type']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Aggregation Type' key not found")
                pass

            try:
                self.min_hourly_history = json_data['Min Hourly History']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Min Hourly History' key not found")
                pass

            try:
                self.g_func_pairs = json_data['G-func Pairs']
                self.g_func_present = True
                self.update_g_func_interp_lists()
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'G-func Pairs' key not found")
                pass

            # load data for each GHX
            self.load_ghx_data(json_data)

            # success
            if self.print_output: print("....Success")
        except ValueError:  # pragma: no cover
            if self.print_output: print("Error loading data into data structs")
            if self.print_output: print("Program exiting")
            sys.exit(1)

    def load_ghx_data(self, json_data):

        """
        Instantiate and load data into GHX class for individual ground heat exchangers.
        If key values are not found in input file, messages output to the user.

        :param json_data: json data loaded from input file
        """

        # num ghx's
        num_ghx = len(json_data['GHXs'])

        # read json data into GHX class for each ghx
        for i in range(num_ghx):
            # new instance of GHX class on GHX list
            self.ghx_list.append(GHX())

            # import GHX data
            try:
                self.ghx_list[i].name = json_data['GHXs'][i]['Name']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Name' key not found")
                pass

            try:
                self.ghx_list[i].location = json_data['GHXs'][i]['Location']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Location' key not found")
                pass

            try:
                self.ghx_list[i].bh_length = json_data['GHXs'][i]['BH Length']
                self.total_bh_length += json_data['GHXs'][i]['BH Length']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'BH Length' key not found")
                pass

            try:
                self.ghx_list[i].bh_radius = json_data['GHXs'][i]['BH Radius']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'BH Radius' key not found")
                pass

            try:
                self.ghx_list[i].grout_cond = json_data['GHXs'][i]['Grout Cond']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Grout Cond' key not found")
                pass

            try:
                self.ghx_list[i].pipe_cond = json_data['GHXs'][i]['Pipe Cond']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Pipe Cond' key not found")
                pass

            try:
                self.ghx_list[i].pipe_out_dia = json_data['GHXs'][i]['Pipe Dia']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Pipe Dia' key not found")
                pass

            try:
                self.ghx_list[i].shank_space = json_data['GHXs'][i]['Shank Space']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Shank Space' key not found")
                pass

            try:
                self.ghx_list[i].pipe_thickness = json_data['GHXs'][i]['Pipe Thickness']
            except ValueError:  # pragma: no cover
                if self.print_output: print("....'Pipe Thickness' key not found")
                pass

    def get_loads(self, load_path):

        """
        Reads loads from the load input file. If data load is not successful, program exits.

        :param load_path: path of csv file containing time series loads
        """

        try:
            if self.print_output: print("Importing loads")
            self.load_pairs = np.genfromtxt(load_path, delimiter=',', names=True)
            self.update_load_lists()
            if self.print_output: print("....Success")
        except ValueError:  # pragma: no cover
            if self.print_output: print("Error importing loads")
            if self.print_output: print("Program exiting")
            sys.exit(1)

    def calc_ts(self):

        """
        Calculates non-dimensional time. Selects length scale based on deepest GHX
        """

        try:
            max_h = 0.0
            self.ground_thermal_diff = self.ground_cond / self.ground_heat_capacity

            for i in range(self.num_bh):
                if max_h < self.ghx_list[i].bh_length:
                    max_h = self.ghx_list[i].bh_length

            self.ts = max_h ** 2 / (9 * self.ground_thermal_diff)

        except ValueError: # pragma: no cover
            if self.print_output: print("Error calculating simulation time scale \"ts\"")
            if self.print_output: print("Program exiting")
            sys.exit(1)

    def set_load_aggregation(self):

        """
        Sets the load aggregation intervals based on the type specified by the user.

        Intervals must be integer multiples.
        """

        if self.aggregation_type == "Monthly":
            self.agg_load_intervals = [730]
        elif self.aggregation_type == "Monthly-Annual":
            self.agg_load_intervals = [730, 8760]
        elif self.aggregation_type == "Weekly-Monthly-Annual":
            self.agg_load_intervals = [146, 730, 8760]
        elif self.aggregation_type == "Testing":
            self.agg_load_intervals = [5, 10, 20, 40]
        elif self.aggregation_type == "None":
            self.agg_load_intervals = [hours_in_year * self.sim_years]
            self.min_hourly_history = 0
        else:
            if self.print_output: print("Load aggregation interval not recognized")
            if self.print_output: print("....Defaulting to monthly intervals")
            self.agg_load_intervals = [730]

    def dens(self, temp_in_c):

        """
        Determines the fluid density as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid density.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        """
        return CP.PropsSI('D', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    def cp(self, temp_in_c):

        """
        Determines the fluid specific heat as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid specific heat.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        """

        return CP.PropsSI('C', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    def calc_g_func(self):

        """
        Attempts to calculate g-functions for given ground heat exchangers. If not successful, program exits.

        More documentation to come...
        """

        try:
            if self.print_output: print("Calculating g-functions")
            self.g_func_present = True
            self.update_g_func_interp_lists()
            if self.print_output: print("....Success")
        except ValueError:  # pragma: no cover
            if self.print_output: print("Error calculating g-functions")
            if self.print_output: print("Program exiting")
            sys.exit(1)

    def update_g_func_interp_lists(self):

        """
        Because g-functions are read in as pairs, we need to convert the t/ts and g-func values into individual lists
        so we can use the built in python interpolation routines.
        This takes the given g-function pairs and converts to individual lists.

        Called every time the g-functions are updated.
        """

        num = len(self.g_func_pairs)

        for i in range(num):
            self.g_func_lntts.append(self.g_func_pairs[i][0])
            self.g_func_val.append(self.g_func_pairs[i][1])

    def update_load_lists(self):

        """
        Converts the loads data into single lists.
        """
        num = len(self.load_pairs)

        for i in range(num):
            self.raw_sim_hours.append(self.load_pairs[i][0])
            self.raw_sim_loads.append(self.load_pairs[i][1])

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

    def aggregate_load(self):

        """
        Creates aggregated load object
        """

        if len(self.agg_load_intervals) > 1:
            self.collapse_aggregate_loads()

        prev_sim_hour = self.agg_load_objects[-1].last_sim_hour

        agg_loads = []

        for i in range(self.agg_load_intervals[0]):
            agg_loads.append(self.hourly_loads[i])

        self.agg_load_objects.append(AggregatedLoad(agg_loads, prev_sim_hour))

    def collapse_aggregate_loads(self):

        """
        Collapses aggregated loads
        """

        agg_load_objects_update = []

        i = 0
        while i < len(self.agg_load_objects):
            if i == 0:  # keep '0' time object
                agg_load_objects_update.append(self.agg_load_objects[i])
                i += 1
                continue
            elif len(self.agg_load_objects[i].loads) == self.agg_load_intervals[-1]:  # already max agg interval
                agg_load_objects_update.append(self.agg_load_objects[i])
                i += 1
                continue
            else:
                k = len(self.agg_load_intervals) - 1
                while k >= 0:
                    temp_objs = []
                    agg_int = self.agg_load_intervals[k]
                    for j in range(i, len(self.agg_load_objects)):
                        if len(self.agg_load_objects[j].loads) == agg_int:
                            temp_objs.append(self.agg_load_objects[j])
                        else:
                            continue
                    num_objs = len(temp_objs)
                    i += num_objs
                    if num_objs > 0:
                        if num_objs*agg_int >= self.agg_load_intervals[k+1]:
                            agg_load_objects_update.append(self.merge_agg_load_objs(temp_objs))
                        else:
                            for l in range(len(temp_objs)):
                                agg_load_objects_update.append(temp_objs[l])
                    k -= 1


        self.agg_load_objects = agg_load_objects_update

    def merge_agg_load_objs(self, obj_list):

        """
        Merges AggregatedLoad objects into a single AggregatedLoad object

        :return: merged AggregatedLoad object
        """

        loads = []
        min_hour = hours_in_year * self.sim_years
        max_hour = 0

        for this_obj in obj_list:
            for i in range(len(this_obj.loads)):
                loads.append(this_obj.loads[i])
            if min_hour > this_obj.first_sim_hour:
                min_hour = this_obj.first_sim_hour
            if max_hour < this_obj.last_sim_hour:
                max_hour = this_obj.last_sim_hour

        return AggregatedLoad(loads, min_hour)

    def generate_output_reports(self):

        """
        Generates output results
        """

        try:
            if self.print_output: print("Writing output results")
            cwd = os.getcwd()
            path_to_run_dir = os.path.join(cwd, "run")

            if not os.path.exists(path_to_run_dir):
                os.makedirs(path_to_run_dir)

            # open files
            out_file = open(os.path.join(path_to_run_dir, "GHX.csv"), 'w')

            # write headers
            out_file.write("Hour, BH Temp [C]\n")

            sim_hour = 0
            for temp in self.temp_bh:
                sim_hour += 1
                out_file.write("%d, %0.4f\n" %(sim_hour, temp))

            # close files
            out_file.close()

            if self.print_output: print("....Success")

        except:
            if self.print_output: print("Error writing output results")
            if self.print_output: print("Program exiting")
            sys.exit(1)

    def simulate(self):

        """
        Main simulation routine. Simulates the GHXArray object.

        More docs to come...
        """
        if self.print_output: print("Beginning simulation")

        # calculate g-functions if not present
        if not self.g_func_present:
            if self.print_output: print("G-functions not present")
            self.calc_g_func()

        # pre-load hourly g-functions
        for hour in range(self.agg_load_intervals[0] + self.min_hourly_history):
            ln_t_ts = np.log((hour+1) * 3600 / self.ts)
            self.g_func_hourly.append(self.g_func(ln_t_ts))

        # set aggregate load container max length
        len_hourly_loads = self.min_hourly_history + self.agg_load_intervals[0]
        self.hourly_loads = deque([0]*len_hourly_loads, maxlen=len_hourly_loads)

        for year in range(self.sim_years):
            for month in range(months_in_year):

                if self.print_output: print("....Year/Month: %d/%d" %(year+1, month+1))

                for hour in range(hours_in_month):

                    self.agg_hour += 1
                    self.sim_hour += 1

                    # get raw hourly load and append to hourly list
                    load_index = month * hours_in_month + hour
                    self.hourly_loads.append(self.raw_sim_loads[load_index])

                    # calculate borehole temp
                    # hourly effects
                    temp_bh_hourly = []
                    start_hourly = len(self.hourly_loads) - 1
                    end_hourly  = start_hourly - self.agg_hour
                    g_func_index = -1
                    for i in range(start_hourly, end_hourly, -1):
                        g_func_index += 1
                        q_curr = self.hourly_loads[i]
                        q_prev = self.hourly_loads[i - 1]
                        g = self.g_func_hourly[g_func_index]
                        temp_bh_hourly.append((q_curr - q_prev) /
                                              (2 * np.pi * self.ground_cond * self.total_bh_length) * g)

                    # aggregated load effects
                    temp_bh_agg = []
                    for i in range(len(self.agg_load_objects)):
                        if i == 0:
                            continue
                        curr_obj = self.agg_load_objects[i]
                        prev_obj = self.agg_load_objects[i-1]

                        t_agg = self.sim_hour - curr_obj.time()
                        ln_t_ts = np.log(t_agg * 3600 / self.ts)
                        g = self.g_func(ln_t_ts)
                        temp_bh_agg.append((curr_obj.q - prev_obj.q) /
                                           (2 * np.pi * self.ground_cond * self.total_bh_length) * g)

                    # aggregate load
                    if self.agg_hour == self.agg_load_intervals[0] + self.min_hourly_history - 1:
                        # this has one extra value for comparative purposes
                        # need to get rid of it here
                        self.hourly_loads.popleft()

                        # create new aggregated load object
                        self.aggregate_load()

                        # reset aggregation hour to '0'
                        self.agg_hour = self.agg_hour - self.agg_load_intervals[0]

                    # final bh temp
                    T_BH_ave = sum(temp_bh_agg)
                    T_BH_hour = sum(temp_bh_hourly)
                    T_BH = self.ground_temp + T_BH_hour + T_BH_ave
                    self.temp_bh.append(T_BH)

        self.generate_output_reports()

        if self.print_output: print("Simulation complete")
        if self.print_output: print("Simulation time: %0.3f sec" %(timeit.default_timer() - self.timer_start))


class GHX:

    """
    Class that contains the information for a single ground heat exchanger.
    """

    def __init__(self):

        """
        Constructor for the class.
        """

        self.name = ""
        self.location = []
        self.bh_length = 0.0
        self.bh_radius = 0.0
        self.grout_cond = 0.0
        self.pipe_cond = 0.0
        self.pipe_out_dia = 0.0
        self.shank_space = 0.0
        self.pipe_thickness = 0.0

    def calc_inside_convection_res(self):

        """
        Calculates the inside convection resistance.

        More docs to come...
        """

        return 0

    def calc_resistance(self):

        """
        Calc total thermal resistance of the borehole

        More docs to come...
        """

        self.calc_inside_convection_res()


class AggregatedLoad:

    """
    Class that contains a block of aggregated loads
    """

    def __init__(self, loads, first_sim_hour, init=False):

        """
        Constructor for the class
        """

        self.loads = deque(loads, maxlen=len(loads))
        if init:
            self.last_sim_hour = 0
        else:
            self.last_sim_hour = len(loads) + first_sim_hour
        self.first_sim_hour = first_sim_hour
        self.q = np.mean(self.loads)

    def time(self):

        """
        :returns absolute time (in hours) when load occurred
        """

        return self.first_sim_hour
