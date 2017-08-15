
import os
import sys

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
from ghx.ghx_borehole import *


class TestBoreholeClass(unittest.TestCase):

    def test_init(self):

        dict_bh = {
                  'Name': 'BH 1',
                  'Location': [0, 0],
                  'Depth': 76.2,
                  'Radius': 0.05715,
                  'Shank Spacing': 0.0521,
                  'Pipe':
                       {
                      'Outside Diameter': 0.0267,
                      'Wall Thickness': 0.00243,
                      'Conductivity': 0.389,
                      'Density': 800,
                      'Specific Heat': 1000
                      },
                  'Fluid':
                      {
                      'Type': 'Water',
                      'Concentration': 100,
                      'Flow Rate': 0.5
                      },
                  'Soil':
                      {
                      'Conductivity': 2.493,
                      'Density': 1500,
                      'Specific Heat': 1663.8,
                      'Temperature': 13.0
                      },
                  'Grout':
                      {
                      'Conductivity': 0.744,
                      'Density': 1000,
                      'Specific Heat': 1000
                      }
                  }

        curr_tst = BoreholeClass(dict_bh, False)

        self.assertEqual(curr_tst.name, dict_bh['Name'])
        self.assertEqual(curr_tst.location, dict_bh['Location'])
        self.assertEqual(curr_tst.depth, dict_bh['Depth'])
        self.assertEqual(curr_tst.radius, dict_bh['Radius'])
        self.assertEqual(curr_tst.diameter, dict_bh['Radius'] * 2)
        self.assertEqual(curr_tst.shank_space, dict_bh['Shank Spacing'])
        self.assertEqual(curr_tst.pipe.outer_diameter, dict_bh['Pipe']['Outside Diameter'])

    def test_calc_bh_total_internal_resistance(self):

        dict_bh = {
                  'Name': 'BH 1',
                  'Location': [0, 0],
                  'Depth': 76.2,
                  'Radius': 0.048,
                  'Shank Spacing': 0.032,
                  'Pipe':
                       {
                      'Outside Diameter': 0.032,
                      'Wall Thickness': 0.00243,
                      'Conductivity': 0.389,
                      'Density': 800,
                      'Specific Heat': 1000
                      },
                  'Fluid':
                      {
                      'Type': 'Water',
                      'Concentration': 100,
                      'Flow Rate': 0.5
                      },
                  'Soil':
                      {
                      'Conductivity': 4.0,
                      'Density': 1500,
                      'Specific Heat': 1663.8,
                      'Temperature': 13.0
                      },
                  'Grout':
                      {
                      'Conductivity': 0.6,
                      'Density': 1000,
                      'Specific Heat': 1000
                      }
                  }

        tolerance = 0.00001

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.32365, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.23126, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.19830, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18070, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16947, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16152, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.32754, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.23529, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20214, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18428, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17275, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16453, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.33415, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24161, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20788, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18942, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17734, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16864, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.34783, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.25298, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.21738, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.19744, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18420, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17456, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.45329, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.29701, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24310, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.21511, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.19766, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18555, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.46560, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.30669, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.25113, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.22197, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20363, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.19082, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.48651, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.32190, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.26312, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.23184, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.21196, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.19800, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.52992, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.34923, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.28294, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24724, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.22443, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20837, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.44849, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.33093, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.28097, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.25194, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.23252, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.21839, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.49081, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35908, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.30227, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.26911, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24689, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.23075, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.56145, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.40275, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.33381, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.29370, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.26696, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24762, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.70364, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.47982, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.38537, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.33186, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.29691, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.27207, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35072, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24556, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20667, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18552, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17194, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16235, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35151, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24649, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20760, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18641, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17275, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16310, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35289, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24797, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20901, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18769, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17390, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16412, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35595, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.25077, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.21141, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18971, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17561, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16558, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.79250, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.46254, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35062, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.29359, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.25871, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.23502, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.80334, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.47089, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35730, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.29907, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.26330, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.23893, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.82235, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.48435, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.36744, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.30702, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.26973, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24425, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.86441, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.50970, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.38466, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.31960, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.27937, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.25189, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.61186, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.46146, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.39174, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.34857, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.31835, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.29565, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.68753, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.51388, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.43140, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.38012, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.34428, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.31748, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.81754, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.59704, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.49099, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.42563, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.38053, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.34722, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 1.09392, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.74945, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.59065, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.49705, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.43476, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.39009, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35512, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24806, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20819, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18641, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17239, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16250, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35546, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24847, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20860, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18680, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17275, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16284, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35606, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.24912, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.20922, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18737, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17326, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16329, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35739, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.25036, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.21029, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.18827, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.17402, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.16394, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.99531, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.56245, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.41627, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.34215, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.29705, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.26657, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 1.00551, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.57026, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.42245, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.34718, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.30122, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.27010, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 1.02350, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.58289, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.43187, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.35448, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.30706, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.27488, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 1.06368, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.60688, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.44794, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.36606, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.31582, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.28175, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.68527, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.52300, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.44557, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.39656, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.36169, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.33518, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.77817, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.58840, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.49530, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.43614, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.39417, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.36245, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.93884, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.69271, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.57029, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.49335, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.43958, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.39955, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 1.28480, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.88570, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.69643, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.58336, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.50757, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.45299, delta=tolerance)

    def test_calc_bh_grout_resistance(self):

        dict_bh = {
                  'Name': 'BH 1',
                  'Location': [0, 0],
                  'Depth': 76.2,
                  'Radius': 0.048,
                  'Shank Spacing': 0.032,
                  'Pipe':
                       {
                      'Outside Diameter': 0.032,
                      'Wall Thickness': 0.00243,
                      'Conductivity': 0.389,
                      'Density': 800,
                      'Specific Heat': 1000
                      },
                  'Fluid':
                      {
                      'Type': 'Water',
                      'Concentration': 100,
                      'Flow Rate': 0.5
                      },
                  'Soil':
                      {
                      'Conductivity': 4.0,
                      'Density': 1500,
                      'Specific Heat': 1663.8,
                      'Temperature': 13.0
                      },
                  'Grout':
                      {
                      'Conductivity': 0.6,
                      'Density': 1000,
                      'Specific Heat': 1000
                      }
                  }

        tolerance = 0.00001

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.17701, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09211, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06329, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04861, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03965, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03358, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.17732, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09230, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06341, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04869, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03970, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03361, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.17787, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09259, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06358, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04880, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03977, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03366, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.17910, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09315, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06387, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04897, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03988, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.33333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03373, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.14218, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07445, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05122, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03931, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03200, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02704, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.14295, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07492, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05153, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03952, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03216, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02716, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.14429, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07567, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05199, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03983, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03237, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02732, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.14724, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07707, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05278, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04032, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03270, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.04266667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.44444, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02754, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06695, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04131, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03069, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02461, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02061, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.01776, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07090, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04361, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03222, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02572, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02146, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.01844, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07759, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04720, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03450, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02731, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02265, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.01936, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09138, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05361, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03825, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02979, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02442, delta=tolerance)

        dict_bh['Radius'] = 0.048
        dict_bh['Shank Spacing'] = 0.06400000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.66667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 3.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02069, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.36382, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.18488, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.12489, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09471, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07647, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06424, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.36384, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.18489, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.12490, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09471, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07647, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06424, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.36387, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.18491, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.12491, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09472, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07648, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06424, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.36394, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.18494, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.12493, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09473, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07649, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.16667, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06424, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.26405, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.13316, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08934, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06733, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05407, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04520, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.26434, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.13336, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08948, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06744, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05416, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04527, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.26484, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.13369, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08971, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06760, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05428, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04537, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.26597, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.13430, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09009, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06786, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05447, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.07466667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.38889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04551, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09055, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05854, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04486, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03684, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03146, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02757, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09914, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06410, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04889, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03995, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03397, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.02964, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.11380, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07288, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05492, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04444, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03747, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03247, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.14454, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08878, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06494, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05145, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04270, delta=tolerance)

        dict_bh['Radius'] = 0.096
        dict_bh['Shank Spacing'] = 0.16000000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.83333, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 6.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03656, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.47152, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.23870, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.16076, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.12160, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09798, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08216, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.47153, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.23870, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.16076, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.12160, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09799, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08216, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.47153, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.23871, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.16076, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.12160, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09799, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08216, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.47155, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.23871, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.16077, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.12160, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09799, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.03200000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.11111, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08216, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.32711, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.16421, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.10980, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08254, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06615, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05521, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.32731, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.16436, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.10991, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08263, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06623, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05527, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.32768, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.16460, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.11009, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08276, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06633, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05535, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.32850, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.16507, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.11038, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08297, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06648, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.10666667
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.37037, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05547, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.10481, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06997, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05467, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04553, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03930, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 4.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03472, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.11665, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.07790, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06054, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05011, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04302, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 3.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.03782, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.13696, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.09047, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06934, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05672, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04821, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 2.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04204, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 0.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.18002, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.2
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.11344, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 1.8
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.08403, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 2.4
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.06709, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.0
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.05599, delta=tolerance)

        dict_bh['Radius'] = 0.144
        dict_bh['Shank Spacing'] = 0.25600000
        dict_bh['Soil']['Conductivity'] = 1.0
        dict_bh['Grout']['Conductivity'] = 3.6
        curr_tst = BoreholeClass(dict_bh, False)
        curr_tst.pipe.resist_pipe = 0.05
        self.assertAlmostEqual(curr_tst.theta_1, 0.88889, delta=tolerance)
        self.assertAlmostEqual(curr_tst.theta_2, 9.0, delta=tolerance)
        self.assertAlmostEqual(curr_tst.calc_bh_grout_resistance(), 0.04812, delta=tolerance)

    def test_calc_bh_resistance(self):

        dict_bh = {
                  'Name': 'BH 1',
                  'Location': [0, 0],
                  'Depth': 76.2,
                  'Radius': 0.048,
                  'Shank Spacing': 0.032,
                  'Pipe':
                       {
                      'Outside Diameter': 0.032,
                      'Wall Thickness': 0.00243,
                      'Conductivity': 0.389,
                      'Density': 800,
                      'Specific Heat': 1000
                      },
                  'Fluid':
                      {
                      'Type': 'Water',
                      'Concentration': 100,
                      'Flow Rate': 0.5
                      },
                  'Soil':
                      {
                      'Conductivity': 4.0,
                      'Density': 1500,
                      'Specific Heat': 1663.8,
                      'Temperature': 13.0
                      },
                  'Grout':
                      {
                      'Conductivity': 0.6,
                      'Density': 1000,
                      'Specific Heat': 1000
                      }
                  }

        tolerance = 0.00001

        curr_tst = BoreholeClass(dict_bh, False)

        self.assertAlmostEqual(curr_tst.calc_bh_total_internal_resistance(), 0.36818, delta=tolerance)
