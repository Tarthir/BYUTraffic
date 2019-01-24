import sys
import readers.P0fReader
import readers.AsnReader
import LogList

log_list = LogList.LogList()
# TODO we need the real file here
log_list.load_all("/home/example/file/path/for/now/")
p0fReader = readers.P0fReader.P0fReader()
asnReader = readers.AsnReader.AsnReader()

# read the root asn data into the root data set
asnReader.read(sys.argv[1], log_list)
# read the byu asn data into the byu data set
asnReader.read(sys.argv[2], log_list)
# read the p0f data into the byu data set
p0fReader.read(sys.argv[3], log_list)
# TODO this needs to become the real file
log_list.save_data("/home/example/file/path/for/now/")
