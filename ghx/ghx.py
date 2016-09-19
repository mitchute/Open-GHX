
import sys
import numpy as np
import simplejson as json
import CoolProp.CoolProp as CP


class GHXArray:
    """
    GHXArray is the class object that holds the information that defines a ground heat exchanger array.
    This could be a single borehole, or a field with an arbitrary number of boreholes at arbitrary locations.
    """

    def __init__(self, json_path, loads_path, print_output=True):

        """
        Constructor for the class. Call it wil the path to the json input file and the csv loads file.

        Calls get_input and get_loads to load data into structs.

        GHXArray(<json_path>, <loads_path>)
        """

        self.name = ""
        self.num_bh = 0
        self.flow_rate = 0.0
        self.ground_cond = 0.0
        self.ground_heat_capacity = 0.0
        self.ground_temp = 0.0
        self.fluid = ""
        self.sim_years = 0
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
        self.temp_bh = []

        # ghx data
        self.get_input(json_path)

        # get loads
        self.get_loads(loads_path)

        # calc ts
        self.calc_ts()

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

        except:
            if self.print_output: print("Error reading JSON data file---check file path")
            if self.print_output: print("Program exiting")
            sys.exit(1)

        # load data into data structs
        try:
            if self.print_output: print("Loading data into structs")

            # load GHX Array level inputs first

            try:
                self.name = json_data['Name']
            except:
                if self.print_output: print("\t'Name' key not found")
                pass

            try:
                self.num_bh = json_data['Number BH']
            except:
                if self.print_output: print("\t'Number BH' key not found")
                pass

            try:
                self.flow_rate = json_data['Flow Rate']
            except:
                if self.print_output: print("\t'Flow Rate' key not found")
                pass

            try:
                self.ground_cond = json_data['Ground Cond']
            except:
                if self.print_output: print("\t'Ground Cond' key not found")
                pass

            try:
                self.ground_heat_capacity = json_data['Ground Heat Capacity']
            except:
                if self.print_output: print("\t'Ground Heat Capacity' key not found")
                pass

            try:
                self.ground_temp = json_data['Ground Temp']
            except:
                if self.print_output: print("\t'Ground Temp' key not found")
                pass

            try:
                self.fluid = json_data['Fluid']
            except:
                if self.print_output: print("\t'Fluid' key not found")
                pass

            try:
                self.sim_years = json_data['Simulation Years']
            except:
                if self.print_output: print("\t'Simulation Years' key not found")
                pass

            try:
                self.g_func_pairs = json_data['G-func Pairs']
                self.g_func_present = True
                self.update_g_func_interp_lists()
            except:
                if self.print_output: print("\t'G-func Pairs' key not found")
                pass

            # load data for each GHX
            self.load_ghx_data(json_data)

            # success
            if self.print_output: print("....Success")
        except:
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
            except:
                if self.print_output: print("\t'Name' key not found")
                pass

            try:
                self.ghx_list[i].location = json_data['GHXs'][i]['Location']
            except:
                if self.print_output: print("\t'Location' key not found")
                pass

            try:
                self.ghx_list[i].bh_length = json_data['GHXs'][i]['BH Length']
            except:
                if self.print_output: print("\t'BH Length' key not found")
                pass

            try:
                self.ghx_list[i].bh_radius = json_data['GHXs'][i]['BH Radius']
            except:
                if self.print_output: print("\t'BH Radius' key not found")
                pass

            try:
                self.ghx_list[i].grout_cond = json_data['GHXs'][i]['Grout Cond']
            except:
                if self.print_output: print("\t'Grout Cond' key not found")
                pass

            try:
                self.ghx_list[i].pipe_cond = json_data['GHXs'][i]['Pipe Cond']
            except:
                print("\t'Pipe Cond' key not found")
                pass

            try:
                self.ghx_list[i].pipe_out_dia = json_data['GHXs'][i]['Pipe Dia']
            except:
                if self.print_output: print("\t'Pipe Dia' key not found")
                pass

            try:
                self.ghx_list[i].shank_space = json_data['GHXs'][i]['Shank Space']
            except:
                if self.print_output: print("\t'Shank Space' key not found")
                pass

            try:
                self.ghx_list[i].pipe_thickness = json_data['GHXs'][i]['Pipe Thickness']
            except:
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
        except:
            if self.print_output: print("Error importing loads")
            if self.print_output: print("Program exiting")
            sys.exit(1)

    def dens(self, temp_in_c):

        """
        Determines the fluid density as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid density.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        :returns: float
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
        except:
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
            return ((ln_t_ts - self.g_func_lntts[lower_index]) / (self.g_func_lntts[lower_index + 1] - self.g_func_lntts[lower_index])) * (self.g_func_val[lower_index + 1] - self.g_func_val[lower_index]) + self.g_func_val[lower_index]
        elif ln_t_ts > self.g_func_lntts[upper_index]:
            # if value is above range, extrapolate up
            return ((ln_t_ts - self.g_func_lntts[upper_index]) / (self.g_func_lntts[upper_index - 1] - self.g_func_lntts[upper_index])) * (self.g_func_val[upper_index - 1] - self.g_func_val[upper_index]) + self.g_func_val[upper_index]
        else:
            # value is in range
            return np.interp(ln_t_ts, self.g_func_lntts, self.g_func_val)

    def calc_aggregate_load(self):

        """
        Calculates aggregated load
        """

        return 0

    def calc_ts(self):

        """
        Calculates non-dimensional time.

        Selects length scale based on deepest GHX
        """

        max_h = 0.0

        self.ground_thermal_diff = self.ground_cond / self.ground_heat_capacity

        for i in range(self.num_bh):
            if max_h < self.ghx_list[i].bh_length:
                max_h = self.ghx_list[i].bh_length

        self.ts = max_h**2 / (9 * self.ground_thermal_diff)

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

        for i in range(len(self.raw_sim_hours)):
            temp_bh = 0.0

            self.calc_aggregate_load()

            if i == 0:
                ln_t_ts = np.log((i + 1) * 3600 / self.ts)
                g = self.g_func(ln_t_ts)
                temp_bh = self.raw_sim_loads[0] / (2 * np.pi * self.ground_cond * self.ghx_list[0].bh_length) * g
            else:
                for j in range(i):
                    ln_t_ts = np.log((j + 1) * 3600 / self.ts)
                    g = self.g_func(ln_t_ts)
                    temp_bh += (self.raw_sim_loads[i] - self.raw_sim_loads[i-1]) / (2 * np.pi * self.ground_cond * self.ghx_list[0].bh_length) * g

            # don't forget to add the ground temp in
            temp_bh += self.ground_temp

            self.temp_bh.append(temp_bh)

            print("Hour: %4d\tTemp: %0.4f" %(i+1, temp_bh))

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

