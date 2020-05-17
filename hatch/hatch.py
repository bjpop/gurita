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
        '--outdir',  metavar='DIR', type=str,
        required=False,
        help=f'Name of optional output directory.')
    parser.add_argument(
        '--filetype',  metavar='FILETYPE', type=str,
        required=False, choices=ALLOWED_FILETYPES,
        default=DEFAULT_FILETYPE,
        help=f'Type of input file')
    parser.add_argument(
        '--name',  metavar='NAME', type=str,
        required=False, 
        help=f'Name prefix for output files')
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument(
        '--log',
        metavar='LOG_FILE',
        type=str,
        help='record program progress in LOG_FILE')
    parser.add_argument(
        '--nolegend', action='store_true',
        help=f'Turn off the legend in the plot')
    parser.add_argument(
        '--filter', metavar='EXPR', required=False, type=str,
        help='Filter rows: only retain rows that make this expression True')
    parser.add_argument(
        '--navalues', metavar='STR', required=False, type=str,
        help='Treat values in this space separated list as NA values. Example: --navalues ". - !"')

    subparsers = parser.add_subparsers(help='sub-command help', dest='cmd')  

    histparser = subparsers.add_parser('hist', help='Plot histograms of columns') 
    histparser.add_argument(
        '--columns',  metavar='FEATURE', nargs="+", required=True, type=str,
        help=f'Columns to plot')
    histparser.add_argument(
        '--bins',  metavar='NUMBINS', required=False, default=DEFAULT_BINS, type=int,
        help=f'Number of bins for histogram (default={DEFAULT_BINS})')
    histparser.add_argument(
        '--cumulative', action='store_true',
        help=f'Generate cumulative histogram')
    histparser.add_argument(
        '--logy', action='store_true',
        help=f'Use a log scale on the vertical axis')
    histparser.add_argument(
        'data',  metavar='DATA', type=str, help='Filepaths of input CSV/TSV file')

    distparser = subparsers.add_parser('dist', help='Plot distributions of data') 
    distparser.add_argument(
        '--columns',  metavar='FEATURE', nargs="+", required=True, type=str,
        help=f'Columns to plot')
    distparser.add_argument(
        '--group',  metavar='FEATURE', nargs="+", required=True, type=str,
        help=f'Plot distributions of of the columns where data are grouped by these features')
    distparser.add_argument(
        '--logy', action='store_true',
        help=f'Use a log scale on the vertical axis')
    distparser.add_argument(
        '--type', choices=ALLOWED_DISTPLOT_TYPES, default=DEFAULT_DIST_PLOT_TYPE,
        help=f'Type of plot, default({DEFAULT_DIST_PLOT_TYPE})')
    distparser.add_argument(
        'data',  metavar='DATA', type=str, help='Filepaths of input CSV/TSV file')

    scatterparser = subparsers.add_parser('scatter', help='Plot scatter of two numerical columns in data') 
    scatterparser.add_argument(
        '--pairs',  metavar='FEATURE,FEATURE', nargs="+", required=True, type=str,
        help=f'Pairs of features to plot, format: feature1,feature2')
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
    scatterparser.add_argument(
        'data',  metavar='DATA', type=str, help='Filepaths of input CSV/TSV file')

    lineparser = subparsers.add_parser('line', help='Plot line plots of columns') 
    lineparser.add_argument(
        '--pairs',  metavar='FEATURE,FEATURE', nargs="+", required=True, type=str,
        help=f'Pairs of features to plot, format: feature1,feature2')
    lineparser.add_argument(
        '--overlay', action='store_true', 
        help=f'Overlay line plots on the same axes, otherwise make a separate plot for each')
    lineparser.add_argument(
        '--logy', action='store_true',
        help=f'Use a log scale on the vertical axis')
    lineparser.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature (column headings) to group data for line plot')
    lineparser.add_argument(
        'data',  metavar='DATA', type=str, help='Filepaths of input CSV/TSV file')

    heatmapparser = subparsers.add_parser('heatmap', help='Plot a heatmap of two categories with numerical values') 
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
    heatmapparser.add_argument(
        'data',  metavar='DATA', type=str, help='Filepaths of input CSV/TSV file')

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
    if options.filetype == 'CSV':
        data = pd.read_csv(options.data, sep=",", keep_default_na=True, na_values=na_values)
    elif options.filetype == 'TSV':
        data = pd.read_csv(options.data, sep="\t", keep_default_na=True, na_values=na_values)
    if options.filter:
        try:
            data = eval("data[ " + options.filter + "]")
        except:
            exit_with_error(f"Bad filter expression: {options.filter}", EXIT_COMMAND_LINE_ERROR)
    return data 

def get_output_name(options):
    if options.name:
        return options.name
    else:
        return Path(options.data).stem
        

def histogram(options, df):
    for column in options.columns:
        if column in df.columns:
            plt.clf()
            plt.suptitle('')
            fig, ax = plt.subplots(figsize=(10,8))
            sns.distplot(df[column], hist_kws={'cumulative': options.cumulative}, kde=False, bins=options.bins) 
            output_name = get_output_name(options)
            filename = Path('.'.join([output_name, column.replace(' ', '_'), 'histogram.png']))
            ax.set(xlabel=column, ylabel='count')
            if options.logy:
                ax.set(yscale="log")
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
        else:
            logging.warn(f"Column: {column} does not exist in data, skipping")


def distribution(options, df):
    for group in options.group:
        if group in df.columns:
            plot_distributions_by(df, options, group)
        else:
            logging.warn(f"Column: {group} does not exist in data, skipping")

def plot_distributions_by(df, options, group):
    for column in options.columns:
        if column in df.columns:
            plt.clf()
            plt.suptitle('')
            fig, ax = plt.subplots(figsize=(10,8))
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
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
        else:
            logging.warn(f"Column: {column} does not exist in data, skipping")

def line(options, df):
    for pair in options.pairs:
        pair_fields = pair.split(",") 
        if len(pair_fields) == 2:
            feature1, feature2 = pair_fields
            line_plot(options, df, feature1, feature2)
        else:
            logging.warn(f"Badly formed feature pair: {pair}, must be feature1,feature2 (comma separated, no spaces) ")

def line_plot(options, df, feature1, feature2):
    plt.clf()
    plt.suptitle('')
    fig, ax = plt.subplots(figsize=(10,8))
    sns.lineplot(data=df, x=feature1, y=feature2, hue=options.hue) 
    output_name = get_output_name(options)
    feature1_str = feature1.replace(' ', '_')
    feature2_str = feature2.replace(' ', '_')
    output_name = get_output_name(options)
    filename = Path('.'.join([output_name, feature1_str, feature2_str, 'line.png'])) 
    ax.set(xlabel=feature1, ylabel=feature2)
    if options.logy:
        ax.set(yscale="log")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def heatmap(options, df):
    plt.clf()
    plt.suptitle('')
    fig, ax = plt.subplots(figsize=(10,8))
    pivot_data = df.pivot(index=options.rows, columns=options.columns, values=options.values)
    g=sns.heatmap(data=pivot_data, cmap=options.cmap)
    output_name = get_output_name(options)
    filename = Path('.'.join([output_name, options.rows, options.columns, options.values, 'heatmap.png'])) 
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def scatter(options, df):
    for pair in options.pairs:
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
    fig, ax = plt.subplots(figsize=(10,8))
    g=sns.scatterplot(data=df, x=feature1, y=feature2, hue=options.hue, alpha=options.alpha, size=options.size, linewidth=options.linewidth)
    g.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    if options.nolegend:
        g.legend_.remove()
    feature1_str = feature1.replace(' ', '_')
    feature2_str = feature2.replace(' ', '_')
    output_name = get_output_name(options)
    filename = Path('.'.join([output_name, feature1_str, feature2_str, 'scatter.png'])) 
    ax.set(xlabel=feature1, ylabel=feature2)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def make_output_directories(options):
    pass


def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    init_logging(options.log)
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
    logging.info("Completed")


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
