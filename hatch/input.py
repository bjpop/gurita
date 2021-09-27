'''
Module      : input.py 
Description : Read a CSV/TSV file in from stdin or a named file 
Copyright   : (c) Bernie Pope, 27 September 2021 
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
import pandas as pd

class Stdin(CommandBase, name="stdin"):
    description = "Read a CSV/TSV file from standard input."
    category = "input/output"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args=[]):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.file_format, io_args.na, io_args.navalues], add_help=True)
        self.options = parser.parse_args(args)

    def run(self, _df_ignore):
        options = self.options
        if options.navalues:
            na_values = options.navalues.split()
        else:
            na_values = None
        sep = ',' 
        if options.format == 'tsv':
            sep = "\t"
        elif options.format == 'csv':
            sep = ','
        dtype = None
        df = pd.read_csv(sys.stdin, sep=sep, keep_default_na=True, na_values=na_values, dtype=dtype)
        return df

class In(CommandBase, name="in"):
    description = "Read CSV/TSV data from a named input file." 
    category = "input/output"

    def __init__(self):
        self.options = None

    def parse_args(self, args=[]):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.file_format, io_args.na, io_args.navalues], add_help=True)
        parser.add_argument('input_file', metavar='FILE', type=str, 
            help=f'Read input from a named file.')
        self.options = parser.parse_args(args)

    def run(self, _df_ignore):
        options = self.options
        if options.navalues:
            na_values = options.navalues.split()
        else:
            na_values = None
        sep = None
        maybe_filetype = utils.get_filetype_from_extension(options.input_file)
        if options.format == 'TSV':
            sep = "\t"
        elif options.format == 'CSV':
            sep = ','
        elif maybe_filetype == 'TSV':
            sep = "\t"
        elif maybe_filetype == 'CSV':
            sep = ","
        try:
            dtype = None
            #if options.category:
            #   dtype = { column : 'category' for column in options.category }
            df = pd.read_csv(options.input_file, sep=sep, keep_default_na=True, na_values=na_values, dtype=dtype)
        except IOError:
            utils.exit_with_error(f"Could not open or read from file: {options.input_file}", const.EXIT_FILE_IO_ERROR)
        return df
