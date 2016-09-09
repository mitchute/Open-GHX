
import os
import sys

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx

class TestGHXArray(unittest.TestCase):

    def test_initGHXArray(self):

        json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.json')
        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', '1x2_Std_GHX.csv')

        ghx.GHXArray(json_file_path, csv_file_path)
        self.assertEqual(0.0, 0.0)

# allow execution directly as python tests/test_ghx.py
if __name__ == '__main__':
	unittest.main()
