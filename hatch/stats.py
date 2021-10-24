'''
Module      : Stats 
Description : Statistical calculations for Hatch 
Copyright   : (c) Bernie Pope, 16 Oct 2019-2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import logging
import pandas as pd
import numpy as np
from itertools import combinations
import math
import scipy
from hatch.command_base import CommandBase
import hatch.utils as utils
import hatch.constants as const

class IsNorm(CommandBase, name="isnorm"):
    description = "Test whether numerical features differ from a normal distribution."
    category = "transformation"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-c', '--columns', metavar='FEATURE', nargs="*", type=str, required=False,
        help=f'Select only these columns (columns)')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        selected_df = df

        if options.columns is not None:
            utils.validate_columns_error(df, options.columns)
            selected_df = df[options.columns]

        # select only the numeric columns
        selected_df = selected_df.select_dtypes(include=np.number)
        selected_columns = selected_df.columns

        out_columns = []
        out_stats = []
        out_p_values = []

        # process each column in turn, computing normaltest 
        # we do each column separately so that we can handle NAs independently in each column
        for column in selected_columns:
            this_column = df[column]
            this_notna = this_column.dropna()
            k2, p_value = scipy.stats.normaltest(this_notna) 
            out_columns.append(column)
            out_stats.append(k2)
            out_p_values.append(p_value)

        result_df = pd.DataFrame({'column': out_columns, 'statistic': out_stats, 'p_value': out_p_values})
        return result_df


class Correlation(CommandBase, name="corr"):
    description = "Pairwise correlation between numerical columns." 
    category = "transformation"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-c', '--columns', metavar='FEATURE', nargs="*", type=str, required=False,
        help=f'Select only these columns (columns)')
        parser.add_argument('--method', required=False, default=const.DEFAULT_CORR_METHOD, choices=const.ALLOWED_CORR_METHODS,
        help=f'Method for determining correlation. Allowed values: %(choices)s. Default: %(default)s.')

        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        if options.columns is not None:
            utils.validate_columns_error(df, options.columns)
            df = df[options.columns]
        df = df.corr(method=options.method).reset_index()
        return df


# XXX we should bundle various summary stats together, so you can ask for a bunch of them at once,
# rather than one at a time

def stdev(df, options):
    if options.columns is not None:
        columns = options.columns
        utils.check_df_has_columns(df, columns)
    else:
        numeric_df = df.select_dtypes(include=np.number)
        columns = list(numeric_df.columns)
    print("column,stdev")
    for f in columns:
        val = df[f].std()
        print(f"{f},{val}")
