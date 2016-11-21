from __future__ import division
import os
import sys

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import numpy as np

import unittest
import ghx.ghx_pipe


class TestPipeClass(unittest.TestCase):

    def test_init(self):

        """
        Test initialization
        """

        dict_pipe = {
                     'Outside Diameter': 0.0267,
                     'Wall Thickness': 0.00243,
                     'Conductivity': 0.389,
                     'Density': 800,
                     'Specific Heat': 1000
                    }

        dict_fluid = {
                     'Type': 'Water',
                     'Concentration': 100,
                     'Flow Rate': 0.000303
                     }

        curr_tst = ghx.PipeClass(dict_pipe, dict_fluid, 13.0, False)

        self.assertEqual(curr_tst.outer_diameter, dict_pipe['Outside Diameter'])
        self.assertEqual(curr_tst.outer_radius, dict_pipe['Outside Diameter'] / 2)

        self.assertEqual(curr_tst.inner_diameter, dict_pipe['Outside Diameter'] - 2 * dict_pipe['Wall Thickness'])
        self.assertEqual(curr_tst.inner_radius, (dict_pipe['Outside Diameter'] - 2 * dict_pipe['Wall Thickness']) / 2)

    def test_friction_factor(self):

        """
        Test the smooth tube friction factor calculations
        """

        dict_pipe = {
                    'Outside Diameter': 0.0267,
                    'Wall Thickness': 0.00243,
                    'Conductivity': 0.389,
                    'Density': 800,
                    'Specific Heat': 1000
                    }

        dict_fluid = {
                     'Type': 'Water',
                     'Concentration': 100,
                     'Flow Rate': 0.000303
                     }

        curr_tst = ghx.PipeClass(dict_pipe, dict_fluid, 13.0, False)

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

    def test_calc_pipe_convection_resistance(self):

        """
        Tests the pipe inside convection resistance calculation
        """

        dict_pipe = {
                    'Outside Diameter': 0.0267,
                    'Wall Thickness': 0.00243,
                    'Conductivity': 0.389,
                    'Density': 800,
                    'Specific Heat': 1000
                    }

        dict_fluid = {'Type': 'Water',
                      'Concentration': 100,
                      'Flow Rate': 0.000303
                     }

        curr_tst = ghx.PipeClass(dict_pipe, dict_fluid, 13.0, False)

        tolerance = 0.00001

        self.assertAlmostEqual(curr_tst.calc_pipe_convection_resistance(), 0.005716, delta=tolerance)

        curr_tst.fluid.flow_rate /= 10

        self.assertAlmostEqual(curr_tst.calc_pipe_convection_resistance(), 0.1428580, delta=tolerance)

    def test_calc_pipe_conduction_resistance(self):

        """
        Tests the 1-D radial thermal resistance calculation
        """

        dict_pipe = {
                    'Outside Diameter': 0.0267,
                    'Wall Thickness': 0.00243,
                    'Conductivity': 0.389,
                    'Density': 800,
                    'Specific Heat': 1000
                    }

        dict_fluid = {
                     'Type': 'Water',
                     'Concentration': 100,
                     'Flow Rate': 0.000303
                     }

        curr_tst = ghx.PipeClass(dict_pipe, dict_fluid, 13.0, False)

        tolerance = 0.00001

        self.assertAlmostEqual(curr_tst.calc_pipe_conduction_resistance(), 0.082204, delta=tolerance)

    def test_calc_pipe_resistance(self):

        """
        Tests the total pipe thermal resistance
        """

        dict_pipe = {
                    'Outside Diameter': 0.0267,
                    'Wall Thickness': 0.00243,
                    'Conductivity': 0.389,
                    'Density': 800,
                    'Specific Heat': 1000
                    }

        dict_fluid = {
                     'Type': 'Water',
                     'Concentration': 100,
                     'Flow Rate': 0.000303
                     }

        curr_tst = ghx.PipeClass(dict_pipe, dict_fluid, 13.0, False)

        tolerance = 0.00001

        self.assertAlmostEqual(curr_tst.calc_pipe_resistance(), 0.082204 + 0.005716, delta=tolerance)
