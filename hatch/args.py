'''
Module      : Args 
Description : Command line argument parsing for Hatch
Copyright   : (c) Bernie Pope, 16 Oct 2019-2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import sys
import logging
import os
from pathlib import Path
import hatch.constants as const

def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, usage='hatch [-v] [-h] command <arguments>')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s ' + const.PROGRAM_VERSION)

    # Common command line arguments for input/output
    io_common_arguments = argparse.ArgumentParser()
    io_common_arguments_group = io_common_arguments.add_argument_group('Input and Output', 'input/output related arguments that are provided across all hatch sub-commands') 
    io_common_arguments_group.add_argument(
        '-o', '--out', metavar='FILE', type=str,
        required=False,
        help=f'Use this filename when saving output to file (override the default output filename)')
    io_common_arguments_group.add_argument(
        '--filetype',  type=str,
        required=False, choices=const.ALLOWED_FILETYPES,
        help=f'Type of input file. Allowed values: %(choices)s. Otherwise inferred from filename extension.')
    io_common_arguments_group.add_argument(
        '--logfile',
        required=False,
        metavar='LOG_FILE',
        type=str,
        help='record program progress in LOG_FILE')
    io_common_arguments_group.add_argument(
        '--filter', metavar='EXPR', required=False, type=str,
        help='Filter rows: only retain rows that make this expression True')
    io_common_arguments_group.add_argument(
        '--features', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Select only these features (columns)')
    io_common_arguments_group.add_argument(
        '--eval', metavar='EXPR', required=False, type=str, nargs="+",
        help='Construct new data columns based on an expression')
    io_common_arguments_group.add_argument(
        '--sample', metavar='NUM', required=False, type=float,
        help='Sample rows from the input data, if NUM >= 1 then sample NUM rows, if 0 <= NUM < 1, then sample NUM fraction of rows')
    io_common_arguments_group.add_argument(
        '--verbose', action='store_true',
        default=False,
        help=f'Print information about the progress of the program')
    io_common_arguments_group.add_argument(
        '--navalues', metavar='STR', required=False, type=str,
        help='Treat values in this space separated list as NA values. Example: --navalues ". - !"')
    io_common_arguments_group.add_argument(
        '--prefix',  metavar='NAME', type=str,
        required=False, 
        help=f'Name prefix for output file')
    io_common_arguments_group.add_argument(
        'data',  metavar='DATA', type=str, nargs='?', help='Filepath of input CSV/TSV file')

    # Common command line arguments for plotting sub-commands
    # turn off add_help here because the help option comes from io_common_arguments
    plot_common_arguments = argparse.ArgumentParser(add_help=False)
    plot_common_arguments_group = plot_common_arguments.add_argument_group('Plotting', 'arguments that are provided across all hatch plotting sub-commands') 
    plot_common_arguments_group.add_argument(
        '--format',  type=str,
        choices=const.ALLOWED_PLOT_FORMATS, default=const.DEFAULT_PLOT_FORMAT,
        help=f'Graphic file format to use for saved plots. Allowed values: %(choices)s. Default: %(default)s.')
    plot_common_arguments_group.add_argument(
        '--show', action='store_true',
        default=False,
        help=f'Show an interactive plot window instead of saving to a file')
    plot_common_arguments_group.add_argument(
        '--nolegend', action='store_true',
        default=False,
        help=f'Turn off the legend in the plot')
    plot_common_arguments_group.add_argument(
        '--style', choices=const.ALLOWED_STYLES, required=False, default=const.DEFAULT_STYLE,
        help=f'Aesthetic style of plot. Allowed values: %(choices)s. Default: %(default)s.')
    plot_common_arguments_group.add_argument(
        '--context', choices=const.ALLOWED_CONTEXTS, required=False, default=const.DEFAULT_CONTEXT,
        help=f'Aesthetic context of plot. Allowed values: %(choices)s. Default: %(default)s.')
    plot_common_arguments_group.add_argument(
        '--title', metavar='STR', required=False, type=str,
        help='Plot title. By default no title will be added.')
    plot_common_arguments_group.add_argument(
        '--width', metavar='SIZE', required=False, type=float,
        default=const.DEFAULT_PLOT_WIDTH,
        help=f'Plot width in inches. Default: %(default)s')
    plot_common_arguments_group.add_argument(
        '--height', metavar='SIZE', required=False, type=float,
        default=const.DEFAULT_PLOT_HEIGHT,
        help=f'Plot height in inches. Default: %(default)s')
    plot_common_arguments_group.add_argument(
        '--xlabel', metavar='STR', required=False, type=str,
        help=f'Label for horizontal (X) axis')
    plot_common_arguments_group.add_argument(
        '--ylabel', metavar='STR', required=False, type=str,
        help=f'Label for vertical (Y) axis')
    plot_common_arguments_group.add_argument(
        '--noxticklabels', action='store_true',
        help=f'Turn of horizontal (X) axis tick labels')
    plot_common_arguments_group.add_argument(
        '--noyticklabels', action='store_true',
        help=f'Turn of veritcal (Y) axis tick labels')
    plot_common_arguments_group.add_argument(
        '--rotxticklabels', metavar='ANGLE', required=False, type=float,
        help=f'Rotate X axis tick labels by ANGLE')
    plot_common_arguments_group.add_argument(
        '--rotyticklabels', metavar='ANGLE', required=False, type=float,
        help=f'Rotate Y axis tick labels by ANGLE')

    x_argument = argparse.ArgumentParser(add_help=False)
    x_argument.add_argument(
        '-x', '--xaxis', metavar='FEATURE', required=False, type=str,
        help=f'Feature to plot along the X axis')

    y_argument = argparse.ArgumentParser(add_help=False)
    y_argument.add_argument(
        '-y', '--yaxis', metavar='FEATURE', required=False, type=str,
        help=f'Feature to plot along the Y axis')

    hue_argument = argparse.ArgumentParser(add_help=False)
    hue_argument.add_argument(
        '--hue',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature to use for colouring/grouping the plotted data')

    row_argument = argparse.ArgumentParser(add_help=False)
    row_argument.add_argument(
        '-r', '--row', metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature to use for facet rows')

    col_argument = argparse.ArgumentParser(add_help=False)
    col_argument.add_argument(
        '-c', '--col', metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature to use for facet columns')

    order_arguments = argparse.ArgumentParser(add_help=False)
    order_arguments.add_argument(
        '--order', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Order to display categorical values')

    hue_order_arguments = argparse.ArgumentParser(add_help=False)
    hue_order_arguments.add_argument(
        '--hueorder', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Order to display categorical values selected for hue')

    orient_argument = argparse.ArgumentParser(add_help=False)
    orient_argument.add_argument(
        '--orient', choices=const.ALLOWED_ORIENTATIONS, required=False, default=const.DEFAULT_ORIENTATION,
        help=f'Orientation of plot. Allowed values: %(choices)s. Default: %(default)s.')

    logx_argument = argparse.ArgumentParser(add_help=False)
    logx_argument.add_argument(
        '--logx', action='store_true',
        help=f'Use a log scale on the horizontal (X) axis')

    logy_argument = argparse.ArgumentParser(add_help=False)
    logy_argument.add_argument(
        '--logy', action='store_true',
        help=f'Use a log scale on the veritical (Y) axis')

    xlim_argument = argparse.ArgumentParser(add_help=False)
    xlim_argument.add_argument(
        '--xlim',  metavar='BOUND', nargs=2, required=False, type=float,
        help=f'Limit horizontal axis range to [LOW,HIGH]')

    ylim_argument = argparse.ArgumentParser(add_help=False)
    ylim_argument.add_argument(
        '--ylim',  metavar='BOUND', nargs=2, required=False, type=float,
        help=f'Limit vertical axis range to [LOW,HIGH]')

    dotsize_argument = argparse.ArgumentParser(add_help=False)
    dotsize_argument.add_argument(
        '--dotsize',  metavar='FEATURE', type=str, required=False, 
        help=f'Name of feature to use for plotted point size')

    dotalpha_argument = argparse.ArgumentParser(add_help=False)
    dotalpha_argument.add_argument(
        '--dotalpha',  metavar='ALPHA', type=float, default=const.DEFAULT_ALPHA,
        help=f'Alpha value for plotted points. Default: %(default)s')

    dotlinewidth_argument = argparse.ArgumentParser(add_help=False)
    dotlinewidth_argument.add_argument(
        '--dotlinewidth',  metavar='WIDTH', type=int, default=const.DEFAULT_LINEWIDTH,
        help=f'Line width value for plotted points. Default: %(default)s')

    colwrap_argument = argparse.ArgumentParser(add_help=False)
    colwrap_argument.add_argument(
        '--colwrap',  metavar='INT', type=int, required=False, 
        help=f'Wrap the facet column at this width, to span multiple rows.')

    # Subcommands 

    subparsers_description = """
    Plotting: 
    ---------

    bar                 Bar plot of categorical feature
    box                 Box plot of numerical feature
    boxen               Boxen plot of numerical feature
    clustermap          Clustered heatmap of two numerical features 
    count               Count plot of categorical feature
    heatmap             Heatmap of two numerical features 
    hist                Histogram of numerical or categorical feature 
    line                Line plot of numerical feature
    pca                 Principal components analysis (PCA)
    point               Point plot of numerical feature
    scatter             Scatter plot of two numerical features
    strip               Strip plot of numerical feature
    swarm               Swarm plot of numerical feature
    violin              Violin plot of numerical feature

    Data manipulation:
    ------------------

    trans               Tranform the input data and save the result to a new file

    Statistics:
    -----------

    corr                Correlation between numerical features
    info                Show summary information about features in the input data set
    normtest            Test whether numerical features differ from a normal distribution 
    stdev               Compute the standard deviation of numerical features
    """

    subparsers = parser.add_subparsers(title='Sub command', help=argparse.SUPPRESS, dest='cmd', description=subparsers_description)  

    def facet_parser(kind, help='', additional_parents=[]):
        return subparsers.add_parser(kind,
                parents=[io_common_arguments, plot_common_arguments, y_argument, x_argument, hue_argument, row_argument, col_argument,
                         order_arguments, hue_order_arguments, orient_argument, logx_argument, logy_argument, xlim_argument, ylim_argument, colwrap_argument] + additional_parents, add_help=False) 

    barparser = facet_parser('bar')

    boxparser = facet_parser('box')

    boxenparser = facet_parser('boxen')

    clustmapparser = subparsers.add_parser('clustermap', parents=[io_common_arguments, plot_common_arguments, y_argument, x_argument], add_help=False) 
    clustmapparser.add_argument(
        '-v', '--val', metavar='FEATURE', required=True, type=str,
        help=f'Interpret this feature (column of data) as the values of the heatmap')
    clustmapparser.add_argument(
        '--cmap',  metavar='COLOR_MAP_NAME', type=str, 
        help=f'Use this color map, will use Seaborn default if not specified')
    clustmapparser.add_argument(
        '--log', action='store_true',
        help=f'Use a log scale on the numerical data')
    clustmapparser.add_argument(
        '--dendroratio', metavar='NUM', type=float, default=const.DEFAULT_DENDRO_RATIO,
        help=f'Ratio of the figure size devoted to the dendrogram. Default: %(default)s.')
    clustmapparser.add_argument('--rowclust', dest='rowclust', action='store_true',
        help='Cluster by rows (default).')
    clustmapparser.add_argument('--no-rowclust', dest='rowclust', action='store_false',
        help='Do not cluster by rows')
    clustmapparser.set_defaults(rowclust=True)
    clustmapparser.add_argument('--colclust', dest='colclust', action='store_true',
        help='Cluster by columns (default).')
    clustmapparser.add_argument('--no-colclust', dest='colclust', action='store_false',
        help='Do not cluster by columns')
    cluster_normalise_group = clustmapparser.add_mutually_exclusive_group()
    cluster_normalise_group.add_argument('--zscore', required=False, choices=['y', 'x'],
        help='Normalise either across rows (y) or down columns (x) using z-score. Allowed values: %(choices)s.')
    cluster_normalise_group.add_argument('--stdscale', required=False, choices=['y', 'x'],
        help='Normalise either across rows (y) or down columns (x) by subtracting the minimum and dividing by the maximum. Allowed values: %(choices)s.')
    clustmapparser.add_argument('--method', required=False, choices=const.ALLOWED_CLUSTERMAP_METHODS, default=const.DEFAULT_CLUSTERMAP_METHOD,
        help='Linkage method to use for calculating clusters. Allowed values: %(choices)s. Default: %(default)s.')
    clustmapparser.add_argument('--metric', required=False, choices=const.ALLOWED_CLUSTERMAP_METRICS, default=const.DEFAULT_CLUSTERMAP_METRIC,
        help='Distance metric to use for calculating clusters. Allowed values: %(choices)s. Default: %(default)s.')
    clustmapparser.set_defaults(colclust=True)

    corrparser = subparsers.add_parser('corr', parents=[io_common_arguments], add_help=False)
    corrparser.add_argument('--method', required=False, default=const.DEFAULT_CORR_METHOD, choices=const.ALLOWED_CORR_METHODS,
        help=f'Method for determining correlation. Allowed values: %(choices)s. Default: %(default)s.')

    countparser = facet_parser('count')

    heatmapparser = subparsers.add_parser('heatmap', parents=[io_common_arguments, plot_common_arguments, y_argument, x_argument], add_help=False) 
    heatmapparser.add_argument(
        '-v', '--val', metavar='FEATURE', required=True, type=str,
        help=f'Interpret this feature (column of data) as the values of the heatmap')
    heatmapparser.add_argument(
        '--cmap',  metavar='COLOR_MAP_NAME', type=str, 
        help=f'Use this color map, will use Seaborn default if not specified')
    heatmapparser.add_argument(
        '--log', action='store_true',
        help=f'Use a log scale on the numerical data')

    histparser = subparsers.add_parser('hist', parents=[io_common_arguments, plot_common_arguments, x_argument, y_argument, logx_argument, logy_argument, xlim_argument, ylim_argument, hue_argument, hue_order_arguments, row_argument, col_argument, colwrap_argument], add_help=False) 
    histparser.add_argument(
        '--bins',  metavar='NUM', required=False, type=int,
        help=f'Number of bins for histogram.')
    histparser.add_argument(
        '--binwidth',  metavar='NUM', required=False, type=float,
        help=f'Width of histogram bins, overrides "--bins".')
    histparser.add_argument(
       '--cumulative', action='store_true',
        help=f'Generate cumulative histogram')
    histparser.add_argument(
       '--kde', action='store_true',
        help=f'Plot a kernel density estimate for the distribution and show as a line')
    histparser.add_argument(
        '--multiple', required=False, choices=const.ALLOWED_HIST_MULTIPLES,
        help=f"How to display overlapping subsets of data. Allowed values: %(choices)s.")

    infoparser = subparsers.add_parser('info', parents=[io_common_arguments], add_help=False)

    isnormparser = subparsers.add_parser('normtest', parents=[io_common_arguments], add_help=False)

    # XXX maybe this nanpolicy needs to be more general?
    isnormparser.add_argument('--nanpolicy', required=False, default=const.DEFAULT_ISNORM_NANPOLICY, choices=const.ALLOWED_ISNORM_NAN_POLICIES,
        help=f'Method for nan propagation. Allowed values: %(choices)s. Default: %(default)s. Propagate retains the nan. Raise throws an error. Omit discards nan values')

    stdevparser = subparsers.add_parser('stdev', parents=[io_common_arguments], add_help=False)

    lineparser = facet_parser('line')

    pcaparser = subparsers.add_parser('pca', parents=[io_common_arguments, plot_common_arguments, xlim_argument, ylim_argument, hue_argument, dotsize_argument, dotalpha_argument, dotlinewidth_argument], add_help=False) 
    pcaparser.add_argument(
        '--missing', required=False, default=const.DEFAULT_PCA_MISSING, choices=const.ALLOWED_PCA_MISSING,
        help=f'How to deal with rows that contain missing data. Allowed values: %(choices)s. Default: %(default)s.')

    pointparser = facet_parser('point')
    pointparser.add_argument(
        '--nojoin', action='store_true', required=False, 
        help=f'Do not connect point estimates by a line')

    scatterparser = facet_parser('scatter', additional_parents=[dotsize_argument, dotalpha_argument, dotlinewidth_argument])
    scatterparser.add_argument( '--vlines',  metavar='AXIS_LOCATION', required=False, type=float, nargs="+", help=f'Draw vertical lines on the plot at specified axes locations')
    scatterparser.add_argument( '--hlines',  metavar='AXIS_LOCATION', required=False, type=float, nargs="+", help=f'Draw horizontal lines on the plot at specified axes locations')


    stripparser = facet_parser('strip')

    swarmparser = facet_parser('swarm')

    trans_parser = subparsers.add_parser('trans', parents=[io_common_arguments], add_help=False)

    violinparser = facet_parser('violin')

    return parser.parse_args()
