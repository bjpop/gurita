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
import math


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
PROGRAM_NAME = "hatch"

DEFAULT_ALPHA = 0.5
DEFAULT_LINEWIDTH = 0
DEFAULT_FILETYPE = 'CSV'
DEFAULT_PCA_MISSING = 'drop'
ALLOWED_FILETYPES = ['CSV', 'TSV']
ALLOWED_PLOT_FORMATS = ['png', 'jpg', 'pdf', 'svg']
DEFAULT_PLOT_WIDTH = 8 
DEFAULT_PLOT_HEIGHT = 8 
DEFAULT_PLOT_NAME = "plot"
DEFAULT_ORIENTATION = "v"
DEFAULT_STYLE = "darkgrid"
DEFAULT_CONTEXT = "notebook"
DEFAULT_CORR_METHOD = "pearson"
DEFAULT_PLOT_FORMAT = plt.rcParams["savefig.format"] 

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

    subparsers = parser.add_subparsers(title='Sub command', help='sub-command help', dest='cmd')  

    common_arguments = ArgumentParser()
    common_arguments_group = common_arguments.add_argument_group('common arguments', 'arguments that are provided across all hatch sub-commands') 
    common_arguments_group.add_argument(
        '-o', '--out', metavar='FILE', type=str,
        required=False,
        help=f'Use this filename when saving the plot (override the default output filename)')
    #common_arguments_group.add_argument(
    #    '--outdir',  metavar='DIR', type=str,
    #    required=False,
    #    help=f'Name of optional output directory.')
    common_arguments_group.add_argument(
        '--format',  type=str,
        choices=ALLOWED_PLOT_FORMATS, default=DEFAULT_PLOT_FORMAT,
        help=f'Graphic file format to use for saved plots. Allowed values: %(choices)s. Default: %(default)s.')
    common_arguments_group.add_argument(
        '--filetype',  type=str,
        required=False, choices=ALLOWED_FILETYPES,
        help=f'Type of input file. Allowed values: %(choices)s. Otherwise inferred from filename extension.')
    common_arguments_group.add_argument(
        '--prefix',  metavar='NAME', type=str,
        required=False, 
        help=f'Name prefix for output files')
    common_arguments_group.add_argument(
        '--logfile',
        metavar='LOG_FILE',
        type=str,
        help='record program progress in LOG_FILE')
    common_arguments_group.add_argument(
        '--info', '-i', action='store_true',
        default=False,
        help=f'Print summary information about the data set')
    common_arguments_group.add_argument(
        '--show', action='store_true',
        default=False,
        help=f'Show an interactive plot window instead of saving to a file')
    common_arguments_group.add_argument(
        '--verbose', action='store_true',
        default=False,
        help=f'Print information about the progress of the program')
    common_arguments_group.add_argument(
        '--save', '-s', metavar='FILEPATH', required=False, type=str, 
        help=f'Save the data set to a CSV file after running filter and eval commands')
    common_arguments_group.add_argument(
        '--nolegend', action='store_true',
        default=False,
        help=f'Turn off the legend in the plot')
    common_arguments_group.add_argument(
        '--filter', metavar='EXPR', required=False, type=str,
        help='Filter rows: only retain rows that make this expression True')
    common_arguments_group.add_argument(
        '--eval', metavar='EXPR', required=False, type=str, nargs="+",
        help='Construct new data columns based on an expression')
    common_arguments_group.add_argument(
        '--sample', metavar='NUM', required=False, type=float,
        help='Sample rows from the input data, if NUM >= 1 then sample NUM rows, if 0 <= NUM < 1, then sample NUM fraction of rows')
    common_arguments_group.add_argument(
        '--style', choices=['darkgrid', 'whitegrid', 'dark', 'white', 'ticks'], required=False, default=DEFAULT_STYLE,
        help=f'Aesthetic style of plot. Allowed values: %(choices)s. Default: %(default)s.')
    common_arguments_group.add_argument(
        '--context', choices=['paper', 'notebook', 'talk', 'poster'], required=False, default=DEFAULT_CONTEXT,
        help=f'Aesthetic context of plot. Allowed values: %(choices)s. Default: %(default)s.')
    common_arguments_group.add_argument(
        '--navalues', metavar='STR', required=False, type=str,
        help='Treat values in this space separated list as NA values. Example: --navalues ". - !"')
    common_arguments_group.add_argument(
        '--title', metavar='STR', required=False, type=str,
        help='Plot title. By default no title will be added.')
    common_arguments_group.add_argument(
        '--width', metavar='SIZE', required=False, type=float,
        default=DEFAULT_PLOT_WIDTH,
        help=f'Plot width in inches. Default: %(default)s')
    common_arguments_group.add_argument(
        '--height', metavar='SIZE', required=False, type=float,
        default=DEFAULT_PLOT_HEIGHT,
        help=f'Plot height in inches. Default: %(default)s')
    common_arguments_group.add_argument(
        '--xlabel', metavar='STR', required=False, type=str,
        help=f'Label for horizontal (X) axis')
    common_arguments_group.add_argument(
        '--ylabel', metavar='STR', required=False, type=str,
        help=f'Label for vertical (Y) axis')
    common_arguments_group.add_argument(
        '--noxticklabels', action='store_true',
        help=f'Turn of horizontal (X) axis tick labels')
    common_arguments_group.add_argument(
        '--noyticklabels', action='store_true',
        help=f'Turn of veritcal (Y) axis tick labels')
    common_arguments_group.add_argument(
        '--rotxticklabels', metavar='ANGLE', required=False, type=float, 
        help=f'Rotate X axis tick labels by ANGLE')
    #common_arguments_group.add_argument(
    #    '--category', metavar='STR', required=False, type=str, nargs="+",
    #    help=f'Force the interpretation of the listed columns as categorical types')
    common_arguments_group.add_argument(
        'data',  metavar='DATA', type=str, nargs='?', help='Filepaths of input CSV/TSV file')

    features_arguments = ArgumentParser(add_help=False)
    features_arguments.add_argument(
        '--features', metavar='FEATURE', nargs="+", required=True, type=str,
        help=f'Features to use in the PCA')

    x_argument = ArgumentParser(add_help=False)
    x_argument.add_argument(
        '-x', '--xaxis', metavar='FEATURE', required=False, type=str,
        help=f'Feature to plot along the X axis')

    y_argument = ArgumentParser(add_help=False)
    y_argument.add_argument(
        '-y', '--yaxis', metavar='FEATURE', required=False, type=str,
        help=f'Feature to plot along the Y axis')

    hue_argument = ArgumentParser(add_help=False)
    hue_argument.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature to use for colouring the plotted data')

    row_argument = ArgumentParser(add_help=False)
    row_argument.add_argument(
        '-r', '--row', metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature to use for facet rows')

    col_argument = ArgumentParser(add_help=False)
    col_argument.add_argument(
        '-c', '--col', metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature to use for facet columns')

    order_arguments = ArgumentParser(add_help=False)
    order_arguments.add_argument(
        '--order', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Order to display categorical values')

    hue_order_arguments = ArgumentParser(add_help=False)
    hue_order_arguments.add_argument(
        '--hueorder', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Order to display categorical values selected for hue')

    orient_argument = ArgumentParser(add_help=False)
    orient_argument.add_argument(
        '--orient', choices=['v', 'h'], required=False, default=DEFAULT_ORIENTATION,
        help=f'Orientation of plot. Allowed values: %(choices)s. Default: %(default)s.')

    logx_argument = ArgumentParser(add_help=False)
    logx_argument.add_argument(
        '--logx', action='store_true',
        help=f'Use a log scale on the horizontal (X) axis')

    logy_argument = ArgumentParser(add_help=False)
    logy_argument.add_argument(
        '--logy', action='store_true',
        help=f'Use a log scale on the veritical (Y) axis')

    xlim_argument = ArgumentParser(add_help=False)
    xlim_argument.add_argument(
        '--xlim',  metavar='BOUND', nargs=2, required=False, type=float,
        help=f'Limit horizontal axis range to [LOW,HIGH]')

    ylim_argument = ArgumentParser(add_help=False)
    ylim_argument.add_argument(
        '--ylim',  metavar='BOUND', nargs=2, required=False, type=float,
        help=f'Limit vertical axis range to [LOW,HIGH]')

    dotsize_argument = ArgumentParser(add_help=False)
    dotsize_argument.add_argument(
        '--dotsize',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature to use for plotted point size')

    dotalpha_argument = ArgumentParser(add_help=False)
    dotalpha_argument.add_argument(
        '--dotalpha',  metavar='ALPHA', type=float, default=DEFAULT_ALPHA,
        help=f'Alpha value for plotted points. Default: %(default)s')

    dotlinewidth_argument = ArgumentParser(add_help=False)
    dotlinewidth_argument.add_argument(
        '--dotlinewidth',  metavar='WIDTH', type=int, default=DEFAULT_LINEWIDTH,
        help=f'Line width value for plotted points. Default: %(default)s')

    colwrap_argument = ArgumentParser(add_help=False)
    colwrap_argument.add_argument(
        '--colwrap',  metavar='INT', type=int, required=False, 
        help=f'Wrap the facet column at this width, to span multiple rows.')

    corrparser = subparsers.add_parser('corr', help='Correlation between two numerical features', parents=[x_argument, y_argument], add_help=False)
    corrparser.add_argument('--method', required=False, default=DEFAULT_CORR_METHOD, choices=['pearson', 'kendall', 'spearman'],
        help=f'Method for determining correlation. Allowed values: %(choices)s. Default: %(default)s.')

    pcaparser = subparsers.add_parser('pca', help='Principal components analysis', parents=[common_arguments, features_arguments, xlim_argument, ylim_argument, hue_argument, dotsize_argument, dotalpha_argument, dotlinewidth_argument], add_help=False) 
    pcaparser.add_argument(
        '--missing', required=False, default=DEFAULT_PCA_MISSING, choices=['drop', 'imputemean', 'imputemedian', 'imputemostfrequent'],
        help=f'How to deal with rows that contain missing data. Allowed values: %(choices)s. Default: %(default)s.')

    histparser = subparsers.add_parser('hist', help='Histograms of numerical data', parents=[common_arguments, x_argument, y_argument, logx_argument, logy_argument, xlim_argument, ylim_argument], add_help=False) 
    histparser.add_argument(
        '--bins',  metavar='NUM', required=False, type=int,
        help=f'Number of bins for histogram.')
    histparser.add_argument(
        '--cumulative', action='store_true',
        help=f'Generate cumulative histogram')

    noplot_parser = subparsers.add_parser('noplot', help="Do not generate a plot, but run filter and eval commands", parents=[common_arguments], add_help=False)

    def facet_parser(kind, help, additional_parents=[]):
        return subparsers.add_parser(kind, help=help, 
                parents=additional_parents + [common_arguments, y_argument, x_argument, hue_argument, row_argument, col_argument, order_arguments, hue_order_arguments, orient_argument, logx_argument, logy_argument, xlim_argument, ylim_argument, colwrap_argument], add_help=False) 


    boxparser = facet_parser('box', help='Box plot of numerical feature, optionally grouped by categorical features')
    violinparser = facet_parser('violin', help='Violin plot of numerical feature, optionally grouped by categorical features')
    swarmparser = facet_parser('swarm', help='Swarm plot of numerical feature, optionally grouped by categorical features')
    stripparser = facet_parser('strip', help='Strip plot of numerical feature, optionally grouped by categorical features')
    boxenparser = facet_parser('boxen', help='Boxen plot of numerical feature, optionally grouped by categorical features')
    countparser = facet_parser('count', help='Count plot of categorical feature')
    barparser = facet_parser('bar', help='Bar plot of categorical feature')
    pointparser = facet_parser('point', help='Point plot of numerical feature, optionally grouped by categorical features')
    scatterparser = facet_parser('scatter', help='Scatter plot of two numerical features', additional_parents=[dotsize_argument, dotalpha_argument, dotlinewidth_argument])
    lineparser = facet_parser('line', help='Line plot of numerical feature')

    heatmapparser = subparsers.add_parser('heatmap', help='Heatmap of two categories with numerical values', parents=[common_arguments, y_argument, x_argument], add_help=False) 
    heatmapparser.add_argument(
        '-v', '--val', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Interpret this feature (column of data) as the values of the heatmap')
    heatmapparser.add_argument(
        '--cmap',  metavar='COLOR_MAP_NAME', type=str, 
        help=f'Use this color map, will use Seaborn default if not specified')
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
    if options.sample is not None:
        if options.sample >= 1:
            data = data.sample(n = math.trunc(options.sample))
        elif 0 < options.sample < 1:
            data = data.sample(frac = options.sample)
        else:
            exit_with_error(f"Sample argument {options.sample} out of range. Must be > 0", EXIT_COMMAND_LINE_ERROR)
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

    def plot(self):
        options = self.options
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
        if hasattr(options, 'noxticklabels') and options.noxticklabels:
            self.ax.set(xticks=[])
            self.ax.set(xticklabels=[])
        if hasattr(options, 'noyticklabels') and options.noyticklabels:
            self.ax.set(yticks=[])
            self.ax.set(yticklabels=[])
        if hasattr(options, 'rotxticklabels') and options.rotxticklabels is not None:
            self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=options.rotxticklabels)
        if options.logy:
            self.ax.set(yscale="log")
        if options.logx:
            self.ax.set(xscale="log")
        #plt.tight_layout()
        if options.show:
            plt.show()
        else:
           output_filename = self.make_output_filename()
           plt.savefig(output_filename, bbox_inches='tight', format=self.options.format)
           if self.options.verbose:
               print(f"Graph written to {output_filename}")
        plt.close()

    def render_data(self):
        raise NotImplementedError

    def make_output_filename(self):
        raise NotImplementedError


class Histogram(Plot):
    def __init__(self, options, df):
        super().__init__(options, df)
        self.x = options.xaxis
        self.y = options.yaxis
    
    def render_data(self):
        if self.options.bins:
            sns.histplot(data=self.df, x=self.x, y=self.y, bins=self.options.bins,
                cumulative=self.options.cumulative)
        else:
            sns.histplot(data=self.df, x=self.x, y=self.y,
                cumulative=self.options.cumulative)

    def make_output_filename(self):
        if self.options.out:
            return self.options.out
        else:
            extension = self.options.format
            output_name = get_output_name(self.options)
            if self.x is not None:
                return Path('.'.join([output_name, self.x.replace(' ', '_'), 'histogram', extension]))
            elif self.y is not None:
                return Path('.'.join([output_name, self.y.replace(' ', '_'), 'histogram', extension]))


class Facetplot(object):
    def __init__(self, kind, options, df, kwargs):
        self.options = options
        self.df = df
        self.kind = kind
        self.x = options.xaxis
        self.y = options.yaxis
        self.hue = options.hue
        self.row = options.row
        self.col = options.col
        self.kwargs = kwargs

    def plot(self):
        options = self.options
        graph = self.make_graph(self.kwargs)
        if options.logx:
            graph.set(xscale="log")
        if options.logy:
            graph.set(yscale="log")
        if hasattr(options, 'title') and options.title is not None:
            plt.title(options.title)
        if hasattr(options, 'xlim') and options.xlim is not None:
            xlow, xhigh = options.xlim
            plt.xlim(xlow, xhigh)
        if hasattr(options, 'ylim') and options.ylim is not None:
            ylow, yhigh = options.ylim
            plt.ylim(ylow, yhigh)
        if hasattr(options, 'rotxticklabels') and options.rotxticklabels is not None:
            for ax in graph.axes.ravel():
                ax.set_xticklabels(ax.get_xticklabels(), rotation=options.rotxticklabels)
        if options.show:
            plt.show()
        else:
           output_filename = self.make_output_filename()
           plt.savefig(output_filename, bbox_inches='tight', format=self.options.format)
           if self.options.verbose:
               print(f"Graph written to {output_filename}")
        plt.close() 

    def make_graph(self, kwargs):
        raise NotImplementedError

    def make_output_filename(self):
        options = self.options
        if options.out:
            return options.out
        else:
            extension = [options.format]
            output_name = [get_output_name(options)]
            y_str = output_field(self.y)
            x_str = output_field(self.x)
            hue_str = output_field(self.hue)
            row_str = output_field(self.row)
            col_str = output_field(self.col)
            type_str = [self.kind]
            return Path('.'.join(output_name + y_str + x_str +
                                 hue_str + row_str + col_str +
                                 type_str + extension))

def output_field(field):
    return [field.replace(' ', '_')] if field is not None else []

# Catplots call the catlplot interface in Seaborn, and thus share common
# functionality https://seaborn.pydata.org/tutorial/categorical.html
class Catplot(Facetplot):
    def __init__(self, kind, options, df, kwargs):
        super().__init__(kind, options, df, kwargs)

    def make_graph(self, kwargs):
        options = self.options
        facet_kws = { 'legend_out': True }
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.kind, data=self.df,
                x=self.x, y=self.y, col=self.col, row=self.row,
                height=options.height, aspect=aspect, hue=self.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        return graph


# Relplots call the relplot interface in Seaborn, and thus share common
# functionality https://seaborn.pydata.org/tutorial/relational.html 
class Relplot(Facetplot):
    def __init__(self, kind, options, df, kwargs):
        super().__init__(kind, options, df, kwargs)

    def make_graph(self, kwargs):
        options = self.options
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        facet_kws = { 'legend_out': True }
        graph = sns.relplot(kind=self.kind, data=self.df,
                x=self.x, y=self.y, col=self.col, row=self.row,
                height=options.height, aspect=aspect, hue=self.hue,
                hue_order=options.hueorder, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        return graph


class PCA(Plot):
    def __init__(self, options, df):
        super().__init__(options, df)

    def render_data(self):
        feature_names = self.options.features
        # Build a dataframe with the columns that we are interested in
        selected_columns = self.df[feature_names]
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
        if self.options.out:
            return self.options.out
        else:
            extension = self.options.format
            output_name = get_output_name(self.options)
            return Path('.'.join([output_name, 'pca', extension])) 


class Heatmap(Plot):
    def __init__(self, options, df, x, y, val):
        super().__init__(options, df)
        self.x = x
        self.y = y
        self.val = val

    def render_data(self):
        pivot_data = self.df.pivot(index=self.y, columns=self.x, values=self.val)
        sns.heatmap(data=pivot_data, cmap=self.options.cmap)
        #sns.clustermap(data=pivot_data, cmap=self.options.cmap)

    def make_output_filename(self):
        options = self.options
        if options.out:
            return options.out
        else:
            extension = [options.format]
            output_name = [get_output_name(options)]
            x_str = output_field(self.x)
            y_str = output_field(self.y)
            val_str = output_field(self.val)
            type_str = ['heatmap']
            return Path('.'.join(output_name + x_str + y_str + val_str + type_str + extension))


def make_output_directories(options):
    pass


def heatmap_plot(options, df):
    y_fields = options.yaxis if options.yaxis is not None else [None]
    x_fields = options.xaxis if options.xaxis is not None else [None]
    v_fields = options.val if options.val is not None else [None]
    args = iter.product(x_fields, y_fields, v_fields)
    for (x, y, val) in args:
        if x is not None and x not in df.columns:
            logging.warn(f"{x} is not an attribute of the data set, skipping")
            continue
        if y is not None and y not in df.columns:
            logging.warn(f"{y} is not an attribute of the data set, skipping")
            continue
        if val is not None and val not in df.columns:
            logging.warn(f"{val} is not an attribute of the data set, skipping")
            continue
        Heatmap(options, df, x, y, val).plot()

#def facet_plot(options, plot_type, df, plotfun, kwargs):
#    # XXX check numerical and categorical columns have the right type
#    y_fields = options.yaxis if options.yaxis is not None else [None]
#    x_fields = options.xaxis if options.xaxis is not None else [None]
#    hue_fields = options.hue if options.hue is not None else [None]
#    row_fields  = options.row if options.row is not None else [None]
#    col_fields  = options.col if options.col is not None else [None]
#    args = iter.product(x_fields, y_fields, hue_fields, row_fields, col_fields)
#    for (x, y, hue, row, col) in args:
#        if x is not None and x not in df.columns:
#            logging.warn(f"{x} is not an attribute of the data set, skipping")
#            continue
#        if y is not None and y not in df.columns:
#            logging.warn(f"{y} is not an attribute of the data set, skipping")
#            continue
#        if hue is not None and hue not in df.columns:
#            logging.warn(f"{hue} is not an attribute of the data set, skipping")
#            continue
#        if row is not None and row not in df.columns:
#            logging.warn(f"{row} is not an attribute of the data set, skipping")
#            continue
#        if col is not None and col not in df.columns:
#            logging.warn(f"{col} is not an attribute of the data set, skipping")
#            continue
#        plotfun(plot_type, options, df, x, y, hue, row, col, kwargs).plot()

#def plot_by_x_y(options, df, plotfun):
#    if options.xaxis:
#        for x in options.xaxis:
#            if x in df.columns:
#                plotfun(options, df, x=x, y=None).plot()
#            else:
#                logging.warn(f"{x} is not an attribute of the data set, skipping")
#    if options.yaxis:
#        for y in options.yaxis:
#            if y in df.columns:
#                plotfun(options, df, x=None, y=y).plot()
#            else:
#                logging.warn(f"{y} is not an attribute of the data set, skipping")


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
    sns.set_style(options.style)
    sns.set_context(options.context)
    init_logging(options.logfile)
    make_output_directories(options)
    df = read_data(options)
    kwargs = {}
    if options.info:
        display_info(df)
    if options.save:
        save(options, df)
    if options.cmd == 'hist':
        if options.xaxis is not None and options.yaxis is not None:
            exit_with_error("You cannot use both -x (--xaxis) and -y (--yaxis) at the same time in a histogram", EXIT_COMMAND_LINE_ERROR)
        elif options.xaxis is not None:
            Histogram(options, df).plot()
        elif options.yaxis is not None:
            Histogram(options, df).plot()
        else:
            exit_with_error("A histogram requires either -x (--xaxis) or -y (--yaxis) to be specified", EXIT_COMMAND_LINE_ERROR)
    elif options.cmd == 'count':
        if options.xaxis is not None and options.yaxis is not None:
            exit_with_error("You cannot use both -x (--xaxis) and -y (--yaxis) at the same time in a count plot", EXIT_COMMAND_LINE_ERROR)
        elif options.xaxis is not None:
            Catplot(options.cmd, options, df, kwargs).plot()
        elif options.yaxis is not None:
            Catplot(options.cmd, options, df, kwargs).plot()
        else:
            exit_with_error("A count plot requires either -x (--xaxis) or -y (--yaxis) to be specified", EXIT_COMMAND_LINE_ERROR)
    elif options.cmd in ['box', 'violin', 'swarm', 'strip', 'boxen', 'bar', 'point']:
        Catplot(options.cmd, options, df, kwargs).plot()
    elif options.cmd == 'line':
        Relplot(options.cmd, options, df, kwargs).plot()
    elif options.cmd == 'scatter':
        kwargs = { 'size': options.dotsize, 'alpha': options.dotalpha, 'linewidth': options.dotlinewidth }
        Relplot(options.cmd, options, df, kwargs).plot()
    elif options.cmd == 'heatmap':
        heatmap_plot(options, df)
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
