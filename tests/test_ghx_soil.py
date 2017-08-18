import unittest

from ghx.soil import SoilClass


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
