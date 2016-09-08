
import numpy as np
import simplejson as json
import CoolProp.CoolProp as CP

class GHXArray:
    """
    GHXArray is the class object that holds the information that defines a ground heat exchanger array. This could be a single borehole, or a field with an arbitrary number of boreholes at arbitrary locations.
    """

    def __init__(self, json_path, loads_path):

        """
        Constructor for the class. Call it wil the path to the json input file and the csv loads file.

        Calls get_input and get_loads to load data into structs.

        GHXArray(<json_path>, <loads_path>)
        """

        self.name = ""
        self.num_bh = 0
        self.flow_rate = 0.0
        self.grnd_cond = 0.0
        self.grnd_cp = 0.0
        self.grnd_temp = 0.0
        self.fluid = ""
        self.ghx_list = []
        self.g_func_pairs = []
        self.g_func_present = False

        # ghx data
        self.get_input(json_path)

        # get loads
        self.get_loads(loads_path)

    def get_input(self, json_path):

        """
        Reads data from the json file using the simplejson python library. If the json data is loaded successfully, the GHXArray data structure is populated. If data load is not successful, program exits.

        :param json_path: path to the json input file containing information about the GHX array
        """

        # read from JSON file
        try:
            print("Reading JSON input")
            with open(json_path) as json_file:
                json_data = json.load(json_file)
            print("....Success")
        except:
            print("Error reading JSON data file---check input file")
            print("Program exiting")
            sys.exit(1)

        # load data into data structs
        try:
            print("Loading data into structs")

            # load GHX Array level inputs first

            try:
                self.name = json_data['Name']
            except:
                print("\t'Name' key not found")
                pass

            try:
                self.num_bh = json_data['Num BH']
            except:
                print("\t'Num BH' key not found")
                pass

            try:
                self.flow_rate = json_data['Flow Rate']
            except:
                print("\t'Flow Rate' key not found")
                pass

            try:
                self.grnd_cond = json_data['Grnd Cond']
            except:
                print("\t'Grnd Cond' key not found")
                pass

            try:
                self.grnd_cp = json_data['Grnd Cp']
            except:
                print("\t'Grnd Cp' key not found")
                pass

            try:
                self.grnd_temp = json_data['Grnd Temp']
            except:
                print("\t'Grnd Temp' key not found")
                pass

            try:
                self.fluid = json_data['Fluid']
            except:
                print("\t'Fluid' key not found")
                pass

            try:
                self.g_func_pairs = json_data['G-func Pairs']
                self.g_func_present = True
                self.update_g_func_interp_lists()
            except:
                print("\t'G-func Pairs' key not found")
                pass

            # load data for each GHX
            self.load_GHX_data(json_data)

            # success
            print("....Success")
        except:
            print("Error loading data into data structs")
            print("Program exiting")
            sys.exit(1)

    def load_GHX_data(self, json_data):

        """
        Instansiates and loades data into GHX class for individual ground heat exchangers. If key values are not found in input file, messages output to the user.

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
                print("\t'Name' key not found")
                pass

            try:
                self.ghx_list[i].location = json_data['GHXs'][i]['Location']
            except:
                print("\t'Location' key not found")
                pass

            try:
                self.ghx_list[i].bh_length = json_data['GHXs'][i]['BH Length']
            except:
                print("\t'BH Length' key not found")
                pass

            try:
                self.ghx_list[i].bh_radius = json_data['GHXs'][i]['BH Radius']
            except:
                print("\t'BH Radius' key not found")
                pass

            try:
                self.ghx_list[i].grount_cond = json_data['GHXs'][i]['Grout Cond']
            except:
                print("\t'Grout Cond' key not found")
                pass

            try:
                self.ghx_list[i].pipe_cond = json_data['GHXs'][i]['Pipe Cond']
            except:
                print("\t'Pipe Cond' key not found")
                pass

            try:
                self.ghx_list[i].pipe_out_dia = json_data['GHXs'][i]['Pipe Dia']
            except:
                print("\t'Pipe Dia' key not found")
                pass

            try:
                self.ghx_list[i].shank_space = json_data['GHXs'][i]['Shank Space']
            except:
                print("\t'Shank Space' key not found")
                pass

            try:
                self.ghx_list[i].pipe_thickness = json_data['GHXs'][i]['Pipe Thickness']
            except:
                print("\t'Pipe Thickness' key not found")
                pass

    def get_loads(self, load_path):

        """
        Reads loads from the load input file. If data load is not successful, program exits.

        :param load_path: path of csv file containing timeseries loads
        """

        try:
            print("Importing loads")
            self.load_pairs = np.genfromtxt(load_path, delimiter=',', names=True)
            self.update_load_lists()
            print("....Success")
        except:
            print("Error importing loads")
            print("Program exiting")
            sys.exit(1)

    def dens(self, temp_in_c):

        """
        Determines the fluid density as a function of temperature, in Celsius. Uses the CoolProp python library to find the fluid density. Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        :returns: float
        """
        return CP.PropsSI('D', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    def cp(self, temp_in_c):

        """
        Determines the fluid specific heat as a function of temperature, in Celsius. Uses the CoolProp python library to find the fluid specific heat. Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        :returns: float
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
            print("....Success")
        except:
            print("Error calculating g-functions")
            print("Program exiting")
            sys.exit(1)

    def update_g_func_interp_lists(self):

        """
        Because g-funcitons are read in as pairs, we need to convert the t/ts and g-func values into individual lists so we can use the built in python interpolation routines. This takes the given g-function pairs and converts to individual lists.

        Called every time the g-functions are updated.
        """

        num = len(self.g_func_pairs)

        self.g_func_x = []
        self.g_func_y = []

        for i in range(num):
            self.g_func_x.append(self.g_func_pairs[i][0])
            self.g_func_y.append(self.g_func_pairs[i][1])

    def update_load_lists(self):

        """
        Converts the loads data into single lists.
        """
        num = len(self.load_pairs)

        self.sim_hours = []
        self.sim_loads = []

        for i in range(num):
            self.sim_hours.append(self.load_pairs[i][0])
            self.sim_loads.append(self.load_pairs[i][1])

    def g_func(self, x):

        """
        Interpolates to the correct g-function value
        """

        num = len(self.g_func_pairs)
        lower_index = 0
        upper_index = num - 1

        # check whether requested val is inside the range
        if x < self.g_func_x[lower_index] or x > self.g_func_x[upper_index]:
            print("G-function value requested beyond range of data")
            print("Program exiting")
            sys.exit(1)

        return np.interp(x, self.g_func_x, self.g_func_y)

    def simulate(self):

        """
        Main simulation routine. Simulates the GHXArray object.

        More docs to come...
        """
        print("Beginning simulation")

        # calculate g-functions if not present
        if self.g_func_present == False:
            print("G-functions not present")
            self.calc_g_func()

        for cur_time in self.sim_hours:
            print(cur_time)

        print("Simulation complete")

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
        self.grount_cond = 0.0
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

    def calc_short_circuiting_res(self):

        """
        Calculates short circuiting resistance.

        More docs to come...
        """

        return 0

    def calc_resistance(self):

        """
        Calc total thermal resistance of the borehole

        More docs to come...
        """

        self.calc_inside_convection_res()
        self.calc_short_circuiting_res()

