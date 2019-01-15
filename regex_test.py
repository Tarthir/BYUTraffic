import re
import sys

regex = re.compile(r'(?i)^([0-9-]+)T([0-9:]+)-([0-9:]+) ([a-z0-9]+) ([a-z0-9]+)\[([0-9]+)\]: client ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})#([0-9]+) \(([a-z0-9.-]+)\): query: ([a-z0-9.-]+) ([a-z]+) ([a-z]+) -([a-z]+)* \(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\)')


if len(sys.argv) != 2:
    print("Error, ereojsldkafjld;fjalf")
    sys.exit()

if re.match(regex, sys.argv[1]):
    print("True")
else:
    print("False")