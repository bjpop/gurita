'''
Module      : reshape 
Description : Reshape data using melt and pivot 
Copyright   : (c) Bernie Pope, 30 September 2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
from hatch.command_base import CommandBase
import hatch.constants as const
import hatch.utils as utils

class Melt(CommandBase, name="melt"):
    description = "Convert a wide format dataset into a long format dataset by reshaping columns."
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
            '--varname', metavar='NAME', nargs=1, type=str, required=False, default=const.DEFAULT_MELT_VARNAME,
            help=f'Use this name for the new "variable" column. Default: "%(default)s."')
        parser.add_argument(
            '--valname', metavar='NAME', nargs=1, type=str, required=False, default=const.DEFAULT_MELT_VALNAME,
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
