from __future__ import division

from ghx_base import *
from ghx_aggregated_load import *


class GHXArrayEulerAggBlocks(BaseGHX):

    """
    GHXArrayEulerAggBlocks is the class object that holds the information that defines a ground heat exchanger array.
    This could be a single borehole, or a field with an arbitrary number of boreholes at arbitrary locations.
    Aggregation load blocks are "Euler" relative to "present" simulation time, meaning, at every time step
    the load block shift one time step further from the "present" simulation time.
    """

    def __init__(self, json_data, loads_path, print_output=True):

        """
        Constructor for the class.
        """

        # init base class
        BaseGHX.__init__(self, json_data, loads_path, print_output)

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

        monthly = [12, 24, 48, 96, 192, 384, 768]
        testing = [5, 10, 20, 40]

        if self.aggregation_type == "Monthly":
            self.agg_load_intervals = monthly
        elif self.aggregation_type == "Test Euler Blocks":
            self.agg_load_intervals = testing
        elif self.aggregation_type == "None":
            self.agg_loads_flag = False
            self.agg_load_intervals = [self.hours_in_year * self.sim_years]
            self.min_hourly_history = 0
        else:
            self.my_print("Load aggregation scheme not recognized", self._color_warn)
            self.my_print("....Defaulting to monthly intervals", self._color_warn)
            self.agg_load_intervals = monthly

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

        self.agg_load_objects.append(AggregatedLoad(agg_loads, prev_sim_hour, len(agg_loads)))

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
            elif len(self.agg_load_objects[i].loads) == self.agg_load_intervals[-1]:  # already max agg interval
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
                        if num_objs*agg_int >= self.agg_load_intervals[k+1]:
                            agg_load_objects_update.append(self.merge_agg_load_objs(temp_objs))
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
        min_hour = self.hours_in_year * self.sim_years
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

        self.my_print("Beginning simulation")

        # calculate g-functions if not present
        if not self.g_func_present:
            self.my_print("G-functions not present", self._color_warn)
            self.calc_g_func()

        # pre-load hourly g-functions
        for hour in range(self.agg_load_intervals[0] + self.min_hourly_history):
            ln_t_ts = np.log((hour+1) * 3600 / self.ts)
            self.g_func_hourly.append(self.g_func(ln_t_ts))

        # set aggregate load container max length
        len_hourly_loads = self.min_hourly_history + self.agg_load_intervals[0]
        self.hourly_loads = deque([0]*len_hourly_loads, maxlen=len_hourly_loads)

        for year in range(self.sim_years):
            for month in range(self.months_in_year):

                self.my_print("....Year/Month: %d/%d" % (year+1, month+1))

                for hour in range(self.hours_in_month):

                    self.agg_hour += 1
                    self.sim_hour += 1

                    # get raw hourly load and append to hourly list
                    load_index = month * self.hours_in_month + hour
                    self.hourly_loads.append(self.sim_loads[load_index])

                    # calculate borehole resistance
                    self.calc_bh_effective_resistance()

                    # calculate borehole temp
                    # hourly effects
                    temp_bh_hourly = []
                    temp_mft_hourly = []
                    start_hourly = len(self.hourly_loads) - 1
                    end_hourly = start_hourly - self.agg_hour
                    g_func_index = -1
                    for i in range(start_hourly, end_hourly, -1):
                        g_func_index += 1
                        q_curr = self.hourly_loads[i]
                        q_prev = self.hourly_loads[i - 1]
                        g = self.g_func_hourly[g_func_index]
                        # calculate average bh temp
                        delta_q = (q_curr - q_prev) / (2 * np.pi * self.ground_cond * self.total_bh_length)
                        temp_bh_hourly.append(delta_q * g)

                        # calculate mean fluid temp
                        g_rb = g + self.resist_bh

                        if g_rb < 0:
                            g = -self.resist_bh * 2 * np.pi * self.ground_cond
                            g_rb = g + self.resist_bh

                        temp_mft_hourly.append(delta_q * g_rb)

                    # aggregated load effects
                    temp_bh_agg = []
                    temp_mft_agg = []
                    if self.agg_loads_flag:
                        for i in range(len(self.agg_load_objects)):
                            if i == 0:
                                continue
                            curr_obj = self.agg_load_objects[i]
                            prev_obj = self.agg_load_objects[i-1]

                            t_agg = self.sim_hour - curr_obj.time()
                            ln_t_ts = np.log(t_agg * 3600 / self.ts)
                            g = self.g_func(ln_t_ts)
                            # calculate the average borehole temp
                            delta_q = (curr_obj.q - prev_obj.q) / (2 * np.pi * self.ground_cond * self.total_bh_length)
                            temp_bh_agg.append(delta_q * g)

                            # calculate the mean fluid temp
                            g_rb = g + self.resist_bh

                            if g_rb < 0:
                                g = -self.resist_bh * 2 * np.pi * self.ground_cond
                                g_rb = g + self.resist_bh

                            temp_mft_agg.append(delta_q * g_rb)

                        # aggregate load
                        if self.agg_hour == self.agg_load_intervals[0] + self.min_hourly_history - 1:
                            # this has one extra value for comparative purposes
                            # need to get rid of it here
                            self.hourly_loads.popleft()

                            # create new aggregated load object
                            self.aggregate_load()

                            # reset aggregation hour to '0'
                            self.agg_hour -= self.agg_load_intervals[0]

                    # final bh temp
                    self.temp_bh.append(self.ground_temp + sum(temp_bh_hourly) + sum(temp_bh_agg))

                    # final mean fluid temp
                    self.temp_mft.append(self.ground_temp + sum(temp_mft_hourly) + sum(temp_mft_agg))

        self.generate_output_reports()
