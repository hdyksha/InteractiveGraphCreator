* You can run the python script without any arguments and can interactively select required parameters to be used for drawing graphs.
* You can also explicitly assign parameters by command line arguments (e.g. filename, plot type, x-axis, etc.)

### Use the program as a console command

```
$ python graph_manager.py -h
usage: graph_manager.py [-h] [-f FILE] [-o OUTFILE] [-p PLOT] [-n] [-x X]
                        [-y Y] [-xl XLABEL] [-yl YLABEL] [-t TITLE] [-u [HUE]]
                        [-c [CONTEXT]] [-s [STYLE]] [-P [PALETTE]]

This script interactively creates a graph using seaborn

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  specify a csv file to be read
  -o OUTFILE, --outfile OUTFILE
                        specify a filename of an output image file
  -p PLOT, --plot PLOT  specify a type of graph
  -n, --noheader        not read a header in a csv file
  -x X, --x X           specify a column for x-axis
  -y Y, --y Y           specify a column for y-axis
  -xl XLABEL, --xlabel XLABEL
                        overwrite the xlabel
  -yl YLABEL, --ylabel YLABEL
                        overwrite the ylabel
  -t TITLE, --title TITLE
                        add title to the graph
  -u [HUE], --hue [HUE]
                        use hue option when drawing a plot
  -c [CONTEXT], --context [CONTEXT]
                        set context (paper, notebook, talk, poster)
  -s [STYLE], --style [STYLE]
                        set style (darkgrid, whitegrid, ticks, etc.)
  -P [PALETTE], --palette [PALETTE]
                        set palette (deep, muted, pastel, etc.)
```
### Use the program as a module in ipython-notebook
ref: [graph_creator.ipynb](./graph_creator.ipynb)
