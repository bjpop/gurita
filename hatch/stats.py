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
    category = "summary information"

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
        if options.columns is not None:
            columns = options.columns
            valid_columns, invalid_columns = utils.validate_columns(df, columns)
        else:
            numeric_df = df.select_dtypes(include=np.number)
            valid_columns = list(numeric_df.columns)
        if valid_columns:
            print("column,statistic,p-value")
            for f in valid_columns:
                k2, p_value = scipy.stats.normaltest(df[f]) 
                print(f"{f},{k2},{p_value}")
        else:
            print(f"\n{self.name} command: no valid columns were specified in the data")
        if invalid_columns:
            print(f"\n{self.name} command: following requested columns are not in the data:")
            print("\n".join(invalid_columns))
        return df


class Correlation(CommandBase, name="corr"):
    description = "Test for pairwise correlation between numerical columns." 
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
            valid_columns = utils.validate_columns_error(df, options.columns)
            if valid_columns:
                df = df[valid_columns]
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
