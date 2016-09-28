# imports
import sys
import os
import numpy as np
import simplejson as json
import CoolProp.CoolProp as CP
from collections import deque

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

        ## Class data

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

        ## initialize methods

        # get ghx data
        self.get_input(json_path)

        # get loads
        self.get_loads(loads_path)

        # calc ts
        self.calc_ts()

        # set load aggregation intervals
        self.set_load_aggregation()

        # set first aggregated load, which is zero. Need this for later
        self.agg_load_objects.append(AggregatedLoad([0], 0))

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

        except ValueError: # pragma: no cover
            if self.print_output: print("Error reading JSON data file---check file path")
            if self.print_output: print("Program exiting")
            sys.exit(1)

        # load data into data structs
        try:
            if self.print_output: print("Loading data into structs")

            # load GHX Array level inputs first

            try:
                self.name = json_data['Name']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Name' key not found")
                pass

            try:
                self.num_bh = json_data['Number BH']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Number BH' key not found")
                pass

            try:
                self.flow_rate = json_data['Flow Rate']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Flow Rate' key not found")
                pass

            try:
                self.ground_cond = json_data['Ground Cond']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Ground Cond' key not found")
                pass

            try:
                self.ground_heat_capacity = json_data['Ground Heat Capacity']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Ground Heat Capacity' key not found")
                pass

            try:
                self.ground_temp = json_data['Ground Temp']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Ground Temp' key not found")
                pass

            try:
                self.fluid = json_data['Fluid']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Fluid' key not found")
                pass

            try:
                self.sim_years = json_data['Simulation Years']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Simulation Years' key not found")
                pass

            try:
                self.aggregation_type = json_data['Aggregation Type']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Aggregation Type' key not found")
                pass

            try:
                self.g_func_pairs = json_data['G-func Pairs']
                self.g_func_present = True
                self.update_g_func_interp_lists()
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'G-func Pairs' key not found")
                pass

            # load data for each GHX
            self.load_ghx_data(json_data)

            # success
            if self.print_output: print("....Success")
        except ValueError: # pragma: no cover
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
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Name' key not found")
                pass

            try:
                self.ghx_list[i].location = json_data['GHXs'][i]['Location']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Location' key not found")
                pass

            try:
                self.ghx_list[i].bh_length = json_data['GHXs'][i]['BH Length']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'BH Length' key not found")
                pass

            try:
                self.ghx_list[i].bh_radius = json_data['GHXs'][i]['BH Radius']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'BH Radius' key not found")
                pass

            try:
                self.ghx_list[i].grout_cond = json_data['GHXs'][i]['Grout Cond']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Grout Cond' key not found")
                pass

            try:
                self.ghx_list[i].pipe_cond = json_data['GHXs'][i]['Pipe Cond']
            except ValueError: # pragma: no cover
                print("\t'Pipe Cond' key not found")
                pass

            try:
                self.ghx_list[i].pipe_out_dia = json_data['GHXs'][i]['Pipe Dia']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Pipe Dia' key not found")
                pass

            try:
                self.ghx_list[i].shank_space = json_data['GHXs'][i]['Shank Space']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Shank Space' key not found")
                pass

            try:
                self.ghx_list[i].pipe_thickness = json_data['GHXs'][i]['Pipe Thickness']
            except ValueError: # pragma: no cover
                if self.print_output: print("\t'Pipe Thickness' key not found")
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
        except ValueError: # pragma: no cover
            if self.print_output: print("Error importing loads")
            if self.print_output: print("Program exiting")
            sys.exit(1)

    def set_load_aggregation(self):

        """
        Sets the load aggregation intervals based on the type specified by the user
        """

        if self.aggregation_type == "Monthly":
            self.agg_load_intervals = [730]
        elif self.aggregation_type == "Testing":
            self.agg_load_intervals = [5, 10, 20, 40]
        else:
            self.agg_load_intervals = [1]

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
            print("Calculating g-functions")
            self.g_func_present = True
            self.update_g_func_interp_lists()
            if self.print_output: print("....Success")
        except ValueError: # pragma: no cover
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

    def aggregate_load(self, sim_hour):

        """
        Creates aggregated load object
        """

        self.agg_load_objects.append(AggregatedLoad(self.hourly_loads, sim_hour))
        self.collapse_aggregate_loads()
        self.agg_hour = 0

    def collapse_aggregate_loads(self):

        """
        Collapses aggregated loads
        """

    def calc_ts(self):

        """
        Calculates non-dimensional time. Selects length scale based on deepest GHX
        """

        max_h = 0.0

        self.ground_thermal_diff = self.ground_cond / self.ground_heat_capacity

        for i in range(self.num_bh):
            if max_h < self.ghx_list[i].bh_length:
                max_h = self.ghx_list[i].bh_length

        self.ts = max_h ** 2 / (9 * self.ground_thermal_diff)

    def generate_output_reports(self):

        """
        Generates output results
        """

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
            out_file.write("%d, %0.2f\n" %(sim_hour, temp))

        # close files
        out_file.close()

    def simulate(self):

        """
        Main simulation routine. Simulates the GHXArray object.

        More docs to come...
        """
        print("Beginning simulation")

        # calculate g-functions if not present
        if not self.g_func_present:
            if self.print_output: print("G-functions not present")
            self.calc_g_func()

        # pre-load first month of hourly g-functions
        for hour in range(hours_in_month):
            ln_t_ts = np.log((hour+1) * 3600 / self.ts)
            self.g_func_hourly.append(self.g_func(ln_t_ts))

        # set aggregate load container max length
        # length is equal to the shortest interval + 1 so we can compare against the previous load
        self.hourly_loads = deque([0]*(self.agg_load_intervals[0]+1), maxlen=self.agg_load_intervals[0]+1)

        for year in range(self.sim_years):
            for month in range(months_in_year):

                print("....Year/Month: %d/%d" %(year+1, month+1))

                for hour in range(hours_in_month):

                    self.agg_hour += 1
                    self.sim_hour += 1

                    # get raw hourly load and append to hourly list
                    load_index = month * hours_in_month + hour
                    self.hourly_loads.append(self.raw_sim_loads[load_index])

                    # calculate borehole temp
                    # hourly effects
                    temp_bh_hourly = []
                    for i in range(self.agg_hour):
                        index_cur_hour = self.agg_load_intervals[0] - i
                        index_prev_hour = self.agg_load_intervals[0]- i - 1

                        q_cur_hour = self.hourly_loads[index_cur_hour]
                        q_prev_hour = self.hourly_loads[index_prev_hour]
                        g = self.g_func_hourly[i]
                        temp_bh_hourly.append((q_cur_hour - q_prev_hour) / (2 * np.pi * self.ground_cond * self.num_bh * self.ghx_list[0].bh_length) * g)

                    # aggregated load effects
                    temp_bh_agg = []
                    for i in range(len(self.agg_load_objects)):
                        if i == 0:
                            continue
                        curr_obj = self.agg_load_objects[i]
                        prev_obj = self.agg_load_objects[i-1]

                        t = self.sim_hour - ((curr_obj.time() + prev_obj.time()) / 2.0)
                        ln_t_ts = np.log(t * 3600 / self.ts)

                        g = self.g_func(ln_t_ts)

                        temp_bh_agg.append((curr_obj.q - prev_obj.q) / (2 * np.pi * self.ground_cond * self.num_bh * self.ghx_list[0].bh_length) * g)

                    # final bh temp
                    self.temp_bh.append(self.ground_temp + sum(temp_bh_hourly) + sum(temp_bh_agg))

                    # aggregate load
                    if self.agg_hour == self.agg_load_intervals[0]:
                        self.hourly_loads.popleft()
                        self.aggregate_load(self.sim_hour)

        self.generate_output_reports()

        if self.print_output: print("Simulation complete")


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

    def __init__(self, loads, sim_hour):

        """
        Constructor for the class
        """

        self.loads = deque(loads,maxlen=len(loads))
        self.sim_hour = sim_hour
        self.q = np.mean(self.loads)

    def time(self):

        """
        :returns absolute time (in hours) when load occurred
        """

        return self.sim_hour
