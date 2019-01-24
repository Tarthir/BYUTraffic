import gzip
import sys

# Argument 1: Path to the DITL file to read
# Argument 2: Path to Byu authoritative client ips
# Argument 3: Directory to write results
if len(sys.argv) != 4:
    print("Path to the DITL file required")
    sys.exit()

# python ditl_byu_comparison.py ~/Documents/RA-IMAAL/imaal-data/ditl-2018/resolver-count-all.txt.gz ~/Documents/RA-IMAAL/imaal-data/dns-queries/byu/testing-results2 ~/Documents/RA-IMAAL/imaal-data/dns-queries/byu/testing-results/

# Store all ditl ips
# Compare with BYU ips

# Save the similar ones
# Save the ditl unique

# Store all the byu ips
# Compare with ditl

# Save all the similar ones, double check with above
# Save the byu unique

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
        # ip = line.decode("utf-8")
        print(line)
        ip = line.rstrip('\n')         # Get rid of the newline that comes with reading the file
        # byu_list.append(ip)
        byu_set.add(ip)
        test2.write(str(ip))

# Because I need to do something different for lists
# def interSection(arr1,arr2): 
  
#      # filter(lambda x: x in arr1, arr2)  --> 
#      # filter element x from list arr2 where x 
#      # also lies in arr1 
#      result = list(filter(lambda x: x in arr1, arr2))  
#      print ("Intersection : ",result) 
# intersection_list = ditl_list.intersection(byu_list)
# ditl_unique = ditl_list - byu_list
# byu_unique = byu_list - ditl_list


# The ways of the sets
intersection_set = ditl_set.intersection(byu_set)
ditl_unique_set = ditl_set.difference(byu_set)
byu_unique_set = byu_set.difference(ditl_set)

test3 = open(str(sys.argv[3]) + "intersection", "w")
test4 = open(str(sys.argv[3]) + "ditl_unique", "w")
test5 = open(str(sys.argv[3]) + "byu_unique", "w")

print("Intersection length: " + str(len(intersection_set)))
print("DITL UNIQUE length: " + str(len(ditl_unique_set)))
print("BYU UNIQUE length: " + str(len(byu_unique_set)))

for a in intersection_set:
    test3.write(a)
    test3.write("\n")

for b in ditl_unique_set:
    test4.write(b)
    test4.write("\n") 

for c in byu_unique_set:
    test5.write(c)
    test5.write("\n")