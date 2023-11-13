'''
Module      : Stats 
Description : Statistical calculations for Gurita 
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
from gurita.command_base import CommandBase
import gurita.utils as utils
import gurita.constants as const

class Normtest(CommandBase, name="normtest"):
    description = "Test whether data in numerical column(s) differs from a normal distribution."
    category = "transformation"

    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--col', metavar='COLUMN', nargs="*", type=str, required=False,
            help=f'Select only these columns (columns)')
        self.optional.add_argument(
            '-m', '--method', choices=const.ALLOWED_NORMTEST_METHODS, 
            default=const.DEFAULT_NORMTEST_METHOD,
            help=f'Method for testing normality. Allowed values: %(choices)s. Default: %(default)s.')
        self.optional.add_argument(
            '-a', '--alpha', metavar='ALPHA', type=float, required=False,
            default=const.DEFAULT_NORMTEST_ALPHA,
            help=f'Threshold for significance. If p <= ALPHA then data is not normal. Default: %(default)s.')
        self.optional.add_argument(
            '-p', '--pvalue', action='store_true', default=False, 
            help=f'Include the p-value in the result') 
        self.optional.add_argument(
            '-s', '--stat', action='store_true', default=False, 
            help=f'Include the test statistic in the result') 


    def run(self, df):
        options = self.options
        selected_df = df

        if options.col is not None:
            utils.validate_columns_error(df, options.col)
            selected_df = df[options.col]

        # select only the numeric columns
        selected_df = selected_df.select_dtypes(include=np.number)
        selected_columns = selected_df.columns

        out_columns = []
        out_stats = []
        out_p_values = []
        out_is_normal = []

        # process each column in turn, computing normaltest 
        # we do each column separately so that we can handle NAs independently in each column
        for column in selected_columns:
            this_column = df[column]
            this_notna = this_column.dropna()
            k2 = None
            p_value = None
            if options.method == 'dagostino':
                k2, p_value = scipy.stats.normaltest(this_notna) 
            elif options.method == 'shapiro':
                k2, p_value = scipy.stats.shapiro(this_notna) 
            out_columns.append(column)
            out_stats.append(k2)
            out_p_values.append(p_value)
            out_is_normal.append(p_value > options.alpha)

        result_dict = {}
        result_dict['column'] = out_columns
        result_dict['is_normal'] = out_is_normal
        if options.pvalue:
            result_dict['p_value'] = out_p_values 
        if options.stat:
            result_dict['stat'] = out_stats 
        result_df = pd.DataFrame(result_dict)
        return result_df


class Correlation(CommandBase, name="corr"):
    description = "Pairwise correlation between numerical columns." 
    category = "transformation"

    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--col', metavar='COLUMN', nargs="*", type=str, required=False,
            help=f'Select only these columns (columns)')
        self.optional.add_argument('--method', required=False,
            default=const.DEFAULT_CORR_METHOD, choices=const.ALLOWED_CORR_METHODS,
            help=f'Method for determining correlation. Allowed values: %(choices)s. Default: %(default)s.')


    def run(self, df):
        options = self.options
        if options.col is not None:
            utils.validate_columns_error(df, options.col)
            df = df[options.col]
        corr_df_wide = df.corr(method=options.method).reset_index()
        corr_df_long = pd.melt(corr_df_wide, id_vars='index')
        return corr_df_long.rename(columns={"index": "col1", "variable": "col2", "value": "corr"})


class Zscore(CommandBase, name="zscore"):
    description = "Compute Z-score for numerical columns"
    category = "transformation"

    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--col', metavar='NAME', nargs="+", type=str, required=False,
            help=f'Select only these named columns. Only applies if --axis is "rows"')
        self.optional.add_argument(
            '--suffix', required=False, default=const.DEFAULT_ZSCORE_SUFFIX,
            help=f'Label suffix for new z-score columns. Default: %(default)s.')


    def run(self, df):
        options = self.options
        selected_df = df
        # optionally choose user specified columns
        if options.col is not None:
            utils.validate_columns_error(df, options.col)
            selected_df = df[options.col]

        # select only the numeric columns
        selected_df = selected_df.select_dtypes(include=np.number)
        selected_columns = selected_df.columns
        # process each column in turn, computing z-score, adding new columns to the df 
        # we do each column separately so that we can handle NAs independently in each column
        for column in selected_columns:
            this_column = df[column]
            this_notna = this_column.dropna()
            this_z = scipy.stats.zscore(this_notna)
            new_column = column + "_" + self.options.suffix
            df[new_column] = pd.Series(data=this_z, index=this_notna.index).reindex(df.index)
        return df


class Outlier(CommandBase, name="outlier"):
    description = "Detect outliers in numerical columns using interquartile range."
    category = "transformation"

    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--col', metavar='NAME', nargs="+", type=str, required=False,
            help=f'Select only these named columns. Only applies if --axis is "rows"')
        self.optional.add_argument(
            '--suffix', required=False, default=const.DEFAULT_OUTLIER_COLUMN,
            help=f'Label suffix for new outlier columns. Default: %(default)s.')
        self.optional.add_argument(
            '--iqrscale', metavar='S', required=False, type=float, default=const.DEFAULT_OUTLIER_IQR_SCALE,
            help=f'Scale factor S for determining outliers. x < (Q1 - S*IQR) or x > (Q3 + S*IQR). Larger values return fewer outliers. Default: %(default)s.')


    def run(self, df):
        options = self.options
        selected_df = df
        # optionally choose user specified columns
        if options.col is not None:
            utils.validate_columns_error(df, options.col)
            selected_df = df[options.col]

        # select only the numeric columns
        selected_df = selected_df.select_dtypes(include=np.number)
        selected_columns = selected_df.columns
 
        scale = options.iqrscale

        # process each column in turn, computing z-score, adding new columns to the df 
        # we do each column separately so that we can handle NAs independently in each column
        for column in selected_columns:
            this_column = selected_df[column]
            q1 = this_column.quantile(0.25)
            q3 = this_column.quantile(0.75)
            iqr = q3 - q1 
            outliers = (this_column < (q1 - scale * iqr)) | (this_column > (q3 + scale * iqr))
            new_column_label = column + "_" + options.suffix
            df[new_column_label] = outliers 
        return df


# XXX we should bundle various summary stats together, so you can ask for a bunch of them at once,
# rather than one at a time

def stdev(df, options):
    if options.col is not None:
        columns = options.col
        utils.check_df_has_columns(df, columns)
    else:
        numeric_df = df.select_dtypes(include=np.number)
        columns = list(numeric_df.columns)
    print("column,stdev")
    for f in columns:
        val = df[f].std()
        print(f"{f},{val}")
