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
        self.all_input_args = ["x", "y", "hue"]
        self.default_args = []
        self.optional_args = []
        self.post_init()

    @abstractmethod
    def post_init(self):
        pass

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
        self.set_input()
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

    def set_input(self):
        self.print_header()
        for key in self.default_args:
            self.default_input(key)
        for key in self.optional_args:
            self.optional_input(key)
        residual_args = list(set(self.all_input_args) - set(self.default_args) - set(self.optional_args))
        for key in residual_args:
            self.remove_item(key)

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
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        sns.lmplot(**self.arg_dict, fit_reg=False)

class PointPlotDrawer(PlotDrawer):
    """ ScatterPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        sns.pointplot(**self.arg_dict)

class BarPlotDrawer(PlotDrawer):
    """ BarPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        sns.barplot(**self.arg_dict)

class DistPlotDrawer(PlotDrawer):
    """ DistPlotDrawer """
    def post_init(self):
        self.default_args = ["x"]

    def plot(self):
        sns.distplot(self.df[self.arg_dict["x"]])

class BoxPlotDrawer(PlotDrawer):
    """ BoxPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        sns.boxplot(**self.arg_dict)

class CountPlotDrawer(PlotDrawer):
    """ CountPlotDrawer """
    def post_init(self):
        self.default_args = ["x"]
        self.optional_args = ["hue"]

    def plot(self):
        sns.countplot(**self.arg_dict)

class JointPlotDrawer(PlotDrawer):
    """ JointPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]

    def plot(self):
        sns.jointplot(**self.arg_dict)

class PairPlotDrawer(PlotDrawer):
    """ PairPlotDrawer """
    def post_init(self):
        self.optional_args = ["hue"]

    def plot(self):
        sns.pairplot(**self.arg_dict)
