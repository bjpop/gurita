'''
Module      : out.py 
Description : Print the current dataframe to stdout or a file
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import sys
import hatch.io_arguments as io_args
import hatch.utils as utils
from pathlib import Path
from hatch.command_base import CommandBase

class Stdout(CommandBase, name="stdout"):
    description = "Print the current dataset to the standard output."
    category = "input/output"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.file_format, io_args.na], add_help=False)
        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sep = None
        if options.format == 'tsv':
            sep = "\t"
        elif options.format == 'csv':
            sep = ','
        df.to_csv(sys.stdout, sep=sep, na_rep=options.na, index=False)
        return df

class Out(CommandBase, name="out"):
    name = "out" 
    description = "Write the current dataset to a file"
    category = "input/output"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.file_format, io_args.na], add_help=True)
        parser.add_argument('out', metavar='FILE', type=str, nargs='?',
            help=f'Write output to a file. Use filename if provided, otherwise a filename will be automatically chosen.')
        parser.add_argument('--prefix',  metavar='NAME', type=str, required=False, help=f'Prefix for output file')

        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sep = None
        suffix = None
        if options.format == 'tsv':
            sep = '\t'
            suffix = 'tsv'
        elif options.format == 'csv':
            sep = ','
            suffix = 'csv'
        output_name = make_output_filename(options) 
        df.to_csv(output_name, sep=sep, na_rep=options.na, index=False)
        return df

def make_output_filename(options):
    if options.out is not None:
        # don't try to make this unique, just use what user specified, they may want to overwrite the old file
        return Path(options.out)
    else:
        extension = [options.format]
        output_name = [utils.get_output_name(options)]
        path = Path('.'.join(output_name + extension))
        return utils.make_unique_numbered_filepath(path)
