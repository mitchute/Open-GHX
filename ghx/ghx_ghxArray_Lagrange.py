from __future__ import division

from ghx_base import *
from ghx_aggregated_load import *


class GHXArrayLagrangeAggBlocks(BaseGHXClass):

    def __init__(self, ghx_input_json_path, loads_path, output_path, print_output=True):

        """
        Class constructor
        """

        # init base class
        BaseGHXClass.__init__(self, ghx_input_json_path, loads_path, output_path, print_output)

        # class data

        cwd = os.getcwd()
        path_to_run_dir = os.path.join(cwd, "run")

        if not os.path.exists(path_to_run_dir):
            os.makedirs(path_to_run_dir)

        # open files
        self.debug_file = open(os.path.join(path_to_run_dir, "debug.csv"), 'w')

        # set load aggregation intervals
        self.set_load_aggregation()

    def set_load_aggregation(self):

        """
        Sets the load aggregation intervals based on the type specified by the user.

        Bernier, M.A., Labib, R., Pinel, P., and Paillot, R. 2004. 'A multiple load aggregation algorithm
        for annual hourly simulations of GCHP systems.' HVAC&R Research, 10(4): 471-487.
        """

        MLAA = [12, 48, 168, 360]
        testing = [2, 2, 4, 8]

        if self.aggregation_type == "MLAA":  # Bernier et al. 2004
            self.agg_load_intervals = MLAA
        elif self.aggregation_type == "Test Lagrange Blocks":
            self.agg_load_intervals = testing
        else:
            self.my_print("Load aggregation scheme not recognized", self._color_warn)
            self.my_print("....Defaulting to MLAA algorithm", self._color_warn)
            self.agg_load_intervals = MLAA

        # need to add one extra entry to the first interval to account for the '0' hour
        # self.agg_load_intervals[0] += 1

        # set first load, which is zero--need this for later
        self.agg_load_objects.append(AggregatedLoad([0], 0, self.agg_load_intervals[0], True))

    def shift_loads(self, curr_load):

        """
        Manages shifting loads between aggregation blocks
        :param curr_load: current load on GHX
        """

        length_new_object = 0

        # append new aggregated load object if the last one is full
        last_object_index = min(len(self.agg_load_objects), len(self.agg_load_intervals)) - 1

        if len(self.agg_load_objects[-1].loads) == self.agg_load_objects[-1].max_length:
            if last_object_index >= len(self.agg_load_intervals) - 1:
                length_new_object = self.agg_load_intervals[-1]
            else:
                length_new_object = self.agg_load_intervals[last_object_index + 1]

            self.agg_load_objects.append(AggregatedLoad([], 0, length_new_object, True))

        for i in range(len(self.agg_load_objects) - 1, 0, -1):
            self.agg_load_objects[i].loads.append(self.agg_load_objects[i - 1].loads[0])
            if i == 1:
                self.agg_load_objects[i].new_q_val = self.agg_load_objects[i - 1].loads[0]
            else:
                self.agg_load_objects[i].new_q_val = self.agg_load_objects[i - 1].q_est
            self.agg_load_objects[i - 1].loads.popleft()

        self.agg_load_objects[0].loads.append(curr_load)

        for obj in self.agg_load_objects:
            obj.calc_q()
            obj.estimate_q()

    def debug(self):

        self.debug_file.write("%d" % (self.sim_hour))

        for i in range(1,len(self.agg_load_objects)):
            self.debug_file.write(", %f, %f" % (self.agg_load_objects[i].q, self.agg_load_objects[i].q_est))

        self.debug_file.write("\n")

    def simulate(self):

        """
        More docs to come...
        """

        self.my_print("Beginning simulation")

        for year in range(self.sim_years):
            for month in range(self.months_in_year):

                self.my_print("....Year/Month: %d/%d" % (year + 1, month + 1))

                for hour in range(self.hours_in_month):

                    self.sim_hour += 1

                    # get raw hourly load and append to hourly list
                    load_index = month * self.hours_in_month + hour
                    curr_load = self.sim_loads[load_index]

                    self.shift_loads(curr_load)

                    self.debug()

                    #for i in range(len(self.agg_load_objects)):
                    #    if i == 0:
                    #        for j in range(len(self.agg_load_objects[0].loads), 0, -1):
                    #
                    #    else:
                     #       return 1

        self.generate_output_reports()
