from __future__ import division

from ghx_base import *
from ghx_aggregated_load import *
from ghx_constants import ConstantClass


class GHXArrayShiftingAggBlocks(BaseGHXClass):

    def __init__(self, ghx_input_json_path, loads_path, output_path, print_output=True):

        """
        Class constructor
        """

        # init base class
        BaseGHXClass.__init__(self, ghx_input_json_path, loads_path, output_path, print_output)

        # set load aggregation intervals
        self.set_load_aggregation()

    def set_load_aggregation(self):

        """
        Sets the load aggregation intervals based on the type specified by the user.
        """

        pass

        # need to add one extra entry to the first interval to account for the '0' hour
        # self.agg_load_intervals[0] += 1

        # set first load, which is zero--need this for later
        # self.agg_load_objects.append(AggregatedLoad([0], 0, self.agg_load_intervals[0], True))

    def shift_loads(self, curr_load):

        """
        Manages shifting loads between aggregation blocks
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

    def simulate(self):

        """
        More docs to come...
        """

        PrintClass.my_print("Beginning simulation")

        sim_hour = 0

        for year in range(self.sim_years):
            for month in range(ConstantClass.months_in_year):

                PrintClass.my_print("....Year/Month: %d/%d" % (year + 1, month + 1))

                for hour in range(ConstantClass.hours_in_month):

                    sim_hour += 1

                    # get raw hourly load and append to hourly list
                    load_index = month * ConstantClass.hours_in_month + hour
                    curr_load = self.sim_loads[load_index]

                    self.shift_loads(curr_load)

        self.generate_output_reports()
