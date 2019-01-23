import pickle
import sys


# A class which holds all of our log data from:
# packets coming to BYU from the wild
# packets going to the root zone from byu
class LogList:

    def __init__(self) -> None:
        # IP -> [logObj1,logObj2,logObj3]
        # The key is an ip address and the value is a list of query log objects
        self.IP_to_Log_byu = {}
        self.IP_to_asn = {}
        # this dict holds the data from the .pcap files that were to root from byu
        self.IP_to_p0f = {}
        # our saved data
        self.my_pickled_data_byu = None
        self.my_pickled_data_root = None
        self.my_pickled_data_asn = None
        self.my_pickled_data_p0f = None
        # The files names
        self.byu_file_name = "byu_log.bin"
        self.root_file_name = "root_log.bin"
        self.asn_file_name = "asn_log.bin"
        self.p0f_file_name = "p0f_log.bin"

#####################################

    # Saves the byu and root data given valid file paths
    def save_data(self, data_file_path):
        try:
            self.__save(data_file_path, self.IP_to_Log_byu, self.byu_file_name)
            self.__save(data_file_path, self.IP_to_asn, self.asn_file_name)
            self.__save(data_file_path, self.IP_to_p0f, self.p0f_file_name)
        except IOError as err:
            sys.stderr.write('ERROR: %s' % str(err))

    # Here we save all our data to a file
    # Use this when parsing is complete
    def __save(self, file_path, log_dict, filename):
        if log_dict:
            binary_file = open(file_path + filename, mode='wb')
            self.my_pickled_data = pickle.dump(log_dict, binary_file)
            binary_file.close()
####################################

    # Loads and returns both sets of data
    def load_all(self, file_path):
        self.IP_to_Log_byu = self.__load_data(file_path + self.byu_file_name)
        self.IP_to_asn = self.__load_data(file_path + self.asn_file_name)
        self.IP_to_p0f = self.__load_data(file_path + self.p0f_file_name)

    # Loads data from a given file path
    @staticmethod
    def __load_data(file_path_and_name):
        try:
            return pickle.load(open(file_path_and_name, 'rb'))
        except IOError as err:
            sys.stderr.write('ERROR: %s' % str(err))
        except EOFError as err:
            sys.stderr.write('ERROR: %s' % str(err))

#####################################

    # Add data to one of our dictionaries held by this class
    # data: the data that is to be added, AsnData, P0fData, or query_log objects
    # data_structure: one of the three dicts found at the top of this class
    @staticmethod
    def add_to_data_structure(data, data_structure):
        if data.client not in data_structure.keys():
            data_structure[data.client] = []
        data_structure[data.client].append(data)


#####################################


