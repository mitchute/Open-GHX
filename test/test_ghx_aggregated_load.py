import os
import sys

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx.ghx_aggregated_load


class TestAggregatedLoad(unittest.TestCase):

    def test_init(self):

        """
        Tests AggregatedLoad Class
        """

        # init
        curr_tst = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, 10)

        # check average load
        self.assertEqual(curr_tst.q, 5.5)

        # check time
        self.assertEqual(curr_tst.time(), 0)
