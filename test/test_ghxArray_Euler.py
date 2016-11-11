from __future__ import division
import os
import sys
from collections import deque

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx


class TestGHXArrayEulerAggBlocks(unittest.TestCase):

    def test_init(self):

        """
        Tests input processing
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.GHXArrayEulerAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

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
        self.assertEqual(curr_tst.aggregation_type, "Test Euler Blocks")
        self.assertEqual(curr_tst.min_hourly_history, 192)

    def test_merge_agg_load_objs(self):

        """
        Tests merge_agg_load_objs, which merges AggregatedLoad objects into a single object
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.GHXArrayEulerAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

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
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.GHXArrayEulerAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

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
