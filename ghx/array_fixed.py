import timeit
from collections import deque

import numpy as np

from ghx.aggregated_loads import AggregatedLoad
from ghx.base import BaseGHXClass
from ghx.constants import ConstantClass
from ghx.my_print import PrintClass


class GHXArrayFixedAggBlocks(BaseGHXClass):
    """
    GHXArrayFixedAggBlocks is the class object that holds the information that defines a ground heat exchanger array.
    This could be a single borehole, or a field with an arbitrary number of boreholes at arbitrary locations.
    """

    def __init__(self, json_data, loads_path, output_path, print_output=True):
        """
        Constructor for the class.
        """

        PrintClass(print_output, output_path)

        # init base class
        BaseGHXClass.__init__(self, json_data, loads_path,
                              output_path, print_output)

        errors_found = False

        try:
            self.min_hourly_history = json_data['Simulation Configuration']['Min Hourly History']
        except:  # pragma: no cover
            PrintClass.my_print(
                "....'Min Hourly History' key not found", 'warn')
            errors_found = True

        try:
            self.agg_load_intervals = json_data['Simulation Configuration']['Intervals']
        except:  # pragma: no cover
            PrintClass.my_print("....'Intervals' key not found", 'warn')
            errors_found = True

        if not errors_found:
            # success
            PrintClass.my_print("Simulation successfully initialized")
        else:  # pragma: no cover
            PrintClass.fatal_error(message="Error initializing GHXArrayFixedAggBlocks")

        # class data

        # set load aggregation intervals
        self.set_load_aggregation()

        # set first aggregated load, which is zero. Need this for later
        self.agg_load_objects.append(AggregatedLoad([0], 0, 1, True))

    def set_load_aggregation(self):
        """
        Sets the load aggregation intervals based on the type specified by the user.

        Intervals must be integer multiples.
        """

        if self.aggregation_type == "Fixed":
            pass
        elif self.aggregation_type == "None":
            self.agg_loads_flag = False
            self.agg_load_intervals = [
                ConstantClass.hours_in_year * self.sim_years]
            self.min_hourly_history = 0

    def aggregate_load(self):
        """
        Creates aggregated load object
        """

        if len(self.agg_load_intervals) > 1:
            self.collapse_aggregate_loads()

        prev_sim_hour = self.agg_load_objects[-1].last_sim_hour

        agg_loads = []

        for i in range(self.agg_load_intervals[0]):
            agg_loads.append(self.hourly_loads[i])

        self.agg_load_objects.append(AggregatedLoad(
            agg_loads, prev_sim_hour, len(agg_loads)))

    def collapse_aggregate_loads(self):
        """
        Collapses aggregated loads
        """

        agg_load_objects_update = []

        i = 0
        while i < len(self.agg_load_objects):
            if i == 0:  # keep '0' time object
                agg_load_objects_update.append(self.agg_load_objects[i])
                i += 1
                continue
            # already max agg interval
            elif len(self.agg_load_objects[i].loads) == self.agg_load_intervals[-1]:
                agg_load_objects_update.append(self.agg_load_objects[i])
                i += 1
                continue
            else:
                k = len(self.agg_load_intervals) - 1
                while k >= 0:
                    temp_objs = []
                    agg_int = self.agg_load_intervals[k]
                    for j in range(i, len(self.agg_load_objects)):
                        if len(self.agg_load_objects[j].loads) == agg_int:
                            temp_objs.append(self.agg_load_objects[j])
                        else:
                            continue
                    num_objs = len(temp_objs)
                    i += num_objs
                    if num_objs > 0:
                        if num_objs * agg_int >= self.agg_load_intervals[k + 1]:
                            agg_load_objects_update.append(
                                self.merge_agg_load_objs(temp_objs))
                        else:
                            for l in range(len(temp_objs)):
                                agg_load_objects_update.append(temp_objs[l])
                    k -= 1

        self.agg_load_objects = agg_load_objects_update

    def merge_agg_load_objs(self, obj_list):
        """
        Merges AggregatedLoad objects into a single AggregatedLoad object

        :return: merged AggregatedLoad object
        """

        loads = []
        min_hour = ConstantClass.hours_in_year * self.sim_years
        max_hour = 0

        for this_obj in obj_list:
            for i in range(len(this_obj.loads)):
                loads.append(this_obj.loads[i])
            if min_hour > this_obj.first_sim_hour:
                min_hour = this_obj.first_sim_hour
            if max_hour < this_obj.last_sim_hour:
                max_hour = this_obj.last_sim_hour

        return AggregatedLoad(loads, min_hour, len(loads))

    def simulate(self):
        """
        More docs to come...
        """

        PrintClass.my_print("Beginning simulation")

        # calculate g-functions if not present
        if not self.g_func_present:
            PrintClass.my_print("G-functions not present", 'warn')
            self.calc_g_func()

        # pre-load hourly g-functions
        for hour in range(self.agg_load_intervals[0] + self.min_hourly_history):
            ln_t_ts = np.log((hour + 1) * 3600 / self.ts)
            self.g_func_hourly.append(self.g_func(ln_t_ts))

        # set aggregate load container max length
        len_hourly_loads = self.min_hourly_history + self.agg_load_intervals[0]
        self.hourly_loads = deque(
            [0] * len_hourly_loads, maxlen=len_hourly_loads)

        agg_hour = 0
        sim_hour = 0

        for year in range(self.sim_years):
            for month in range(ConstantClass.months_in_year):

                PrintClass.my_print("....Year/Month: %d/%d" %
                                    (year + 1, month + 1))

                for hour in range(ConstantClass.hours_in_month):

                    agg_hour += 1
                    sim_hour += 1

                    # get raw hourly load and append to hourly list
                    curr_index = month * ConstantClass.hours_in_month + hour
                    self.hourly_loads.append(self.sim_loads[curr_index])
                    curr_flow_rate = self.total_flow_rate[curr_index]

                    # update borehole flow rate
                    self.borehole.pipe.fluid.update_fluid_state(
                        new_flow_rate=curr_flow_rate)

                    # calculate borehole resistance
                    self.borehole.calc_bh_resistance()

                    # calculate borehole temp
                    # hourly effects
                    temp_bh_hourly = []
                    temp_mft_hourly = []
                    start_hourly = len(self.hourly_loads) - 1
                    end_hourly = start_hourly - agg_hour
                    g_func_index = -1
                    for i in range(start_hourly, end_hourly, -1):
                        g_func_index += 1
                        q_curr = self.hourly_loads[i]
                        q_prev = self.hourly_loads[i - 1]
                        g = self.g_func_hourly[g_func_index]
                        # calculate average bh temp
                        delta_q = (q_curr - q_prev) / \
                                  (2 * np.pi * self.borehole.soil.conductivity *
                                   self.total_bh_length)
                        temp_bh_hourly.append(delta_q * g)

                        # calculate mean fluid temp
                        g_rb = g + self.borehole.resist_bh

                        if g_rb < 0:
                            g = -self.borehole.resist_bh * 2 * np.pi * self.borehole.soil.conductivity
                            g_rb = g + self.borehole.resist_bh

                        temp_mft_hourly.append(delta_q * g_rb)

                    # aggregated load effects
                    temp_bh_agg = []
                    temp_mft_agg = []
                    if self.agg_loads_flag:
                        for i in range(len(self.agg_load_objects)):
                            if i == 0:
                                continue
                            curr_obj = self.agg_load_objects[i]
                            prev_obj = self.agg_load_objects[i - 1]

                            t_agg = sim_hour - curr_obj.time()
                            ln_t_ts = np.log(t_agg * 3600 / self.ts)
                            g = self.g_func(ln_t_ts)
                            # calculate the average borehole temp
                            delta_q = (curr_obj.q - prev_obj.q) / (
                                2 * np.pi * self.borehole.soil.conductivity * self.total_bh_length)
                            temp_bh_agg.append(delta_q * g)

                            # calculate the mean fluid temp
                            g_rb = g + self.borehole.resist_bh

                            if g_rb < 0:
                                g = -self.borehole.resist_bh * 2 * np.pi * self.borehole.soil.conductivity
                                g_rb = g + self.borehole.resist_bh

                            temp_mft_agg.append(delta_q * g_rb)

                        # aggregate load
                        if agg_hour == self.agg_load_intervals[0] + self.min_hourly_history - 1:
                            # this has one extra value for comparative purposes
                            # need to get rid of it here
                            self.hourly_loads.popleft()

                            # create new aggregated load object
                            self.aggregate_load()

                            # reset aggregation hour to '0'
                            agg_hour -= self.agg_load_intervals[0]

                    # final bh temp
                    self.temp_bh.append(
                        self.borehole.soil.undisturbed_temp + sum(temp_bh_hourly) + sum(temp_bh_agg))

                    # final mean fluid temp
                    self.temp_mft.append(
                        self.borehole.soil.undisturbed_temp + sum(temp_mft_hourly) + sum(temp_mft_agg))

                    # update borehole temperature
                    self.borehole.pipe.fluid.update_fluid_state(
                        new_temp=self.temp_mft[-1])

        self.generate_output_reports()

        PrintClass.my_print("Simulation complete", "success")
        PrintClass.my_print("Simulation time: %0.3f sec" %
                            (timeit.default_timer() - self.timer_start))

        PrintClass.write_log_file()
