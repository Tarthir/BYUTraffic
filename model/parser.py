import sys
import os
import glob
import errno
import gzip
import re


if len(sys.argv) != 2:
    print("Error, ereojsldkakwanimwatchingyoufjld;fjalf")
    sys.exit()


class query_log:
    def __init__(self):
        self.date = None
        self.time_zone = None
        self.authoritative_name = None
        self.process_name = None
        self.process_id = None
        self.client_ip = None
        self.client_port = None
        self.query = None
        self.dns_class = None
        self.resource_record = None
        self.set = None
        self.flag = None
        self.authoritative_ip = None

    
directory_name = sys.argv[1]

# file_write = open(file_name, "r")

print(directory_name)

# for filename in glob.glob(os.path.join(directory_name, '*.gz')):
#     # print(filename)
#     try:
#         with gzip.open(filename) as f:
#             print(f)
#             # sys.stdout.write(f.read())
#     except IOError as exc:
#         if exc.errno != errno.EISDIR:
#             raise


# for line in file_write:
#     sys.stdout.write(line)
    #print(line) #prints extra new line with output :(
# The beautiful regex, not complete yet
# (?i)^([0-9-]+)T([0-9:]+)-([0-9:]+) ([a-z0-9]+) ([a-z0-9]+)\[([0-9]+)\]: client ([0-9]{3}\.[0-9]{3}\.[0-9]{3}\.[0-9]{3})#([0-9]+) \(([a-z0-9.]+)\): query: ([a-z0-9.]+) ([a-z]+) ([a-z]+) -([a-z]+) \(([0-9]{3}\.[0-9]{3}\.[0-9]{3}\.[0-9]{3})\)



output_file = open("sample_output.txt", "w")

regex = re.compile(r'(?i)^([0-9-]+)T([0-9:]+)-([0-9:]+) ([a-z0-9]+) ([a-z0-9]+)\[([0-9]+)\]: client ([0-9a-f.:]+)#([0-9]+) \((.*?)\): query: (.*?) ([a-z]+) ([a-z0-9]+) ([-+])([a-z]+)* \((.*?)\)')

for root, dirs, files in os.walk(sys.argv[1], topdown=True):
    for name in files:
        if name.endswith('.gz'):
            output_file.write(str(name) + ' ')
            line_count = 0
            with gzip.open(os.path.join(root,name), 'rt') as f: # rt - read and text, default is rb - read and bytes
                for line in f:
                    line_count += 1
                    if re.match(regex, line):
                        sys.stdout.write(line) # write to stdout prevents extra newline
                    else:
                        sys.stderr.write(line)
            output_file.write(str(line_count) + '\n')
#    for name in files:
#       print(os.path.join(root, name))
#    for name in dirs:
#       print(os.path.join(root, name))