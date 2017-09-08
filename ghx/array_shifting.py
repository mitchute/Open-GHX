import timeit

import numpy as np

from ghx.aggregated_loads import AggregatedLoadShifting
from ghx.base import BaseGHXClass
from ghx.constants import ConstantClass
from ghx.my_print import PrintClass


class GHXArrayShiftingAggBlocks(BaseGHXClass):
    def __init__(self, json_data, loads_path, output_path, print_output=True):
        """
        Class constructor
        """

        # init base class
        BaseGHXClass.__init__(self, json_data, loads_path,
                              output_path, print_output)

        errors_found = False

        try:
            self.history_depth = json_data['Simulation Configuration']['History Depth']
        except:  # pragma: no cover
            PrintClass.my_print(
                "....'History Depth' key not found", 'warn')
            errors_found = True

        try:
            self.history_expansion_rate = json_data['Simulation Configuration']['History Expansion Rate']
        except:  # pragma: no cover
            PrintClass.my_print("....'History Expansion Rate' key not found", 'warn')
            errors_found = True

        # set load aggregation intervals
        self.set_load_aggregation()

        # pre-calculate all g-functions for load blocks
        self.load_g_functions()

        if not errors_found:
            # success
            PrintClass.my_print("Simulation successfully initialized")
        else:  # pragma: no cover
            PrintClass.fatal_error(message="Error initializing GHXArrayShiftingAggBlocks")

    def set_load_aggregation(self):
        """
        Sets the load aggregation intervals based on the type specified by the user.
        """

        max_sim_hours = self.sim_years * ConstantClass.hours_in_year

        agg_sim_hours = 0
        level = 0
        while max_sim_hours > agg_sim_hours:
            level_interval = self.history_expansion_rate ** level
            for depth in range(self.history_depth):
                self.agg_load_objects.append(AggregatedLoadShifting(max_loads=level_interval))
                agg_sim_hours += level_interval
            level += 1

    def shift_loads(self, curr_energy):
        """
        Manages shifting loads between aggregation blocks
        """

        write_debug_csv = False

        # shift the loads so energy is conserved
        for i, this_block in enumerate(self.agg_load_objects):
            if i == 0:
                break_now = self.agg_load_objects[0].shift_energy(curr_energy)
            else:
                break_now = this_block.shift_energy(self.agg_load_objects[i-1].energy_to_shift_out)

            if break_now:
                break

        # now that energy is shifted, update the q values
        for this_block in self.agg_load_objects:
            if this_block.num_loads > 0:
                this_block.calc_q()
            else:
                break

        # debugging
        if write_debug_csv:  # pragma: no cover
            with open('debug.csv', 'a') as f:
                str_out = ''
                for this_block in self.agg_load_objects:
                    str_out += '%0.4f,' % this_block.energy

                f.write(str_out + '\n')

    def load_g_functions(self):
        """
        Pre-computes the g-functions for each block.
        This is only done once.
        """

        hour = 0

        for this_block in self.agg_load_objects:
            hour += this_block.max_num_loads
            ln_t_ts = np.log((hour + 1) * 3600 / self.ts)
            this_block.g_func = self.g_func(ln_t_ts)

    def simulate(self):
        """
        More docs to come...
        """

        PrintClass.my_print("Beginning simulation")

        sim_hour = 0
        sim_hour_old = 0

        for year in range(self.sim_years):
            for month in range(ConstantClass.months_in_year):

                PrintClass.my_print("....Year/Month: %d/%d" %
                                    (year + 1, month + 1))

                temp_bh_hourly = []
                temp_mft_hourly = []

                for hour in range(ConstantClass.hours_in_month):
                    sim_hour += 1

                    # get raw hourly load and append to hourly list
                    load_index = month * ConstantClass.hours_in_month + hour
                    curr_load = self.sim_loads[load_index]

                    # aggregate energy in load blocks
                    energy = curr_load * (sim_hour - sim_hour_old) * ConstantClass.sec_in_hour
                    self.shift_loads(energy)

                    # get current data
                    curr_index = month * ConstantClass.hours_in_month + hour
                    curr_flow_rate = self.total_flow_rate[curr_index]

                    # update borehole flow rate
                    self.borehole.pipe.fluid.update_fluid_state(
                        new_flow_rate=curr_flow_rate)

                    # calculate borehole resistance
                    self.borehole.calc_bh_resistance()

                    for i, curr_obj in enumerate(self.agg_load_objects):

                        if curr_obj.num_loads == 0:
                            break

                        if i == 0:
                            q_curr = curr_obj.q
                            q_prev = 0
                        else:
                            prev_obj = self.agg_load_objects[i - 1]
                            q_curr = curr_obj.q
                            q_prev = prev_obj.q

                        # calculate average bh temp
                        delta_q = (q_curr - q_prev) / \
                                  (2 * np.pi * self.borehole.soil.conductivity *
                                   self.total_bh_length)

                        g = curr_obj.g_func
                        temp_bh_hourly.append(delta_q * g)

                        # calculate mean fluid temp
                        g_rb = g + self.borehole.resist_bh

                        if g_rb < 0:
                            g = -self.borehole.resist_bh * 2 * np.pi * self.borehole.soil.conductivity
                            g_rb = g + self.borehole.resist_bh

                        temp_mft_hourly.append(delta_q * g_rb)

                    # final bh temp
                    self.temp_bh.append(self.borehole.soil.undisturbed_temp + sum(temp_bh_hourly))

                    # final mean fluid temp
                    self.temp_mft.append(self.borehole.soil.undisturbed_temp + sum(temp_mft_hourly))

                    # update borehole temperature
                    self.borehole.pipe.fluid.update_fluid_state(new_temp=self.temp_mft[-1])

                    sim_hour_old = sim_hour

        self.generate_output_reports()

        PrintClass.my_print("Simulation complete", "success")
        PrintClass.my_print("Simulation time: %0.3f sec" %
                            (timeit.default_timer() - self.timer_start))

        PrintClass.write_log_file()
