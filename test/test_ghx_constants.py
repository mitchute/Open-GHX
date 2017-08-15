import os
import sys

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx.ghx_constants


class TestConstantClass(unittest.TestCase):

    def test_init(self):

        """
        Test initialization
        """

        curr_tst = ghx.ConstantClass()

        self.assertEqual(curr_tst.months_in_year, 12)
        self.assertEqual(curr_tst.hours_in_month, 730)
        self.assertEqual(curr_tst.hours_in_year, 8760)
        self.assertEqual(curr_tst.celsius_to_kelvin, 273.15)
