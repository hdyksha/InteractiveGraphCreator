from plot_drawer import *

class PlotDrawerFactory():
    """ PlotDrawerFactory """
    def __init__(self):
        """ init """
        pass

    def create(self, file, plot_type):
        """ create """
        if plot_type == "scatter":
            return ScatterPlotDrawer(file)
        elif plot_type == "point":
            return PointPlotDrawer(file)
        elif plot_type == "bar":
            return BarPlotDrawer(file)
        elif plot_type == "dist":
            return DistPlotDrawer(file)
        elif plot_type == "box":
            return BoxPlotDrawer(file)
        elif plot_type == "count":
            return CountPlotDrawer(file)
        elif plot_type == "joint":
            return JointPlotDrawer(file)
        elif plot_type == "pair":
            return PairPlotDrawer(file)
        else:
            print("The plot type is not implemented")
            sys.exit(1)
