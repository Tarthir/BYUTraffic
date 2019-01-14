import states.ReaderState as State
from model import PlotDataHolder as Holder
import sys


class AsnReader(State.ReaderState):
    def __init__(self):
        self.__SIZE_OF_COUNTRY_CODES = 2
        super().__init__()



    # Goes through the asn data file(s) and
    def read(self, filename, log_list):
        fd = open(filename, "r")
        while True:
            line = None
            try:
                line = fd.readline()
            except UnicodeDecodeError as err:
                sys.stderr.write('KeyError in DataHolderList: %s\n' % str(err))
            if not line:
                break  # EOF
            line_arr = line.split("|")
            # Strip away all unneeded whitespace
            holder_to_update = query_log()
            self.__parse_asn(line_arr, holder_to_update)
            log_list.append(holder_to_update)

    # Helper function which deals with the complicated logic of parsing asn lines
    # In this function what comes in is longname_country_arr of length 1
    # It may contain the country code, if it does we grab it
    # If it does not then we see if it was parsed out in an earlier step from 'name'
    def __check_small_len(self, longname_country_arr, name, holder):
        holder.vars['longname']      = name[0]
        # If there is no country code that was parsed, return
        if len(longname_country_arr[0].strip()) > self.__SIZE_OF_COUNTRY_CODES:
            # If 'name' has the country code
            if len(name) == 3:
                holder.vars['country'] = name[2]
                return
            # If there is no country code given to us
            holder.vars['country'] = None
            return
        holder.vars['country'] = longname_country_arr[0].strip()

    # This method parses ASN lines
    # Basically these lines are laid out thusly: ASN | IP | SHORT_NAME - LONGNAME, COUNTRY CODE
    # However there are exceptions which complicate the logic
    # line_arr will usually look like this: [ASN,IP,REST] with REST = 'SHORT_NAME - LONGNAME, COUNTRY CODE'
    def __parse_asn(self, line_arr, holder):
        holder.vars['asn'] = line_arr[0]
        holder.vars['client'] = line_arr[1].strip()
        #holder.holder_ip = line_arr[1]
        # Will split: MIT-GATEWAYS - Massachusetts Institute of Technology, US
        # to: [MIT-GATEWAYS, Massachusetts Institute of Technology, US ]
        # and GNW-ASN39211, EE
        # to: [GNW-ASN39211, EE]
        name = line_arr[2].split(" - ", 1) if " - " in line_arr[2] else line_arr[2].split(", ", 1)
        # This first part will be the 'short name'
        holder.vars['short_name'] = name[0]
        if name[0] != "NA":
            idx = 1
            # if we are given a very small result we may not have a " - " to split on
            if len(name) == 1:
                idx = 0
            # split the name array into longname and country attributes
            longname_country_arr = name[idx].rsplit(', ', 1)
            if len(longname_country_arr) == 1:
                self.__check_small_len(longname_country_arr, name, holder)
            else:
                holder.vars['longname'] = longname_country_arr[0].strip()
                holder.vars['country'] = longname_country_arr[1].strip()

