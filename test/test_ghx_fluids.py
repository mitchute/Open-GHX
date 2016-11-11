from __future__ import division
import os
import sys
import numpy as np

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx


class TestFluidsClass(unittest.TestCase):

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
