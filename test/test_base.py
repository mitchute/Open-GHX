import os
import unittest

from ghx.base import BaseGHXClass


class TestBaseGHXClass(unittest.TestCase):
    def test_init(self):

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
        curr_tst = BaseGHXClass(dict_bh, csv_file_path, output_path, False)

        self.assertEqual(curr_tst.name, dict_bh['Name'])
        self.assertEqual(curr_tst.sim_years, dict_bh['Simulation Configuration']['Simulation Years'])
        self.assertEqual(curr_tst.aggregation_type, dict_bh['Simulation Configuration']['Aggregation Type'])
        self.assertEqual(curr_tst.min_hourly_history, dict_bh['Simulation Configuration']['Min Hourly History'])
        self.assertEqual(curr_tst.agg_load_intervals, dict_bh['Simulation Configuration']['Intervals'])

        i = 0

        for this_ghx in curr_tst.ghx_list:
            self.assertEqual(this_ghx.name, dict_bh['GHXs'][i]['Name'])
            self.assertEqual(this_ghx.location, dict_bh['GHXs'][i]['Location'])
            self.assertEqual(this_ghx.depth, dict_bh['GHXs'][i]['Depth'])
            self.assertEqual(this_ghx.radius, dict_bh['GHXs'][i]['Radius'])
            self.assertEqual(this_ghx.shank_space, dict_bh['GHXs'][i]['Shank Spacing'])
            self.assertEqual(this_ghx.pipe.outer_diameter, dict_bh['GHXs'][i]['Pipe']['Outside Diameter'])
            self.assertEqual(this_ghx.pipe.thickness, dict_bh['GHXs'][i]['Pipe']['Wall Thickness'])
            self.assertEqual(this_ghx.pipe.conductivity, dict_bh['GHXs'][i]['Pipe']['Conductivity'])
            self.assertEqual(this_ghx.pipe.density, dict_bh['GHXs'][i]['Pipe']['Density'])
            self.assertEqual(this_ghx.pipe.specific_heat, dict_bh['GHXs'][i]['Pipe']['Specific Heat'])
            self.assertEqual(this_ghx.pipe.fluid.fluid_type, dict_bh['GHXs'][i]['Fluid']['Type'])
            self.assertEqual(this_ghx.pipe.fluid.concentration, dict_bh['GHXs'][i]['Fluid']['Concentration'])
            self.assertEqual(this_ghx.pipe.fluid.flow_rate, dict_bh['GHXs'][i]['Fluid']['Flow Rate'])
            self.assertEqual(this_ghx.soil.conductivity, dict_bh['GHXs'][i]['Soil']['Conductivity'])
            self.assertEqual(this_ghx.soil.density, dict_bh['GHXs'][i]['Soil']['Density'])
            self.assertEqual(this_ghx.soil.specific_heat, dict_bh['GHXs'][i]['Soil']['Specific Heat'])
            self.assertEqual(this_ghx.soil.undisturbed_temp, dict_bh['GHXs'][i]['Soil']['Temperature'])
            self.assertEqual(this_ghx.grout.conductivity, dict_bh['GHXs'][i]['Grout']['Conductivity'])
            self.assertEqual(this_ghx.grout.density, dict_bh['GHXs'][i]['Grout']['Density'])
            self.assertEqual(this_ghx.grout.specific_heat, dict_bh['GHXs'][i]['Grout']['Specific Heat'])
            i += 1

        for i in range(len(curr_tst.g_func_val)):
            self.assertEqual(curr_tst.g_func_lntts[i], dict_bh['G-func Pairs'][i][0])
            self.assertEqual(curr_tst.g_func_val[i], dict_bh['G-func Pairs'][i][1])

    def test_merge_dicts(self):

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
        }

        csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'testing.csv')
        output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'run', 'testing')
        curr_tst = BaseGHXClass(dict_bh, csv_file_path, output_path, False)

        x = {
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
        }
        y = {
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

        dict_list = [x, y]

        merged_dict = curr_tst.merge_dicts(dict_list)

        for key in merged_dict.keys():
            sub_keys_exist = False
            try:
                if len(merged_dict[key].keys()) > 0:
                    sub_keys_exist = True
            except:
                pass

            if sub_keys_exist:
                for sub_key in merged_dict[key].keys():
                    self.assertEqual(merged_dict[key][sub_key], dict_list[-1][key][sub_key])
            else:
                self.assertEqual(merged_dict[key], dict_list[0][key])

    def test_interp_g_funcs(self):

        """
        Tests g-function interpolation
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
        curr_tst = BaseGHXClass(dict_bh, csv_file_path, output_path, False)

        tolerance = 0.1

        # extrapolate down
        self.assertAlmostEqual(curr_tst.g_func(-17.0), -4.38, delta=tolerance)

        # in-range
        self.assertAlmostEqual(curr_tst.g_func(0.0), 7.70, delta=tolerance)

        # extrapolate up
        self.assertAlmostEqual(curr_tst.g_func(5.0), 8.29, delta=tolerance)

    def test_calc_ts(self):

        """
        Tests calc_ts which sets timescale
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
        curr_tst = BaseGHXClass(dict_bh, csv_file_path, output_path, False)

        tolerance = 0.1

        self.assertAlmostEqual(curr_tst.ts, 645858729.2, delta=tolerance)
