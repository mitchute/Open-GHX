from __future__ import division

import timeit
from ghx_ghxArray_Euler import *
from ghx_ghxArray_Lagrange import *


class GHXArray(PrintClass):

    def __init__(self, ghx_input_json_path, sim_conf_json_path, loads_path, print_output=True):

        """
        Class constructor
        """

        # init inherited classes
        PrintClass.__init__(self, print_output)

        self.timer_start = timeit.default_timer()

        self.ghx_input_json_path = ghx_input_json_path
        self.sim_conf_json_path = sim_conf_json_path
        self.loads_path = loads_path
        self.print_output = print_output

        self.Euler_agg_types = ['Monthly', 'Test Euler Blocks', 'None']
        self.Lagrange_agg_types = ['MLAA', 'Test Lagrange Blocks']

        self.aggregation_type = ''

        self.get_sim_config(self.sim_conf_json_path)

    def get_sim_config(self, sim_config_path):

        """
        Reads the simulation configuration. If not successful, program exits.

        :param sim_config_path: path of json file containing the simulation configuration
        """

        errors_found = False

        # read from JSON file
        try:
            with open(sim_config_path) as json_file:
                json_data = json.load(json_file)
        except:  # pragma: no cover
            self.my_print("Error reading simulation configuration---check file path", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

        try:
            try:
                self.aggregation_type = json_data['Aggregation Type']
            except:  # pragma: no cover
                self.my_print("....'Aggregation Type' key not found", self.color_warn)
                errors_found = True
                pass

        except:  # pragma: no cover
            self.my_print("Error reading simulation configuration", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

        if errors_found:  # pragma: no cover
            self.my_print("Error loading data", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

    def simulate(self):

        """
        Main simulation routine. Simulates the GHXArray object.

        More docs to come...
        """

        self.my_print("Beginning simulation")

        if self.aggregation_type in self.Euler_agg_types:
            GHXArrayEulerAggBlocks(self.ghx_input_json_path,
                                   self.sim_conf_json_path,
                                   self.loads_path,
                                   self.print_output).simulate()
        elif self.aggregation_type in self.Lagrange_agg_types:
            GHXArrayLagrangeAggBlocks(self.ghx_input_json_path,
                                      self.sim_conf_json_path,
                                      self.loads_path,
                                      self.print_output).simulate()
        else:
            self.my_print("Error starting program", self.color_fail)
            self.my_print("Program exiting", self.color_fail)
            sys.exit(1)

        self.my_print("Simulation complete", self.color_success)
        self.my_print("Simulation time: %0.3f sec" % (timeit.default_timer() - self.timer_start))
