'''
Module      : strip_plot 
Description : Create a strip plot from the data 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import seaborn as sns
import hatch.render_plot as render_plot
import hatch.io_arguments as io_args 
import hatch.plot_arguments as plot_args 
import argparse
from hatch.command_base import CommandBase

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
