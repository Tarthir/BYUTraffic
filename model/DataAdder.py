import sys
import os
import AsnReader
import P0fReader
import LogList

log_list = LogList.LogList()
log_list.load_all(sys.argv[4])
p0fReader = P0fReader.P0fReader()
asnReader = AsnReader.AsnReader()

# read the root asn data into the root data set
asnReader.read(sys.argv[1], log_list)
# read the byu asn data into the byu data set
asnReader.read(sys.argv[2], log_list)
# read the p0f data into the byu data set
for file in os.listdir(sys.argv[3]):
    p0fReader.read(sys.argv[3] + file, log_list)
log_list.save_data(sys.argv[4])
