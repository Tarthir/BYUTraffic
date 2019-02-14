import sys
import os
import glob
import errno
import gzip
import re
import mysql.connector
import time


# Takes in the file path directory to read all the zip files
# For Example from base /home/imaal/dns-queries/byu
# Argument 1: Directory path to the zip files to read from
if len(sys.argv) > 2:
    print("Error, Give the path of the directory to zip file")

time_start = time.time()
print("Start: ")

directory_of_zip = sys.argv[1] # Path of the directory holding the zip files

mydb = mysql.connector.connect(
    host="localhost",
    user="kwankyu",
    password="password"
)

mycursor = mydb.cursor()
mycursor.execute("create database if not exists ByuTrafficDBOrg")
mycursor.execute("use ByuTrafficDBOrg")

# drop table before creating
sql = "DROP TABLE IF EXISTS parser"
mycursor.execute(sql)

mycursor.execute("create table if not exists parser (id int auto_increment primary key, date varchar(255), time varchar(255), time_zone varchar(255), \
    authoritative_name varchar(255), process_name varchar(255), process_id varchar(255), client_ip varchar(255), client_port varchar(255), query varchar(255), \
        dns_class varchar(255), resource_record varchar(255), set_bool varchar(255), flag varchar(255), authoritative_ip varchar(255))")
sql = "insert into parser (date, time, time_zone, authoritative_name, process_name, process_id, client_ip, client_port, query, dns_class, resource_record, \
    set_bool, flag, authoritative_ip) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# val = ("the date", "the time", "the time zone", "the authoritative name", "the process name", "process_id", "client_ip", "client_port", "query", "dns_class", \
#     "resource record", "set_bool", "flag", "authoritative_ip")
val = []

regex = re.compile(r'(?i)^([0-9-]+)T([0-9:]+)-([0-9:]+) ([a-z0-9]+) ([a-z0-9]+)\[([0-9]+)\]: client ([0-9a-f.:]+)#([0-9]+) \((.*?)\): query: (.*?) ([a-z]+) ([a-z0-9]+) ([-+])([a-z]+)* \((.*?)\)')

output_file = open("sample_output.txt", "w") # Creates a file with extra info about the files
total_line_count = 0 # For sample output file

time_loop = time.time()
print("Before loop: " + str(time_loop - time_start))
for root, dirs, files in os.walk(directory_of_zip, topdown=True): # Start from the top and go down the directory
    for name in files:
        if name.endswith('.gz'):
            output_file.write(str(name) + ' ') # For sample output file
            # print(str(name))
            line_count = 0 # For sample output file
            # with gzip.open(os.path.join(root,name), 'rt') as f: # rt - read and text, default is rb - read and bytes
            with gzip.open(str(root) + "/" + str(name), 'rt') as f: # rt - read and text, default is rb - read and bytes    
                for line in f:
                    line_count += 1 # For sample output file
                    # print(line_count)
                    # print(line)
                    if re.match(regex, line):
                        regex_groups = re.match(regex, line) # Hold all the matched groups

                        # val.append((regex_groups.group(1), regex_groups.group(2), regex_groups.group(3), regex_groups.group(4), regex_groups.group(5)\
                        # , regex_groups.group(6), regex_groups.group(7), regex_groups.group(8), regex_groups.group(10), regex_groups.group(11)\
                        # , regex_groups.group(12), regex_groups.group(13), regex_groups.group(14), regex_groups.group(15)))

                        val = (regex_groups.group(1), regex_groups.group(2), regex_groups.group(3), regex_groups.group(4), regex_groups.group(5)\
                        , regex_groups.group(6), regex_groups.group(7), regex_groups.group(8), regex_groups.group(10), regex_groups.group(11)\
                        , regex_groups.group(12), regex_groups.group(13), regex_groups.group(14), regex_groups.group(15))

                        mycursor.execute(sql, val)  
                    # else:
                        # sys.stderr.write(line) # Testing
            output_file.write(str(line_count) + '\n') # for sample output file
            total_line_count += line_count # for sample output file

time_finish = time.time()
print("finish: " + str(time_finish - time_loop))
# mycursor.executemany(sql, val)
mydb.commit()

time_commit = time.time()
print("commit: " + str(time_commit - time_finish))

output_file.write("Total Lines Read:" + str(total_line_count) + "\n") # for sample output file



