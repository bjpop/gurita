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
from hatch.command_base import CommandBase
import hatch.utils as utils

class Describe(CommandBase, name="describe"):
    description = "Show summary information about columns in the input data set."
    category = "information"
    
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
        rows, cols = df.shape
        pd.set_option('display.max_columns', None)
        if options.columns:
            columns = options.columns
            valid_columns, invalid_columns = utils.validate_columns(df, columns)
            if valid_columns:
                print(df[valid_columns].describe(include='all'))
            if invalid_columns:
                print(f"\n{self.name} command: following requested columns are not in the data:")
                print("\n".join(invalid_columns))
        else:
            print(df.describe(include='all'))
        return df
