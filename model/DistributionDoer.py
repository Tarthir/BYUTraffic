import sys

class DistributionDoer:

    # This function goes through our data structure and gets the values associated with var
    # those values are added up and put into the result Object.
    # var is the variable we want to look at
    # ip_to_data is the data structure we are looking through
    def get_x_and_y_values(self, var, ip_to_data):
        if var == 'client':
            return self.__get_client(ip_to_data)
        result = {}
        # get the list of objects, query_obj, associated with a given key
        for key, query_obj in ip_to_data.items():
            # Go through every object in the list and add to our results
            for item in query_obj:
                attr_val = getattr(item, var)
                # if we did not find anything, check the asn or p0f data objects
                if attr_val is None:
                    # TODO probably need a try-catch
                    attr_val = self.__check_objects(item, var)
                # create the entry or add to it depending on whether we have seen it before or not
                if attr_val in result.keys():
                    result[attr_val] += 1
                else:
                    result[attr_val] = 1
        return list(result.keys()), list(result.values())  # Returning the x/y values from the dictionary we made

    # Do we need to look into our objects for the var asked for?
    # if the var asked for is in the asn or p0f data use this function to get it out
    @staticmethod
    def __check_objects(item, var):
        try:
            a = getattr(getattr(item, 'asn_data'), var)
            return a if a is not None else getattr(getattr(item, 'p0f_data'), var)
        except AttributeError as err:
            #sys.stderr.write('ERROR: %s\n' % str(err))
            return None
    # Returns two lists, x and y values. With x values being he IP address and y being the number
    # of times that IP value showed up in one of our data sets
    @staticmethod
    def __get_client(ip_to_data):
        data = ip_to_data.copy()
        sum = len(list(data.values()))
        for k in data:
            data[k] = len(data[k])/sum
        # sort into tuples
        s = [(k, data[k]) for k in sorted(data, key=data.get, reverse=True)]
        a, b = zip(*s)
        # convert into lists
        return list(a), list(b)
