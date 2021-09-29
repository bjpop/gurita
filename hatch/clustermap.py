'''
Module      : Clustermap 
Description : Clustermap plot of two features 
Copyright   : (c) Bernie Pope, 22 September 2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import sys
import logging
import argparse
import hatch.constants as const
import seaborn as sns
from hatch.command_base import CommandBase
import hatch.render_plot as render_plot
import hatch.io_arguments as io_args
import hatch.plot_arguments as plot_args

class Clustermap(CommandBase, name="clustermap"):
    description = "Cluster map of two categorical features associated with a numerical value" 
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
                     parents=[io_args.io_arguments, plot_args.plot_arguments,
                         plot_args.x_argument, plot_args.y_argument], add_help=False)
        parser.add_argument(
            '-v', '--val', metavar='FEATURE', required=True, type=str,
            help=f'Interpret this feature (column of data) as the values of the heatmap')
        parser.add_argument(
            '--cmap',  metavar='COLOR_MAP_NAME', type=str,
            help=f'Use this color map, will use Seaborn default if not specified')
        parser.add_argument(
            '--log', action='store_true',
            help=f'Use a log scale on the numerical data')
        parser.add_argument(
            '--dendroratio', metavar='NUM', type=float, default=const.DEFAULT_DENDRO_RATIO,
            help=f'Ratio of the figure size devoted to the dendrogram. Default: %(default)s.')
        parser.add_argument('--rowclust', dest='rowclust', action='store_true',
            help='Cluster by rows (default).')
        parser.add_argument('--no-rowclust', dest='rowclust', action='store_false',
            help='Do not cluster by rows')
        parser.set_defaults(rowclust=True)
        parser.add_argument('--colclust', dest='colclust', action='store_true',
            help='Cluster by columns (default).')
        parser.add_argument('--no-colclust', dest='colclust', action='store_false',
            help='Do not cluster by columns')
        cluster_normalise_group = parser.add_mutually_exclusive_group()
        cluster_normalise_group.add_argument('--zscore', required=False, choices=['y', 'x'],
            help='Normalise either across rows (y) or down columns (x) using z-score. Allowed values: %(choices)s.')
        cluster_normalise_group.add_argument('--stdscale', required=False, choices=['y', 'x'],
            help='Normalise either across rows (y) or down columns (x) by subtracting the minimum and dividing by the maximum. Allowed values: %(choices)s.')
        parser.add_argument('--method', required=False, choices=const.ALLOWED_CLUSTERMAP_METHODS, default=const.DEFAULT_CLUSTERMAP_METHOD,
            help='Linkage method to use for calculating clusters. Allowed values: %(choices)s. Default: %(default)s.')
        parser.add_argument('--metric', required=False, choices=const.ALLOWED_CLUSTERMAP_METRICS, default=const.DEFAULT_CLUSTERMAP_METRIC,
            help='Distance metric to use for calculating clusters. Allowed values: %(choices)s. Default: %(default)s.')
        parser.set_defaults(colclust=True)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        if options.xaxis not in df.columns:
            utils.exit_with_error(f"{options.xaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        if options.yaxis not in df.columns:
            utils.exit_with_error(f"{options.yaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        if options.val not in df.columns:
            utils.exit_with_error(f"{options.val} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        self.x = options.xaxis
        self.y = options.yaxis
        self.val = options.val
        pivot_data = df.pivot(index=self.y, columns=self.x, values=self.val)
        figsize = (options.width, options.height)
        z_score = None
        if options.zscore == 'y':
            z_score = 0
        elif options.zscore == 'x':
            z_score = 1
        standard_scale = None
        if options.stdscale == 'y':
            standard_scale = 0
        elif options.zscore == 'x':
            standard_scale = 1
        xticklabels = True
        if options.noxticklabels:
            xticklabels = False
        yticklabels = True
        if options.noyticklabels:
            yticklabels = False
        # clustermap does not allow both zscore and standard_scale to be specified at the
        # same time, even if only one is None.
        if standard_scale is not None:
            graph = sns.clustermap(data=pivot_data, cmap=options.cmap, figsize=figsize,
                      dendrogram_ratio=options.dendroratio, row_cluster=options.rowclust,
                      col_cluster=options.colclust, yticklabels=yticklabels, xticklabels=xticklabels,
                      standard_scale=standard_scale, method=options.method, metric=options.metric)
        elif z_score is not None:
            graph = sns.clustermap(data=pivot_data, cmap=options.cmap, figsize=figsize,
                      dendrogram_ratio=options.dendroratio, row_cluster=options.rowclust,
                      col_cluster=options.colclust, z_score=z_score, yticklabels=yticklabels,
                      xticklabels=xticklabels, method=options.method, metric=options.metric)
        else:
            graph = sns.clustermap(data=pivot_data, cmap=options.cmap, figsize=figsize,
                      dendrogram_ratio=options.dendroratio, row_cluster=options.rowclust,
                      col_cluster=options.colclust, yticklabels=yticklabels, xticklabels=xticklabels,
                      method=options.method, metric=options.metric)
        render_plot.render_plot(options, graph, self.name)
        return df

