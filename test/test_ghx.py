from __future__ import division
import os
import sys
import numpy as np
from collections import deque

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx


class TestBaseGHX(unittest.TestCase):
    def test_dens(self):
        """
        Tests fluid density calculation routine
        """
        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 0.1

        # expect passing test
        self.assertAlmostEqual(curr_tst.dens(20), 998.2, delta=tolerance)

    def test_cp(self):
        """
        Tests fluid specific heat calculation routine
        """
        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 0.1

        # expect passing test
        self.assertAlmostEqual(curr_tst.cp(20), 4184.1, delta=tolerance)

    def test_interp_g_funcs(self):
        """
        Tests g-function interpolation
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 0.1

        # extrapolate down
        self.assertAlmostEqual(curr_tst.g_func(-17.0), -4.38, delta=tolerance)

        # in-range
        self.assertAlmostEqual(curr_tst.g_func(0.0), 7.70, delta=tolerance)

        # extrapolate up
        self.assertAlmostEqual(curr_tst.g_func(5.0), 8.29, delta=tolerance)

    def test_calc_ts(self):
        """
        Tests calc_ts which sets timescale
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_ts()

        tolerance = 0.1

        self.assertAlmostEqual(curr_tst.ts, 645858729.2, delta=tolerance)

    def test_calc_pipe_resistance(self):
        """
        Tests the 1-D radial thermal resistance calculation
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_pipe_resistance()

        tolerance = 0.00001

        self.assertAlmostEqual(curr_tst.resist_pipe, 0.082204, delta=tolerance)

    def test_calc_bh_average_thermal_resistance(self):
        """
        Tests average borehole thermal resistance calculation, Eq 13 from:

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_pipe_resistance()

        theta_1 = curr_tst.ave_shank_space / (2 * curr_tst.ave_bh_radius)
        theta_2 = curr_tst.ave_bh_radius / curr_tst.ave_pipe_out_dia
        theta_3 = 1 / (2 * theta_1 * theta_2)
        sigma = (curr_tst.grout_cond - curr_tst.ground_cond) / (curr_tst.grout_cond + curr_tst.ground_cond)
        beta = 2 * np.pi * curr_tst.grout_cond * curr_tst.resist_pipe

        tolerance = 0.0000001

        self.assertAlmostEqual(theta_1, 0.455818022747, delta=tolerance)
        self.assertAlmostEqual(theta_2, 2.1404494382, delta=tolerance)
        self.assertAlmostEqual(theta_3, 0.512476007678, delta=tolerance)
        self.assertAlmostEqual(sigma, -0.54031510658, delta=tolerance)
        self.assertAlmostEqual(beta, 0.384279661722, delta=tolerance)

        curr_tst.calc_bh_average_thermal_resistance(theta_1, theta_2, theta_3, sigma, beta)

        self.assertAlmostEqual(curr_tst.resist_bh_ave, 0.115768625391, delta=tolerance)

    def test_calc_bh_total_internal_thermal_resistance(self):
        """
        Tests total borehole internal thermal resistance calculation, Eq 26 from:

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_pipe_resistance()

        theta_1 = curr_tst.ave_shank_space / (2 * curr_tst.ave_bh_radius)
        theta_2 = curr_tst.ave_bh_radius / curr_tst.ave_pipe_out_dia
        theta_3 = 1 / (2 * theta_1 * theta_2)
        sigma = (curr_tst.grout_cond - curr_tst.ground_cond) / (curr_tst.grout_cond + curr_tst.ground_cond)
        beta = 2 * np.pi * curr_tst.grout_cond * curr_tst.resist_pipe

        tolerance = 0.0000001

        self.assertAlmostEqual(theta_1, 0.455818022747, delta=tolerance)
        self.assertAlmostEqual(theta_2, 2.1404494382, delta=tolerance)
        self.assertAlmostEqual(theta_3, 0.512476007678, delta=tolerance)
        self.assertAlmostEqual(sigma, -0.54031510658, delta=tolerance)
        self.assertAlmostEqual(beta, 0.384279661722, delta=tolerance)

        curr_tst.calc_bh_total_internal_thermal_resistance(theta_1, theta_3, sigma, beta)

        self.assertAlmostEqual(curr_tst.resist_bh_total_internal, 0.334506985755, delta=tolerance)

    def test_calc_bh_effective_resistance(self):
        """
        Tests effective borehole resistance calculation, Eq 3-67 from:

        Javed, S. & Spitler, J.D. Calculation of Borehole Thermal Resistance. In 'Advances in
        Ground-Source Heat Pump Systems,' pp. 84. Rees, S.J. ed. Cambridge, MA. Elsevier Ltd. 2016.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 0.0000001

        curr_tst.calc_bh_effective_resistance()

        self.assertAlmostEqual(curr_tst.resist_bh_effective, 0.119361468501, delta=tolerance)


class TestAggregatedLoad(unittest.TestCase):
    def test_init(self):
        """
        Tests AggregatedLoad Class
        """

        # init
        curr_tst = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, 10)

        # check average load
        self.assertEqual(curr_tst.q, 5.5)

        # check time
        self.assertEqual(curr_tst.time(), 0)


class TestGHXArrayDynamicAggBlocks(unittest.TestCase):
    def test_init(self):
        """
        Tests input processing
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.GHXArrayDynamicAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

        # check data
        self.assertEqual(curr_tst.name, "Vertical GHE 1x2 Std")
        self.assertEqual(curr_tst.num_bh, 2)
        self.assertEqual(curr_tst.flow_rate, 0.000303)
        self.assertEqual(curr_tst.ground_cond, 2.493)
        self.assertEqual(curr_tst.ground_heat_capacity, 2.4957E06)
        self.assertEqual(curr_tst.ground_temp, 13.0)
        self.assertEqual(curr_tst.grout_cond, 0.744)
        self.assertEqual(curr_tst.fluid, "Water")
        self.assertTrue(curr_tst.g_func_present)

        for i in range(curr_tst.num_bh):
            self.assertEqual(curr_tst.ghx_list[i].name, "BH %d" % (i + 1))
            self.assertEqual(curr_tst.ghx_list[i].location, [0, 0])
            self.assertEqual(curr_tst.ghx_list[i].bh_length, 76.2)
            self.assertEqual(curr_tst.ghx_list[i].bh_radius, 0.05715)
            self.assertEqual(curr_tst.ghx_list[i].pipe_cond, 0.389)
            self.assertEqual(curr_tst.ghx_list[i].pipe_out_dia, 0.0267)
            self.assertEqual(curr_tst.ghx_list[i].shank_space, 0.0521)
            self.assertEqual(curr_tst.ghx_list[i].pipe_thickness, 0.00243)

        self.assertEqual(curr_tst.sim_years, 1)
        self.assertEqual(curr_tst.aggregation_type, "Test Dynamic Blocks")
        self.assertEqual(curr_tst.min_hourly_history, 192)

    def test_merge_agg_load_objs(self):
        """
        Tests merge_agg_load_objs, which merges AggregatedLoad objects into a single object
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.GHXArrayDynamicAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

        # make a few dummy AggregatedLoad classes
        obj_1 = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, 10)
        obj_2 = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10, 10)
        obj_3 = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 20, 10)
        obj_4 = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 30, 10)

        obj_list = [obj_1, obj_2, obj_3, obj_4]

        ret_obj = curr_tst.merge_agg_load_objs(obj_list)

        # check average load
        self.assertEqual(ret_obj.q, 5.5)

        # check time
        self.assertEqual(ret_obj.time(), 0)

    def test_aggregate_load(self):
        """
        Tests aggregate_load which aggregates and merges aggregated objects
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_dynamic_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.GHXArrayDynamicAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

        # should initialize empty first object for comparative purposes
        # [0]
        self.assertEqual(len(curr_tst.agg_load_objects), 1)

        # add object from hours 1-5
        # [0, 5]
        curr_tst.hourly_loads = deque([1, 1, 1, 1, 1])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 2)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1)

        # add object from hours 6-10
        # [0, 5, 5]
        curr_tst.hourly_loads = deque([2, 2, 2, 2, 2])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 3)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 5)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 2)

        # add object from hours 11-15
        # first two 5 hour blocks collapse into one 10 hour block
        # [0,10,5]
        curr_tst.hourly_loads = deque([3, 3, 3, 3, 3])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 3)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 10)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1.5)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 3)

        # add object from hours 16-20
        # [0,10,5,5]
        curr_tst.hourly_loads = deque([4, 4, 4, 4, 4])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 10)
        self.assertEqual(curr_tst.agg_load_objects[3].time(), 15)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1.5)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 3)
        self.assertEqual(curr_tst.agg_load_objects[3].q, 4)

        # add object from hours 21-25
        # second two 5 hour blocks collapse into one 10 hour block
        # [0,10,10,5]
        curr_tst.hourly_loads = deque([5, 5, 5, 5, 5])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 10)
        self.assertEqual(curr_tst.agg_load_objects[3].time(), 20)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1.5)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 3.5)
        self.assertEqual(curr_tst.agg_load_objects[3].q, 5)

        # add object from hours 26-30
        # first two 10 hour blocks collapse into one 20 hour block
        # [0,20,5,5]
        curr_tst.hourly_loads = deque([6, 6, 6, 6, 6])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 20)
        self.assertEqual(curr_tst.agg_load_objects[3].time(), 25)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 2.5)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 5.0)
        self.assertEqual(curr_tst.agg_load_objects[3].q, 6.0)


class TestGHXArrayStaticAggBlocks(unittest.TestCase):
    def test_init(self):
        """
        Tests input processing
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_static_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.GHXArrayStaticAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

        # check data
        self.assertEqual(curr_tst.name, "Vertical GHE 1x2 Std")
        self.assertEqual(curr_tst.num_bh, 2)
        self.assertEqual(curr_tst.flow_rate, 0.000303)
        self.assertEqual(curr_tst.ground_cond, 2.493)
        self.assertEqual(curr_tst.ground_heat_capacity, 2.4957E06)
        self.assertEqual(curr_tst.ground_temp, 13.0)
        self.assertEqual(curr_tst.grout_cond, 0.744)
        self.assertEqual(curr_tst.fluid, "Water")
        self.assertTrue(curr_tst.g_func_present)

        for i in range(curr_tst.num_bh):
            self.assertEqual(curr_tst.ghx_list[i].name, "BH %d" % (i + 1))
            self.assertEqual(curr_tst.ghx_list[i].location, [0, 0])
            self.assertEqual(curr_tst.ghx_list[i].bh_length, 76.2)
            self.assertEqual(curr_tst.ghx_list[i].bh_radius, 0.05715)
            self.assertEqual(curr_tst.ghx_list[i].pipe_cond, 0.389)
            self.assertEqual(curr_tst.ghx_list[i].pipe_out_dia, 0.0267)
            self.assertEqual(curr_tst.ghx_list[i].shank_space, 0.0521)
            self.assertEqual(curr_tst.ghx_list[i].pipe_thickness, 0.00243)

        self.assertEqual(curr_tst.sim_years, 1)
        self.assertEqual(curr_tst.aggregation_type, "Test Static Blocks")
        self.assertEqual(curr_tst.min_hourly_history, 192)

    def test_shift_loads(self):
        """
        Test how loads are shifted
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_static_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.GHXArrayStaticAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

        l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

        i = 1
        curr_tst.shift_loads(l[i])
        self.assertEqual(len(curr_tst.agg_load_objects), 1)
        self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))

        for i in range(2, 4):
            curr_tst.shift_loads(l[i])
            self.assertEqual(len(curr_tst.agg_load_objects), 2)
            self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))
            if i == 2:
                self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 2]]))
            elif i ==3:
                self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 3], l[i - 2]]))

        for i in range(4, 8):
            curr_tst.shift_loads(i)
            self.assertEqual(len(curr_tst.agg_load_objects), 3)
            self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))
            self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 3], l[i - 2]]))
            if i == 4:
                self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 4]]))
            elif i == 5:
                self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 5], l[i - 4]]))
            elif i == 6:
                self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 6], l[i - 5], l[i - 4]]))
            elif i == 7:
                self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 7], l[i - 6], l[i - 5], l[i - 4]]))

        for i in range(8, 16):
            curr_tst.shift_loads(i)
            self.assertEqual(len(curr_tst.agg_load_objects), 4)
            self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))
            self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 3], l[i - 2]]))
            self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 7], l[i - 6], l[i - 5], l[i - 4]]))
            if i == 8:
                self.assertEqual(curr_tst.agg_load_objects[3].q, np.mean([l[i - 8]]))
            elif i == 9:
                self.assertEqual(curr_tst.agg_load_objects[3].q, np.mean([l[i - 9], l[i - 8]]))
            elif i == 10:
                self.assertEqual(curr_tst.agg_load_objects[3].q, np.mean([l[i - 10], l[i - 9], l[i - 8]]))
            elif i == 11:
                self.assertEqual(curr_tst.agg_load_objects[3].q, np.mean([l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
            elif i == 12:
                self.assertEqual(curr_tst.agg_load_objects[3].q,
                                 np.mean([l[i - 12], l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
            elif i == 13:
                self.assertEqual(curr_tst.agg_load_objects[3].q,
                                 np.mean([l[i - 13], l[i - 12], l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
            elif i == 14:
                self.assertEqual(curr_tst.agg_load_objects[3].q,
                                 np.mean([l[i - 14], l[i - 13], l[i - 12], l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
            elif i == 15:
                self.assertEqual(curr_tst.agg_load_objects[3].q,
                                 np.mean([l[i - 15], l[i - 14], l[i - 13], l[i - 12],
                                          l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))

        for i in range(16, 24):
            curr_tst.shift_loads(i)
            self.assertEqual(len(curr_tst.agg_load_objects), 5)
            self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))
            self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 3], l[i - 2]]))
            self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 7], l[i - 6], l[i - 5], l[i - 4]]))
            self.assertEqual(curr_tst.agg_load_objects[3].q,
                             np.mean([l[i - 15], l[i - 14], l[i - 13], l[i - 12],
                                      l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
            if i == 16:
                self.assertEqual(curr_tst.agg_load_objects[4].q, np.mean([l[i - 16]]))
            elif i == 17:
                self.assertEqual(curr_tst.agg_load_objects[4].q, np.mean([l[i - 17], l[i - 16]]))
            elif i == 18:
                self.assertEqual(curr_tst.agg_load_objects[4].q, np.mean([l[i - 18], l[i - 17], l[i - 16]]))
            elif i == 19:
                self.assertEqual(curr_tst.agg_load_objects[4].q,
                                 np.mean([l[i - 19], l[i - 18], l[i - 17], l[i - 16]]))
            elif i == 20:
                self.assertEqual(curr_tst.agg_load_objects[4].q,
                                 np.mean([l[i - 20], l[i - 19], l[i - 18], l[i - 17], l[i - 16]]))
            elif i == 21:
                self.assertEqual(curr_tst.agg_load_objects[4].q,
                                 np.mean([l[i - 21], l[i - 20], l[i - 19], l[i - 18], l[i - 17], l[i - 16]]))
            elif i == 22:
                self.assertEqual(curr_tst.agg_load_objects[4].q,
                                 np.mean([l[i - 22], l[i - 21], l[i - 20], l[i - 19],
                                          l[i - 18], l[i - 17], l[i - 16]]))
            elif i == 23:
                self.assertEqual(curr_tst.agg_load_objects[4].q,
                                 np.mean([l[i - 23], l[i - 22], l[i - 21], l[i - 20],
                                          l[i - 19], l[i - 18], l[i - 17], l[i - 16]]))

    def test_shift_loads_for_q_est(self):
        """
        q_estimate method
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                     'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_static_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                     'testing.csv')

        # init
        curr_tst = ghx.GHXArrayStaticAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

        l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

        for i in range(1, 10):
            curr_tst.shift_loads(l[i])
            if i == 2:
                self.assertEqual(curr_tst.agg_load_objects[1].q_est, 0)
            elif i == 3:
                self.assertEqual(curr_tst.agg_load_objects[1].q_est, 0.5)
            elif i == 4:
                self.assertEqual(curr_tst.agg_load_objects[1].q_est, 1.25)
                self.assertEqual(curr_tst.agg_load_objects[2].q_est, 0.5)
            elif i == 5:
                self.assertEqual(curr_tst.agg_load_objects[1].q_est, 2.125)
                self.assertEqual(curr_tst.agg_load_objects[2].q_est, 0.875)

# allow execution directly as python tests/test_ghx.py
if __name__ == '__main__':
    unittest.main()
