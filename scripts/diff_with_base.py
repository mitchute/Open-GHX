from sklearn.metrics import mean_squared_error
import numpy as np
import sys
import os
from math import sqrt


def calc_rms_err(y_actual, y_predicted):
    y_actual, y_predicted = np.array(y_actual), np.array(y_predicted)
    return sqrt(mean_squared_error(y_actual, y_predicted))


def calc_map_err(y_actual, y_predicted):
    y_actual, y_predicted = np.array(y_actual), np.array(y_predicted)
    return np.mean(np.abs((y_actual - y_predicted) / y_actual)) * 100


def calc_max_abs_err(y_actual, y_predicted):
    y_actual, y_predicted = np.array(y_actual), np.array(y_predicted)
    return np.max(np.abs(y_actual - y_predicted))


def diff_csv_files(base_csv, test_csv):

    base_data = np.genfromtxt(base_csv, delimiter=',', skip_header=1)
    test_data = np.genfromtxt(test_csv, delimiter=',', skip_header=1)

    if base_data.shape != test_data.shape:
        print("'base' and 'test' do not have the same shape")
        sys.exit(1)

    if np.any(base_data[:,0]) != np.any(test_data[:,0]):
        print("time step mis-match")
        sys.exit(1)

    rms_err = []  # root-mean squared error
    #map_err = []  # mean absolute percent error
    max_abs_err = []  # absolute max error

    for i in range(1, base_data.shape[1]):
        rms_err.append(calc_rms_err(base_data[:, i], test_data[:, i]))
        #map_err.append(calc_map_err(base_data[:, i], test_data[:, i]))
        max_abs_err.append(calc_max_abs_err(base_data[:, i], test_data[:, i]))

    return rms_err, max_abs_err


def get_time(base_txt, test_txt):

    base_file = open(base_txt, 'r')
    test_file = open(test_txt, 'r')

    base_tokens = []
    test_tokens = []

    for line in base_file:
        if "Simulation time:" in line:
            base_tokens = line.split(' ')

    for line in test_file:
        if "Simulation time:" in line:
            test_tokens = line.split(' ')

    t = float(test_tokens[2])
    b = float(base_tokens[2])

    return t, 1.0 - ((b - t) / b)


def diff_dir(path_to_base, path_to_root):

    base_csv = os.path.join(path_to_base, "GHX.csv")
    base_txt = os.path.join(path_to_base, "ghx.log")

    if not os.path.exists(base_csv):
        print("base csv file not found")
        sys.exit(1)

    if not os.path.exists(base_txt):
        print("base txt file not found")
        sys.exit(1)

    out_file = open(os.path.join(path_to_root, "summary.csv"), 'w')
    out_file.write("Dir,"
                   "Depth,"
                   "Min Hist,"
                   "Agg Start,"
                   "RMS Error BH Temp,"
                   "Max Abs Err BH Temp,"
                   "RMS Error MFT,"
                   "Max Abs Err MFT,"
                   "Abs Sim Time,"
                   "Percent of Base Sim Time\n")

    for root, dirs, files in os.walk(path_to_root):
        for dir in dirs:

            test_dir = os.path.join(root, dir)

            test_csv = os.path.join(test_dir, "GHX.csv")
            test_txt = os.path.join(test_dir, "ghx.log")

            if not os.path.exists(test_csv):
                pass
            else:
                print(os.path.join(root, dir))
                rms_err, max_abs_err = diff_csv_files(base_csv, test_csv)
                abs_sim_time, percent_base_sim_time = get_time(base_txt, test_txt)

                try:
                    num = test_dir.split('\\')[-2]

                    if num == "one":
                        num = "1"
                    elif num == "two":
                        num = "2"
                    elif num == "three":
                        num = "3"
                    elif num == "four":
                        num = "4"
                    elif num == "five":
                        num = "5"
                    elif num == "six":
                        num = "6"
                    elif num == "seven":
                        num = "7"
                    elif num == "eight":
                        num = "8"
                    elif num == "nine":
                        num = "9"
                    elif num == "ten":
                        num = "10"
                    elif num == "eleven":
                        num = "11"
                    elif num == "twelve":
                        num = "12"

                    min_hist = test_dir.split('\\')[-1].split('-')[0]
                    agg_start = test_dir.split('\\')[-1].split('-')[-1]
                except:
                    num = "0"
                    min_hist = "0"
                    agg_start = "0"

                out_file.write("%s,%s,%s,%s," % (test_dir, num, min_hist, agg_start))

                for i in range(len(rms_err)):
                    out_file.write("%0.5f,%0.5f," % (rms_err[i], max_abs_err[i]))

                out_file.write("%0.1f,%0.4f\n" % (abs_sim_time, percent_base_sim_time))

    out_file.close()

path_to_base_file = sys.argv[1]
path_to_root = sys.argv[2]

if __name__ == '__main__':
    diff_dir(path_to_base_file, path_to_root)
