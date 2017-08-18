# from __future__ import division
# import os
# import sys
# import numpy as np

# add the source directory to the path so the unit test framework can find it
# sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

# import unittest
# import ghx


# class TestGHXArrayShiftingAggBlocks(unittest.TestCase):

# def test_shift_loads(self):

# """
# Test how loads are shifted
# """

# ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.json')
# config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
# 'test_Shifting_config.json')
# csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')

# init
# curr_tst = ghx.GHXArrayShiftingAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

# l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# i = 1
# curr_tst.shift_loads(l[i])
# self.assertEqual(len(curr_tst.agg_load_objects), 1)
# self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))

# for i in range(2, 4):
# curr_tst.shift_loads(l[i])
# self.assertEqual(len(curr_tst.agg_load_objects), 2)
# self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))
# if i == 2:
# self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 2]]))
# elif i ==3:
# self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 3], l[i - 2]]))

# for i in range(4, 8):
# curr_tst.shift_loads(i)
# self.assertEqual(len(curr_tst.agg_load_objects), 3)
# self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))
# self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 3], l[i - 2]]))
# if i == 4:
# self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 4]]))
# elif i == 5:
# self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 5], l[i - 4]]))
# elif i == 6:
# self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 6], l[i - 5], l[i - 4]]))
# elif i == 7:
# self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 7], l[i - 6], l[i - 5], l[i - 4]]))

# for i in range(8, 16):
# curr_tst.shift_loads(i)
# self.assertEqual(len(curr_tst.agg_load_objects), 4)
# self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))
# self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 3], l[i - 2]]))
# self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 7], l[i - 6], l[i - 5], l[i - 4]]))
# if i == 8:
# self.assertEqual(curr_tst.agg_load_objects[3].q, np.mean([l[i - 8]]))
# elif i == 9:
# self.assertEqual(curr_tst.agg_load_objects[3].q, np.mean([l[i - 9], l[i - 8]]))
# elif i == 10:
# self.assertEqual(curr_tst.agg_load_objects[3].q, np.mean([l[i - 10], l[i - 9], l[i - 8]]))
# elif i == 11:
# self.assertEqual(curr_tst.agg_load_objects[3].q, np.mean([l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
# elif i == 12:
# self.assertEqual(curr_tst.agg_load_objects[3].q,
# np.mean([l[i - 12], l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
# elif i == 13:
# self.assertEqual(curr_tst.agg_load_objects[3].q,
# np.mean([l[i - 13], l[i - 12], l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
# elif i == 14:
# self.assertEqual(curr_tst.agg_load_objects[3].q,
# np.mean([l[i - 14], l[i - 13], l[i - 12], l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
# elif i == 15:
# self.assertEqual(curr_tst.agg_load_objects[3].q,
# np.mean([l[i - 15], l[i - 14], l[i - 13], l[i - 12],
# l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))

# for i in range(16, 24):
# curr_tst.shift_loads(i)
# self.assertEqual(len(curr_tst.agg_load_objects), 5)
# self.assertEqual(curr_tst.agg_load_objects[0].q, np.mean([l[i - 1], l[i]]))
# self.assertEqual(curr_tst.agg_load_objects[1].q, np.mean([l[i - 3], l[i - 2]]))
# self.assertEqual(curr_tst.agg_load_objects[2].q, np.mean([l[i - 7], l[i - 6], l[i - 5], l[i - 4]]))
# self.assertEqual(curr_tst.agg_load_objects[3].q,
# np.mean([l[i - 15], l[i - 14], l[i - 13], l[i - 12],
# l[i - 11], l[i - 10], l[i - 9], l[i - 8]]))
# if i == 16:
# self.assertEqual(curr_tst.agg_load_objects[4].q, np.mean([l[i - 16]]))
# elif i == 17:
# self.assertEqual(curr_tst.agg_load_objects[4].q, np.mean([l[i - 17], l[i - 16]]))
# elif i == 18:
# self.assertEqual(curr_tst.agg_load_objects[4].q, np.mean([l[i - 18], l[i - 17], l[i - 16]]))
# elif i == 19:
# self.assertEqual(curr_tst.agg_load_objects[4].q,
# np.mean([l[i - 19], l[i - 18], l[i - 17], l[i - 16]]))
# elif i == 20:
# self.assertEqual(curr_tst.agg_load_objects[4].q,
# np.mean([l[i - 20], l[i - 19], l[i - 18], l[i - 17], l[i - 16]]))
# elif i == 21:
# self.assertEqual(curr_tst.agg_load_objects[4].q,
# np.mean([l[i - 21], l[i - 20], l[i - 19], l[i - 18], l[i - 17], l[i - 16]]))
# elif i == 22:
# self.assertEqual(curr_tst.agg_load_objects[4].q,
# np.mean([l[i - 22], l[i - 21], l[i - 20], l[i - 19],
# l[i - 18], l[i - 17], l[i - 16]]))
# elif i == 23:
# self.assertEqual(curr_tst.agg_load_objects[4].q,
# np.mean([l[i - 23], l[i - 22], l[i - 21], l[i - 20],
# l[i - 19], l[i - 18], l[i - 17], l[i - 16]]))

# def test_shift_loads_for_q_est(self):

# """
# q_estimate method
# """

# ghx_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
# 'testing.json')
# config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
# 'test_Shifting_config.json')
# csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples',
# 'testing.csv')

# init
# curr_tst = ghx.GHXArrayShiftingAggBlocks(ghx_file_path, config_file_path, csv_file_path, False)

# l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# for i in range(1, 10):
# curr_tst.shift_loads(l[i])
# if i == 2:
# self.assertEqual(curr_tst.agg_load_objects[1].q_est, 0)
# elif i == 3:
# self.assertEqual(curr_tst.agg_load_objects[1].q_est, 0.5)
# elif i == 4:
# self.assertEqual(curr_tst.agg_load_objects[1].q_est, 1.25)
# self.assertEqual(curr_tst.agg_load_objects[2].q_est, 0.5)
# elif i == 5:
# self.assertEqual(curr_tst.agg_load_objects[1].q_est, 2.125)
# self.assertEqual(curr_tst.agg_load_objects[2].q_est, 0.875)
