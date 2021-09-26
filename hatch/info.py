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
        parser = argparse.ArgumentParser(add_help=True)
        self.options = parser.parse_args(args)

    def run(self, df):
        rows, cols = df.shape
        pd.set_option('display.max_columns', None)
        #if options.features is not None:
        #    df = df[options.features]
        print(df.describe(include='all'))
        return df
