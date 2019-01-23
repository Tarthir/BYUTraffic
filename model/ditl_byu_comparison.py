import gzip
import sys

# Argument 1: Path to the DITL file to read
# Argument 2: Path to Byu authoritative client ips
# Argument 3: Directory to write results
if len(sys.argv) != 4:
    print("Path to the DITL file required")
    sys.exit()


# Store all ditl ips
# Compare with BYU ips

# Save the similar ones
# Save the ditl unique

# Store all the byu ips
# Compare with ditl

# Save all the similar ones, double check with above
# Save the byu unique

ditl_file = gzip.open(sys.argv[1], "r")

count = 0 #Debugging purpose
for line in ditl_file:
    #print(line)                        #Debug Output
    line_array = line.split()           #Breaks up the line by whitespace into an array
    ip = line_array[0]                  #Grabs the first word of the line/array (Which in this case is my IP address)
    ip = ip.decode("utf-8")             #At this point the ip is in byte form, so I decode in into utf-8 (string) Otherwise my output has b' signifying byte
    ip_list.append(ip)                  #For now. Storing the IP into a list
    out_file.write(ip)                  #Writes the lines to an output text file, it has to be in bytes yet
    out_file.write('\n')                #Otherwise it is all one big mega IP address
    if ":" in ip:
        out_file_ipv6.write(ip)         #If it has : then it is ipv61
        out_file_ipv6.write('\n')   
    else:
        # print(count)
        count += 1
        out_file_ipv4.write(ip)
        out_file_ipv4.write('\n')