from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class PlotDrawer(metaclass=ABCMeta):
    """ PlotDrawer """
    def __init__(self, file):
        """ init """
        print("{} starts drawing a graph".format(self.__class__.__name__))
        self.file = file
        self.arg_dict = {}

    def read_csv(self):
        print("reading the csv file")
        if not self.noheader:
            self.df = pd.read_csv(self.file)
        else:
            self.df = pd.read_csv(self.file, header=None)
            self.df.columns = [ "column"+str(x) for x in self.df.columns ]
        self.arg_dict["data"] = self.df
        self.columns = self.df.columns

    @abstractmethod
    def plot(self):
        pass

    def draw(self, arg_dict):
        self.set_conf(arg_dict)
        self.read_csv()
        sns.set_style("whitegrid")
        self.plot()
        sns.plt.savefig(self.outfile)

    def print_header(self):
        print("--------------------------------------------------")
        print("please select column(s) to be used as axises")
        for i, column in enumerate(self.columns):
            print("    {}: {}".format(i, column))

    def input_x(self):
        self.print_header()
        print("input(x-axis): ", end='')
        self.arg_dict["x"] = self.columns[str(input())]

    def input_x_y(self):
        self.input_x()
        print("input(y-axis): ", end='')
        self.arg_dict["y"] = self.columns[str(input())]

    def input_hue(self):
        if self.hue:
            print("input(hue): ", end='')
            self.arg_dict["hue"] = self.columns[str(input())]

    def set_conf(self, arg_dict):
        self.outfile = arg_dict["outfile"] if arg_dict["outfile"] else self.file.replace(".csv", ".png")
        self.noheader = True if arg_dict["noheader"] else False
        self.hue = True if arg_dict["hue"] else False

class ScatterPlotDrawer(PlotDrawer):
    """ ScatterPlotDrawer """
    def plot(self):
        self.input_x_y()
        self.input_hue()
        sns.lmplot(**self.arg_dict, fit_reg=False)

class PointPlotDrawer(PlotDrawer):
    """ ScatterPlotDrawer """
    def plot(self):
        self.input_x_y()
        self.input_hue()
        sns.pointplot(**self.arg_dict)

class BarPlotDrawer(PlotDrawer):
    """ BarPlotDrawer """
    def plot(self):
        self.input_x_y()
        self.input_hue()
        sns.barplot(**self.arg_dict)

class DistPlotDrawer(PlotDrawer):
    """ DistPlotDrawer """
    def plot(self):
        self.input_x()
        sns.distplot(self.df[self.arg_dict["x"]])

class BoxPlotDrawer(PlotDrawer):
    """ BoxPlotDrawer """
    def plot(self):
        self.input_x_y()
        self.input_hue()
        sns.boxplot(**self.arg_dict)

class CountPlotDrawer(PlotDrawer):
    """ CountPlotDrawer """
    def plot(self):
        self.input_x()
        self.input_hue()
        sns.countplot(**self.arg_dict)

class JointPlotDrawer(PlotDrawer):
    """ JointPlotDrawer """
    def plot(self):
        self.input_x_y()
        sns.jointplot(**self.arg_dict)

class PairPlotDrawer(PlotDrawer):
    """ PairPlotDrawer """
    def plot(self):
        self.input_hue()
        sns.pairplot(**self.arg_dict)
