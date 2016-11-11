from __future__ import division
import os
import sys
import numpy as np

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx


class TestBaseGHX(unittest.TestCase):
    def test_dens(self):
        """
        Tests fluid density calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 1.0

        self.assertAlmostEqual(curr_tst.dens(20), 998.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.dens(40), 992.1, delta=tolerance)
        self.assertAlmostEqual(curr_tst.dens(60), 983.3, delta=tolerance)
        self.assertAlmostEqual(curr_tst.dens(80), 971.8, delta=tolerance)

    def test_cp(self):
        """
        Tests fluid specific heat calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 4.0

        self.assertAlmostEqual(curr_tst.cp(20), 4182, delta=tolerance)
        self.assertAlmostEqual(curr_tst.cp(40), 4179, delta=tolerance)
        self.assertAlmostEqual(curr_tst.cp(60), 4185, delta=tolerance)
        self.assertAlmostEqual(curr_tst.cp(80), 4197, delta=tolerance)

    def test_visc(self):
        """
        Tests fluid viscosity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 1E-4

        self.assertAlmostEqual(curr_tst.visc(20), 1.002E-3, delta=tolerance)
        self.assertAlmostEqual(curr_tst.visc(40), 0.653E-3, delta=tolerance)
        self.assertAlmostEqual(curr_tst.visc(60), 0.467E-3, delta=tolerance)
        self.assertAlmostEqual(curr_tst.visc(80), 0.355E-3, delta=tolerance)

    def test_cond(self):
        """
        Tests fluid conductivity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 1E-2

        self.assertAlmostEqual(curr_tst.cond(20), 0.598, delta=tolerance)
        self.assertAlmostEqual(curr_tst.cond(40), 0.631, delta=tolerance)
        self.assertAlmostEqual(curr_tst.cond(60), 0.654, delta=tolerance)
        self.assertAlmostEqual(curr_tst.cond(80), 0.670, delta=tolerance)

    def test_pr(self):
        """
        Tests fluid Prandtl number calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 1E-1

        self.assertAlmostEqual(curr_tst.pr(20), 7.01, delta=tolerance)
        self.assertAlmostEqual(curr_tst.pr(40), 4.32, delta=tolerance)
        self.assertAlmostEqual(curr_tst.pr(60), 2.99, delta=tolerance)
        self.assertAlmostEqual(curr_tst.pr(80), 2.22, delta=tolerance)

    def test_interp_g_funcs(self):
        """
        Tests g-function interpolation
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
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
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_ts()

        tolerance = 0.1

        self.assertAlmostEqual(curr_tst.ts, 645858729.2, delta=tolerance)

    def test_init_bh_resistance_calcs(self):
        """
        Tests parameters that are initialized for bh resistance calcs
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_pipe_resistance()

        theta_1 = curr_tst.ave_shank_space / (2 * curr_tst.ave_bh_radius)
        theta_2 = curr_tst.ave_bh_radius / (curr_tst.ave_pipe_out_dia / 2)
        theta_3 = 1 / (2 * theta_1 * theta_2)
        sigma = (curr_tst.grout_cond - curr_tst.ground_cond) / (curr_tst.grout_cond + curr_tst.ground_cond)

        tolerance = 0.0000001

        self.assertAlmostEqual(curr_tst.theta_1, theta_1, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, theta_2, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_3, theta_3, delta=tolerance)
        self.assertAlmostEqual(curr_tst.sigma, sigma, delta=tolerance)

    def test_calc_pipe_convection_resistance(self):
        """
        Tests the pipe inside convection resistance calculation
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 0.00001

        curr_tst.calc_pipe_convection_resistance()

        self.assertAlmostEqual(curr_tst.resist_pipe_convection, 0.0044539, delta=tolerance)

        curr_tst.flow_rate /= 10

        curr_tst.calc_pipe_convection_resistance()

        self.assertAlmostEqual(curr_tst.resist_pipe_convection, 0.1357208, delta=tolerance)

    def test_calc_pipe_conduction_resistance(self):
        """
        Tests the 1-D radial thermal resistance calculation
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_pipe_conduction_resistance()

        tolerance = 0.00001

        self.assertAlmostEqual(curr_tst.resist_pipe_conduction, 0.082204, delta=tolerance)

    def test_calc_bh_average_thermal_resistance(self):
        """
        Tests average borehole thermal resistance calculation
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_pipe_resistance()

        tolerance = 0.0000001

        curr_tst.calc_bh_average_thermal_resistance()

        #self.assertAlmostEqual(curr_tst.resist_bh_ave, 0.059461853, delta=tolerance)

    def test_calc_bh_total_internal_thermal_resistance(self):
        """
        Tests total borehole internal thermal resistance calculation
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        curr_tst.calc_pipe_resistance()

        tolerance = 0.0000001

        curr_tst.calc_bh_total_internal_thermal_resistance()

        #self.assertAlmostEqual(curr_tst.resist_bh_total_internal, 0.12100078627, delta=tolerance)

    def test_calc_bh_effective_resistance(self):
        """
        Tests effective borehole resistance calculation
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 0.0000001

        curr_tst.calc_bh_effective_resistance()

        #self.assertAlmostEqual(curr_tst.resist_bh_effective, 0.122119276229, delta=tolerance)

    def test_friction_factor(self):
        """
        Test the smooth tube friction factor calculations
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance = 0.00001

        # laminar tests
        re = 100
        self.assertEqual(curr_tst.friction_factor(re), 64.0/re)

        re = 1000
        self.assertEqual(curr_tst.friction_factor(re), 64.0/re)

        re = 1400
        self.assertEqual(curr_tst.friction_factor(re), 64.0/re)

        # transitional tests
        re = 2000
        self.assertAlmostEqual(curr_tst.friction_factor(re), 0.034003503, delta=tolerance)

        re = 3000
        self.assertAlmostEqual(curr_tst.friction_factor(re), 0.033446219, delta=tolerance)

        re = 4000
        self.assertAlmostEqual(curr_tst.friction_factor(re), 0.03895358, delta=tolerance)

        # turbulent tests
        re = 5000
        self.assertEqual(curr_tst.friction_factor(re), (0.79 * np.log(re) - 1.64)**(-2.0))

        re = 15000
        self.assertEqual(curr_tst.friction_factor(re), (0.79 * np.log(re) - 1.64)**(-2.0))

        re = 25000
        self.assertEqual(curr_tst.friction_factor(re), (0.79 * np.log(re) - 1.64)**(-2.0))

    def test_grout_resistance(self):
        """
        Tests the grout resistance. Validation values come from Javed & Spitler 2016

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.
        """

        ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
        config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
                                        'test_Euler_config.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

        # init
        curr_tst = ghx.BaseGHX(ghx_file_path, config_file_path, csv_file_path, False)

        tolerance_low = 0.001
        tolerance_high = 0.0001

        curr_tst.ground_cond = 3.0
        curr_tst.grout_cond = 0.6

        curr_tst.ave_pipe_out_dia = 0.032
        curr_tst.ave_bh_radius = 0.096/2.0
        curr_tst.ave_shank_space = 0.333 * 2 * curr_tst.ave_bh_radius
        curr_tst.resist_pipe = 0.05
        curr_tst.beta = 2 * np.pi * curr_tst.resist_pipe * curr_tst.grout_cond
        curr_tst.init_bh_resistance_calcs()

        self.assertEqual(curr_tst.theta_2, 3)
        self.assertAlmostEqual(curr_tst.theta_1, 0.333, delta=tolerance_low)

        curr_tst.calc_bh_average_thermal_resistance()

        resist_grout = curr_tst.resist_bh_ave - curr_tst.resist_pipe/2.0

        self.assertAlmostEqual(resist_grout, 0.17742, delta=tolerance_high)
