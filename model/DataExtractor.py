import model.DistributionDoer as d
import model.LogList as l
import sys
import graphs.plotter as plot
from model.QueryLog import query_log


lst = l.LogList()
lst.load_all(sys.argv[1])
doer = d.DistributionDoer()
a, b = doer.get_x_and_y_values("client", lst.IP_to_Log_byu)

plt = plot.Plotter()
plt.bar_graph("Title", "x", "y" , a, b)
