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
DEFAULT_PLOT_WIDTH=10
DEFAULT_PLOT_HEIGHT=8
DEFAULT_PLOT_NAME="plot"

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
        '--nolegend', action='store_true',
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
    common_arguments.add_argument(
        'data',  metavar='DATA', type=str, nargs='?', help='Filepaths of input CSV/TSV file')

    xy_arguments = ArgumentParser(add_help=False)
    xy_arguments.add_argument(
        '--xy',  metavar='X,Y', nargs="+", required=True, type=str,
        help=f'Pairs of features to plot, format: name1,name2')

    columns_arguments = ArgumentParser(add_help=False)
    columns_arguments.add_argument(
        '--columns',  metavar='FEATURE', nargs="+", required=True, type=str,
        help=f'Columns to plot')

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

    hue_arguments = ArgumentParser(add_help=False)
    hue_arguments.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to use for colouring the plotted data')

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

    distparser = subparsers.add_parser('dist', help='Distributions of numerical data', parents=[common_arguments, columns_arguments, logy_arguments, ylim_arguments], add_help=False) 
    distparser.add_argument(
        '--group',  metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Plot distributions of of the columns where data are optionally grouped by these features')
    distparser.add_argument(
        '--type', choices=ALLOWED_DISTPLOT_TYPES, default=DEFAULT_DIST_PLOT_TYPE,
        help=f'Type of plot. Default: %(default)s')

    lineparser = subparsers.add_parser('line', help='Line plots of numerical data', parents=[common_arguments, xy_arguments, logy_arguments, xlim_arguments, ylim_arguments], add_help=False) 
    lineparser.add_argument(
        '--overlay', action='store_true', 
        help=f'Overlay line plots on the same axes, otherwise make a separate plot for each')
    lineparser.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to group data for line plot')

    countparser = subparsers.add_parser('count', help='Counts (bar plots) of categorical data', parents=[common_arguments, columns_arguments, logy_arguments], add_help=False) 
    countparser.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to group data for count plot')
    countparser.add_argument(
        '--sorted',  action='store_true', 
        help=f'Display horizontal (X) axis values in sorted order of count')

    heatmapparser = subparsers.add_parser('heatmap', help='Heatmap of two categories with numerical values', parents=[common_arguments], add_help=False) 
    heatmapparser.add_argument(
        '--cmap',  metavar='COLOR_MAP_NAME', type=str, 
        help=f'Use this color map, will use Seaborn default if not specified')
    heatmapparser.add_argument(
        '--rows',  metavar='FEATURE', type=str, required=True,
        help=f'Interpret this feature (column of data) as the row labels of the heatmap')
    heatmapparser.add_argument(
        '--columns',  nargs='+', metavar='FEATURE', type=str, required=True,
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
        data = pd.read_csv(input_file, sep=sep, keep_default_na=True, na_values=na_values)
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
        plt.suptitle('')
        self.fig, self.ax = plt.subplots(figsize=(options.width, options.height))
        self.render_data()
        if hasattr(options, 'title') and options.title is not None:
            plt.title(options.title)
        if hasattr(options, 'xlabel') and options.xlabel is not None:
            self.ax.set(xlabel=options.xlabel)
        if hasattr(options, 'ylabel') and options.ylabel is not None:
            self.ax.set(ylabel=options.ylabel)
        if hasattr(options, 'xlim') and options.xlim is not None:
            xlow, xhigh = options.xlim
            plt.xlim(xlow, xhigh)
        if hasattr(options, 'ylim') and options.ylim is not None:
            ylow, yhigh = options.ylim
            plt.ylim(ylow, yhigh)
        if hasattr(options, 'logx') and options.logx:
            self.ax.set(xscale="log")
        if hasattr(options, 'logy') and options.logy:
            self.ax.set(yscale="log")
        if hasattr(options, 'noxticklabels') and options.noxticklabels:
            self.ax.set(xticks=[])
            self.ax.set(xticklabels=[])
        if hasattr(options, 'noyticklabels') and options.noyticklabels:
            self.ax.set(yticks=[])
            self.ax.set(yticklabels=[])
        plt.tight_layout()
        output_filename = self.make_output_filename()
        plt.savefig(output_filename)
        plt.close()

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


class Distribution(Plot):
    def __init__(self, options, df, group, column):
        super().__init__(options, df)
        self.group = group 
        self.column = column
        self.type = options.type

    def render_data(self):
        if self.type == 'box':
            sns.boxplot(data=self.df, x=self.group, y=self.column) 
        elif self.type == 'violin':
            sns.violinplot(data=self.df, x=self.group, y=self.column) 
        elif self.type == 'boxen':
            sns.boxenplot(data=self.df, x=self.group, y=self.column) 
        elif self.type == 'strip':
            sns.stripplot(data=self.df, x=self.group, y=self.column) 
        elif self.type == 'swarm':
            sns.swarmplot(data=self.df, x=self.group, y=self.column) 
        self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=90)
        self.ax.set(xlabel=self.group, ylabel=self.column)

    def make_output_filename(self):
        output_name = get_output_name(self.options)
        column_str = self.column.replace(' ', '_')
        type_str = self.options.type
        if self.group is not None:
            group_str = self.group.replace(' ', '_')
            return Path('.'.join([output_name, column_str, group_str, type_str, 'png']))
        else:
            return Path('.'.join([output_name, column_str, type_str, 'png']))


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
        column_names = self.options.columns
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
        column_names = self.options.columns
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


def plot_distribution(options, df):
    for column in options.columns:
        if column in df.columns:
            if options.group:
                for group in options.group:
                    if group in df.columns:
                        Distribution(options, df, group, column).plot()
                    else:
                        logging.warn(f"Column: {group} does not exist in data, skipping")
            else:
                Distribution(options, df, None, column).plot() 
        else:
            logging.warn(f"Column: {column} does not exist in data, skipping")
'''
    for group in options.group:
        if group in df.columns:
            for column in options.columns:
                if column in df.columns:
                    Distribution(options, df, group, column).plot()
                else:
                    logging.warn(f"Column: {column} does not exist in data, skipping")
        else:
            logging.warn(f"Column: {group} does not exist in data, skipping")
'''


def plot_by_column(options, df, plotter):
    #df = df.dropna()
    for column in options.columns:
        if column in df.columns:
            plotter(options, df, column).plot()
        else:
            logging.warn(f"Column: {column} does not exist in data, skipping")


def main():
    options = parse_args()
    init_logging(options.logfile)
    make_output_directories(options)
    df = read_data(options)
    if options.cmd == 'hist':
        plot_by_column(options, df, Histogram)
    elif options.cmd == 'dist':
        plot_distribution(options, df)
    elif options.cmd == 'scatter':
        plot_by_xy(options, df, Scatter)
    elif options.cmd == 'line':
        plot_by_xy(options, df, Line)
    elif options.cmd == 'heatmap':
        Heatmap(options, df).plot()
    elif options.cmd == 'count':
        plot_by_column(options, df, Count)
    elif options.cmd == 'pca':
        PCA(options, df).plot()
    logging.info("Completed")


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
