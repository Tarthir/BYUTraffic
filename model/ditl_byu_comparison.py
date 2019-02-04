import gzip
import sys
import LogList

# Argument 1: Path to the DITL file to read
# Argument 2: Path to Byu authoritative client ips file
# Argument 3: Directory to store results
if len(sys.argv) != 4:
    print("DITL IP File Path all.gz\n BYU Traffic Client IP Path .asn\n Directory to store results")
    sys.exit()


ditl_file = gzip.open(sys.argv[1], "r")
byu_file = open(sys.argv[2], "r")

ditl_list = []
byu_list = []

ditl_set = set()
byu_set = set()

test1= open(str(sys.argv[3]) + "ditl_sample", "w")
test2= open(str(sys.argv[3]) + "byu_sample", "w")

count = 0 #Debugging purpose
for line in ditl_file:
    #print(line)                        #Debug Output
    line_array = line.split()           #Breaks up the line by whitespace into an array
    ip = line_array[0]                  #Grabs the first word of the line/array (Which in this case is my IP address)
    ip = ip.decode("utf-8")             #At this point the ip is in byte form, so I decode in into utf-8 (string) Otherwise my output has b' signifying byte
    # ditl_list.append(ip)              # Using sets instead of lists
    ditl_set.add(ip)
    test1.write(str(ip) + "\n")

for line in byu_file:
    if line != "begin\n" and line != "end\n": # if reading from the ip's created from parser.py we don't want the begin and end needed for asn
        print(line)
        ip = line.rstrip('\n')         # Get rid of the newline that comes with reading the file
        # byu_list.append(ip)
        byu_set.add(ip)
        test2.write(str(ip))

# The ways of the sets
intersection_set = ditl_set.intersection(byu_set)
ditl_unique_set = ditl_set.difference(byu_set)
byu_unique_set = byu_set.difference(ditl_set)

# Create Log object. Load all data. Add new data. Save data
mighty_log = LogList.LogList()
mighty_log.load_all(sys.argv[3])
mighty_log.ditl_byu_intersection = intersection_set
mighty_log.ditl_unique = ditl_unique_set
mighty_log.byu_unique = byu_unique_set
mighty_log.save_data(sys.argv[3])

# Test Purposes
# test3 = open(str(sys.argv[3]) + "intersection", "w")
# test4 = open(str(sys.argv[3]) + "ditl_unique", "w")
# test5 = open(str(sys.argv[3]) + "byu_unique", "w")

# print("Intersection length: " + str(len(intersection_set)))
# print("DITL UNIQUE length: " + str(len(ditl_unique_set)))
# print("BYU UNIQUE length: " + str(len(byu_unique_set)))

# for a in intersection_set:

#     test3.write(a)
#     test3.write("\n")

# for b in ditl_unique_set:
#     test4.write(b)
#     test4.write("\n") 

# for c in byu_unique_set:
#     test5.write(c)
#     test5.write("\n")
