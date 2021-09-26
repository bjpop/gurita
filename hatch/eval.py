'''
Module      : eval 
Description : Compute new columns for each row based on existing columns
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import hatch.utils as utils
import hatch.constants as const
from hatch.command_base import CommandBase

class Eval(CommandBase, name="eval"):
    description = "Compute new columns for each row based on existing columns with an expression."
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
