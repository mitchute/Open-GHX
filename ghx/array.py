import json
import timeit

from ghx.array_fixed import GHXArrayFixedAggBlocks
from ghx.array_shifting import GHXArrayShiftingAggBlocks
from ghx.constants import ConstantClass
from ghx.my_print import PrintClass


class GHXArray:
    def __init__(self, ghx_input_json_path, loads_path, output_path, print_output=True):

        """
        Class constructor
        """

        PrintClass(print_output, output_path)
        ConstantClass()

        self.timer_start = timeit.default_timer()

        self.ghx_input_json_path = ghx_input_json_path
        self.json_data = None
        self.loads_path = loads_path
        self.output_path = output_path
        self.print_output = print_output

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

        if self.aggregation_type == "Fixed" or self.aggregation_type == "None":
            GHXArrayFixedAggBlocks(self.json_data,
                                   self.loads_path,
                                   self.output_path,
                                   self.print_output).simulate()
        elif self.aggregation_type == "Shifting":
            GHXArrayShiftingAggBlocks(self.json_data,
                                      self.loads_path,
                                      self.output_path,
                                      self.print_output).simulate()
        else:
            PrintClass.my_print("\tAggregation Type \"%s\" not found" % self.aggregation_type, "warn")
            PrintClass.fatal_error(message="Error starting program")
