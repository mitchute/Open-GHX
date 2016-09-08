
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

# format the string once
def formatted_str(tabs, key, val):

    if tabs == 1:
        tab_val = tab1
    elif tabs == 2:
        tab_val = tab2
    elif tabs == 3:
        tab_val = tab3

    return tab_val + "\"" + key + "\":" + val + ",\n"

# store the command line arguments
path_to_idf = sys.argv[1]
path_to_json = sys.argv[2]

# open files
in_file = open(path_to_idf, 'r')
out_file = open(path_to_json, 'w')

# write prelim json brackets
out_file.write("{\"GHXs\":\n")
out_file.write(tab1 + "[\n")
out_file.write(tab2 + "{\n")

# num g-func pairs
num_pairs = 0
pair_counter = 0

# write json object
for line in in_file:

    # strip white space
    line = line.strip()

    # eliminate "+" for FORTRAN exponents
    line = line.replace("+", "")

    # split line into tokens
    if "," in line:
        tokens = line.split(",")
    elif ";" in line:
        tokens = line.split(";")

    if "!- Name" in line:
        out_file.write(formatted_str(3, "Name", "\"" + tokens[0] + "\""))
        out_file.write(formatted_str(3, "Location", "[0,0]"))

    if "Design Flow Rate" in line:
        out_file.write(formatted_str(3, "Flow Rate", tokens[0]))

    if "Number of Bore Holes" in line:
        out_file.write(formatted_str(3, "Num BH", tokens[0]))

    if "Bore Hole Length" in line:
        out_file.write(formatted_str(3, "BH Length", tokens[0]))

    if "Bore Hole Radius" in line:
        out_file.write(formatted_str(3, "BH Radius", tokens[0]))

    if "Ground Thermal Conductivity" in line:
        out_file.write(formatted_str(3, "Grnd Cond", tokens[0]))

    if "Ground Thermal Heat Capacity" in line:
        out_file.write(formatted_str(3, "Grnd Cp", tokens[0]))

    if "Ground Temperature" in line:
        out_file.write(formatted_str(3, "Grnd Temp", tokens[0]))

    if "Grout Thermal Conductivity" in line:
        out_file.write(formatted_str(3, "Grout Cond", tokens[0]))

    if "Pipe Thermal Conductivity" in line:
        out_file.write(formatted_str(3, "Pipe Cond", tokens[0]))

    if "Pipe Out Diameter" in line:
        out_file.write(formatted_str(3, "Pipe Dia", tokens[0]))

    if "U-Tube Distance" in line:
        out_file.write(formatted_str(3, "Shank Space", tokens[0]))

    if "Pipe Thickness" in line:
        out_file.write(formatted_str(3, "Pipe Thickness", tokens[0]))

    if "G-Function Reference Ratio" in line:
        out_file.write(formatted_str(3, "Ref Ratio", tokens[0]))

    if "Number of Data Pairs of the G Function" in line:
        num_pairs = int(tokens[0])
        out_file.write(tab3 + "\"G-func Pairs\": [\n")

    if "G-Function Ln(T/Ts) Value" in line:
        pair_counter += 1
        out_file.write(tab4 + "[" + tokens[0] + ",")

    if "G-Function G Value" in line:
        if pair_counter == num_pairs:
            out_file.write(tokens[0] + "]\n")
        else:
            out_file.write(tokens[0] + "],\n")

# write closing json brackets
out_file.write(tab3 + "]\n")
out_file.write(tab2 + "}\n")
out_file.write(tab1 + "]\n")
out_file.write("}\n")

# don't forget to close the file
out_file.close()


