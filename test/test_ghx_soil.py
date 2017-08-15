import os
import sys

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
from ghx.ghx_soil import *


class TestSoilClass(unittest.TestCase):

    def test_init(self):

        dict_soil = {
               'Conductivity': 2.493,
               'Density': 1500,
               'Specific Heat': 1663.8,
               'Temperature': 13.0
               }

        curr_tst = SoilClass(dict_soil, False)

        self.assertEqual(curr_tst.conductivity, dict_soil['Conductivity'])
        self.assertEqual(curr_tst.density, dict_soil['Density'])
        self.assertEqual(curr_tst.specific_heat, dict_soil['Specific Heat'])
        self.assertEqual(curr_tst.undisturbed_temp, dict_soil['Temperature'])


