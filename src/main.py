
import simplejson as json
import sys
import CoolProp.CoolProp as CP
import numpy as np

# nice usage function
def usage():
    print("""Call this script with two command line arguments:
    $ main.py <path to json> <path to loads>""")

# check the command line arguments
if not len(sys.argv) == 3:
    print("Invalid command line arguments")
    usage()
    sys.exit(1)

# store command line args
path_to_json = sys.argv[1]
path_to_loads = sys.argv[2]

class GHXArray(object):
    """
    GHX Array Docs
    """

    def __init__(self, json_path, loads_path):
        # class data
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

    # reads json input file
    def get_input(self, json_path):

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

    # loads json into GHX data structures
    def load_GHX_data(self, json_data):

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

    # import loads
    def get_loads(self, load_path):

        try:
            print("Importing loads")
            self.load_pairs = np.genfromtxt(load_path, delimiter=',', names=True)
            self.update_load_lists()
            print("....Success")
        except:
            print("Error importing loads")
            print("Program exiting")
            sys.exit(1)

    # density of working fluid
    def dens(self, temp_in_c):
        return CP.PropsSI('D', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    # specfic heat of working fluid
    def cp(self, temp_in_c):
        return CP.PropsSI('C', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    # calculate g-funcitons if not present
    def calc_g_func(self):

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
        num = len(self.g_func_pairs)

        self.g_func_x = []
        self.g_func_y = []

        for i in range(num):
            self.g_func_x.append(self.g_func_pairs[i][0])
            self.g_func_y.append(self.g_func_pairs[i][1])

    def update_load_lists(self):
        num = len(self.load_pairs)

        self.sim_hours = []
        self.sim_loads = []

        for i in range(num):
            self.sim_hours.append(self.load_pairs[i][0])
            self.sim_loads.append(self.load_pairs[i][1])

    # interpolate to correct value of g-function
    def g_func(self, x):

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
        print("Beginning simulation")

        # calculate g-functions if not present
        if self.g_func_present == False:
            print("G-functions not present")
            self.calc_g_func()

        for cur_time in self.sim_hours:
            print(cur_time)

        print("Simulation complete")

class GHX:
    def __init__(self):
        self.name = ""
        self.location = []
        self.bh_length = 0.0
        self.bh_radius = 0.0
        self.grount_cond = 0.0
        self.pipe_cond = 0.0
        self.pipe_out_dia = 0.0
        self.shank_space = 0.0
        self.pipe_thickness = 0.0

    def calc_inside_convection(self):
        return 0

    def calc_short_circuiting(self):
        return 0

    def calc_resistance(self):
        self.calc_inside_convection()
        self.calc_short_circuiting()

GHXArray(path_to_json, path_to_loads).simulate()

