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


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
PROGRAM_NAME = "hatch"

DEFAULT_ALPHA = 0.3
DEFAULT_LINEWIDTH = 0
DEFAULT_FILETYPE = 'CSV'
DEFAULT_BINS = 100
ALLOWED_FILETYPES = ['CSV', 'TSV']
DEFAULT_DIST_PLOT_TYPE = 'box'
ALLOWED_DISTPLOT_TYPES = ['box', 'violin']
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
        default=DEFAULT_FILETYPE,
        help=f'Type of input file')
    common_arguments.add_argument(
        '--name',  metavar='NAME', type=str,
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
        '--navalues', metavar='STR', required=False, type=str,
        help='Treat values in this space separated list as NA values. Example: --navalues ". - !"')
    common_arguments.add_argument(
        '--title', metavar='STR', required=False, type=str,
        help='Plot title. By default no title will be added.')
    common_arguments.add_argument(
        '--width', metavar='SIZE', required=False, type=float,
        default=DEFAULT_PLOT_WIDTH,
        help=f'Plot width in inches (default: {DEFAULT_PLOT_WIDTH})')
    common_arguments.add_argument(
        '--height', metavar='SIZE', required=False, type=float,
        default=DEFAULT_PLOT_HEIGHT,
        help=f'Plot height in inches (default: {DEFAULT_PLOT_HEIGHT})')
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
        help=f'Use a log scale on the horizontal axis')

    logy_arguments = ArgumentParser(add_help=False)
    logy_arguments.add_argument(
        '--logy', action='store_true',
        help=f'Use a log scale on the veritical axis')

    xlim_arguments = ArgumentParser(add_help=False)
    xlim_arguments.add_argument(
        '--xlim',  metavar='LOW HIGH', nargs=2, required=False, type=float,
        help=f'Limit horizontal axis range to [LOW,HIGH]')

    ylim_arguments = ArgumentParser(add_help=False)
    ylim_arguments.add_argument(
        '--ylim',  metavar='LOW HIGH', nargs=2, required=False, type=float,
        help=f'Limit vertical axis range to [LOW,HIGH]')

    histparser = subparsers.add_parser('hist', help='Histograms of numerical data', parents=[common_arguments, columns_arguments, logy_arguments, xlim_arguments, ylim_arguments], add_help=False) 
    histparser.add_argument(
        '--bins',  metavar='NUMBINS', required=False, default=DEFAULT_BINS, type=int,
        help=f'Number of bins for histogram (default={DEFAULT_BINS})')
    histparser.add_argument(
        '--cumulative', action='store_true',
        help=f'Generate cumulative histogram')

    distparser = subparsers.add_parser('dist', help='Distributions of numerical data', parents=[common_arguments, columns_arguments, logy_arguments, ylim_arguments], add_help=False) 
    distparser.add_argument(
        '--group',  metavar='FEATURE', nargs="+", required=True, type=str,
        help=f'Plot distributions of of the columns where data are grouped by these features')
    distparser.add_argument(
        '--type', choices=ALLOWED_DISTPLOT_TYPES, default=DEFAULT_DIST_PLOT_TYPE,
        help=f'Type of plot, default({DEFAULT_DIST_PLOT_TYPE})')

    scatterparser = subparsers.add_parser('scatter', help='Scatter plots of numerical data', parents=[common_arguments, xy_arguments, logx_arguments, logy_arguments, xlim_arguments, ylim_arguments], add_help=False) 
    scatterparser.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to use for colouring dots')
    scatterparser.add_argument(
        '--size',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to use for dot size')
    scatterparser.add_argument(
        '--alpha',  metavar='ALPHA', type=float, default=DEFAULT_ALPHA,
        help=f'Alpha value for plotting points (default: {DEFAULT_ALPHA})')
    scatterparser.add_argument(
        '--linewidth',  metavar='WIDTH', type=int, default=DEFAULT_LINEWIDTH,
        help=f'Line width value for plotting points (default: {DEFAULT_LINEWIDTH})')

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

    heatmapparser = subparsers.add_parser('heatmap', help='Heatmap of two categories with numerical values', parents=[common_arguments], add_help=False) 
    heatmapparser.add_argument(
        '--cmap',  metavar='COLOR_MAP_NAME', type=str, 
        help=f'Use this color map, will use Seaborn default if not specified')
    heatmapparser.add_argument(
        '--rows',  metavar='FEATURE', type=str, required=True,
        help=f'Interpret this feature (column of data) as the rows of the heatmap')
    heatmapparser.add_argument(
        '--columns',  metavar='FEATURE', type=str, required=True,
        help=f'Interpret this feature (column of data) as the columns of the heatmap')
    heatmapparser.add_argument(
        '--values',  metavar='FEATURE', type=str, required=True,
        help=f'Interpret this feature (column of data) as the values of the heatmap')
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

    sep = ","
    if options.filetype == "TSV":
       sep = "\t"
    input_file = sys.stdin
    if options.data is not None:
        input_file = options.data
    try:
        data = pd.read_csv(input_file, sep=sep, keep_default_na=True, na_values=na_values)
    except IOError:
        exit_with_error(f"Could not open file: {options.data}", EXIT_FILE_IO_ERROR)
    if options.filter:
        try:
            data = data.query(options.filter)
        except:
            exit_with_error(f"Bad filter expression: {options.filter}", EXIT_COMMAND_LINE_ERROR)
    return data 

def get_output_name(options):
    if options.name:
        return options.name
    elif options.data is not None:
        return Path(options.data).stem
    else:
        return DEFAULT_PLOT_NAME 
        

def histogram(options, df):
    for column in options.columns:
        if column in df.columns:
            plt.clf()
            plt.suptitle('')
            fig, ax = plt.subplots(figsize=(options.width,options.height))
            sns.distplot(df[column], hist_kws={'cumulative': options.cumulative}, kde=False, bins=options.bins) 
            output_name = get_output_name(options)
            filename = Path('.'.join([output_name, column.replace(' ', '_'), 'histogram.png']))
            ax.set(xlabel=column, ylabel='count')
            if options.logy:
                ax.set(yscale="log")
            if options.title:
                plt.title(options.title)
            if options.xlim:
                xlow, xhigh = options.xlim
                plt.xlim(xlow, xhigh)
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
        else:
            logging.warn(f"Column: {column} does not exist in data, skipping")


def distribution(options, df):
    for group in options.group:
        if group in df.columns:
            plot_distributions_by(options, df, group)
        else:
            logging.warn(f"Column: {group} does not exist in data, skipping")

def plot_distributions_by(options, df, group):
    for column in options.columns:
        if column in df.columns:
            plt.clf()
            plt.suptitle('')
            fig, ax = plt.subplots(figsize=(options.width,options.height))
            if options.type == 'box':
                sns.boxplot(data=df, x=group, y=column) 
            elif options.type == 'violin':
                sns.violinplot(data=df, x=group, y=column) 
            output_name = get_output_name(options)
            group_str = group.replace(' ', '_')
            column_str = column.replace(' ', '_')
            filename = Path('.'.join([output_name, column_str, group_str, 'dist', 'png']))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            ax.set(xlabel=group, ylabel=column)
            if options.logy:
                ax.set(yscale="log")
            if options.title:
                plt.title(options.title)
            if options.ylim:
                ylow, yhigh = options.ylim
                plt.ylim(ylow, yhigh)
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
        else:
            logging.warn(f"Column: {column} does not exist in data, skipping")

def line(options, df):
    for pair in options.xy:
        pair_fields = pair.split(",") 
        if len(pair_fields) == 2:
            feature1, feature2 = pair_fields
            line_plot(options, df, feature1, feature2)
        else:
            logging.warn(f"Badly formed feature pair: {pair}, must be feature1,feature2 (comma separated, no spaces) ")

def line_plot(options, df, feature1, feature2):
    plt.clf()
    plt.suptitle('')
    fig, ax = plt.subplots(figsize=(options.width,options.height))
    sns.lineplot(data=df, x=feature1, y=feature2, hue=options.hue) 
    output_name = get_output_name(options)
    feature1_str = feature1.replace(' ', '_')
    feature2_str = feature2.replace(' ', '_')
    output_name = get_output_name(options)
    filename = Path('.'.join([output_name, feature1_str, feature2_str, 'line.png'])) 
    ax.set(xlabel=feature1, ylabel=feature2)
    if options.logy:
        ax.set(yscale="log")
    if options.title:
        plt.title(options.title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def heatmap(options, df):
    plt.clf()
    plt.suptitle('')
    fig, ax = plt.subplots(figsize=(options.width,options.height))
    pivot_data = df.pivot(index=options.rows, columns=options.columns, values=options.values)
    g=sns.heatmap(data=pivot_data, cmap=options.cmap)
    output_name = get_output_name(options)
    filename = Path('.'.join([output_name, options.rows, options.columns, options.values, 'heatmap.png'])) 
    if options.title:
        plt.title(options.title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def scatter(options, df):
    for pair in options.xy:
        pair_fields = pair.split(",") 
        if len(pair_fields) == 2:
            feature1, feature2 = pair_fields
            scatter_plot(options, df, feature1, feature2)
        else:
            logging.warn(f"Badly formed feature pair: {pair}, must be feature1,feature2 (comma separated, no spaces) ")
           

def scatter_plot(options, df, feature1, feature2):
    alpha = options.alpha
    linewidth = options.linewidth
    plt.clf()
    plt.suptitle('')
    # XXX this needs to be a parameter
    fig, ax = plt.subplots(figsize=(options.width,options.height))
    g=sns.scatterplot(data=df, x=feature1, y=feature2, hue=options.hue, alpha=options.alpha, size=options.size, linewidth=options.linewidth)
    if options.hue is not None:
        g.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    if options.nolegend:
        g.legend_.remove()
    feature1_str = feature1.replace(' ', '_')
    feature2_str = feature2.replace(' ', '_')
    output_name = get_output_name(options)
    filename = Path('.'.join([output_name, feature1_str, feature2_str, 'scatter.png'])) 
    ax.set(xlabel=feature1, ylabel=feature2)
    if options.title:
        plt.title(options.title)
    if options.xlim:
        xlow, xhigh = options.xlim
        plt.xlim(xlow, xhigh)
    if options.ylim:
        ylow, yhigh = options.ylim
        plt.ylim(ylow, yhigh)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def count(options, df):
    for column in options.columns:
        if column in df.columns:
            plt.clf()
            plt.suptitle('')
            fig, ax = plt.subplots(figsize=(options.width,options.height))
            sns.countplot(data=df, x=column, hue=options.hue) 
            output_name = get_output_name(options)
            column_str = column.replace(' ', '_')
            hue_str = ''
            if options.hue:
                hue_str = options.hue.replace(' ', '_')
                filename = Path('.'.join([output_name, column_str, hue_str, 'count', 'png']))
            else:
                filename = Path('.'.join([output_name, column_str, 'count', 'png']))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            ax.set(xlabel=column)
            if options.logy:
                ax.set(yscale="log")
            if options.title:
                plt.title(options.title)
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
        else:
            logging.warn(f"Column: {column} does not exist in data, skipping")


def make_output_directories(options):
    pass


def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    init_logging(options.logfile)
    make_output_directories(options)
    df = read_data(options)
    if options.cmd == 'hist':
        histogram(options, df)
    elif options.cmd == 'dist':
        distribution(options, df)
    elif options.cmd == 'scatter':
        scatter(options, df)
    elif options.cmd == 'line':
        line(options, df)
    elif options.cmd == 'heatmap':
        heatmap(options, df)
    elif options.cmd == 'count':
        count(options, df)
    logging.info("Completed")


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
