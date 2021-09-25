'''
Module      : filter_rows 
Description : Filter (retain) rows in the data using a logical expression 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse

class FilterRows:
    def __init__(self):
        self.options = None

    def run(self, df):
        try:
            df = df.query(self.options.expr)
        except:
            utils.exit_with_error(f"Bad filter expression: {options.filter}", const.EXIT_COMMAND_LINE_ERROR)
        return df

    def parse_args(self, args):
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument('expr', metavar='EXPR', type=str,
            help='Filter rows: only retain rows that make this expression True')
        # XXX Catch exceptions here
        self.options = parser.parse_args(args)
