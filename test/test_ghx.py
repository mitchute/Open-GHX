
import os
import sys

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

        # expect fail test
        # with self.assertRaises(StandardError):
            # A.dens(-10) # out of range

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

        # expect fail test
        # with self.assertRaises(StandardError):
            # A.cp(-10) # out of range


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

    def test_AggregatedLoad_class(self):

        """
        Tests AggregatedLoad Class
        """

        # init
        A = ghx.AggregatedLoad([0,1,2,3,4,5,6,7,8,9], 10)

        # check average load
        self.assertEqual(A.q, 4.5)

        # check time
        self.assertEqual(A.time(), 10)

# allow execution directly as python tests/test_ghx.py
if __name__ == '__main__':
	unittest.main()
