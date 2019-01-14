import readers.ReaderState as State
import re
#from parse import query_log as log
import sys


class P0fReader(State.ReaderState):

    @staticmethod
    def __check_host_change(line):
        return re.search(r'mod=([^|]+)', line).group(1) == "host change"

    # Reads the p0f data and creates P0fDataHolder from the data
    # File reader must handle the appending to the PlotDataHolderList

    def read(self, filename, log_list):
        # Read two lines at a time from p0f as each IP has two lines of data
        fd = open(filename, "r")
        while True:
            line1 = fd.readline()
            line2 = fd.readline()
            line3 = None
            if not line1 or not line2:
                break  # EOF
            if self.__check_host_change(line2):
                line3 = fd.readline()
            # Make a data holder and parse the p0f data
            holder = query_log()
            self.__parse_p0f(line1, line2, line3, holder)
            log_list.append(holder)

    def __parse_p0f(self, line1, line2, line3, holder):
        # parse the lines and hold the data
        self.__parse_p0f_line1(line1, holder)
        self.__parse_p0f_line2(line2, holder)
        if line3 is not None:
            sys.stderr.write("IP with host change found: {}\n".format(holder.vars["client"]))
            self.__parse_p0f_line2(line3, holder)
            #holder.vars['holder_ip = holder.vars['var_dict["client"]

    def __parse_p0f_line1(self, line1, holder):
        try:
            holder.vars['mod'] = re.search(r'mod=([^|]+)', line1).group(1)
            ip = (re.search("cli=([^|]+)", line1, re.DOTALL).group(1)).split("/")
            holder.vars['client'] = ip[0].strip()
            # self.ports_found_on.append(ip[1])
            holder.vars['srv'] = re.search("srv=([^|]+)", line1, re.DOTALL).group(1)
            holder.vars['subj'] = re.search("subj=([^|]+)", line1, re.DOTALL).group(1)
            holder.vars['os'] = re.search("os=([^|]+)", line1, re.DOTALL).group(1)
            holder.vars['dist'] = re.search("dist=([^|]+)", line1, re.DOTALL).group(1)
            holder.vars['params'] = re.search("params=([^|]+)", line1, re.DOTALL).group(1)
            holder.vars['raw_sig'] = re.search("raw_sig=([^|]+)", line1, re.DOTALL).group(1).rstrip()
        except AttributeError as err:
            sys.stderr.write('ERROR: %sn' % str(err))

    def __parse_p0f_line2(self, line2, holder):
        try:
            if re.search(r'mod=([^|]+)', line2).group(1) != "host change":
                holder.vars['link'] = re.search("link=([^|]+)", line2, re.DOTALL).group(1)
                holder.vars['raw_mtu'] = re.search("raw_mtu=([^|]+)", line2, re.DOTALL).group(1).rstrip()
            else:
                holder.vars['reason'] = re.search("reason=([^|]+)", line2, re.DOTALL).group(1)
        except AttributeError as err:
            sys.stderr.write('ERROR: %sn' % str(err))