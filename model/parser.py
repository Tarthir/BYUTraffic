import sys
import os
import glob
import errno
import gzip


if len(sys.argv) != 2:
    print("Error, ereojsldkafjld;fjalf")
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
        self.flag = None
        self.authoritative_ip = None
        self.asn_data = None
        self.p0f_data = None

    
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



with gzip.open("/home/kwankyu/Documents/RA-IMAAL/imaal-data/byu/*.gz", 'rb') as f:
    file_content = f.read()
    print(file_content)