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
        self.IP_to_Log_root = {}
        # our saved data
        self.my_pickled_data_byu = None
        self.my_pickled_data_root = None

#####################################

    # Saves the byu and root data given valid file paths
    def save_data(self, data_file_byu, data_file_root):
        try:
            self.__save(data_file_byu, self.IP_to_Log_byu)
            self.__save(data_file_root, self.IP_to_Log_root)
        except IOError as err:
            sys.stderr.write('ERROR: %sn' % str(err))

    # Here we save all our data to a file
    # Use this when parsing is complete
    def __save(self, file_path_and_name, log_dict):
        binary_file = open(file_path_and_name + '.bin', mode='wb')
        self.my_pickled_data = pickle.dump(log_dict, binary_file)
        binary_file.close()

####################################

    # Loads and returns both sets of data
    def load_all(self, file_path_and_name=None):
        return self.load_byu(file_path_and_name), self.load_root(file_path_and_name)

    # Loads and returns the byu data
    def load_byu(self, file_path_and_name=None):
        self.IP_to_Log_byu = self.load(self.my_pickled_data_byu, file_path_and_name)
        return self.IP_to_Log_byu

    # Loads and returns the root data
    def load_root(self, file_path_and_name=None):
        self.IP_to_Log_root = self.load(self.my_pickled_data_root, file_path_and_name)
        return self.IP_to_Log_root

    # Loads data from either a pickled file object or from a given file path
    def __load_data(self, my_pickled_data, file_path_and_name=None):
        # See if our pickled obj is in memory or not
        if my_pickled_data is not None:
            return pickle.loads(my_pickled_data)
        # if they gave us a file path
        elif file_path_and_name is not None:
            try:
                return pickle.load(open(file_path_and_name, 'rb'))
            except IOError as err:
                sys.stderr.write('ERROR: %sn' % str(err))
        # if they gave us no way to retrieve the information
        else:
            sys.stderr.write('ERROR: Please specify a file and its path')

#####################################

    # This function adds a log object to the byu log dict
    def add_to_byu(self, log_obj):
        self.__add_to_log(log_obj, self.IP_to_Log_byu)

    # This function adds a log object to the root log dict
    def add_to_root(self, log_obj):
        self.__add_to_log(log_obj, self.IP_to_Log_root)

    # Handles the actually adding of data to the right dictionary
    def __add_to_log(self, log_obj, log_dict):
        if log_obj.client_ip not in log_dict.keys():
            log_dict[log_obj.client_ip] = []
        log_dict[log_obj.client_ip].append(log_obj)

