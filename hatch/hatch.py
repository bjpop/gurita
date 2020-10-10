'''
Module      : Main
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX


Plot tabular data in a variety of ways from input CSV/TSV files
'''

from argparse import ArgumentParser
import sys
import logging
import pkg_resources
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import sklearn.decomposition as sk_decomp 
from sklearn.impute import SimpleImputer
import itertools as iter


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
PROGRAM_NAME = "hatch"

DEFAULT_ALPHA = 0.5
DEFAULT_LINEWIDTH = 0
DEFAULT_FILETYPE = 'CSV'
DEFAULT_BINS = 100
DEFAULT_PCA_MISSING = 'drop'
ALLOWED_FILETYPES = ['CSV', 'TSV']
DEFAULT_DIST_PLOT_TYPE = 'box'
ALLOWED_DISTPLOT_TYPES = ['box', 'violin', 'boxen', 'swarm', 'strip']
DEFAULT_PLOT_WIDTH = 10
DEFAULT_PLOT_HEIGHT = 8
DEFAULT_PLOT_NAME = "plot"
DEFAULT_ORIENTATION = "v"

try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)



def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    description = 'Generate plots of tabular data'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s ' + PROGRAM_VERSION)

    subparsers = parser.add_subparsers(title='Plot type', help='sub-command help', dest='cmd')  

    common_arguments = ArgumentParser()
    common_arguments.add_argument(
        '--outdir',  metavar='DIR', type=str,
        required=False,
        help=f'Name of optional output directory.')
    common_arguments.add_argument(
        '--filetype',  metavar='FILETYPE', type=str,
        required=False, choices=ALLOWED_FILETYPES,
        help=f'Type of input file. Allowed values: %(choices)s. Otherwise inferred from filename extension.')
    common_arguments.add_argument(
        '--prefix',  metavar='NAME', type=str,
        required=False, 
        help=f'Name prefix for output files')
    common_arguments.add_argument(
        '--logfile',
        metavar='LOG_FILE',
        type=str,
        help='record program progress in LOG_FILE')
    common_arguments.add_argument(
        '--info', '-i', action='store_true',
        default=False,
        help=f'Print summary information about the data set')
    common_arguments.add_argument(
        '--verbose', action='store_true',
        default=False,
        help=f'Print information about the progress of the program')
    common_arguments.add_argument(
        '--save', '-s', metavar='FILEPATH', required=False, type=str, 
        help=f'Save the data set to a CSV file after running filter and eval commands')
    common_arguments.add_argument(
        '--nolegend', action='store_true',
        default=False,
        help=f'Turn off the legend in the plot')
    common_arguments.add_argument(
        '--filter', metavar='EXPR', required=False, type=str,
        help='Filter rows: only retain rows that make this expression True')
    common_arguments.add_argument(
        '--eval', metavar='EXPR', required=False, type=str, nargs="+",
        help='Construct new columns based on an expression')
    common_arguments.add_argument(
        '--navalues', metavar='STR', required=False, type=str,
        help='Treat values in this space separated list as NA values. Example: --navalues ". - !"')
    common_arguments.add_argument(
        '--title', metavar='STR', required=False, type=str,
        help='Plot title. By default no title will be added.')
    common_arguments.add_argument(
        '--width', metavar='SIZE', required=False, type=float,
        default=DEFAULT_PLOT_WIDTH,
        help=f'Plot width in inches. Default: %(default)s')
    common_arguments.add_argument(
        '--height', metavar='SIZE', required=False, type=float,
        default=DEFAULT_PLOT_HEIGHT,
        help=f'Plot height in inches. Default: %(default)s')
    common_arguments.add_argument(
        '--xlabel', metavar='STR', required=False, type=str,
        help=f'Label for horizontal (X) axis')
    common_arguments.add_argument(
        '--ylabel', metavar='STR', required=False, type=str,
        help=f'Label for vertical (Y) axis')
    common_arguments.add_argument(
        '--noxticklabels', action='store_true',
        help=f'Turn of horizontal (X) axis tick labels')
    common_arguments.add_argument(
        '--noyticklabels', action='store_true',
        help=f'Turn of veritcal (Y) axis tick labels')
    #common_arguments.add_argument(
    #    '--category', metavar='STR', required=False, type=str, nargs="+",
    #    help=f'Force the interpretation of the listed columns as categorical types')
    common_arguments.add_argument(
        'data',  metavar='DATA', type=str, nargs='?', help='Filepaths of input CSV/TSV file')

    xy_arguments = ArgumentParser(add_help=False)
    xy_arguments.add_argument(
        '--xy',  metavar='X,Y', nargs="+", required=True, type=str,
        help=f'Pairs of features to plot, format: name1,name2')

    columns_arguments = ArgumentParser(add_help=False)
    columns_arguments.add_argument(
        '--cols', '-c', metavar='FEATURE', nargs="+", required=True, type=str,
        help=f'Columns to plot')

    x_arguments = ArgumentParser(add_help=False)
    x_arguments.add_argument(
        '-x', '--xaxis', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Feature to plot along the X axis')

    y_arguments = ArgumentParser(add_help=False)
    y_arguments.add_argument(
        '-y', '--yaxis', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Feature to plot along the Y axis')

    hue_arguments = ArgumentParser(add_help=False)
    hue_arguments.add_argument(
        '--hue',  metavar='FEATURE', nargs="+", type=str, required=False, 
        help=f'Name of feature (column heading) to use for colouring the plotted data')

    row_arguments = ArgumentParser(add_help=False)
    row_arguments.add_argument(
        '--row', '-r',  metavar='FEATURE', nargs="+", type=str, required=False, 
        help=f'Name of feature (column heading) to use for facet rows')

    col_arguments = ArgumentParser(add_help=False)
    col_arguments.add_argument(
        '--col', '-c',  metavar='FEATURE', nargs="+", type=str, required=False, 
        help=f'Name of feature (column heading) to use for facet columns')

    order_arguments = ArgumentParser(add_help=False)
    order_arguments.add_argument(
        '--order', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Order to display categorical values')

    hue_order_arguments = ArgumentParser(add_help=False)
    hue_order_arguments.add_argument(
        '--hueorder', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Order to display categorical values selected for hue')

    orient_arguments = ArgumentParser(add_help=False)
    orient_arguments.add_argument(
        '--orient', choices=['v', 'h'], required=False, default=DEFAULT_ORIENTATION,
        help=f'Orientation of plot. Allowed values: %(choices)s. Default: %(default)s.')

    logx_arguments = ArgumentParser(add_help=False)
    logx_arguments.add_argument(
        '--logx', action='store_true',
        help=f'Use a log scale on the horizontal (X) axis')

    logy_arguments = ArgumentParser(add_help=False)
    logy_arguments.add_argument(
        '--logy', action='store_true',
        help=f'Use a log scale on the veritical (Y) axis')

    xlim_arguments = ArgumentParser(add_help=False)
    xlim_arguments.add_argument(
        '--xlim',  metavar='LOW HIGH', nargs=2, required=False, type=float,
        help=f'Limit horizontal axis range to [LOW,HIGH]')

    ylim_arguments = ArgumentParser(add_help=False)
    ylim_arguments.add_argument(
        '--ylim',  metavar='LOW HIGH', nargs=2, required=False, type=float,
        help=f'Limit vertical axis range to [LOW,HIGH]')


    dotsize_arguments = ArgumentParser(add_help=False)
    dotsize_arguments.add_argument(
        '--dotsize',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to use for plotted point size')

    dotalpha_arguments = ArgumentParser(add_help=False)
    dotalpha_arguments.add_argument(
        '--dotalpha',  metavar='ALPHA', type=float, default=DEFAULT_ALPHA,
        help=f'Alpha value for plotted points. Default: %(default)s')

    dotlinewidth_arguments = ArgumentParser(add_help=False)
    dotlinewidth_arguments.add_argument(
        '--dotlinewidth',  metavar='WIDTH', type=int, default=DEFAULT_LINEWIDTH,
        help=f'Line width value for plotted points. Default: %(default)s')

    pcaparser = subparsers.add_parser('pca', help='Principal components analysis', parents=[common_arguments, columns_arguments, xlim_arguments, ylim_arguments, hue_arguments, dotsize_arguments, dotalpha_arguments, dotlinewidth_arguments], add_help=False) 
    pcaparser.add_argument(
        '--missing',  metavar='STRATEGY', required=False, default=DEFAULT_PCA_MISSING, choices=['drop', 'imputemean', 'imputemedian', 'imputemostfrequent'],
        help=f'How to deal with rows that contain missing data. Allowed values: %(choices)s. Default: %(default)s.')

    scatterparser = subparsers.add_parser('scatter', help='Scatter plots of numerical data', parents=[common_arguments, xy_arguments, logx_arguments, logy_arguments, xlim_arguments, ylim_arguments, hue_arguments, dotsize_arguments, dotalpha_arguments, dotlinewidth_arguments], add_help=False) 

    histparser = subparsers.add_parser('hist', help='Histograms of numerical data', parents=[common_arguments, columns_arguments, logy_arguments, xlim_arguments, ylim_arguments], add_help=False) 
    histparser.add_argument(
        '--bins',  metavar='NUMBINS', required=False, default=DEFAULT_BINS, type=int,
        help=f'Number of bins for histogram. Default: %(default)s')
    histparser.add_argument(
        '--cumulative', action='store_true',
        help=f'Generate cumulative histogram')

    noplot_parser = subparsers.add_parser('noplot', help="Do not generate a plot, but run filter and eval commands", parents=[common_arguments], add_help=False)

    def make_catplot_parser(kind, help):
        return subparsers.add_parser(kind, help=help, 
                parents=[common_arguments, y_arguments, x_arguments, hue_arguments, row_arguments, col_arguments, order_arguments, hue_order_arguments, orient_arguments, logx_arguments, logy_arguments, xlim_arguments, ylim_arguments], add_help=False) 


    boxparser = make_catplot_parser('box', help='Box plot of numerical column, optionally grouped by categorical columns')
    violinparser = make_catplot_parser('violin', help='Violin plot of numerical column, optionally grouped by categorical columns')
    swarmparser = make_catplot_parser('swarm', help='Swarm plot of numerical column, optionally grouped by categorical columns')
    stripparser = make_catplot_parser('strip', help='Strip plot of numerical column, optionally grouped by categorical columns')
    boxenparser = make_catplot_parser('boxen', help='Boxen plot of numerical column, optionally grouped by categorical columns')

    lineparser = subparsers.add_parser('line', help='Line plots of numerical data', parents=[common_arguments, xy_arguments, logy_arguments, xlim_arguments, ylim_arguments], add_help=False) 
    lineparser.add_argument(
        '--overlay', action='store_true', 
        help=f'Overlay line plots on the same axes, otherwise make a separate plot for each')
    lineparser.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to group data for line plot')

    countparser = make_catplot_parser('count', help='Count plot of categorical column')
    barparser = make_catplot_parser('bar', help='Bar plot of categorical column')
    pointparser = make_catplot_parser('point', help='Point plot of numerical column, optionally grouped by categorical columns')

    '''
    countparser = subparsers.add_parser('count', help='Counts (bar plots) of categorical data', parents=[common_arguments, columns_arguments, logy_arguments], add_help=False) 
    countparser.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to group data for count plot')
    countparser.add_argument(
        '--sorted',  action='store_true', 
        help=f'Display horizontal (X) axis values in sorted order of count')
    '''

    heatmapparser = subparsers.add_parser('heatmap', help='Heatmap of two categories with numerical values', parents=[common_arguments], add_help=False) 
    heatmapparser.add_argument(
        '--cmap',  metavar='COLOR_MAP_NAME', type=str, 
        help=f'Use this color map, will use Seaborn default if not specified')
    heatmapparser.add_argument(
        '--rows',  metavar='FEATURE', type=str, required=True,
        help=f'Interpret this feature (column of data) as the row labels of the heatmap')
    heatmapparser.add_argument(
        '--cols',  '-c', nargs='+', metavar='FEATURE', type=str, required=True,
        help=f'Interpret these features (columns of data) as the columns of the heatmap')
    #heatmapparser.add_argument(
    #    '--values',  metavar='FEATURE', type=str, required=True,
    #    help=f'Interpret this feature (column of data) as the values of the heatmap')
    heatmapparser.add_argument(
        '--log', action='store_true',
        help=f'Use a log scale on the numerical data')

    return parser.parse_args()


def init_logging(log_filename):
    '''If the log_filename is defined, then
    initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: either None, if logging is not required, or the
            string name of the log file to write to
    Result:
        None
    '''
    if log_filename is not None:
        logging.basicConfig(filename=log_filename,
                            level=logging.DEBUG,
                            filemode='w',
                            format='%(asctime)s %(levelname)s - %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S')
        logging.info('program started')
        logging.info('command line: %s', ' '.join(sys.argv))


def read_data(options):
    if options.navalues:
        na_values = options.navalues.split()
    else:
        na_values = None

    if options.data is not None:
        input_file = options.data
        maybe_filetype = get_filetype_from_extension(input_file)
        if options.filetype == 'TSV':
            sep = "\t"
        elif options.filetype == 'CSV':
            sep = ','
        elif maybe_filetype == 'TSV':
            sep = "\t"
        elif maybe_filetype == 'CSV':
            sep = ","
        else: 
            exit_with_error(f'Cannot deduce input file type: {input_file}. Either rename file or use the --filetype flag', EXIT_FILE_IO_ERROR)
    else:
        input_file = sys.stdin
        sep = ","
        if options.filetype == "TSV":
           sep = "\t"
    try:
        dtype = None
        #if options.category:
        #   dtype = { column : 'category' for column in options.category }
        data = pd.read_csv(input_file, sep=sep, keep_default_na=True, na_values=na_values, dtype=dtype)
    except IOError:
        exit_with_error(f"Could not open file: {options.data}", EXIT_FILE_IO_ERROR)
    if options.eval:
        try:
            eval_str = '\n'.join(options.eval)
            data = data.eval(eval_str)
        except:
            exit_with_error(f"Bad eval expression: {options.eval}", EXIT_COMMAND_LINE_ERROR)
    if options.filter:
        try:
            data = data.query(options.filter)
        except:
            exit_with_error(f"Bad filter expression: {options.filter}", EXIT_COMMAND_LINE_ERROR)
    return data 


def get_filetype_from_extension(filename):
    path = Path(filename)
    if path.suffix.upper() == '.TSV':
        return 'TSV'
    elif path.suffix.upper() == '.CSV':
        return 'CSV'
    else:
        return None

def get_output_name(options):
    if options.prefix:
        return options.prefix
    elif options.data is not None:
        return Path(options.data).stem
    else:
        return DEFAULT_PLOT_NAME 
        

class Plot:
    def __init__(self, options, df):
        self.options = options
        self.df = df
        self.fig = None
        self.ax = None

    # Make a plot, parameterised by plot_command which does specific actions for
    # the particular kind of plot being performed
    def plot(self):
        options = self.options
        plt.clf()
        #plt.suptitle('')
        #self.fig, self.ax = plt.subplots(figsize=(options.width, options.height))
        self.render_data()
        if hasattr(options, 'title') and options.title is not None:
            plt.title(options.title)
        '''
        if hasattr(options, 'xlabel') and options.xlabel is not None:
            self.ax.set(xlabel=options.xlabel)
        if hasattr(options, 'ylabel') and options.ylabel is not None:
            self.ax.set(ylabel=options.ylabel)
        '''
        if hasattr(options, 'xlim') and options.xlim is not None:
            xlow, xhigh = options.xlim
            plt.xlim(xlow, xhigh)
        if hasattr(options, 'ylim') and options.ylim is not None:
            ylow, yhigh = options.ylim
            plt.ylim(ylow, yhigh)
        '''
        if hasattr(options, 'noxticklabels') and options.noxticklabels:
            self.ax.set(xticks=[])
            self.ax.set(xticklabels=[])
        if hasattr(options, 'noyticklabels') and options.noyticklabels:
            self.ax.set(yticks=[])
            self.ax.set(yticklabels=[])
        '''
        plt.tight_layout()
        output_filename = self.make_output_filename()
        plt.savefig(output_filename)
        plt.close()
        if self.options.verbose:
            print(f"Graph written to {output_filename}")

    def render_data(self):
        raise NotImplementedError

    def make_output_filename(self):
        raise NotImplementedError


class Histogram(Plot):
    def __init__(self, options, df, column):
        super().__init__(options, df)
        self.column = column
    
    def render_data(self):
        sns.distplot(self.df[self.column], hist_kws={'cumulative': self.options.cumulative}, kde=False, bins=self.options.bins) 
        self.ax.set(xlabel=self.column, ylabel='count')

    def make_output_filename(self):
        output_name = get_output_name(self.options)
        return Path('.'.join([output_name, self.column.replace(' ', '_'), 'histogram.png']))

def output_field(field):
    return [field.replace(' ', '_')] if field is not None else []

# Cat plots call the catlplot interface in Seaborn, and thus share common
# functionality https://seaborn.pydata.org/tutorial/categorical.html
class Catplot(Plot):
    def __init__(self, kind, options, df, y, x, hue, row, col):
        super().__init__(options, df)
        self.yaxis = y
        self.xaxis = x
        self.row = row
        self.col = col
        self.hue = hue
        self.kind = kind

    def render_data(self):
        aspect = 1
        if self.options.width > 0:
            aspect = self.options.width / self.options.height
        row_field = None
        col_field = None
        graph = sns.catplot(kind=self.kind, data=self.df, x=self.xaxis, y=self.yaxis, col=self.col, row=self.row, height=self.options.height, aspect=aspect, hue=self.hue, legend=False, order=self.options.order, hue_order=self.options.hueorder, orient=self.options.orient)
        # legend_out parameter does not appear to work well with tight_layout, so
        # we adjust the legend manually
        if self.options.logx:
            graph.set(xscale="log")
        if self.options.logy:
            graph.set(yscale="log")
        if (not self.options.nolegend) and self.options.hue is not None:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        if self.options.orient == 'v':
            graph.set_xticklabels(rotation=90)

    def make_output_filename(self):
        output_name = [get_output_name(self.options)]
        y_str = output_field(self.yaxis)
        x_str = output_field(self.xaxis)
        hue_str = output_field(self.hue)
        row_str = output_field(self.row)
        col_str = output_field(self.col)
        type_str = [self.kind]
        return Path('.'.join(output_name + y_str + x_str + hue_str + row_str + col_str + type_str) + '.png')

class Line(Plot):
    def __init__(self, options, df, feature1, feature2):
        super().__init__(options, df)
        self.feature1 = feature1
        self.feature2 = feature2

    def render_data(self):
        sns.lineplot(data=self.df, x=self.feature1, y=self.feature2, hue=self.options.hue) 
        self.ax.set(xlabel=self.feature1, ylabel=self.feature2)

    def make_output_filename(self):
        feature1_str = self.feature1.replace(' ', '_')
        feature2_str = self.feature2.replace(' ', '_')
        output_name = get_output_name(self.options)
        return Path('.'.join([output_name, feature1_str, feature2_str, 'line.png'])) 

           
class Scatter(Plot):
    def __init__(self, options, df, feature1, feature2):
        super().__init__(options, df)
        self.feature1 = feature1
        self.feature2 = feature2

    def render_data(self):
        graph=sns.scatterplot(data=self.df, x=self.feature1, y=self.feature2, hue=self.options.hue,
                          alpha=self.options.dotalpha, size=self.options.dotsize, linewidth=self.options.dotlinewidth)
        self.ax.set(xlabel=self.feature1, ylabel=self.feature2)
        if self.options.hue is not None:
            graph.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        if self.options.nolegend:
            graph.legend_.remove()

    def make_output_filename(self):
        feature1_str = self.feature1.replace(' ', '_')
        feature2_str = self.feature2.replace(' ', '_')
        output_name = get_output_name(self.options)
        return Path('.'.join([output_name, feature1_str, feature2_str, 'scatter.png'])) 


class PCA(Plot):
    def __init__(self, options, df):
        super().__init__(options, df)

    def render_data(self):
        column_names = self.options.cols
        # Build a dataframe with the columns that we are interested in
        selected_columns = self.df[column_names]
        # Handle rows in the data that have missing values
        if self.options.missing == 'drop':
            selected_columns = selected_columns.dropna()
        elif self.options.missing == 'imputemean':
            imputer = SimpleImputer(strategy='mean')
            selected_columns = imputer.fit_transform(selected_columns)
        elif self.options.missing == 'imputemedian':
            imputer = SimpleImputer(strategy='median')
            selected_columns = imputer.fit_transform(selected_columns)
        elif self.options.missing == 'imputemostfrequent':
            imputer = SimpleImputer(strategy='most_frequent')
            selected_columns = imputer.fit_transform(selected_columns)
        # Standardize features by removing the mean and scaling to unit variance 
        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(selected_columns)
        # Perform PCA on the standardized data
        pca = sk_decomp.PCA(n_components=2)
        pca_transform = pca.fit_transform(standardized_data)
        # Build a new dataframe for the PCA transformed data, adding columnd headings for the 2 components
        first_two_components = pd.DataFrame(data = pca_transform, columns = ['principal component 1', 'principal component 2'])
        # Optionally select a column to use for colouring the dots in the plot
        if self.options.hue is not None:
            hue_column = self.df[self.options.hue]
            first_two_components = first_two_components.join(hue_column)
        # Generate a scatter plot for the PCA transformed data
        graph=sns.scatterplot(data=first_two_components, x='principal component 1', y='principal component 2', hue=self.options.hue,
                          alpha=self.options.dotalpha, size=self.options.dotsize, linewidth=self.options.dotlinewidth)
        self.ax.set(xlabel='principal component 1', ylabel='principal component 2')
        if self.options.hue is not None:
            graph.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        if self.options.nolegend:
            graph.legend_.remove()

    def make_output_filename(self):
        output_name = get_output_name(self.options)
        return Path('.'.join([output_name, 'pca.png'])) 


class Heatmap(Plot):
    def __init__(self, options, df):
        super().__init__(options, df)

    def render_data(self):
        self.df.set_index(self.options.rows, inplace=True)
        column_names = self.options.cols
        # Build a dataframe with the columns that we are interested in
        selected_columns = self.df[column_names]
        sns.heatmap(data=selected_columns, cmap=self.options.cmap)
        #sns.clustermap(data=pivot_data, cmap=self.options.cmap)

    def make_output_filename(self):
        output_name = get_output_name(self.options)
        return Path('.'.join([output_name, 'heatmap.png'])) 


class Count(Plot):
    def __init__(self, options, df, column):
        super().__init__(options, df)
        self.column = column

    def render_data(self):
        if self.options.sorted:
            order_index = self.df[self.column].value_counts().index
        else:
            order_index = None
        sns.countplot(data=self.df, x=self.column, hue=self.options.hue, order=order_index) 
        self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=90)
        self.ax.set(xlabel=self.column)

    def make_output_filename(self):
        output_name = get_output_name(self.options)
        column_str = self.column.replace(' ', '_')
        hue_str = ''
        if self.options.hue:
            hue_str = self.options.hue.replace(' ', '_')
            filename = Path('.'.join([output_name, column_str, hue_str, 'count', 'png']))
        else:
            filename = Path('.'.join([output_name, column_str, 'count', 'png']))
        return filename


def make_output_directories(options):
    pass


def plot_by_xy(options, df, plotter):
    for pair in options.xy:
        pair_fields = pair.split(",") 
        if len(pair_fields) == 2:
            feature1, feature2 = pair_fields
            if feature1 in df.columns and feature2 in df.columns:
                plotter(options, df, feature1, feature2).plot() 
            else:
                logging.warn(f"One or both of the columns {feature1} and {feature2} does not exist in data, skipping")
        else:
            logging.warn(f"Badly formed feature pair: {pair}, must be feature1,feature2 (comma separated, no spaces) ")


def plot_heatmap(options, df):
    Heatmap(options, df).plot()


def plot_catplot(options, plot_type, df):
    # XXX check numerical and categorical columns have the right type
    y_fields = options.yaxis if options.yaxis is not None else [None]
    x_fields = options.xaxis if options.xaxis is not None else [None]
    hue_fields = options.hue if options.hue is not None else [None]
    row_fields  = options.row if options.row is not None else [None]
    col_fields  = options.col if options.col is not None else [None]
    args = iter.product(y_fields, x_fields, hue_fields, row_fields, col_fields)
    for (y, x, hue, row, col) in args:
        if y is not None and y not in df.columns:
            logging.warn(f"{y} is not a column heading, skipping")
            continue
        if x is not None and x not in df.columns:
            logging.warn(f"{x} is not a column heading, skipping")
            continue
        if hue is not None and hue not in df.columns:
            logging.warn(f"{hue} is not a column heading, skipping")
            continue
        if row is not None and row not in df.columns:
            logging.warn(f"{row} is not a column heading, skipping")
            continue
        if col is not None and col not in df.columns:
            logging.warn(f"{col} is not a column heading, skipping")
            continue
        Catplot(plot_type, options, df, y, x, hue, row, col).plot()


def plot_by_column(options, df, plotter):
    for column in options.cols:
        if column in df.columns:
            plotter(options, df, column).plot()
        else:
            logging.warn(f"Column: {column} does not exist in data, skipping")


def display_info(df):
    pd.set_option('display.max_columns', None)
    print(df.describe(include='all'))
    rows, cols = df.shape 
    print(f"rows: {rows}, cols: {cols}")

def save(options, df):
    df.to_csv(options.save, header=True, index=False)
    if options.verbose:
        print(f"Data written to {options.save}")

def main():
    options = parse_args()
    init_logging(options.logfile)
    make_output_directories(options)
    df = read_data(options)
    if options.info:
        display_info(df)
    if options.save:
        save(options, df)
    if options.cmd == 'hist':
        plot_by_column(options, df, Histogram)
    if options.cmd in ['box', 'violin', 'swarm', 'strip', 'boxen', 'count', 'bar', 'point']:
        plot_catplot(options, options.cmd, df)
    elif options.cmd == 'scatter':
        plot_by_xy(options, df, Scatter)
    elif options.cmd == 'line':
        plot_by_xy(options, df, Line)
    elif options.cmd == 'heatmap':
        Heatmap(options, df).plot()
    elif options.cmd == 'pca':
        PCA(options, df).plot()
    elif options.cmd == 'noplot':
        pass
    else:
        logging.error(f"Unrecognised plot type: {options.cmd}")
    logging.info("Completed")


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
