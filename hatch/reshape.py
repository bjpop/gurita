'''
Module      : reshape 
Description : Reshape data using melt and pivot 
Copyright   : (c) Bernie Pope, 30 September 2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import pandas as pd
from hatch.command_base import CommandBase
import hatch.constants as const
import hatch.utils as utils

class Melt(CommandBase, name="melt"):
    description = "Reshape a wide format dataset into a long format dataset. Opposite of pivot."
    category = "transformation"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-i', '--ids', metavar='NAME', nargs="*", type=str, required=False,
            help=f'Select these "identifier" columns to remain unmelted')
        parser.add_argument(
            '-v', '--vals', metavar='NAME', nargs="*", type=str, required=False,
            help=f'Select these "variable" columns to be melted')
        parser.add_argument(
            '--varname', metavar='NAME', type=str, required=False, default=const.DEFAULT_MELT_VARNAME,
            help=f'Use this name for the new "variable" column. Default: "%(default)s."')
        parser.add_argument(
            '--valname', metavar='NAME', type=str, required=False, default=const.DEFAULT_MELT_VALNAME,
            help=f'Use this name for the new "value" column. Default: "%(default)s."')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        if options.ids:
            utils.validate_columns_error(df, options.ids)
        if options.vals:
            utils.validate_columns_error(df, options.vals)
        df = df.melt(id_vars=options.ids, value_vars=options.vals, var_name=options.varname, value_name=options.valname)
        return df


class Pivot(CommandBase, name="pivot"):
    description = "Reshape a long format dataset into a wide format dataset. Opposite of melt."
    category = "transformation"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-i', '--index', metavar='NAME', nargs='+', type=str, required=False,
            help=f'Select these columns as the index')
        parser.add_argument(
            '-v', '--vals', metavar='NAME', nargs='+', type=str, required=False,
            help=f'Column(s) to be used to populate the values in the result')
        parser.add_argument(
            '-c', '--cols', metavar='NAME', nargs='+', type=str, required=True,
            help=f'Column(s) to be used to make new columns in the result')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        if options.index and type(options.index) == list:
            utils.validate_columns_error(df, options.index)
            if len(options.index) == 1:
                options.index = options.index[0]
        if options.vals and type(options.vals) == list:
            utils.validate_columns_error(df, options.vals)
            if len(options.vals) == 1:
                options.vals = options.vals[0]
        if options.cols and type(options.cols) == list:
            utils.validate_columns_error(df, options.cols)
            if len(options.cols) == 1:
                options.cols = options.cols[0]
        df = df.pivot(index=options.index, columns=options.cols, values=options.vals).reset_index()
        # Flatten a multi-index column index if one is created
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.to_flat_index().map(combine_index_names)
        return df

def combine_index_names(items):
    return '_'.join([x for x in items if x])
