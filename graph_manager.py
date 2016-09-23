import sys
from argparse import ArgumentParser
import glob
from plot_drawer_factory import *

class GraphManager():
    """ GraphManager """
    def __init__(self):
        """ init """
        self.file = None
        self.plot_type = None
        self.plot_types = ['scatter',
                           'point',
                           'bar',
                           'dist',
                           'box',
                           'count',
                           'joint',
                           'pair']
        self.arg_dict = {}

    def select_file(self):
        file_lst = glob.glob('*.csv')
        if file_lst:
            return self.prompt_file_selection(file_lst)
        else:
            print("Any csv files are not found")
            raise  FileNotFoundError

    def prompt_file_selection(self, file_lst):
        print("--------------------------------------------------")
        print("please select the number of csv file")
        for i, file in enumerate(file_lst):
            print("    {}: {}".format(i, file))
        try:
            print("input(file): ", end='')
            selected_file = file_lst[int(input())]
        except IndexError:
            print("please input valid number")
            sys.exit(1)
        print("{} is selected".format(selected_file))
        return selected_file

    def manage_graph_drawer(self):
        if not self.file: self.file = self.select_file()

        pdfactory = PlotDrawerFactory()
        if not self.plot_type:
            print("--------------------------------------------------")
            print("please select the number of plot types")
            for i, plot_type in enumerate(self.plot_types):
                print("    {}: {}".format(i, plot_type))
            print("input(plot type): ", end='')
            self.plot_type = self.plot_types[int(input())]
        pdfactory.create(self.file, self.plot_type).draw(self.arg_dict)

    def parse_args(self):
        desc = "This script interactively creates a graph using seaborn"
        parser = ArgumentParser(description=desc)
        parser.add_argument("-f",
                            "--file",
                            type=str,
                            help="specify a csv file to be read")
        parser.add_argument("-o",
                            "--outfile",
                            type=str,
                            help="specify a filename of an output image file")
        parser.add_argument("-p",
                            "--plot",
                            type=str,
                            help="specify a type of graph")
        parser.add_argument("-n",
                            "--noheader",
                            action="store_true",
                            help="not read a header in a csv file")
        parser.add_argument("-x",
                            "--xaxis",
                            type=str,
                            help="specify a column for x-axis")
        parser.add_argument("-y",
                            "--yaxis",
                            type=str,
                            help="specify a column for y-axis")
        parser.add_argument("-u",
                            "--hue",
                            type=str,
                            nargs="?",
                            const="?",
                            help="use hue option when drawing a plot")
        args = parser.parse_args()
        print(vars(args))
        for k, v in vars(args).items():
            if v:
                if k == "file": self.file = args.file
                elif k == "plot": self.plot_type = args.plot
                else: self.arg_dict[k] = v

    def main(self):
        self.parse_args()
        self.manage_graph_drawer()

if __name__ == '__main__':
    gm = GraphManager()
    gm.main()
