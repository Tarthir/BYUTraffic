import sys
import os
import glob
import errno
import gzip
import re
import LogList

# Takes in the file path directory to read all the zip files
# For Example from base /home/imaal/dns-queries/byu
if len(sys.argv) != 2:
    print("Error, Give the path of the directory")
    sys.exit()


class query_log:
    def __init__(self, date, time, time_zone, authoritative_name, process_name, process_id,\
    client_ip, client_port, query, dns_class, resource_record, set_bool, flag, authoritative_ip):
        self.date = date
        self.time = time
        self.time_zone = time_zone
        self.authoritative_name = authoritative_name
        self.process_name = process_name
        self.process_id = process_id
        self.client_ip = client_ip
        self.client_port = client_port
        self.query = query
        self.dns_class = dns_class
        self.resource_record = resource_record
        self.set = set_bool
        self.flag = flag
        self.authoritative_ip = authoritative_ip
        self.asn_data = None
        self.p0f_data = None
    
    # Print all the data members
    def display(self):
        print(str(self.date) + " " + str(self.time) + " " + str(self.time_zone) + " " + str(self.authoritative_name)\
        + " " + str(self.process_name) + " " + str(self.process_id) + " " + str(self.client_ip) + " " + str(self.client_port)\
        + " " + str(self.query) + " " + str(self.dns_class) + " " + str(self.resource_record) + " " + str(self.set)\
        + " " + str(self.flag) + " " + str(self.authoritative_ip) + " " + str(self.asn_data) + " " + str(self.p0f_data))

    
directory_name = sys.argv[1] # Path of the directory holding the zip files

mighty_log = LogList()


output_file = open("sample_output.txt", "w") # Creates a file with extra info about the files

regex = re.compile(r'(?i)^([0-9-]+)T([0-9:]+)-([0-9:]+) ([a-z0-9]+) ([a-z0-9]+)\[([0-9]+)\]: client ([0-9a-f.:]+)#([0-9]+) \((.*?)\): query: (.*?) ([a-z]+) ([a-z0-9]+) ([-+])([a-z]+)* \((.*?)\)')

total_line_count = 0
for root, dirs, files in os.walk(sys.argv[1], topdown=True): # Start from the top and go down the directory
    for name in files:
        if name.endswith('.gz'):
            output_file.write(str(name) + ' ')
            line_count = 0
            with gzip.open(os.path.join(root,name), 'rt') as f: # rt - read and text, default is rb - read and bytes
                for line in f:
                    line_count += 1
                    if re.match(regex, line):
                        # sys.stdout.write(line) # write to stdout prevents extra newline
                        regex_groups = re.match(regex, line)
                        log_object = query_log(regex_groups.group(1), regex_groups.group(2), regex_groups.group(3), regex_groups.group(4), regex_groups.group(5)\
                        , regex_groups.group(6), regex_groups.group(7), regex_groups.group(8), regex_groups.group(10), regex_groups.group(11)\
                        , regex_groups.group(12), regex_groups.group(13), regex_groups.group(14), regex_groups.group(15))
                        log_object.display()
                        mighty_log.add_to_byu(log_object)
                    else:
                        # sys.stderr.write(line)
            output_file.write(str(line_count) + '\n')
            total_line_count += line_count

output_file.write("Total Lines Read:" + str(total_line_count))
#    for name in files:
#       print(os.path.join(root, name))
#    for name in dirs:
#       print(os.path.join(root, name))