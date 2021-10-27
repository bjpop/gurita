'''
Module      : io.py 
Description : Read/write a CSV/TSV file in/out from stdin or a named file 
Copyright   : (c) Bernie Pope, 27 September 2021 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import sys
import pandas as pd
from pathlib import Path
from hatch.command_base import CommandBase
import hatch.io_arguments as io_args
import hatch.utils as utils
import hatch.constants as const


class Stdin(CommandBase, name="stdin"):
    description = "Read a CSV/TSV file from standard input."
    category = "input/output"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args=[]):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.file_format, io_args.navalues], add_help=True)
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
            parents=[io_args.file_format, io_args.navalues], add_help=True)
        parser.add_argument('input', metavar='FILE', type=str, help=f'Read input from a named file.')
        self.options = parser.parse_args(args)

    def run(self, _df_ignore):
        options = self.options
        if options.navalues:
            na_values = options.navalues.split()
        else:
            na_values = None
        sep = None
        maybe_filetype = utils.get_filetype_from_extension(options.input)
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
            df = pd.read_csv(options.input, sep=sep, keep_default_na=True, na_values=na_values, dtype=dtype)
        except IOError:
            utils.exit_with_error(f"Could not open or read from file: {options.input}", const.EXIT_FILE_IO_ERROR)
        return df


class Stdout(CommandBase, name="stdout"):
    description = "Print the current dataset to the standard output in CSV/TSV format."
    category = "input/output"
    
    def __init__(self):
        self.options = None

    def parse_args(self, args=[]):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.file_format, io_args.na], add_help=True)
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
    description = "Write the current dataset to a file in CSV/TSV format."
    category = "input/output"

    def __init__(self):
        self.options = None

    def parse_args(self, args=[]):
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
