import re
import os
import sys

# this script will go through all the logfiles and search for all client ips
# we will then do ASN lookups on them from a batch file and a netcat command
# that data will then be stored in this same directory
if len(sys.argv) != 3:
    print("Usage is getASN.py <asnData.asn path> <location of p0f log files>")
    sys.exit(1)

asnData = sys.argv[2]  # '/home/tyler/data_gathering/asnGeoData/asnData.asn'
logFilesLoc = sys.argv[3]

# asnFinalData = '/home/tyler/asnData/finalASNData.data'
# def write_addr(type_of_addr):
# get all ipv4
cnt = 0
ip_set = {}
ip_set = set()
os.chdir(logFilesLoc)
# os.chdir("/home/tyler/data_gathering/p0f/p0fdata/")
# we have to put 'begin' at the start of the file for the netcat call to work for ASN lookup
with open(asnData, 'w') as tmp:
    tmp.write("begin\n")

for file in os.listdir(logFilesLoc):
    # print(file)
    # TODO may want to get rid of this requirement, may want to read files other then ones that are .p0f
    if file.endswith(".p0f"):
        # lets go through all the p0f files and get the IP addresses we find
        with open(file, 'r') as f:
            for line in f:
                # TODO may want to expand this so we can get the ip from
                # TODO more then just these .pof files (more usability outside this project)
                ip_addr = re.search('cli=(.*?)/', line, re.DOTALL).group(1)
                if ip_addr:
                    ip_set.add(ip_addr)

# Now that the ip addresses are in a set we will not use any duplicates
with open(asnData, 'a') as output:
    for ip in ip_set:
        ip = ip + '\n'
        output.write(ip)
        cnt = cnt + 1
# we have to put 'end' at the end of the file for ASN lookup to work
with open(asnData, 'a') as tmp:
    tmp.write("end\n")

print('Found ' + str(cnt) + ' unique ip addresses')

# after running this script the bash script will run:
# netcat whois.cymru.com 43 < asnPreProcessedData.data | sort -n > asnFinalData.
