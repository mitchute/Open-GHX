
import sys
import ghx.ghx as ghx

# nice usage function
def usage():
    print("""Call this script with two command line arguments:
    $ main.py <path to json> <path to loads>""")

# check the command line arguments
if not len(sys.argv) == 3:
    print("Invalid command line arguments")
    usage()
    sys.exit(1)

# store command line args
path_to_json = sys.argv[1]
path_to_loads = sys.argv[2]

if __name__ == "__main__":
    ghx.GHXArray(path_to_json, path_to_loads).simulate()
