from __future__ import division

import timeit
from ghx_print import PrintClass
from ghx_ghxArray_Euler import *
from ghx_ghxArray_Lagrange import *


class GHXArray:

    def __init__(self, ghx_input_json_path, loads_path, output_path, print_output=True):

        """
        Class constructor
        """

        PrintClass(print_output)

        self.timer_start = timeit.default_timer()

        self.ghx_input_json_path = ghx_input_json_path
        self.json_data = None
        self.loads_path = loads_path
        self.output_path = output_path
        self.print_output = print_output

        self.Euler_agg_types = ['Monthly', 'Type 628', 'Test Euler Blocks', 'None']
        self.Lagrange_agg_types = ['MLAA', 'Test Lagrange Blocks']

        self.aggregation_type = ''

        self.get_sim_config(self.ghx_input_json_path)

    def get_sim_config(self, sim_config_path):

        """
        Reads the simulation configuration. If not successful, program exits.

        :param sim_config_path: path of json file containing the simulation configuration
        """

        errors_found = False

        # read from JSON file
        try:
            with open(sim_config_path) as json_file:
                self.json_data = json.load(json_file)
        except:  # pragma: no cover
            PrintClass.fatal_error(message="Error reading simulation configuration---check file path")

        try:
            try:
                self.aggregation_type = self.json_data['Simulation Configuration']['Aggregation Type']
            except:  # pragma: no cover
                PrintClass.my_print("....'Aggregation Type' key not found", "warn")
                errors_found = True

        except:  # pragma: no cover
            PrintClass.fatal_error(message="Error reading simulation configuration")

        if errors_found:  # pragma: no cover
            PrintClass.fatal_error(message="Error loading data")

    def simulate(self):

        """
        Main simulation routine. Simulates the GHXArray object.

        More docs to come...
        """

        PrintClass.my_print("Initializing simulation")

        if self.aggregation_type in self.Euler_agg_types:
            GHXArrayEulerAggBlocks(self.json_data,
                                   self.loads_path,
                                   self.output_path,
                                   self.print_output).simulate()
        elif self.aggregation_type in self.Lagrange_agg_types:
            GHXArrayLagrangeAggBlocks(self.ghx_input_json_path,
                                      self.loads_path,
                                      self.output_path,
                                      self.print_output).simulate()
        else:
            PrintClass.my_print("\tAggregation Type \"%s\" not found" % self.aggregation_type, "warn")
            PrintClass.fatal_error(message="Error starting program")

        PrintClass.my_print("Simulation complete", "success")
        PrintClass.my_print("Simulation time: %0.3f sec" % (timeit.default_timer() - self.timer_start))

        PrintClass.write_log_file(self.output_path)
