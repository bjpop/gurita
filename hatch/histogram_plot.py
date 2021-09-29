'''
Module      : histogram_plot 
Description : Create a histogram plot from the data 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import seaborn as sns
import hatch.render_plot as render_plot
import hatch.io_arguments as io_args 
import hatch.plot_arguments as plot_args 
import hatch.constants as const
from hatch.command_base import CommandBase

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
