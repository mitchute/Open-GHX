
import os
import sys
from collections import deque

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx

class TestGHXArray(unittest.TestCase):

    def test_initGHXArray(self):

        """
        Tests input processing
        """
        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.csv')

        # init
        A = ghx.GHXArray(json_file_path, csv_file_path, False) # pass 'False' to suppress output

        # check data
        self.assertEqual(A.name, "Vertical GHE 1x2 Std")
        self.assertEqual(A.num_bh, 2)
        self.assertEqual(A.flow_rate, 0.000303)
        self.assertEqual(A.ground_cond, 2.493)
        self.assertEqual(A.ground_heat_capacity, 2.4957E06)
        self.assertEqual(A.ground_temp, 13.0)
        self.assertEqual(A.fluid, "Water")
        self.assertTrue(A.g_func_present)

        for i in range(A.num_bh):
            self.assertEqual(A.ghx_list[i].name, "BH %d" %(i+1))
            self.assertEqual(A.ghx_list[i].location, [0,0])
            self.assertEqual(A.ghx_list[i].bh_length, 76.2)
            self.assertEqual(A.ghx_list[i].bh_radius, 0.05715)
            self.assertEqual(A.ghx_list[i].grout_cond, 0.744)
            self.assertEqual(A.ghx_list[i].pipe_cond, 0.389)
            self.assertEqual(A.ghx_list[i].pipe_out_dia, 0.0267)
            self.assertEqual(A.ghx_list[i].shank_space, 0.0254)
            self.assertEqual(A.ghx_list[i].pipe_thickness, 0.00243)

    def test_dens(self):

        """
        Tests fluid density calculation routine
        """
        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.csv')

        # init
        A = ghx.GHXArray(json_file_path, csv_file_path, False) # pass 'False' to suppress output

        tolerance = 0.1

        # expect passing test
        self.assertAlmostEqual(A.dens(20), 998.2, delta=tolerance)

    def test_cp(self):

        """
        Tests fluid specific heat calculation routine
        """
        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.csv')

        # init
        A = ghx.GHXArray(json_file_path, csv_file_path, False) # pass 'False' to suppress output

        tolerance = 0.1

        # expect passing test
        self.assertAlmostEqual(A.cp(20), 4184.1, delta=tolerance)

    def test_interp_g_funcs(self):

        """
        Tests g-function interpolation
        """
        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.csv')

        # init
        A = ghx.GHXArray(json_file_path, csv_file_path, False) # pass 'False' to suppress output

        tolerance = 0.1

        # extrapolate down
        self.assertAlmostEqual(A.g_func(-17.0), -4.38, delta=tolerance)

        # in-range
        self.assertAlmostEqual(A.g_func(0.0), 7.70, delta=tolerance)

        # extrapolate up
        self.assertAlmostEqual(A.g_func(5.0), 8.29, delta=tolerance)

    def test_calc_ts(self):

        """
        Tests calc_ts which sets timescale
        """

        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.csv')

        # init
        A = ghx.GHXArray(json_file_path, csv_file_path, False) # pass 'False' to suppress output

        A.calc_ts()

        tolerance = 0.1

        self.assertAlmostEqual(A.ts, 645858729.2, delta=tolerance)

    def test_AggregatedLoad_class(self):

        """
        Tests AggregatedLoad Class
        """

        #init
        A = ghx.AggregatedLoad([1,2,3,4,5,6,7,8,9,10], 10, 0)

        # check average load
        self.assertEqual(A.q, 5.5)

        # check time
        self.assertEqual(A.time(), 5)

    def test_merge_agg_load_objs(self):

        """
        Tests merge_agg_load_objs, which merges AggregatedLoad objects into a single object
        """

        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.csv')

        # init
        A = ghx.GHXArray(json_file_path, csv_file_path, False) # pass 'False' to suppress output

        # make a few dummy AggregatedLoad classes
        obj_1 = ghx.AggregatedLoad([1,2,3,4,5,6,7,8,9,10], 10, 0)
        obj_2 = ghx.AggregatedLoad([1,2,3,4,5,6,7,8,9,10], 20, 10)
        obj_3 = ghx.AggregatedLoad([1,2,3,4,5,6,7,8,9,10], 30, 20)
        obj_4 = ghx.AggregatedLoad([1,2,3,4,5,6,7,8,9,10], 40, 30)

        obj_list = [obj_1, obj_2, obj_3, obj_4]

        ret_obj = A.merge_agg_load_objs(obj_list)

        # check average load
        self.assertEqual(ret_obj.q, 5.5)

        # check time
        self.assertEqual(ret_obj.time(), 20)

    def test_aggregate_load(self):

        """
        Tests aggregate_load which aggregates and merges aggregated objects
        """

        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.csv')

        # init
        A = ghx.GHXArray(json_file_path, csv_file_path, False) # pass 'False' to suppress output

        # should initialize empty first object for comparative purposes
        # [0]
        self.assertEqual(len(A.agg_load_objects), 1)

        # add object from hours 1-5
        # [0,5]
        A.hourly_loads = deque([1,1,1,1,1])
        A.aggregate_load(5)

        # check number of objects
        self.assertEqual(len(A.agg_load_objects), 2)

        # check sim hours
        self.assertEqual(A.agg_load_objects[0].ave_sim_hour, 0)
        self.assertEqual(A.agg_load_objects[1].ave_sim_hour, 2.5)

        # check load
        self.assertEqual(A.agg_load_objects[0].q, 0)
        self.assertEqual(A.agg_load_objects[1].q, 1)

        # add object from hours 6-10
        # [0,5,5]
        A.hourly_loads = deque([2,2,2,2,2])
        A.aggregate_load(10)

        # check number of objects
        self.assertEqual(len(A.agg_load_objects), 3)

        # check sim hours
        self.assertEqual(A.agg_load_objects[0].ave_sim_hour, 0)
        self.assertEqual(A.agg_load_objects[1].ave_sim_hour, 2.5)
        self.assertEqual(A.agg_load_objects[2].ave_sim_hour, 7.5)

        # check load
        self.assertEqual(A.agg_load_objects[0].q, 0)
        self.assertEqual(A.agg_load_objects[1].q, 1)
        self.assertEqual(A.agg_load_objects[2].q, 2)

        # add object from hours 11-15
        # first two 5 hour blocks collapse into one 10 hour block
        # [0,10,5]
        A.hourly_loads = deque([3,3,3,3,3])
        A.aggregate_load(15)

        # check number of objects
        self.assertEqual(len(A.agg_load_objects), 3)

        # check sim hours
        self.assertEqual(A.agg_load_objects[0].ave_sim_hour, 0)
        self.assertEqual(A.agg_load_objects[1].ave_sim_hour, 5.0)
        self.assertEqual(A.agg_load_objects[2].ave_sim_hour, 12.5)

        # check load
        self.assertEqual(A.agg_load_objects[0].q, 0)
        self.assertEqual(A.agg_load_objects[1].q, 1.5)
        self.assertEqual(A.agg_load_objects[2].q, 3)

        # add object from hours 16-20
        # [0,10,5,5]
        A.hourly_loads = deque([4,4,4,4,4])
        A.aggregate_load(20)

        # check number of objects
        self.assertEqual(len(A.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(A.agg_load_objects[0].ave_sim_hour, 0)
        self.assertEqual(A.agg_load_objects[1].ave_sim_hour, 5.0)
        self.assertEqual(A.agg_load_objects[2].ave_sim_hour, 12.5)
        self.assertEqual(A.agg_load_objects[3].ave_sim_hour, 17.5)

        # check load
        self.assertEqual(A.agg_load_objects[0].q, 0)
        self.assertEqual(A.agg_load_objects[1].q, 1.5)
        self.assertEqual(A.agg_load_objects[2].q, 3)
        self.assertEqual(A.agg_load_objects[3].q, 4)

        # add object from hours 21-25
        # second two 5 hour blocks collapse into one 10 hour block
        # [0,10,10,5]
        A.hourly_loads = deque([5,5,5,5,5])
        A.aggregate_load(25)

        # check number of objects
        self.assertEqual(len(A.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(A.agg_load_objects[0].ave_sim_hour, 0)
        self.assertEqual(A.agg_load_objects[1].ave_sim_hour, 5.0)
        self.assertEqual(A.agg_load_objects[2].ave_sim_hour, 15.0)
        self.assertEqual(A.agg_load_objects[3].ave_sim_hour, 22.5)

        # check load
        self.assertEqual(A.agg_load_objects[0].q, 0)
        self.assertEqual(A.agg_load_objects[1].q, 1.5)
        self.assertEqual(A.agg_load_objects[2].q, 3.5)
        self.assertEqual(A.agg_load_objects[3].q, 5)

        # add object from hours 26-30
        # first two 10 hour blocks collapse into one 20 hour block
        # [0,20,5,5]
        A.hourly_loads = deque([6,6,6,6,6])
        A.aggregate_load(30)

        # check number of objects
        self.assertEqual(len(A.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(A.agg_load_objects[0].ave_sim_hour, 0)
        self.assertEqual(A.agg_load_objects[1].ave_sim_hour, 10.0)
        self.assertEqual(A.agg_load_objects[2].ave_sim_hour, 22.5)
        self.assertEqual(A.agg_load_objects[3].ave_sim_hour, 27.5)

        # check load
        self.assertEqual(A.agg_load_objects[0].q, 0)
        self.assertEqual(A.agg_load_objects[1].q, 2.5)
        self.assertEqual(A.agg_load_objects[2].q, 5.0)
        self.assertEqual(A.agg_load_objects[3].q, 6.0)

# allow execution directly as python tests/test_ghx.py
if __name__ == '__main__':
    unittest.main()
