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


class BarPlot(CommandBase, name="bar"):
    description = "Bar plot of categorical feature."
    category = "plotting"

    def __init__(self):
        pass

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
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
            parents=[io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
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
            parents=[io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
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


class Heatmap(CommandBase, name="heatmap"):
    description = "Heatmap of two categorical columns." 
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
        graph = sns.heatmap(data=pivot_data, cmap=self.options.cmap)
        render_plot.render_plot(options, graph, self.name)
        return df


class HistogramPlot(CommandBase, name="histogram"):
    description = "Histogram of numerical or categorical feature."
    category = "plotting"

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.plot_arguments,
               plot_args.x_argument, plot_args.y_argument, plot_args.hue, plot_args.row, plot_args.col,
               plot_args.order, plot_args.hue_order, plot_args.orient,
               plot_args.logx, plot_args.logy, plot_args.xlim, plot_args.ylim, plot_args.colwrap],
           add_help=False)
        parser.add_argument(
            '--multiple', required=False, choices=const.ALLOWED_HIST_MULTIPLES,
            help=f"How to display overlapping subsets of data in a histogram. Allowed values: %(choices)s.")
        parser.add_argument(
            '--bins', metavar='NUM', required=False, type=int,
            help=f'Number of histogram bins.')
        parser.add_argument(
            '--binwidth', metavar='NUM', required=False, type=float,
            help=f'Width of histogram bins, overrides "--bins".')
        parser.add_argument(
            '--cumulative', action='store_true',
            help=f'Generate cumulative histogram')
        parser.add_argument(
           '--kde', action='store_true',
            help=f'Plot a kernel density estimate for the histogram and show as a line')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sns.set_style(options.plotstyle)
        sns.set_context(options.context)
        facet_kws = { 'legend_out': True }
        kwargs = {}
        aspect = 1
        if options.bins:
            kwargs['bins'] = options.bins
        if options.binwidth:
            kwargs['binwidth'] = options.binwidth
        if options.width > 0:
            aspect = options.width / options.height
        if options.multiple:
            kwargs['multiple'] = options.multiple
        if options.kde:
            kwargs['kde'] = options.kde
        graph = sns.displot(kind='hist', data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
                cumulative=options.cumulative,
                hue_order=options.hueorder,
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
            parents=[io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        facet_kws = { 'legend_out': True }
        kwargs = {}
        graph = sns.relplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
                hue_order=options.hueorder, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        if options.vlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.vlines:
                    ax.axvline(pos)
        if options.hlines is not None:
            for ax in graph.axes.ravel():
                for pos in options.hlines:
                    ax.axhline(pos)
        render_plot.facet_plot(options, graph, self.name)
        return df


class PointPlot(CommandBase, name="point"):
    description = "Point plot of numerical feature."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
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
            parents=[ io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        facet_kws = { 'legend_out': True }
        kwargs = {}
        graph = sns.relplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
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


class StripPlot(CommandBase, name="strip"):
    description = "Plot distrbution of numerical column using dotted strip."
    category = "plotting"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
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
            parents=[io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
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
            parents=[io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
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
               io_args.io_arguments, plot_args.plot_arguments,
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
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.name, data=df,
                x=options.xaxis, y=options.yaxis, col=options.col, row=options.row,
                height=options.height, aspect=aspect, hue=options.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        render_plot.render_plot(options, graph, self.name)
        return df
