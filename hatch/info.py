'''
Module      : info 
Description : Display summary information about the data in the current data frame 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import pandas as pd
from hatch.command_base import CommandBase

class Info(CommandBase, name="info"):
    description = "Show summary information about features in the input data set."
    category = "statistics"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>', add_help=True)
        parser.add_argument(
            '-f', '--features', metavar='FEATURE', nargs="+", required=False, type=str,
        help=f'Select only these features (columns)')
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        rows, cols = df.shape
        pd.set_option('display.max_columns', None)
        if options.features is not None:
            features = options.features
            valid_features = []
            invalid_features = []
            for f in features:
                if f in df:
                    valid_features.append(f)
                else:
                    invalid_features.append(f)
            print(df[valid_features].describe(include='all'))
            if invalid_features:
                print("\nThe following requested features are not in the data:")
                print("\n".join(invalid_features))
        else:
            print(df.describe(include='all'))
        return df
