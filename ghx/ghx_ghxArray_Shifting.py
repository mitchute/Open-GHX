from ghx.ghx_base import *
from ghx.ghx_aggregated_load import *
from ghx.ghx_constants import ConstantClass
from ghx.ghx_print import PrintClass


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

        # set first load, which is zero--need this for later
        self.agg_load_objects.append(AggregatedLoad([0], 0, 1, True))

        for interval in self.agg_load_intervals:
            for num_interval in range(interval[1]):
                self.agg_load_objects.append(AggregatedLoad([0], 0, ))

    def shift_loads(self, curr_load):

        """
        Manages shifting loads between aggregation blocks
        """


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
