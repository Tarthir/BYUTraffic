import model.DistributionDoer as d
import model.LogList as l
import sys
from model.QueryLog import query_log


doer = d.DistributionDoer()
lst = l.LogList()
lst.load_all(sys.argv[1])

a, b = d.get_x_and_y_values("client", lst.IP_to_Log_byu)
a = 5
