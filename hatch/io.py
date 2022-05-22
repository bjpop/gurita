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


class In(CommandBase, name="in"):
    description = "Read CSV/TSV data from a named input file or standard input" 
    category = "input/output"

    def __init__(self):
        self.options = None

    def parse_args(self, args=[]):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.file_format, io_args.navalues], add_help=True)
        parser.add_argument('input', nargs="?", metavar='FILE', type=str, help=f'Read input from a named file. If this argument is absent input will be read from standard input (stdin).')
        self.options = parser.parse_args(args)

    def is_stdin(self):
        return self.options.input is None

    def run(self, _df_ignore):
        options = self.options
        kwargs = {}
        if options.navalues:
            kwargs['na_values'] = options.navalues
            kwargs['keep_default_na'] = False
        else:
            kwargs['keep_default_na'] = True 
        #if options.category:
        #   dtype = { column : 'category' for column in options.category }
        sep = "," 
        maybe_filetype = None
        input_file = sys.stdin
        input_file_description = "stdin"
        if options.input is not None:
            maybe_filetype = utils.get_filetype_from_extension(options.input)
            input_file = options.input
            input_file_description = options.input
        if options.format is not None:
            if options.format.lower() == 'tsv':
                sep = "\t"
            elif options.format.lower() == 'csv':
                sep = ','
        elif maybe_filetype is not None:
            if maybe_filetype.lower() == 'tsv':
                sep = "\t"
            elif maybe_filetype.lower() == 'csv':
                sep = ","
        try:
            df = pd.read_csv(input_file, sep=sep, **kwargs)
        except IOError:
            utils.exit_with_error(f"Could not open or read from file: {input_file_description}", const.EXIT_FILE_IO_ERROR)
        return df


class Out(CommandBase, name="out"):
    description = "Write the dataset to a file or standard output in CSV/TSV format"
    category = "input/output"

    def __init__(self):
        self.options = None

    def is_stdout(self):
        return self.options.out is None

    def parse_args(self, args=[]):
        parser = argparse.ArgumentParser(usage=f'{self.name} -h | {self.name} <arguments>',
            parents=[io_args.file_format, io_args.na], add_help=True)
        parser.add_argument('out', metavar='FILE', type=str, nargs='?',
            help=f'Write data to a file. If this argument is absent output will be written to standard output (stdout)')

        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        sep = "," 
        maybe_filetype = None
        if options.out is not None:
            maybe_filetype = utils.get_filetype_from_extension(options.out)
            output_file = options.out
            output_file_description = options.out
        else:
            output_file = sys.stdout
        if options.format is not None:
            if options.format.lower() == 'tsv':
                sep = '\t'
            elif options.format.lower() == 'csv':
                sep = ','
        elif maybe_filetype is not None:
            if maybe_filetype.lower() == 'tsv':
                sep = '\t'
            elif maybe_filetype.lower() == 'csv':
                sep = ","
        try:
            df.to_csv(output_file, sep=sep, na_rep=options.na, index=False)
        except IOError:
            utils.exit_with_error(f"Could not open or write to file: {output_file_description}", const.EXIT_FILE_IO_ERROR)
        return df
