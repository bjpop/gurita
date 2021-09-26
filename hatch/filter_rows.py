'''
Module      : filter_rows 
Description : Filter (retain) rows in the data using a logical expression 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
from hatch.command_base import CommandBase

class FilterRows(CommandBase, name="filter"):
    description = "Filter rows with a logical expression."
    category = "transformation"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument('expr', metavar='EXPR', type=str,
            help='Filter rows: only retain rows that make this expression True')
        self.options = parser.parse_args(args)

    def run(self, df):
        try:
            df = df.query(self.options.expr)
        except:
            utils.exit_with_error(f"Bad filter expression: {options.filter}", const.EXIT_COMMAND_LINE_ERROR)
        return df
