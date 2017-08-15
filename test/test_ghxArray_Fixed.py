import os
import sys
from collections import deque

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
import ghx


class TestGHXArrayFixedAggBlocks(unittest.TestCase):

    def test_merge_agg_load_objs(self):

        """
        Tests merge_agg_load_objs, which merges AggregatedLoad objects into a single object
        """

        dict_bh = {
            "Name": "Vertical GHE 1x2 Std",
            "Simulation Configuration":
                {
                "Simulation Years": 2,
                "Aggregation Type": "Fixed",
                "Min Hourly History": 192,
                "Intervals": [5, 10, 20, 40]
                },
            "GHXs":
                [
                    {
                        "Name": "BH 1",
                        "Location": [0, 0],
                        "Depth": 76.2,
                        "Radius": 0.05715,
                        "Shank Spacing": 0.0521,
                        "Pipe":
                            {
                            "Outside Diameter": 0.0267,
                            "Wall Thickness": 0.00243,
                            "Conductivity": 0.389,
                            "Density": 800,
                            "Specific Heat": 1000
                            },
                        "Fluid":
                            {
                            "Type": "Water",
                            "Concentration": 100,
                            "Flow Rate": 0.000303
                            },
                        "Soil":
                            {
                            "Conductivity": 2.493,
                            "Density": 1500,
                            "Specific Heat": 1663.8,
                            "Temperature": 13.0
                            },
                        "Grout":
                            {
                            "Conductivity": 0.744,
                            "Density": 1000,
                            "Specific Heat": 1000
                            }
                    },
                    {
                        "Name": "BH 2",
                        "Location": [0, 0],
                        "Depth": 76.2,
                        "Radius": 0.05715,
                        "Shank Spacing": 0.0521,
                        "Pipe":
                            {
                            "Outside Diameter": 0.0267,
                            "Wall Thickness": 0.00243,
                            "Conductivity": 0.389,
                            "Density": 800,
                            "Specific Heat": 1000
                            },
                        "Fluid":
                            {
                            "Type": "Water",
                            "Concentration": 100,
                            "Flow Rate": 0.000303
                            },
                        "Soil":
                            {
                            "Conductivity": 2.493,
                            "Density": 1500,
                            "Specific Heat": 1663.8,
                            "Temperature": 13.0
                            },
                        "Grout":
                            {
                            "Conductivity": 0.744,
                            "Density": 1000,
                            "Specific Heat": 1000
                            }
                    }
                ]
            ,
            "G-func Pairs": [
                [-14.583933, -3.258945],
                [-14.459771, -3.201266],
                [-14.335609, -3.137149],
                [-14.211447, -3.066044],
                [-14.087285, -2.987396],
                [-13.963123, -2.900662],
                [-13.838961, -2.805328],
                [-13.714800, -2.700928],
                [-13.590638, -2.587074],
                [-13.466476, -2.463485],
                [-13.342314, -2.330018],
                [-13.218152, -2.186711],
                [-13.093990, -2.033816],
                [-12.969828, -1.871834],
                [-12.845666, -1.701555],
                [-12.721504, -1.524070],
                [-12.597342, -1.340786],
                [-12.473181, -1.153409],
                [-12.349019, -0.963910],
                [-12.224857, -0.774455],
                [-12.100695, -0.587314],
                [-11.976533, -0.404737],
                [-11.852371, -0.228815],
                [-11.728209, -0.061337],
                [-11.604047, 0.096338],
                [-11.479885, 0.243375],
                [-11.355724, 0.379509],
                [-11.231562, 0.505025],
                [-11.107400, 0.620671],
                [-10.983238, 0.727536],
                [-10.859076, 0.826882],
                [-10.734914, 0.920004],
                [-10.610752, 1.008099],
                [-10.486590, 1.092190],
                [-10.362428, 1.173104],
                [-10.238267, 1.251474],
                [-10.114105, 1.327774],
                [-9.989943, 1.402357],
                [-9.865781, 1.475491],
                [-9.741619, 1.547380],
                [-9.617457, 1.618189],
                [-9.493295, 1.688052],
                [-9.369133, 1.757083],
                [-9.244971, 1.825377],
                [-9.120809, 1.893016],
                [-8.996648, 1.960074],
                [-8.872486, 2.026612],
                [-8.748324, 2.092687],
                [-8.624162, 2.158347],
                [-8.500000, 2.273322],
                [-7.800000, 2.617322],
                [-7.200000, 2.913059],
                [-6.500000, 3.261270],
                [-5.900000, 3.575221],
                [-5.200000, 3.982441],
                [-4.500000, 4.449827],
                [-3.963000, 4.811057],
                [-3.270000, 5.382808],
                [-2.864000, 5.717286],
                [-2.577000, 5.953762],
                [-2.171000, 6.281028],
                [-1.884000, 6.507398],
                [-1.191000, 7.002874],
                [-0.497000, 7.446504],
                [-0.274000, 7.569030],
                [-0.051000, 7.680608],
                [0.196000, 7.788398],
                [0.419000, 7.873398],
                [0.642000, 7.945924],
                [0.873000, 8.009924],
                [1.112000, 8.064187],
                [1.335000, 8.105450],
                [1.679000, 8.153187],
                [2.028000, 8.185450],
                [2.275000, 8.200450],
                [3.003000, 8.226450]
            ]
        }

        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')
        output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'run', 'testing')
        # init
        curr_tst = ghx.GHXArrayFixedAggBlocks(dict_bh, csv_file_path, output_path, False)

        # make a few dummy AggregatedLoad classes
        obj_1 = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, 10)
        obj_2 = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10, 10)
        obj_3 = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 20, 10)
        obj_4 = ghx.AggregatedLoad([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 30, 10)

        obj_list = [obj_1, obj_2, obj_3, obj_4]

        ret_obj = curr_tst.merge_agg_load_objs(obj_list)

        # check average load
        self.assertEqual(ret_obj.q, 5.5)

        # check time
        self.assertEqual(ret_obj.time(), 0)

    def test_aggregate_load(self):

        """
        Tests aggregate_load which aggregates and merges aggregated objects
        """

        dict_bh = {
            "Name": "Vertical GHE 1x2 Std",
            "Simulation Configuration":
                {
                "Simulation Years": 2,
                "Aggregation Type": "Fixed",
                "Min Hourly History": 192,
                "Intervals": [5, 10, 20, 40]
                },
            "GHXs":
                [
                    {
                        "Name": "BH 1",
                        "Location": [0, 0],
                        "Depth": 76.2,
                        "Radius": 0.05715,
                        "Shank Spacing": 0.0521,
                        "Pipe":
                            {
                            "Outside Diameter": 0.0267,
                            "Wall Thickness": 0.00243,
                            "Conductivity": 0.389,
                            "Density": 800,
                            "Specific Heat": 1000
                            },
                        "Fluid":
                            {
                            "Type": "Water",
                            "Concentration": 100,
                            "Flow Rate": 0.000303
                            },
                        "Soil":
                            {
                            "Conductivity": 2.493,
                            "Density": 1500,
                            "Specific Heat": 1663.8,
                            "Temperature": 13.0
                            },
                        "Grout":
                            {
                            "Conductivity": 0.744,
                            "Density": 1000,
                            "Specific Heat": 1000
                            }
                    },
                    {
                        "Name": "BH 2",
                        "Location": [0, 0],
                        "Depth": 76.2,
                        "Radius": 0.05715,
                        "Shank Spacing": 0.0521,
                        "Pipe":
                            {
                            "Outside Diameter": 0.0267,
                            "Wall Thickness": 0.00243,
                            "Conductivity": 0.389,
                            "Density": 800,
                            "Specific Heat": 1000
                            },
                        "Fluid":
                            {
                            "Type": "Water",
                            "Concentration": 100,
                            "Flow Rate": 0.000303
                            },
                        "Soil":
                            {
                            "Conductivity": 2.493,
                            "Density": 1500,
                            "Specific Heat": 1663.8,
                            "Temperature": 13.0
                            },
                        "Grout":
                            {
                            "Conductivity": 0.744,
                            "Density": 1000,
                            "Specific Heat": 1000
                            }
                    }
                ]
            ,
            "G-func Pairs": [
                [-14.583933, -3.258945],
                [-14.459771, -3.201266],
                [-14.335609, -3.137149],
                [-14.211447, -3.066044],
                [-14.087285, -2.987396],
                [-13.963123, -2.900662],
                [-13.838961, -2.805328],
                [-13.714800, -2.700928],
                [-13.590638, -2.587074],
                [-13.466476, -2.463485],
                [-13.342314, -2.330018],
                [-13.218152, -2.186711],
                [-13.093990, -2.033816],
                [-12.969828, -1.871834],
                [-12.845666, -1.701555],
                [-12.721504, -1.524070],
                [-12.597342, -1.340786],
                [-12.473181, -1.153409],
                [-12.349019, -0.963910],
                [-12.224857, -0.774455],
                [-12.100695, -0.587314],
                [-11.976533, -0.404737],
                [-11.852371, -0.228815],
                [-11.728209, -0.061337],
                [-11.604047, 0.096338],
                [-11.479885, 0.243375],
                [-11.355724, 0.379509],
                [-11.231562, 0.505025],
                [-11.107400, 0.620671],
                [-10.983238, 0.727536],
                [-10.859076, 0.826882],
                [-10.734914, 0.920004],
                [-10.610752, 1.008099],
                [-10.486590, 1.092190],
                [-10.362428, 1.173104],
                [-10.238267, 1.251474],
                [-10.114105, 1.327774],
                [-9.989943, 1.402357],
                [-9.865781, 1.475491],
                [-9.741619, 1.547380],
                [-9.617457, 1.618189],
                [-9.493295, 1.688052],
                [-9.369133, 1.757083],
                [-9.244971, 1.825377],
                [-9.120809, 1.893016],
                [-8.996648, 1.960074],
                [-8.872486, 2.026612],
                [-8.748324, 2.092687],
                [-8.624162, 2.158347],
                [-8.500000, 2.273322],
                [-7.800000, 2.617322],
                [-7.200000, 2.913059],
                [-6.500000, 3.261270],
                [-5.900000, 3.575221],
                [-5.200000, 3.982441],
                [-4.500000, 4.449827],
                [-3.963000, 4.811057],
                [-3.270000, 5.382808],
                [-2.864000, 5.717286],
                [-2.577000, 5.953762],
                [-2.171000, 6.281028],
                [-1.884000, 6.507398],
                [-1.191000, 7.002874],
                [-0.497000, 7.446504],
                [-0.274000, 7.569030],
                [-0.051000, 7.680608],
                [0.196000, 7.788398],
                [0.419000, 7.873398],
                [0.642000, 7.945924],
                [0.873000, 8.009924],
                [1.112000, 8.064187],
                [1.335000, 8.105450],
                [1.679000, 8.153187],
                [2.028000, 8.185450],
                [2.275000, 8.200450],
                [3.003000, 8.226450]
            ]
        }

        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')
        output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'run', 'testing')
        # init
        curr_tst = ghx.GHXArrayFixedAggBlocks(dict_bh, csv_file_path, output_path, False)

        # should initialize empty first object for comparative purposes
        # [0]
        self.assertEqual(len(curr_tst.agg_load_objects), 1)

        # add object from hours 1-5
        # [0, 5]
        curr_tst.hourly_loads = deque([1, 1, 1, 1, 1])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 2)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1)

        # add object from hours 6-10
        # [0, 5, 5]
        curr_tst.hourly_loads = deque([2, 2, 2, 2, 2])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 3)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 5)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 2)

        # add object from hours 11-15
        # first two 5 hour blocks collapse into one 10 hour block
        # [0,10,5]
        curr_tst.hourly_loads = deque([3, 3, 3, 3, 3])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 3)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 10)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1.5)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 3)

        # add object from hours 16-20
        # [0,10,5,5]
        curr_tst.hourly_loads = deque([4, 4, 4, 4, 4])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 10)
        self.assertEqual(curr_tst.agg_load_objects[3].time(), 15)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1.5)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 3)
        self.assertEqual(curr_tst.agg_load_objects[3].q, 4)

        # add object from hours 21-25
        # second two 5 hour blocks collapse into one 10 hour block
        # [0,10,10,5]
        curr_tst.hourly_loads = deque([5, 5, 5, 5, 5])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 10)
        self.assertEqual(curr_tst.agg_load_objects[3].time(), 20)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 1.5)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 3.5)
        self.assertEqual(curr_tst.agg_load_objects[3].q, 5)

        # add object from hours 26-30
        # first two 10 hour blocks collapse into one 20 hour block
        # [0,20,5,5]
        curr_tst.hourly_loads = deque([6, 6, 6, 6, 6])
        curr_tst.aggregate_load()

        # check number of objects
        self.assertEqual(len(curr_tst.agg_load_objects), 4)

        # check sim hours
        self.assertEqual(curr_tst.agg_load_objects[0].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[1].time(), 0)
        self.assertEqual(curr_tst.agg_load_objects[2].time(), 20)
        self.assertEqual(curr_tst.agg_load_objects[3].time(), 25)

        # check load
        self.assertEqual(curr_tst.agg_load_objects[0].q, 0)
        self.assertEqual(curr_tst.agg_load_objects[1].q, 2.5)
        self.assertEqual(curr_tst.agg_load_objects[2].q, 5.0)
        self.assertEqual(curr_tst.agg_load_objects[3].q, 6.0)
