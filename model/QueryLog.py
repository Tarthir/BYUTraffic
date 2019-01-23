class query_log:
    def __init__(self, date, time, time_zone, authoritative_name, process_name, process_id,\
    client_ip, client_port, query, dns_class, resource_record, set_bool, flag, authoritative_ip):
        self.date = date
        self.time = time
        self.time_zone = time_zone
        self.authoritative_name = authoritative_name
        self.process_name = process_name
        self.process_id = process_id
        self.client = client_ip
        self.client_port = client_port
        self.query = query
        self.dns_class = dns_class
        self.resource_record = resource_record
        self.set = set_bool
        self.flag = flag
        self.authoritative_ip = authoritative_ip
        self.asn_data = None
        self.p0f_data = None

        # Print all the data members

    def display(self):
        print(str(self.date) + " " + str(self.time) + " " + str(self.time_zone) + " " + str(self.authoritative_name) \
              + " " + str(self.process_name) + " " + str(self.process_id) + " " + str(self.client) + " " + str(
            self.client_port) \
              + " " + str(self.query) + " " + str(self.dns_class) + " " + str(self.resource_record) + " " + str(
            self.set) \
              + " " + str(self.flag) + " " + str(self.authoritative_ip) + " " + str(self.asn_data) + " " + str(
            self.p0f_data))