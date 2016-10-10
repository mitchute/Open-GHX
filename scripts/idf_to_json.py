
import sys

# nice usage function
def usage():
    print("""Call this script with two command line arguments:
    $ idf_to_json.py <path to idf> <path to json output>""")

# check the command line arguments
if not len(sys.argv) == 3:
    print("Invalid command line arguments")
    usage()
    sys.exit(1)

# define "\t" as four spaces
tab1 = "    "
tab2 = "        "
tab3 = "            "
tab4 = "                "

# store the command line arguments
path_to_idf = sys.argv[1]
path_to_json = sys.argv[2]

# num g-func pairs
num_pairs = 0
pair_counter = 0

tokens = []

keys = ['Object type',
        'Name',
        'Inlet Node',
        'Outlet Node',
        'Flow Rate',
        'Number BH',
        'BH Length',
        'BH Radius',
        'Ground Cond',
        'Ground Heat Capacity',
        'Ground Temp',
        'Grout Cond',
        'Pipe Cond',
        'Pipe Dia',
        'Shank Space',
        'Pipe Thickness',
        'Max Simulation Length',
        'Reference Ratio',
        'Num Pairs']

for i in range(100):
    keys.append("LNTTS %d" %(i+1))
    keys.append("G-Val %d" %(i+1))

dict = {}

# format the string once
def formatted_str(tabs, key, val, val_is_str=False):

    if tabs == 1:
        tab_val = tab1
    elif tabs == 2:
        tab_val = tab2
    elif tabs == 3:
        tab_val = tab3
    elif tabs == 4:
        tab_val = tab4

    if val_is_str:
        return tab_val + "\"" + key + "\":\"" + val + "\",\n"
    else:
        return tab_val + "\"" + key + "\":" + str(val) + ",\n"

def read_idf():

    # open idf file
    in_file = open(path_to_idf, 'r')

    for line in in_file:
        line = line.replace(";", ",")
        line = line.split(",")
        for token in line:
            if "!" in token:
                continue
            elif "\n" in token:
                continue

            if "+" in token:
                token = token.replace("+", "")
            token = token.lstrip()
            tokens.append(token)

    for i in range(len(tokens)):
        dict[keys[i]] = tokens[i]

    # close file
    in_file.close()

def write_json():

    # open json file
    out_file = open(path_to_json, 'w')

    out_file.write("{\n")

    key = "Name"
    out_file.write(formatted_str(1, key, dict[key], True))

    key = "Number BH"
    out_file.write(formatted_str(1, key, dict[key]))

    key = "Flow Rate"
    out_file.write(formatted_str(1, key , dict[key]))

    key = "Ground Cond"
    out_file.write(formatted_str(1, key , dict[key]))

    key = "Ground Heat Capacity"
    out_file.write(formatted_str(1, key , dict[key]))

    key = "Ground Temp"
    out_file.write(formatted_str(1, key , dict[key]))

    key = "Grout Cond"
    out_file.write(formatted_str(1, key , dict[key]))

    key = "Fluid"
    out_file.write(formatted_str(1, key , "Water", True))

    out_file.write(tab1 + "\"GHXs\":\n")
    out_file.write(tab2 + "[\n")
    out_file.write(tab3 + "{\n")

    for i in range(int(dict['Number BH'])):

        key = "Name"
        out_file.write(formatted_str(4, key , "BH %d" %(i+1), True))

        key = "Location"
        out_file.write(formatted_str(4, key , [0,0]))

        key = "BH Length"
        out_file.write(formatted_str(4, key , dict[key]))

        key = "BH Radius"
        out_file.write(formatted_str(4, key , dict[key]))

        key = "Pipe Cond"
        out_file.write(formatted_str(4, key , dict[key]))

        key = "Pipe Dia"
        out_file.write(formatted_str(4, key , dict[key]))

        key = "Shank Space"
        out_file.write(formatted_str(4, key , dict[key]))

        key = "Pipe Thickness"
        out_file.write(tab4 + "\"" + key + "\":" + dict[key] + "\n")

        if i == (int(dict['Number BH'])-1):
            out_file.write(tab3 + "}\n")
        else:
            out_file.write(tab3 + "},\n")
            out_file.write(tab3 + "{\n")

    out_file.write(tab2 + "],\n")
    out_file.write(tab1 + "\"G-func Pairs\": [\n")

    for i in range(int(dict['Num Pairs'])):
        out_file.write(tab2 + "[")
        L_key = ("LNTTS %d" %(i+1))
        G_key = ("G-Val %d" %(i+1))
        out_file.write("%s," %(dict[L_key]))
        out_file.write("%s" %(dict[G_key]))

        if i == (int(dict['Num Pairs'])-1):
            out_file.write("]\n")
        else:
            out_file.write("],\n")

    out_file.write(tab1 + "]\n")
    out_file.write("}\n")

    # close file
    out_file.close()

read_idf()
write_json()
