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

    def draw(self, arg_dict):
        self.set_conf(arg_dict)
        self.read_csv()
        sns.set_style("whitegrid")
        self.plot()
        sns.plt.savefig(self.outfile)

    @abstractmethod
    def plot(self):
        pass

    def print_header(self):
        print("--------------------------------------------------")
        print("please select column(s) to be used as axises")
        for i, column in enumerate(self.columns):
            print("    {}: {}".format(i, column))

    def default_input(self, key):
        if not key in self.arg_dict or not self.arg_dict[key] in self.columns:
            print("input({}): ".format(key), end='')
            self.arg_dict[key] = self.columns[str(input())]

    def optional_input(self, key):
        if key in self.arg_dict and not self.arg_dict[key] in self.columns:
            print("input({}): ".format(key), end='')
            self.arg_dict[key] = self.columns[str(input())]

    def remove_item(self, key):
        if key in self.arg_dict: del self.arg_dict[key]

    def set_conf(self, arg_dict):
        """
        set config dict based on the command line args
        """
        self.outfile = arg_dict["outfile"] if "outfile" in arg_dict else self.file.replace(".csv", ".png")
        self.noheader = arg_dict["noheader"] if "noheader" in arg_dict else False
        if "xaxis" in arg_dict: self.arg_dict["x"] = arg_dict["xaxis"]
        if "yaxis" in arg_dict: self.arg_dict["y"] = arg_dict["yaxis"]
        if "hue" in arg_dict: self.arg_dict["hue"] = arg_dict["hue"]

class ScatterPlotDrawer(PlotDrawer):
    """ ScatterPlotDrawer """
    def plot(self):
        self.print_header()
        self.default_input("x")
        self.default_input("y")
        self.optional_input("hue")
        sns.lmplot(**self.arg_dict, fit_reg=False)

class PointPlotDrawer(PlotDrawer):
    """ ScatterPlotDrawer """
    def plot(self):
        self.print_header()
        self.default_input("x")
        self.default_input("y")
        self.optional_input("hue")
        sns.pointplot(**self.arg_dict)

class BarPlotDrawer(PlotDrawer):
    """ BarPlotDrawer """
    def plot(self):
        self.print_header()
        self.default_input("x")
        self.default_input("y")
        self.optional_input("hue")
        sns.barplot(**self.arg_dict)

class DistPlotDrawer(PlotDrawer):
    """ DistPlotDrawer """
    def plot(self):
        self.print_header()
        self.default_input("x")
        self.remove_item("y")
        self.remove_item("hue")
        sns.distplot(self.df[self.arg_dict["x"]])

class BoxPlotDrawer(PlotDrawer):
    """ BoxPlotDrawer """
    def plot(self):
        self.print_header()
        self.default_input("x")
        self.default_input("y")
        self.optional_input("hue")
        sns.boxplot(**self.arg_dict)

class CountPlotDrawer(PlotDrawer):
    """ CountPlotDrawer """
    def plot(self):
        self.print_header()
        self.default_input("x")
        self.optional_input("hue")
        self.remove_item("y")
        sns.countplot(**self.arg_dict)

class JointPlotDrawer(PlotDrawer):
    """ JointPlotDrawer """
    def plot(self):
        self.print_header()
        self.default_input("x")
        self.default_input("y")
        self.remove_item("hue")
        sns.jointplot(**self.arg_dict)

class PairPlotDrawer(PlotDrawer):
    """ PairPlotDrawer """
    def plot(self):
        self.optional_input("hue")
        self.remove_item("x")
        self.remove_item("y")
        sns.pairplot(**self.arg_dict)
