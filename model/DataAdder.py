import sys
import P0fReader
import AsnReader
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
p0fReader.read(sys.argv[3], log_list)
log_list.save_data(sys.argv[4])
