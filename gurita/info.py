'''
Module      : describe 
Description : Display summary information about the columns in the current data frame 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import pandas as pd
from gurita.command_base import CommandBase
import gurita.utils as utils
import gurita.constants as const 

class Describe(CommandBase, name="describe"):
    description = "Show summary information about the input data set."
    category = "summary information"
    
    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--col', metavar='COLUMN', nargs="*", type=str, required=False,
            help=f'Select only these columns')


    def run(self, df):
        options = self.options
        rows, cols = df.shape
        pd.set_option('display.max_columns', None)
        if options.col:
            utils.validate_columns_error(df, options.col)
            print(df[options.col].describe(include='all'))
        else:
            print(df.describe(include='all'))
        return df


class Pretty(CommandBase, name="pretty"):
    description = "Pretty print a fragment of the data set."
    category = "summary information"
    
    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--col', metavar='COLUMN', nargs="*", type=str, required=False,
            help=f'Select only these columns')
        self.optional.add_argument(
            '--maxrows', metavar='NUM', type=int, required=False, default=const.DEFAULT_PRETTY_MAX_ROWS,
            help=f'Maximum number of rows to pretty print. Default: %(default)s.')
        self.optional.add_argument(
            '--maxcols', metavar='NUM', type=int, required=False, default=const.DEFAULT_PRETTY_MAX_COLS,
            help=f'Maximum number of columns to pretty print. Default: %(default)s.')


    def run(self, df):
        options = self.options
        selected_df = df
        if options.col:
            utils.validate_columns_error(df, options.col)
        print(selected_df.to_string(columns=options.col, header=True, max_rows=options.maxrows, max_cols=options.maxcols, show_dimensions=False, index=False))
        nrows, ncols = df.shape
        print(f"\n[{nrows} rows x {ncols} columns]")
        return df


class Dtype(CommandBase, name="dtype"):
    """
    Command to inspect the data types of columns in the dataset.
    Defaults to showing all columns if no specific column is provided.
    """
    description = "Show the data type of every column, or specified columns."
    category = "summary information"
    
    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--col', metavar='COLUMN', nargs="*", type=str, required=False,
            help=f'Select only these columns to show dtypes')

    def run(self, df):
        options = self.options
        
        # If specific columns are specified, validate them; otherwise, default to all columns
        if options.col:
            utils.validate_columns_error(df, options.col)
            target_cols = options.col
        else:
            target_cols = df.columns
            print("--- All Columns Dtypes ---")
        for col in target_cols:
            print(f"{col}: {df[col].dtype}")   
        return df


class Info(CommandBase, name="info"):
    """
    Command to perform a dataset health check, displaying summary statistics
    such as row/column counts, non-null values, dtypes, and memory usage.
    """
    description = "Show a concise summary of the dataset including rows, columns, non-null counts, and dtypes."
    category = "summary information"
    
    def __init__(self):
        super().__init__()

    def run(self, df):
        total_rows, total_cols = df.shape 
        print(f"<class 'pandas.core.frame.DataFrame'>")
        print(f"Total Rows: {total_rows} entries")
        print(f"Total Columns: {total_cols} columns")
        print("-" * 60)
        print(f"{'Column':<25} | {'Non-Null Count':<15} | {'Dtype'}")
        print("-" * 60)    
        for col in df.columns:
            non_null_count = df[col].count()
            dtype = df[col].dtype
            print(f"{col:<25} | {non_null_count} non-null     | {dtype}")
        print("-" * 60)
        # Calculate overall memory usage in kilobytes
        mem_usage = df.memory_usage(deep=True).sum() / 1024
        print(f"Memory Usage: {mem_usage:.2f} KB")
        return df


#class Unique(CommandBase, name="unique"):
#    description = "Get the unique values from a column."
#    category = "transformation"
#    
#    def __init__(self):
#        super().__init__()
#        self.optional.add_argument(
#            '-c', '--col', metavar='COLUMN', type=str, required=True,
#            help=f'Select unique items from this column')
#        self.optional.add_argument(
#            '--sort', action='store_true',
#            default=False, required=False,
#            help=f'Sort the items in ascending order')
#
#
#    def run(self, df):
#        options = self.options
#        utils.check_df_has_columns(df, [options.col])
#        this_unique = df[options.col].unique()
#        new_column_name = '_'.join([options.col, 'unique'])
#        unique_df = pd.DataFrame({new_column_name: this_unique})
#        return unique_df 
