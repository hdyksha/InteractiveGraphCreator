import os
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
        self.default_args = []
        self.optional_args = []
        self.optional_numeric_args = []
        self.post_init()

    @abstractmethod
    def post_init(self):
        """
        * This method must be implemented in a concrete class of PlotDrawer.
        * All subclasses must re-create lists which include parameters
          used in plotting function
          - self.default_args
          - self.optional_args
          - etc.
        """
        pass

    def read_csv(self, infile, noheader=False):
        """
        Read a csv file and store data as instance variables
        """
        print("reading the csv file")
        if not noheader:
            df = pd.read_csv(infile)
        else:
            df = pd.read_csv(infile, header=None)
            df.columns = [ "column"+str(x) for x in df.columns ]
        self.arg_dict["data"] = df
        self.columns = df.columns

    def draw(self, arg_dict):
        """
        Set configuration based on the arg_dict which includes params specified by
        command line args, draw a plot and save it
        """
        self.set_conf(arg_dict)
        self.plot = self.plot()
        self.set_labels()
        self.set_title()
        sns.plt.savefig(self.outfile)
        print("The plot is saved as {}".format( self.outfile))

    @abstractmethod
    def plot(self):
        """
        * This method must be implemented in a concrete class of PlotDrawer.
        * This method is called after configuration phases and
        actual plot functions should be called in this method.
        """
        pass

    def set_labels(self):
        if "x" in self.arg_dict and self.xlabel:
            sns.plt.xlabel(self.xlabel)
        if "y" in self.arg_dict and self.ylabel:
            sns.plt.ylabel(self.ylabel)

    def set_title(self):
        if self.title:
            sns.plt.title(self.title)

    def print_options(self, options, message="please select a number"):
        print("--------------------------------------------------")
        print(message)
        for i, option in enumerate(options):
            print("    {}: {}".format(i, option))

    def default_input(self, arg_dict, key):
        """
        Get input from user if params are NOT set by args OR
        if params specified by args are not valid
        """
        if key in arg_dict and arg_dict[key] in self.columns:
            self.arg_dict[key] = arg_dict[key]
        else:
            print("input({}): ".format(key), end='')
            self.arg_dict[key] = self.columns[str(input())]

    def optional_input(self, arg_dict, key):
        """
        Get input from user if params are set by args OR
        if params specified by args are not valid
        """
        if key in arg_dict:
            if arg_dict[key] in self.columns:
                self.arg_dict[key] = arg_dict[key]
            else:
                print("input({}): ".format(key), end='')
                self.arg_dict[key] = self.columns[str(input())]

    def optional_numeric_input(self, arg_dict, key):
        if key in arg_dict and isinstance(arg_dict[key], int):
            self.arg_dict[key] = arg_dict[key]
        else:
            print("input({}): ".format(key), end='')
            self.arg_dict[key] = int(input())

    def set_input(self, arg_dict):
        """
        Get input and store them to self.arg_dict[key] by iteratively calling
        XXX_input functions
        """
        msg = "please select columns(s) to be used as axis(es)"
        self.print_options(self.columns, msg)
        for key in self.default_args:
            self.default_input(arg_dict, key)
        for key in self.optional_args:
            self.optional_input(arg_dict, key)
        for key in self.optional_numeric_args:
            self.optional_numeric_input(arg_dict, key)

    def apply_option(self, func, option, options, message):
        if option in options:
            func(option)
        else:
            self.print_options(options, message)
            print("input: ", end='')
            func(options[int(input())])

    def set_context(self, context):
        contexts = ["paper", "notebook", "talk", "poster"]
        msg = "please select a context parameter"
        self.apply_option(sns.set_context, context, contexts, msg)

    def set_style(self, style):
        styles = ["darkgrid", "whitegrid", "dark", "white", "ticks"]
        msg = "please select a style parameter"
        self.apply_option(sns.set_style, style, styles, msg)

    def set_palette(self, palette):
        palettes = ["deep", "muted", "pastel", "bright", "dark", "colorblind"]
        msg = "please select a palette parameter"
        self.apply_option(sns.set_palette, palette, palettes, msg)

    def set_conf(self, arg_dict):
        """
        Set config variables based on the command line args
        """
        noheader = arg_dict["noheader"] if "noheader" in arg_dict else False
        self.read_csv(self.file, noheader)
        self.set_input(arg_dict)
        if "context" in arg_dict: self.set_context(arg_dict["context"])
        else: sns.set_context("notebook") # set default context
        if "style" in arg_dict: self.set_style(arg_dict["style"])
        else: sns.set_style("ticks") # set default style
        if "palette" in arg_dict: self.set_palette(arg_dict["palette"])
        else: sns.set_palette("colorblind") # set default style
        self.xlabel = arg_dict["xlabel"] if "xlabel" in arg_dict else None
        self.ylabel = arg_dict["ylabel"] if "ylabel" in arg_dict else None
        self.title = arg_dict["title"] if "title" in arg_dict else None
        extension = ".png"
        if os.path.exists(self.file) :
            self.outfile = arg_dict["outfile"] if "outfile" in arg_dict else self.file.replace(".csv", extension)
        else : # when the input file is a remote file
            self.outfile = arg_dict["outfile"] if "outfile" in arg_dict else self.file.split("/")[-1].replace(".csv", extension)

class ScatterPlotDrawer(PlotDrawer):
    """ ScatterPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]
#        self.optional_numeric_args = ["size"]

    def plot(self):
        return sns.lmplot(**self.arg_dict, fit_reg=False)

class PointPlotDrawer(PlotDrawer):
    """ ScatterPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        return sns.pointplot(**self.arg_dict)

class BarPlotDrawer(PlotDrawer):
    """ BarPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        return sns.barplot(**self.arg_dict)

class DistPlotDrawer(PlotDrawer):
    """ DistPlotDrawer """
    def post_init(self):
        self.default_args = ["x"]

    def plot(self):
        return sns.distplot(self.arg_dict["data"][self.arg_dict["x"]])

class BoxPlotDrawer(PlotDrawer):
    """ BoxPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        return sns.boxplot(**self.arg_dict)

class CountPlotDrawer(PlotDrawer):
    """ CountPlotDrawer """
    def post_init(self):
        self.default_args = ["x"]
        self.optional_args = ["hue"]

    def plot(self):
        return sns.countplot(**self.arg_dict)

class JointPlotDrawer(PlotDrawer):
    """ JointPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]

    def plot(self):
        return sns.jointplot(**self.arg_dict)

    def set_labels(self):
        xlabel = self.xlabel if self.xlabel else self.arg_dict["x"]
        ylabel = self.ylabel if self.ylabel else self.arg_dict["y"]
        self.plot.set_axis_labels(xlabel, ylabel)

class StripPlotDrawer(PlotDrawer):
    """ JointPlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        return sns.stripplot(**self.arg_dict)

class PairPlotDrawer(PlotDrawer):
    """ PairPlotDrawer """
    def post_init(self):
        self.optional_args = ["hue"]

    def plot(self):
        return sns.pairplot(**self.arg_dict)

class PercentilePlotDrawer(PlotDrawer):
    """ PercentilePlotDrawer """
    def post_init(self):
        self.default_args = ["x", "y"]
        self.optional_args = ["hue"]

    def plot(self):
        plot = sns.lmplot(**self.arg_dict, fit_reg=False)
        xmin = self.arg_dict["data"][self.arg_dict["x"]].min()
        xmax = self.arg_dict["data"][self.arg_dict["x"]].max()
        # http://xkcd.com/color/rgb/
        color = sns.xkcd_rgb["cool grey"]
        p = .99
        percentile = self.arg_dict["data"][self.arg_dict["y"]].quantile(p)
        sns.plt.plot([xmin, xmax], [percentile, percentile], color, linestyle="dashed")
        sns.plt.text(xmin, percentile,
                     '{0}%ile = {1:.2f}'.format(int(p*100), percentile),
                     horizontalalignment="left",
                     verticalalignment="bottom")
        return plot
