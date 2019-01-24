import os
import gzip
import subprocess
import shutil
import sys

# This script runs the program p0f onto ip addresses that responded to us during the maxudp.py test
# need to have tcp dump running:
# sudo tcpdump -i authdns1 -G 600 -z gzip -w dns-recursive-authoritative-%Y%m%d%H%M.pcap dst port 53
# run script like this: PATH=~/user/sbin$PATH python p0fer.py /home/tyler/ /home/tyler/p0f/unzipped_data/ 2> error.log

# cnt keeps track of how many files we are running p0f on
# can send it to /chucks_unzipped_data
# chucks_data = "/home/tyler/unzipped_data/"
if len(sys.argv) != 4:
    print("Usage is p0fer.py <unzipped pcap FileLocation> <destination of unzipped files> <dst of the p0f log files>")
    sys.exit(1)
pcapFilesLoc = sys.argv[1]
destUnzipped = sys.argv[2]
destLogLoc = sys.argv[3]

def p0f_file(unzipped_f, cnt, f_in):
    with open (unzipped_f,'wb') as f_out:
        print("Opening %s and running p0f on it" % unzipped_f) 
        # copy contents of data to my dir in specified file
        shutil.copyfileobj(f_in,f_out)
        f_in.close()
        # write p0f data to a logfile
        logfile = destLogLoc + 'p0finfo' + str(cnt) + '.p0f'
    # now lets run that data through p0f
    # run p0f on the unzipped file
    subprocess.check_output(['/usr/sbin/p0f','-r',unzipped_f,'-o',logfile,'dst port 53 and (dst host 128.187.82.251 or dst host 128.187.82.250 or dst host 128.187.82.230 or dst host 128.187.82.231)'])

cnt = 0
for file in os.listdir(pcapFilesLoc): 
    chuck_file = pcapFilesLoc + file
    unzipped_f = None
    f_in = None

    # need to unzip .gz files
    if file.endswith(".pcap.gz"):
        unzipped_f = destUnzipped + file[:-3]
        f_in = gzip.open(chuck_file, 'rb')
    # if we find just a .pcap file
    elif file.endswith(".pcap"):
        unzipped_f = destUnzipped + file
        f_in = open(chuck_file, 'rb')
    # skip all other files
    else:
        continue
    # open the file and run the data data
    # and lets send it to my dir
    cnt = 1 + cnt
    p0f_file(unzipped_f,cnt,f_in)
        

print("Ran p0f on: " + str(cnt) + " files!")
