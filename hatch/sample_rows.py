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
from hatch.command_base import CommandBase

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
