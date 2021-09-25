'''
Module      : sample_rows 
Description : Randomly sample rows 
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import math

class SampleRows:
    def __init__(self):
        self.options = None

    def run(self, df):
        num = self.options.num
        if num >= 1:
            # clamp the sample size to be within the number of rows in the table
            # the sample method returns an empty result otherwise
            sample_size = min(math.trunc(num), len(data.index))
            df = data.sample(n=sample_size)
        elif 0 < num < 1:
            df = df.sample(frac = num)
        else:
            utils.exit_with_error(f"Sample argument {options.sample} out of range. Must be > 0", const.EXIT_COMMAND_LINE_ERROR)
        return df

    def parse_args(self, args):
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument(
            'num', metavar='NUM', type=float,
            help='Sample rows from the input data, if NUM >= 1 then sample NUM rows, if 0 <= NUM < 1, then sample NUM fraction of rows')

        # XXX Catch exceptions here
        self.options = parser.parse_args(args)
