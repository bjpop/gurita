'''
Module      : heatmap 
Description : Heatmap plot of two features 
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
