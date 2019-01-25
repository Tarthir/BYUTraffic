import sys
import readers.P0fReader
import readers.AsnReader
import model.LogList

log_list = model.LogList.LogList()
log_list.load_all(sys.argv[4])
p0fReader = readers.P0fReader.P0fReader()
asnReader = readers.AsnReader.AsnReader()

# read the root asn data into the root data set
asnReader.read(sys.argv[1], log_list)
# read the byu asn data into the byu data set
asnReader.read(sys.argv[2], log_list)
# read the p0f data into the byu data set
p0fReader.read(sys.argv[3], log_list)
log_list.save_data(sys.argv[4])
