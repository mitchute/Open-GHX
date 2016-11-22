import sys
import ghx.ghx as ghx


# nice usage function
def usage():
    print("""Call this script with three command line arguments:
    $ main.py <path to ghx input> <path to loads> <path to output dir>""")

# check the command line arguments
if not len(sys.argv) == 4:
    print("Invalid command line arguments")
    usage()
    sys.exit(1)

# store command line args
path_to_ghx_input = sys.argv[1]
path_to_loads = sys.argv[2]
path_to_output = sys.argv[3]

if __name__ == "__main__":
    ghx.GHXArray(path_to_ghx_input, path_to_loads, path_to_output).simulate()
