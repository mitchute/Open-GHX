import unittest

from ghx.constants import ConstantClass


class TestConstantClass(unittest.TestCase):
    def test_init(self):
        """
        Test initialization
        """

        curr_tst = ConstantClass()

        self.assertEqual(curr_tst.months_in_year, 12)
        self.assertEqual(curr_tst.hours_in_month, 730)
        self.assertEqual(curr_tst.hours_in_year, 8760)
        self.assertEqual(curr_tst.celsius_to_kelvin, 273.15)
