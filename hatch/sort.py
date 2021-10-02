'''
Module      : sort 
Description : Sort the data based on one or more columns 
Copyright   : (c) Bernie Pope, 2 October 2021 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import pandas as pd
from hatch.command_base import CommandBase
import hatch.utils as utils
import hatch.constants as const
from itertools import chain, repeat

class Sort(CommandBase, name="sort"):
    description = "Sort based on columns in precedence from left to right." 
    category = "transformation"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-c', '--columns', metavar='NAME', nargs="+", type=str, required=True,
            help=f'Sort the data by these columns in precedence from left to right')
        parser.add_argument(
            '--napos', metavar='POS', type=str, required=False, choices=const.ALLOWED_SORT_NAPOS,
            default=const.DEFAULT_SORT_NAPOS,
            help=f'Ordering for missing (NA) values. Allowed values: %(choices)s. Default: %(default)s.')
        parser.add_argument(
            '--order', metavar='ORDER', type=str, nargs='+', required=False,
            choices=const.ALLOWED_SORT_ORDER, default=const.DEFAULT_SORT_ORDER,
            help=f'Ordering to use for sort. Allowed values: %(choices)s. a=ascending, d=descending. Default: %(default)s. The choices match with the specified columns to use for sorting (-c|--columns). If len(--order) < len(-c|--columns) the remaining columns will default to ascending order.')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        ordering = get_ordering(options.columns, options.order)
        print(ordering)
        utils.validate_columns_error(df, options.columns)
        df = df.sort_values(by=options.columns, na_position=options.napos, ascending=ordering)
        return df
    

# True means ascend, False means descend
def get_ordering(columns, order):
    pairs = zip(columns, chain(order, repeat(const.DEFAULT_SORT_ORDER)))
    return [code == const.DEFAULT_SORT_ORDER for (col, code) in pairs]
