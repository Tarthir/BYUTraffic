import sys
import os
import glob
import errno
import gzip
import re
import LogList
import QueryLog


# Takes in the file path directory to read all the zip files
# For Example from base /home/imaal/dns-queries/byu
# Argument 1: Directory path to the zip giles
# Argument 2: The file directory to which we want to save the binary data which happens in loglist save function
# Argument 3: File directory to save client ips, which will be fed to asn reader
if len(sys.argv) != 4:
    print("Error, Give the path of the directory to zip file\n Give the path to where we will save the binary data\n Give the file path to save the client ips ")
    sys.exit()


directory_name = sys.argv[1] # Path of the directory holding the zip files

mighty_log = LogList.LogList() # Our LogList object for which we store our data into

byu_to_asn_file = open(str(sys.argv[3]) + "ip_for_asn_reading", "w") # The file for which we store the client ip for asn. (begin....ip.....end)
byu_to_asn_file.write("begin\n") # Because Tyler's asn file reader is so picky it needs this 'begin'

regex = re.compile(r'(?i)^([0-9-]+)T([0-9:]+)-([0-9:]+) ([a-z0-9]+) ([a-z0-9]+)\[([0-9]+)\]: client ([0-9a-f.:]+)#([0-9]+) \((.*?)\): query: (.*?) ([a-z]+) ([a-z0-9]+) ([-+])([a-z]+)* \((.*?)\)')

output_file = open(str(sys.argv[3]) + "sample_output.txt", "w") # Creates a file with extra info about the files
total_line_count = 0 # For sample output file

for root, dirs, files in os.walk(sys.argv[1], topdown=True): # Start from the top and go down the directory
    for name in files:
        if name.endswith('.gz'):
            output_file.write(str(name) + ' ') # For sample output file
            print(str(name))
            line_count = 0 # For sample output file
            with gzip.open(os.path.join(root,name), 'rt') as f: # rt - read and text, default is rb - read and bytes
                for line in f:
                    line_count += 1 # For sample output file
                    # print(line_count)
                    if re.match(regex, line):
                        regex_groups = re.match(regex, line) # Hold all the matched groups

                        log_object = QueryLog.query_log(regex_groups.group(1), regex_groups.group(2), regex_groups.group(3), regex_groups.group(4), regex_groups.group(5)\
                        , regex_groups.group(6), regex_groups.group(7), regex_groups.group(8), regex_groups.group(10), regex_groups.group(11)\
                        , regex_groups.group(12), regex_groups.group(13), regex_groups.group(14), regex_groups.group(15))

                        mighty_log.add_to_data_structure(log_object, mighty_log.IP_to_Log_byu) # Add to our data structure
                        byu_to_asn_file.write(log_object.client) # Write out to ASN
                        byu_to_asn_file.write("\n") # Write out to ASN
                    # else:
                        # sys.stderr.write(line) # Testing
            output_file.write(str(line_count) + '\n') # for sample output file
            total_line_count += line_count # for sample output file

byu_to_asn_file.write("end\n") # Write out to ASN   
mighty_log.save_data(sys.argv[2]) # Save the log object as binary using pickle in loglist.py

output_file.write("Total Lines Read:" + str(total_line_count) + "\n") # for sample output file

