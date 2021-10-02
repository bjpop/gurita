'''
Module      : transform 
Description : Commands for transforming the data set 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import math
import argparse
from itertools import chain, repeat
import pandas as pd
from hatch.command_base import CommandBase
import hatch.utils as utils
from hatch.constants import PROGRAM_NAME
import hatch.constants as const

class Cut(CommandBase, name="cut"):
    description = "Select a subset of columns by name." 
    category = "transformation"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-c', '--columns', metavar='NAME', nargs="+", type=str, required=False,
        help=f'Select only these named columns')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        if options.columns is not None:
            columns = options.columns
            valid_columns, invalid_columns = utils.validate_columns(df, columns)
            if valid_columns:
                df = df[valid_columns]
            else:
                print(f"{PROGRAM_NAME} {self.name} WARNING: no valid columns were specified")
                # return None as the result, we should stop here 
                df = None 
            if invalid_columns:
                print(f"{PROGRAM_NAME} {self.name} WARNING: the following requested columns are not in the data, and could not be selected:")
                print("\n".join(invalid_columns))
        return df


class Eval(CommandBase, name="eval"):
    description = "Compute new columns for each row with an expression."
    category = "transformation" 
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument('expr', metavar='EXPR', type=str, nargs="+",
            help='Construct new data columns based on an expression')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        try:
            eval_str = '\n'.join(options.expr)
            df = df.eval(eval_str)
        except:
            utils.exit_with_error(f"Bad eval expression: {options.expr}", const.EXIT_COMMAND_LINE_ERROR)
        return df


class FilterRows(CommandBase, name="filter"):
    description = "Filter rows with a logical expression."
    category = "transformation"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument('expr', metavar='EXPR', type=str,
            help='Filter rows: only retain rows that make this expression True')
        self.options = parser.parse_args(args)

    def run(self, df):
        try:
            df = df.query(self.options.expr)
        except:
            utils.exit_with_error(f"Bad filter expression: {options.filter}", const.EXIT_COMMAND_LINE_ERROR)
        return df


class Melt(CommandBase, name="melt"):
    description = "Reshape a wide format dataset into a long format dataset."
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
    description = "Reshape a long format dataset into a wide format dataset."
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


class SampleRows(CommandBase, name="sample"):
    description = "Randomly sample rows."
    category = "transformation"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-n', '--num', metavar='NUM', type=float,
            help='Sample rows from the input data, if NUM >= 1 then sample NUM rows, if 0 <= NUM < 1, then sample NUM fraction of rows')
        self.options = parser.parse_args(args)

    def run(self, df):
        num = self.options.num
        if num >= 1:
            # clamp the sample size to be within the number of rows in the table
            # the sample method returns an empty result otherwise
            sample_size = min(math.trunc(num), len(df.index))
            df = df.sample(n=sample_size)
        elif 0 < num < 1:
            df = df.sample(frac = num)
        else:
            utils.exit_with_error(f"Sample argument {options.sample} out of range. Must be > 0", const.EXIT_COMMAND_LINE_ERROR)
        return df


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
        ordering = get_sort_ordering(options.columns, options.order)
        utils.validate_columns_error(df, options.columns)
        df = df.sort_values(by=options.columns, na_position=options.napos, ascending=ordering)
        return df
    

# True means ascend, False means descend
def get_sort_ordering(columns, order):
    pairs = zip(columns, chain(order, repeat(const.DEFAULT_SORT_ORDER)))
    return [code == const.DEFAULT_SORT_ORDER for (col, code) in pairs]


class Tail(CommandBase, name="tail"):
    description = "Select the last N rows in the data." 
    category = "transformation"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-n', '--num', metavar='NUM', nargs="?", type=int, required=False,
            default=const.DEFAULT_TAIL_NUM,
            help=f'Number of trailing rows to select. If NUM is negative then select all rows except the first NUM rows')
        self.options = parser.parse_args(args)

    def run(self, df):
        return df.tail(self.options.num)
    
class Head(CommandBase, name="head"):
    description = "Select the first N rows in the data." 
    category = "transformation"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-n', '--num', metavar='NUM', nargs="?", type=int, required=False,
            default=const.DEFAULT_TAIL_NUM,
            help=f'Number of leading rows to select. If NUM is negative then select all rows except the last NUM rows')
        self.options = parser.parse_args(args)

    def run(self, df):
        return df.head(self.options.num)
    

#class Transpose(CommandBase, name="transpose"):
#    description = "Transpose the data." 
#    category = "transformation"
#    
#    def __init__(self):
#        self.options = None
#
#    def parse_args(self, args):
#        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
#        self.options = parser.parse_args(args)
#
#    def run(self, df):
#        return df.transpose().reset_index()
    
