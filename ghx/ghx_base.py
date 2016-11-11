from __future__ import division

import sys
import os
import simplejson as json
import numpy as np

from collections import deque
from ghx_constants import *
from ghx_print import *
from ghx_ghx import *
from ghx_fluids import *


class BaseGHX(PrintClass, ConstantClass, FluidsClass):

    """
    Base class for GHXArray
    """

    def __init__(self, ghx_input_json_path, sim_conf_json_path, loads_path, print_output=True):

        """
        Class constructor
        """

        # init inherited classes
        PrintClass.__init__(self, print_output)
        ConstantClass.__init__(self)

        # class variables

        self.name = ""
        self.num_bh = 0
        self.flow_rate = 0.0
        self.ground_cond = 0.0
        self.ground_heat_capacity = 0.0
        self.ground_temp = 0.0
        self.grout_cond = 0.0
        self.fluid = ""
        self.sim_years = 0
        self.aggregation_type = ""
        self.min_hourly_history = 0
        self.ghx_list = []
        self.g_func_pairs = []
        self.g_func_present = False

        self.g_func_lntts = []
        self.g_func_val = []

        self.load_pairs = []

        self.raw_sim_hours = []
        self.raw_sim_loads = []

        self.ground_thermal_diff = 0.0

        self.ts = 0.0
        self.temp_bh = deque()
        self.temp_mft = deque()

        self.agg_load_objects = []

        self.g_func_hourly = deque()
        self.hourly_loads = deque()

        self.agg_loads_flag = True
        self.agg_load_intervals = []
        self.agg_hour = 0
        self.sim_hour = 0

        self.total_bh_length = 0.0
        self.ave_bh_length = 0.0
        self.ave_bh_radius = 0.0
        self.ave_pipe_cond = 0.0
        self.ave_pipe_out_dia = 0.0
        self.ave_pipe_in_dia = 0.0
        self.ave_shank_space = 0.0
        self.ave_pipe_thickness = 0.0

        self.resist_pipe_conduction = 0.0
        self.resist_pipe_convection = 0.0
        self.resist_pipe = 0.0
        self.resist_bh_ave = 0.0
        self.resist_bh_total_internal = 0.0
        self.resist_bh_effective = 0.0

        self.theta_1 = 0.0
        self.theta_2 = 0.0
        self.theta_3 = 0.0
        self.sigma = 0.0
        self.beta = 0.0

        # initialize methods

        # get ghx data
        self.get_input(ghx_input_json_path)

        # get sim configuration
        self.get_sim_config(sim_conf_json_path)

        # get loads
        self.get_loads(loads_path)

        # calc ts
        self.calc_ts()

        # init bh resistance calculations
        self.init_bh_resistance_calcs()

    def get_input(self, ghx_input_json_path):

        """
        Reads data from the json file using the simplejson python library.
        If the json data is loaded successfully, the GHXArray data structure is populated.
        If data load is not successful, program exits.

        :param ghx_input_json_path: path to the json input file containing information about the GHX array
        """

        errors_found = False

        # read from JSON file
        try:
            self.my_print("Reading GHX input")

            with open(ghx_input_json_path) as json_file:
                json_data = json.load(json_file)

            self.my_print("....Success")

        except:  # pragma: no cover
            self.my_print("Error reading GHX data file---check file path", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

        # load data into data structs
        try:
            self.my_print("Loading GHX data")

            # load GHX Array level inputs first

            try:
                self.name = json_data['Name']
            except:  # pragma: no cover
                self.my_print("\t'Name' key not found", self.color_warn)
                errors_found = True

            try:
                self.num_bh = json_data['Number BH']
            except:  # pragma: no cover
                self.my_print("\t'Number BH' key not found", self.color_warn)
                errors_found = True

            try:
                self.flow_rate = json_data['Flow Rate']
            except:  # pragma: no cover
                self.my_print("\t'Flow Rate' key not found", self.color_warn)
                errors_found = True

            try:
                self.ground_cond = json_data['Ground Cond']
            except:  # pragma: no cover
                self.my_print("\t'Ground Cond' key not found", self.color_warn)
                errors_found = True

            try:
                self.ground_heat_capacity = json_data['Ground Heat Capacity']
            except:  # pragma: no cover
                self.my_print("\t'Ground Heat Capacity' key not found", self.color_warn)
                errors_found = True

            try:
                self.ground_temp = json_data['Ground Temp']
            except:  # pragma: no cover
                self.my_print("\t'Ground Temp' key not found", self.color_warn)
                errors_found = True

            try:
                self.grout_cond = json_data['Grout Cond']
            except:  # pragma: no cover
                self.my_print("....'Grout Cond' key not found", self.color_warn)
                errors_found = True

            try:
                self.fluid = json_data['Fluid']
            except:  # pragma: no cover
                self.my_print("\t'Fluid' key not found", self.color_warn)
                errors_found = True

            try:
                self.g_func_pairs = json_data['G-func Pairs']
                self.g_func_present = True
                self.update_g_func_interp_lists()
            except:  # pragma: no cover
                self.my_print("....'G-func Pairs' key not found", self.color_warn)
                errors_found = True

            self.load_ghx_data(json_data)
            self.calc_ave_ghx_props()
            self.validate_input()

        except:  # pragma: no cover
            self.my_print("Error loading data into data structs", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

        if not errors_found:
            # success
            self.my_print("....Success")
        else:  # pragma: no cover
            self.my_print("Error loading data into data structs", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

    def load_ghx_data(self, json_data):

        """
        Instantiate and load data into GHX class for individual ground heat exchangers.
        If key values are not found in input file, messages output to the user.

        :param json_data: json data loaded from input file
        """

        errors_found = False

        num_ghx = len(json_data['GHXs'])

        # read json data into GHX class for each ghx
        for i in range(num_ghx):

            this_ghx = GHX()

            try:
                this_ghx.name = json_data['GHXs'][i]['Name']
            except:  # pragma: no cover
                self.my_print("....'Name' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                this_ghx.location = json_data['GHXs'][i]['Location']
            except:  # pragma: no cover
                self.my_print("....'Location' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                this_ghx.bh_length = json_data['GHXs'][i]['BH Length']
                self.total_bh_length += json_data['GHXs'][i]['BH Length']
            except:  # pragma: no cover
                self.my_print("....'BH Length' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                this_ghx.bh_radius = json_data['GHXs'][i]['BH Radius']
            except:  # pragma: no cover
                self.my_print("....'BH Radius' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                this_ghx.pipe_cond = json_data['GHXs'][i]['Pipe Cond']
            except:  # pragma: no cover
                self.my_print("....'Pipe Cond' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                this_ghx.pipe_out_dia = json_data['GHXs'][i]['Pipe Dia']
            except:  # pragma: no cover
                self.my_print("....'Pipe Dia' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                this_ghx.shank_space = json_data['GHXs'][i]['Shank Space']
            except:  # pragma: no cover
                self.my_print("....'Shank Space' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                this_ghx.pipe_thickness = json_data['GHXs'][i]['Pipe Thickness']
            except:  # pragma: no cover
                self.my_print("....'Pipe Thickness' key not found", self.color_warn)
                errors_found = True
                pass

            self.ghx_list.append(this_ghx)

        if errors_found:  # pragma: no cover
            self.my_print("Error loading GHX data", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

    def calc_ave_ghx_props(self):

        """
        Calculates the average properties from all individual ground heat exchangers
        """

        for ghx in self.ghx_list:
            self.ave_bh_length += ghx.bh_length
            self.ave_bh_radius += ghx.bh_radius
            self.ave_pipe_cond += ghx.pipe_cond
            self.ave_pipe_out_dia += ghx.pipe_out_dia
            self.ave_shank_space += ghx.shank_space
            self.ave_pipe_thickness += ghx.pipe_thickness

        self.ave_bh_length /= len(self.ghx_list)
        self.ave_bh_radius /= len(self.ghx_list)
        self.ave_pipe_cond /= len(self.ghx_list)
        self.ave_pipe_out_dia /= len(self.ghx_list)
        self.ave_shank_space /= len(self.ghx_list)
        self.ave_pipe_thickness /= len(self.ghx_list)

        self.ave_pipe_in_dia = self.ave_pipe_out_dia - (2 * self.ave_pipe_thickness)

    def validate_input(self):

        """
        Validates the inputs, where possible
        """

        errors_found = False

        for ghx in self.ghx_list:
            if ghx.shank_space > (2 * ghx.bh_radius - ghx.pipe_out_dia) or ghx.shank_space < ghx.pipe_out_dia:
                self.my_print("Invalid shank spacing", self.color_warn)
                self.my_print("Check shank spacing, pipe diameter, and borehole radius", self.color_warn)
                errors_found = True

        if errors_found:  # pragma: no cover
            self.my_print("Invalid data--check inputs", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

    def get_sim_config(self, sim_config_path):

        """
        Reads the simulation configuration. If not successful, program exits.

        :param sim_config_path: path of json file containing the simulation configuration
        """

        errors_found = False

        # read from JSON file
        try:
            self.my_print("Reading simulation configuration")

            with open(sim_config_path) as json_file:
                json_data = json.load(json_file)

            self.my_print("....Success")

        except:  # pragma: no cover
            self.my_print("Error reading simulation configuration---check file path", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

        try:
            self.my_print("Loading simulation configuration")

            try:
                self.sim_years = json_data['Simulation Years']
            except:  # pragma: no cover
                self.my_print("\t'Simulation Years' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                self.aggregation_type = json_data['Aggregation Type']
            except:  # pragma: no cover
                self.my_print("....'Aggregation Type' key not found", self.color_warn)
                errors_found = True
                pass

            try:
                self.min_hourly_history = json_data['Min Hourly History']
            except:  # pragma: no cover
                self.my_print("....'Min Hourly History' key not found", self.color_warn)
                errors_found = True
                pass

        except:  # pragma: no cover
            self.my_print("Error loading data", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

        if not errors_found:
            # success
            self.my_print("....Success")
        else:  # pragma: no cover
            self.my_print("Error loading data", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

    def get_loads(self, load_path):

        """
        Reads loads from the load input file. If data load is not successful, program exits.

        :param load_path: path of csv file containing time series loads
        """

        try:
            self.my_print("Importing loads")
            self.load_pairs = np.genfromtxt(load_path, delimiter=',', skip_header=1)
            self.update_load_lists()
            self.my_print("....Success")
        except:  # pragma: no cover
            self.my_print("Error importing loads", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
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

        except:  # pragma: no cover
            self.my_print("Error calculating simulation time scale \"ts\"", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

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
            self.my_print("Error calculating g-functions", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
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

    def init_bh_resistance_calcs(self):

        """
        Initializes the  borehole resistance calculations. Only needs to be called once.
        """

        self.theta_1 = self.ave_shank_space / (2 * self.ave_bh_radius)
        self.theta_2 = self.ave_bh_radius / (self.ave_pipe_out_dia/2.0)
        self.theta_3 = 1 / (2 * self.theta_1 * self.theta_2)
        self.sigma = (self.grout_cond - self.ground_cond)/(self.grout_cond + self.ground_cond)

        self.calc_pipe_conduction_resistance()

    def calc_pipe_conduction_resistance(self):

        """
        Calculates the thermal resistance of a pipe, in [K/(W/m)].

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.
        """

        self.resist_pipe_conduction = np.log(self.ave_pipe_out_dia/self.ave_pipe_in_dia) / \
                                      (2 * np.pi * self.ave_pipe_cond)

    def calc_pipe_convection_resistance(self):

        """
        Calculates the convection resistance using Gnielinski and Petukov, in [k/(W/m)]

        Gneilinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.
        """

        try:
            fluid_temp = self.temp_mft[-1]
        except:
            fluid_temp = self.ground_temp

        mass_flow_rate = self.flow_rate * self.dens(fluid_temp)
        re = 4 * mass_flow_rate / (self.visc(fluid_temp) * np.pi * self.ave_pipe_in_dia)

        if re < 3000:
            nu = np.mean([4.36, 3.66])
        else:
            f = self.friction_factor(re)
            pr = self.pr(fluid_temp)
            nu = (f/8) * (re - 1000) * pr / (1 + 12.7 * (f/8)**0.5 * (pr**(2/3) - 1))

        h = nu * self.cond(fluid_temp) / self.ave_pipe_in_dia

        self.resist_pipe_convection = 1 / (h * np.pi * self.ave_pipe_in_dia)

    def calc_pipe_resistance(self):

        """
        Calculates the combined conduction and convection pipe resistance

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 3
        """

        self.calc_pipe_convection_resistance()

        self.resist_pipe = self.resist_pipe_conduction + self.resist_pipe_convection

    def calc_bh_average_thermal_resistance(self):

        """
        Calculates the average thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 13
        """

        final_term_1 = np.log(self.theta_2/(2 * self.theta_1 * (1 - self.theta_1**4)**self.sigma))
        num_final_term_2 = self.theta_3**2 * (1 - (4 * self.sigma * self.theta_1**4)/(1 - self.theta_1**4))**2
        den_final_term_2_pt_1 = (1 + self.beta)/(1 - self.beta)
        den_final_term_2_pt_2 = self.theta_3**2 * (1 + (16 * self.sigma * self.theta_1**4)/(1 - self.theta_1**4)**2)
        den_final_term_2 = den_final_term_2_pt_1 + den_final_term_2_pt_2
        final_term_2 = num_final_term_2 / den_final_term_2

        self.resist_bh_ave = (1/(4 * np.pi * self.grout_cond)) * (self.beta + final_term_1 - final_term_2)

    def calc_bh_total_internal_thermal_resistance(self):
        """
        Calculates the total internal thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 26
        """

        final_term_1 = np.log(((1 + self.theta_1**2)**self.sigma)/(self.theta_3 * (1 - self.theta_1**2)**self.sigma))
        num_term_2 = self.theta_3**2 * (1 - self.theta_1**4 + 4 * self.sigma * self.theta_1**2)**2
        den_term_2_pt_1 = (1 + self.beta)/(1 - self.beta) * (1 - self.theta_1**4)**2
        den_term_2_pt_2 = self.theta_3**2 * (1 - self.theta_1**4)**2
        den_term_2_pt_3 = 8 * self.sigma * self.theta_1**2 * self.theta_3**2 * (1 + self.theta_1**4)
        den_term_2 = den_term_2_pt_1 - den_term_2_pt_2 + den_term_2_pt_3
        final_term_2 = num_term_2 / den_term_2

        self.resist_bh_total_internal = (1/(np.pi * self.grout_cond)) * (self.beta + final_term_1 - final_term_2)

    def calc_bh_effective_resistance(self):
        """
        Calculates the effective thermal resistance of the borehole assuming a uniform heat flux.

        Javed, S. & Spitler, J.D. Calculation of Borehole Thermal Resistance. In 'Advances in
        Ground-Source Heat Pump Systems,' pp. 84. Rees, S.J. ed. Cambridge, MA. Elsevier Ltd. 2016.

        Eq: 3-67

        Coefficients for equations 13 and 26 from Javed & Spitler 2016 calculated here.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 14
        """

        self.calc_pipe_resistance()
        self.beta = 2 * np.pi * self.grout_cond * self.resist_pipe
        self.calc_bh_total_internal_thermal_resistance()
        self.calc_bh_average_thermal_resistance()

        try:
            fluid_temp = self.temp_mft[-1]
        except:
            fluid_temp = self.ground_temp

        h = self.ave_bh_length
        mass_flow_rate = self.flow_rate * self.dens(fluid_temp)
        fluid_thermal_cap = self.cp(fluid_temp) * mass_flow_rate

        resist_short_circuiting = (1/(3 * self.resist_bh_total_internal)) * (h/fluid_thermal_cap)**2

        self.resist_bh_effective = self.resist_bh_ave + resist_short_circuiting

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
            self.my_print("Error writing output results", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)
