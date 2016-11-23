import os


import simplejson as json
import ghx.ghx as ghx

cwd = os.getcwd()

input_path = os.path.join(cwd, "..", "examples", "1x2_Std_GHX.json")
load_path = os.path.join(cwd, "..", "examples", "1x2_Std_GHX_Sin.csv")

with open(input_path) as json_file:
    json_data = json.load(json_file)

min_hourly = [24, 48, 72, 96, 120, 144, 168, 192]

one =    [
            [10],
            [50],
            [100],
            [200],
            [400],
            [600],
            [800],
            [1000]
            ]

two =    [
            [10, 20],
            [20, 40],
            [30, 60],
            [40, 80],
            [50, 100],
            [60, 120],
            [70, 140],
            [80, 160],
            [90, 180],
            [100, 200]
        ]

three =    [
            [10, 20, 40],
            [20, 40, 80],
            [30, 60, 120],
            [40, 80, 160],
            [50, 100, 200],
            [60, 120, 240],
            [70, 140, 280],
            [80, 160, 320],
            [90, 180, 360],
            [100, 200, 400]
        ]

four =    [
            [10, 20, 40, 80],
            [20, 40, 80, 160],
            [30, 60, 120, 240],
            [40, 80, 160, 320],
            [50, 100, 200, 400],
            [60, 120, 240, 480],
            [70, 140, 280, 560],
            [80, 160, 320, 640],
            [90, 180, 360, 720],
            [100, 200, 400, 800]
        ]

five =    [
            [10, 20, 40, 80, 160],
            [20, 40, 80, 160, 320],
            [30, 60, 120, 240, 480],
            [40, 80, 160, 320, 640],
            [50, 100, 200, 400, 800],
            [60, 120, 240, 480, 960],
            [70, 140, 280, 560, 1120],
            [80, 160, 320, 640, 1280],
            [90, 180, 360, 720, 1440],
            [100, 200, 400, 800, 1600]
        ]


def run(name, hist, d):
    ghx.PrintClass.log_messages = ''
    print("Set: %d-%d" % (hist, d[0]))

    dir_name = "%d-%d" % (hist, d[0])

    output_path = os.path.join(cwd, "..", "run", name, dir_name)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    json_data['Simulation Configuration']['Simulation Years'] = 10
    json_data['Simulation Configuration']['Aggregation Type'] = "Euler"
    json_data['Simulation Configuration']['Min Hourly History'] = hist
    json_data['Simulation Configuration']['Intervals'] = d

    this_test = ghx.GHXArrayEulerAggBlocks(json_data, load_path, output_path, True)

    this_test.simulate()

for hist in min_hourly:
    for d in five:
        run("five", hist, d)
