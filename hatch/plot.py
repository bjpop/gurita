'''
Module      : plot 
Description : Plotting functions 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import sys
import argparse
import logging
import seaborn as sns
from hatch.command_base import CommandBase
import hatch.render_plot as render_plot
import hatch.io_arguments as io_args 
import hatch.plot_arguments as plot_args 
import hatch.constants as const
import hatch.utils as utils


class PairPlot(CommandBase, name="pair"):
    description = "Pair plot of numerical features."
    category = "plotting"

    def __init__(self):
        pass

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments,
                plot_args.make_plot_arguments(const.DEFAULT_PAIR_PLOT_WIDTH, const.DEFAULT_PAIR_PLOT_HEIGHT),
                plot_args.hue, plot_args.hue_order],
                add_help=False)
        parser.add_argument(
            '-c', '--columns', metavar='FEATURE', nargs="*", type=str, required=False,
            help=f'Select only these columns (columns)')
        parser.add_argument(
            '--kind',  type=str,
            choices=const.ALLOWED_PAIRPLOT_KINDS, default=const.DEFAULT_PAIR_PLOT_KIND,
            help=f'Kind of plot to use. Allowed values: %(choices)s. Default: %(default)s.')
        parser.add_argument(
            '--corner', action='store_true',
            default=False,
            help=f'Only plot the lower triangle of comparisons')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        _width_inches, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        kwargs = {}
        graph = sns.pairplot(data=df, height=height_inches, aspect=aspect,
                vars=options.columns, kind=options.kind, hue=options.hue, hue_order=options.hueorder,
                corner=options.corner, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class BarPlot(CommandBase, name="bar"):
    description = "Bar plot of categorical feature."
    category = "plotting"

    def __init__(self):
        pass

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
            plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
            plot_args.order, plot_args.hue_order, plot_args.orient,
            plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap],
            add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class BoxPlot(CommandBase, name="box"):
    description = "Plot distrbution of numerical column using box-and-whiskers."
    category = "plotting"

    def __init__(self):
        self.options = None 

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
                plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
                plot_args.order, plot_args.hue_order, plot_args.orient,
                plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap,
                plot_args.strip, plot_args.nooutliers],
           add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                showfliers=not(options.nooutliers),
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.strip:
            graph.map_dataframe(sns.stripplot, data=df, x=options.xaxis, y=options.yaxis, alpha=0.8, color="black")
        render_plot.render_plot(options, graph, self.name)
        return df


class BoxenPlot(CommandBase, name="boxen"):
    description = "Plot distrbution of numerical column using boxes for quantiles."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
                plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
                plot_args.order, plot_args.hue_order, plot_args.orient,
                plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap,
                plot_args.strip, plot_args.nooutliers],
           add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                showfliers=not(options.nooutliers),
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.strip:
            graph.map_dataframe(sns.stripplot, data=df, x=options.xaxis, y=options.yaxis, alpha=0.8, color="black")
        render_plot.render_plot(options, graph, self.name)
        return df


class Clustermap(CommandBase, name="clustermap"):
    description = "Clustered heatmap of two categorical columns." 
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
                     parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
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
        # clustermap does not allow both zscore and standard_scale to be specified at the same time
        cluster_normalise_group = parser.add_mutually_exclusive_group()
        cluster_normalise_group.add_argument('--zscore', required=False, choices=['y', 'x'],
            help='Normalise either across rows (y) or down columns (x) using z-score. Allowed values: %(choices)s.')
        cluster_normalise_group.add_argument('--stdscale', required=False, choices=['y', 'x'],
            help='Normalise either across rows (y) or down columns (x) by subtracting the minimum and dividing by the maximum. Allowed values: %(choices)s.')
        parser.add_argument('--method', required=False, choices=const.ALLOWED_CLUSTERMAP_METHODS, default=const.DEFAULT_CLUSTERMAP_METHOD,
            help='Linkage method to use for calculating clusters. Allowed values: %(choices)s. Default: %(default)s.')
        parser.add_argument('--metric', required=False, choices=const.ALLOWED_CLUSTERMAP_METRICS, default=const.DEFAULT_CLUSTERMAP_METRIC,
            help='Distance metric to use for calculating clusters. Allowed values: %(choices)s. Default: %(default)s.')
        parser.add_argument(
            '--annot', action='store_true',
            help=f'Display the data value in each cell in the heatmap')
        # See https://docs.python.org/3/library/string.html#formatspec for options on formatting
        parser.add_argument(
            '--fmt', type=str, required=False, default=const.DEFAULT_HEATMAP_STRING_FORMAT,
            help=f'String formatting to be used for displaying cell values using Python format specification, used in conjunction with --annot. Default: %(default)s.')
        parser.add_argument(
            '--vmin', type=float, metavar='NUM', required=False,
            help=f'Minimum anchor value for the colormap, if unset this will be inferred from the dataset')
        parser.add_argument(
            '--vmax', type=float, metavar='NUM', required=False,
            help=f'Maximum anchor value for the colormap, if unset this will be inferred from the dataset')
        parser.add_argument(
            '--robust', action='store_true',
            help=f'If --vmin or --vmax absent, use robust quantiles to set colormap range instead of the extreme data values')
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
        width_inches, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        figsize = (width_inches, height_inches)
        kwargs = {}
        if options.zscore == 'y':
            kwargs['z_score'] = 0
        elif options.zscore == 'x':
            kwargs['z_score'] = 1
        if options.stdscale == 'y':
            kwargs['standard_scale'] = 0
        elif options.stdscale == 'x':
            kwargs['standard_scale'] = 1
        xticklabels = True
        if options.nxtl:
            xticklabels = False
        yticklabels = True
        if options.nytl:
            yticklabels = False
        # the following arguments control heatmap aspects of the clustermap
        kwargs['annot'] = self.options.annot
        kwargs['fmt'] = self.options.fmt
        kwargs['robust'] = self.options.robust
        kwargs['vmin'] = self.options.vmin
        kwargs['vmax'] = self.options.vmax
        # same time, even if only one is None.
        graph = sns.clustermap(data=pivot_data, cmap=options.cmap, figsize=figsize,
                      dendrogram_ratio=options.dendroratio, row_cluster=options.rowclust,
                      col_cluster=options.colclust, yticklabels=yticklabels, xticklabels=xticklabels,
                      method=options.method, metric=options.metric, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class Heatmap(CommandBase, name="heatmap"):
    description = "Heatmap of two categorical columns." 
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
                     parents=[io_args.io_arguments, plot_args.make_plot_arguments()], add_help=False)
        parser.add_argument(
            '-x', '--xaxis', metavar='FEATURE', required=True, type=str,
            help=f'Feature to plot along the X axis.')
        parser.add_argument(
            '-y', '--yaxis', metavar='FEATURE', required=True, type=str,
            help=f'Feature to plot along the Y axis.')
        parser.add_argument(
            '-v', '--val', metavar='FEATURE', required=True, type=str,
            help=f'Interpret this feature (column of data) as the values of the heatmap')
        parser.add_argument(
            '--cmap',  metavar='COLOR_MAP_NAME', type=str,
            help=f'Use this color map, will use Seaborn default if not specified')
        parser.add_argument(
            '--annot', action='store_true', 
            help=f'Display the data value in each cell in the heatmap')
        # See https://docs.python.org/3/library/string.html#formatspec for options on formatting
        parser.add_argument(
            '--fmt', type=str, required=False, default=const.DEFAULT_HEATMAP_STRING_FORMAT,
            help=f'String formatting to be used for displaying cell values using Python format specification, used in conjunction with --annot. Default: %(default)s.')
        parser.add_argument(
            '--vmin', type=float, metavar='NUM', required=False,
            help=f'Minimum anchor value for the colormap, if unset this will be inferred from the dataset')
        parser.add_argument(
            '--vmax', type=float, metavar='NUM', required=False,
            help=f'Maximum anchor value for the colormap, if unset this will be inferred from the dataset')
        parser.add_argument(
            '--robust', action='store_true', 
            help=f'If --vmin or --vmax absent, use robust quantiles to set colormap range instead of the extreme data values')
        parser.add_argument(
            '--log', action='store_true',
            help=f'Use a log scale on the numerical data')
        x_order_group = parser.add_mutually_exclusive_group()
        x_order_group.add_argument(
            '--sortx', metavar='ORDER', type=str, required=False, nargs='?',
            choices=const.ALLOWED_SORT_ORDER, default=const.DEFAULT_SORT_ORDER,
            help=f'Sort the X axis by label. Allowed values: %(choices)s. a=ascending, d=descending. Default: %(default)s. Categorical features will be sorted alphabetically. Numerical features will be sorted numerically.')
        x_order_group.add_argument(
            '--orderx', metavar='LABEL', type=str, required=False, nargs='+',
            help=f'Order the X axis according to a given list of labels, left to right. Unlisted labels will appear in arbitrary order.')
        y_order_group = parser.add_mutually_exclusive_group()
        y_order_group.add_argument(
            '--sorty', metavar='ORDER', type=str, required=False, nargs='?',
            choices=const.ALLOWED_SORT_ORDER, default=const.DEFAULT_SORT_ORDER,
            help=f'Sort the Y axis by label. Allowed values: %(choices)s. a=ascending, d=descending. Default: %(default)s. Categorical features will be sorted alphabetically. Numerical features will be sorted numerically.')
        y_order_group.add_argument(
            '--ordery', metavar='LABEL', type=str, required=False, nargs='+',
            help=f'Order the Y axis according to a given list of labels, top to bottom. Unlisted labels will appear in arbitrary order.')
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
        if self.options.sortx is not None:
            ascending = True if self.options.sortx == 'a' else False
            pivot_data.sort_index(axis=1, ascending=ascending, inplace=True)
        if self.options.sorty is not None:
            ascending = True if self.options.sorty == 'a' else False
            pivot_data.sort_index(axis=0, ascending=ascending, inplace=True)
        if self.options.orderx is not None:
            # orderx must not have duplicates
            if len(self.options.orderx) != len(set(self.options.orderx)):
                utils.exit_with_error("X axis labels for ordering contains duplicates", const.EXIT_COMMAND_LINE_ERROR)
            # orderx must be a subset of the column labels
            column_label_strings = pivot_data.columns.map(str)
            if not set(self.options.orderx).issubset(set(column_label_strings)):
                utils.exit_with_error("X axis labels for ordering are not a subset of column labels", const.EXIT_COMMAND_LINE_ERROR)
            order_map = { item: pos for (pos, item) in enumerate(self.options.orderx) }
            max_index = len(self.options.orderx)
            pivot_data.sort_index(axis=1, inplace=True, key=lambda index: index.map(lambda label: order_map.get(str(label), max_index)))
        if self.options.ordery is not None:
            # ordery must not have duplicates
            if len(self.options.ordery) != len(set(self.options.ordery)):
                utils.exit_with_error("Y axis labels for ordering contains duplicates", const.EXIT_COMMAND_LINE_ERROR)
            # ordery must be a subset of the row labels
            row_label_strings = pivot_data.index.map(str)
            if not set(self.options.ordery).issubset(set(row_label_strings)):
                utils.exit_with_error("Y axis labels for ordering are not a subset of row labels", const.EXIT_COMMAND_LINE_ERROR)
            order_map = { item: pos for (pos, item) in enumerate(self.options.ordery) }
            max_index = len(self.options.ordery)
            pivot_data.sort_index(axis=0, inplace=True, key=lambda index: index.map(lambda label: order_map.get(str(label), max_index)))
        graph = sns.heatmap(data=pivot_data, cmap=self.options.cmap, annot=self.options.annot, robust=self.options.robust,
                    vmin=self.options.vmin, vmax=self.options.vmax, fmt=self.options.fmt)
        render_plot.render_plot(options, graph, self.name)
        return df


class HistogramPlot(CommandBase, name="hist"):
    description = "Histogram of numerical or categorical feature."
    category = "plotting"

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap],
           add_help=False)
        parser.add_argument(
            '--multiple', required=False, choices=const.ALLOWED_HIST_MULTIPLES,
            help=f"How to display overlapping subsets of data in a histogram. Allowed values: %(choices)s.")
        parser.add_argument(
            '--bins', metavar='NUM', required=False, type=int, default=const.DEFAULT_HISTOGRAM_BINS,
            help=f'Number of histogram bins. Default: %(default)s.')
        parser.add_argument(
            '--binwidth', metavar='NUM', required=False, type=float,
            help=f'Width of histogram bins, overrides "--bins".')
        parser.add_argument(
            '--cumulative', action='store_true',
            help=f'Generate cumulative histogram')
        parser.add_argument(
           '--kde', action='store_true',
            help=f'Plot a kernel density estimate for the histogram and show as a line')
        parser.add_argument(
           '--nofill', action='store_true', required=False,
            help=f'Use unfilled histogram bars instead of solid coloured bars')
        parser.add_argument(
           '--element', choices=const.ALLOWED_HISTOGRAM_ELEMENTS, default=const.DEFAULT_HISTOGRAM_ELEMENT,
           help=f'Style of histogram bars. Allowed values: %(choices)s. Default: %(default)s')
        parser.add_argument(
           '--stat', choices=const.ALLOWED_HISTOGRAM_STATS, default=const.DEFAULT_HISTOGRAM_STAT, required=False,
           help=f'Statistic to use for each bin. Allowed values: %(choices)s. Default: %(default)s')
        parser.add_argument(
           '--indnorm', action='store_true', required=False,  
           help=f'For normalised statistics (e.g. percent), normalise each histogram in the plot independently, otherwise normalise over the full dataset')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        if options.bins:
            kwargs['bins'] = options.bins
        if options.binwidth:
            kwargs['binwidth'] = options.binwidth
        if options.multiple:
            kwargs['multiple'] = options.multiple
        if options.kde:
            kwargs['kde'] = options.kde
        log_axes = [False, False]
        if options.logx:
            log_axes[0] = True
            del options.logx
        if options.logy:
            log_axes[1] = True 
            del options.logy
        kwargs['log_scale'] = tuple(log_axes) 
        graph = sns.displot(kind='hist', data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                cumulative=options.cumulative,
                hue_order=options.hueorder,
                element=options.element,
                fill=not(options.nofill),
                stat=options.stat,
                common_norm=not(options.indnorm),
                facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class LinePlot(CommandBase, name="line"):
    description = "Line plot of numerical feature."
    category = "plotting"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap,
               plot_args.vlines, plot_args.hlines],
           add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.relplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                hue_order=options.hueorder, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.vlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.vlines:
                    ax.axvline(pos)
        if options.hlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.hlines:
                    ax.axhline(pos)
        render_plot.render_plot(options, graph, self.name)
        return df


class PointPlot(CommandBase, name="point"):
    description = "Point plot of numerical feature."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap],
           add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class ScatterPlot(CommandBase, name="scatter"):
    description = "Scatter plot of two numerical columns."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[ io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap,
               plot_args.dotsize, plot_args.dotalpha, plot_args.dotlinewidth, plot_args.dotstyle, plot_args.dotsizerange,
               plot_args.vlines, plot_args.hlines],
            add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        facet_kws = { 'legend_out': True }
        kwargs = {}
        sizes = None
        if options.dotsizerange is not None:
            sizes=tuple(options.dotsizerange)
        graph = sns.relplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                style=options.dotstyle, sizes=sizes, size=options.dotsize, alpha=options.dotalpha,
                hue_order=options.hueorder, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.vlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.vlines:
                    ax.axvline(pos)
        if options.hlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.hlines:
                    ax.axhline(pos)
        render_plot.render_plot(options, graph, self.name)
        return df


class LMPlot(CommandBase, name="lmplot"):
    description = "Regression plot"
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[ io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, 
               plot_args.logx, plot_args.xlim, plot_args.ylim, plot_args.colwrap,
               plot_args.dotsize, plot_args.dotalpha, plot_args.dotlinewidth, plot_args.dotstyle, plot_args.dotsizerange],
            add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        facet_kws = { 'legend_out': True }
        kwargs = {}
        #scatter_kws = { 'style': options.dotstyle }
        scatter_kws = {}
        graph = sns.lmplot(data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                hue_order=options.hueorder, scatter_kws=scatter_kws, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class StripPlot(CommandBase, name="strip"):
    description = "Plot distrbution of numerical column using dotted strip."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap],
            add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class SwarmPlot(CommandBase, name="swarm"):
    description = "Plot distrbution of numerical column using dot swarm."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap],
            add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df


class ViolinPlot(CommandBase, name="violin"):
    description = "Plot distrbution of numerical column using violin."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap,
               plot_args.strip],
            add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.strip:
            graph.map_dataframe(sns.stripplot, data=df, x=options.xaxis, y=options.yaxis, alpha=0.8, color="black")
        render_plot.render_plot(options, graph, self.name) 
        return df


class CountPlot(CommandBase, name="count"):
    description = "Plot count of categorical columns using bars."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[
               io_args.io_arguments, plot_args.make_plot_arguments(),
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap],
           add_help=False)
        options = parser.parse_args(args)
        if options.xaxis is not None and options.yaxis is not None:
            utils.exit_with_error("You cannot use both -x (--xaxis) and -y (--yaxis) at the same time in a count plot", const.EXIT_COMMAND_LINE_ERROR)
        if options.xaxis is None and options.yaxis is None:
            utils.exit_with_error("A count plot requires either -x (--xaxis) OR -y (--yaxis) to be specified", const.EXIT_COMMAND_LINE_ERROR)
        self.options = options

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        _width, height_inches, aspect = utils.plot_dimensions_inches(options.width, options.height) 
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=height_inches, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df
