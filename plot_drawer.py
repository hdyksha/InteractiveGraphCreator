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

    def read_csv(self):
        """
        Read the csv file (self.file) and store data as instance variables
        """
        print("reading the csv file")
        if not self.noheader:
            self.df = pd.read_csv(self.file)
        else:
            self.df = pd.read_csv(self.file, header=None)
            self.df.columns = [ "column"+str(x) for x in self.df.columns ]
        self.arg_dict["data"] = self.df
        self.columns = self.df.columns

    def draw(self, arg_dict):
        """
        Set configuration based on the arg_dict which includes params specified by
        command line args, draw a plot and save it
        """
        self.set_conf(arg_dict)
        self.read_csv()
        self.set_input(arg_dict)
        self.set_context()
        self.set_style()
        self.set_palette()
#        print(self.arg_dict)
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

    def print_header(self):
        print("--------------------------------------------------")
        print("please select column(s) to be used as axises")
        for i, column in enumerate(self.columns):
            print("    {}: {}".format(i, column))

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
        self.print_header()
        for key in self.default_args:
            self.default_input(arg_dict, key)
        for key in self.optional_args:
            self.optional_input(arg_dict, key)
        for key in self.optional_numeric_args:
            self.optional_numeric_input(arg_dict, key)

    def set_context(self):
        contexts = ["paper", "notebook", "talk", "poster"]
        if self.context:
            if self.context in contexts:
                sns.set_context(self.context)
            else:
                print("--------------------------------------------------")
                print("please select a context parameter")
                for i, context in enumerate(contexts):
                    print("    {}: {}".format(i, context))
                print("input(context): ", end='')
                sns.set_context(contexts[int(input())])

    def set_style(self):
        styles = ["darkgrid", "whitegrid", "dark", "white", "ticks"]
        if self.style:
            if self.style in styles:
                sns.set_style(self.style)
            else:
                print("--------------------------------------------------")
                print("please select a style parameter")
                for i, style in enumerate(styles):
                    print("    {}: {}".format(i, style))
                print("input(style): ", end='')
                sns.set_style(styles[int(input())])
        else:
            sns.set_style("whitegrid")

    def set_palette(self):
        palettes = ["deep", "muted", "pastel", "bright", "dark", "colorblind"]
        if self.palette:
            if self.palette in palettes:
                sns.set_palette(self.palette)
            else:
                print("--------------------------------------------------")
                print("please select a palette parameter")
                for i, palette in enumerate(palettes):
                    print("    {}: {}".format(i, palette))
                print("input(palette): ", end='')
                sns.set_palette(palettes[int(input())])
        else:
            sns.set_palette("deep")

    def set_conf(self, arg_dict):
        """
        Set config variables based on the command line args
        """
        self.outfile = arg_dict["outfile"] if "outfile" in arg_dict else self.file.replace(".csv", ".eps")
        self.noheader = arg_dict["noheader"] if "noheader" in arg_dict else False
        self.xlabel = arg_dict["xlabel"] if "xlabel" in arg_dict else None
        self.ylabel = arg_dict["ylabel"] if "ylabel" in arg_dict else None
        self.title = arg_dict["title"] if "title" in arg_dict else None
        self.context = arg_dict["context"] if "context" in arg_dict else None
        self.style = arg_dict["style"] if "style" in arg_dict else None
        self.palette = arg_dict["palette"] if "palette" in arg_dict else None

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
        return sns.distplot(self.df[self.arg_dict["x"]])

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
        xmin = self.df[self.arg_dict["x"]].min()
        xmax = self.df[self.arg_dict["x"]].max()
        # http://xkcd.com/color/rgb/
        color = sns.xkcd_rgb["cool grey"]
        p = .99
        percentile = self.df[self.arg_dict["y"]].quantile(p)
        sns.plt.plot([xmin, xmax], [percentile, percentile], color)
        sns.plt.text(xmin, percentile,
                     '{0}%ile = {1:.2f}'.format(int(p*100), percentile),
                     horizontalalignment="left",
                     verticalalignment="bottom")
        return plot
