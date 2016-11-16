import sys
import ghx.ghx as ghx


# nice usage function
def usage():
    print("""Call this script with two command line arguments:
    $ main.py <path to ghx input> <path to loads>""")

# check the command line arguments
if not len(sys.argv) == 3:
    print("Invalid command line arguments")
    usage()
    sys.exit(1)

# store command line args
path_to_ghx_input = sys.argv[1]
path_to_loads = sys.argv[2]

if __name__ == "__main__":
    ghx.GHXArray(path_to_ghx_input, path_to_loads).simulate()
