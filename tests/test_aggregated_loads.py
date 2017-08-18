import unittest

from ghx.aggregated_loads import AggregatedLoad


class TestAggregatedLoad(unittest.TestCase):
    def test_init(self):
        """
        Tests AggregatedLoad Class
        """

        # init
        curr_tst = AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, 10)

        # check average load
        self.assertEqual(curr_tst.q, 5.5)

        # check time
        self.assertEqual(curr_tst.time(), 0)
