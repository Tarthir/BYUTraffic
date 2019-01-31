import operator

import model.DistributionDoer as d
import model.LogList as l
import sys
import graphs.plotter as plot
from model.QueryLog import query_log


lst = l.LogList()
lst.load_all(sys.argv[1])
doer = d.DistributionDoer()
#a, b = doer.get_x_and_y_values("client", lst.IP_to_Log_byu)
#a = a[:10]
#b = b[:10]

plt = plot.Plotter()
#plt.bar_graph("IP's Querying BYU Servers", "IP Addresses",  "Percent of traffic", a, b)

#a, b = doer.get_x_and_y_values("flag",lst.IP_to_Log_byu)
#plt.bar_graph("Title", "x", "y", a, b)

# requests per address
a, b = doer.get_x_and_y_values("client", lst.IP_to_Log_byu)
a = a[:15]
b = b[:15]
#plt.bar_graph("Queries per address", "addresses", "something", a, b)

# requests per ASN
a, b = doer.get_x_and_y_values("asn", lst.IP_to_asn)
a = a[:15]
b = b[:15]
#plt.bar_graph("Requests per asn", "asn", "something", a, b)
# Requests per asn by name
a, b = doer.get_x_and_y_values("short_name", lst.IP_to_asn)
a = a[:15]
b = b[:15]
#plt.bar_graph("Requests per asn", "asn", "something", a, b)
# Client IPs per ASN
dc = {}
for key in lst.IP_to_asn:
    asn = (lst.IP_to_asn[key])[0].asn
    if asn not in dc:
        dc[asn] = 0
    dc[asn] += 1
a, b = doer.make_lists(dc, dc.get)
a = a[:15]
b = b[:15]
#plt.bar_graph("Clients per asn","client","something", a, b)
# client IP's per /24
dct = lst.IP_to_Log_byu.keys()
subnets = {}
subnets2 = {}
for IP in dct:
    try:
        sub = IP[:IP.rindex('.')]
        if sub not in subnets.keys():
            subnets[sub] = 0
            subnets2[sub] = 0
        #if IP not in subnets[sub]:
        subnets[sub] += 1
        subnets2[sub] += len(lst.IP_to_Log_byu[IP])
    except ValueError as err:
        print("Ignoring Ipv6")
        #sub = IP[:IP.rindex('::')]
        continue
a, b = doer.make_lists(subnets, subnets.get)

a = list(a)[:15]
b = b[:15]
plt.bar_graph("Clients per /24", "/24's", "Number of Clients", a, b)
# requests per /24
a, b = doer.make_lists(subnets2, subnets2.get)
a = a[:15]
b = b[:15]
plt.bar_graph("Requests per /24", "/24's", "Number of Requests", a, b)
