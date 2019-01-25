import readers.ReaderState as State
import re
#from parse import query_log as log
import sys
import model.P0fData as p

class P0fReader(State.ReaderState):

    @staticmethod
    def __check_host_change(line):
        return re.search(r'mod=([^|]+)', line).group(1) == "host change"

    # Reads the p0f data and creates P0fDataHolder from the data
    # File reader must handle the appending to the PlotDataHolderList

    def read(self, filename, log_list):
        # Read two lines at a time from p0f as each IP has two lines of data
        try:
            fd = open(filename, "r")
        except IOError as err:
            sys.stderr.write('Error: %s\n' % str(err))
            return
        while True:
            line1 = fd.readline()
            line2 = fd.readline()
            line3 = None
            if not line1 or not line2:
                break  # EOF
            if self.__check_host_change(line2):
                line3 = fd.readline()
            # Make a data holder and parse the p0f data
            holder = p.P0fData()
            self.__parse_p0f(line1, line2, line3, holder)
            log_list.add_to_data_structure(holder, log_list.IP_to_p0f)

    def __parse_p0f(self, line1, line2, line3, holder):
        # parse the lines and hold the data
        self.__parse_p0f_line1(line1, holder)
        self.__parse_p0f_line2(line2, holder)
        if line3 is not None:
            sys.stderr.write("IP with host change found: {}\n".format(holder.client))
            self.__parse_p0f_line2(line3, holder)

    def __parse_p0f_line1(self, line1, holder):
        try:
            holder.mod = re.search(r'mod=([^|]+)', line1).group(1)
            ip = (re.search("cli=([^|]+)", line1, re.DOTALL).group(1)).split("/")
            holder.client = ip[0].strip()
            holder.srv = re.search("srv=([^|]+)", line1, re.DOTALL).group(1)
            holder.subj = re.search("subj=([^|]+)", line1, re.DOTALL).group(1)
            holder.os = re.search("os=([^|]+)", line1, re.DOTALL).group(1)
            holder.dist = re.search("dist=([^|]+)", line1, re.DOTALL).group(1)
            holder.params = re.search("params=([^|]+)", line1, re.DOTALL).group(1)
            holder.raw_sig = re.search("raw_sig=([^|]+)", line1, re.DOTALL).group(1).rstrip()
        except AttributeError as err:
            sys.stderr.write('ERROR: %sn' % str(err))

    def __parse_p0f_line2(self, line2, holder):
        try:
            if re.search(r'mod=([^|]+)', line2).group(1) != "host change":
                holder.link = re.search("link=([^|]+)", line2, re.DOTALL).group(1)
                holder.raw_mtu = re.search("raw_mtu=([^|]+)", line2, re.DOTALL).group(1).rstrip()
            else:
                holder.reason = re.search("reason=([^|]+)", line2, re.DOTALL).group(1)
        except AttributeError as err:
            sys.stderr.write('ERROR: %sn' % str(err))
