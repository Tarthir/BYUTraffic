import sys
import dns

if len(sys.argv) < 1:
    print("error error error")

query_name_file = open(sys.argv[1], "r") # Open up the files with all the query names
unique_query_names = set(query_name_file.readlines()) # Unique query names

output_file = open(str(sys.argv[2]) + "query_ttl", "w")

for line in unique_query_names:
    answer = dns.resolver.query(line)
    output_file.write(str(line) + " " + str(answer.rrset.ttl) # Give us the time to live


# Incomplete
# Not sure if we want to store this in a file or in loglist