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
            parents=[io_args.file_sep, io_args.navalues], add_help=True)
        parser.add_argument('--comment', metavar='CHAR', required=False, type=str,
            help=f'If provided, CHAR marks the start of a comment. Text from this CHAR until the end of the line will be ignored.') 
        parser.add_argument('input', nargs="?", metavar='FILE', type=str, help=f'Read input from a named file. If this argument is absent input will be read from standard input (stdin).')
        self.options = parser.parse_args(args)

    def is_stdin(self):
        return self.options.input is None

    def run(self, _df_ignore):
        options = self.options
        kwargs = {}
        if options.comment is not None:
            if len(options.comment) != 1:
                utils.exit_with_error(f"Comment marker must be exactly one character. Supplied comment marker had length: {len(options.comment)}", const.EXIT_COMMAND_LINE_ERROR)
            kwargs['comment'] = options.comment
        # Ensure that the separator is set to the default. It may be overridden below.
        kwargs['sep'] = const.DEFAULT_SEP
        if options.navalues:
            kwargs['na_values'] = options.navalues
            kwargs['keep_default_na'] = False
        else:
            kwargs['keep_default_na'] = True 
        #if options.category:
        #   dtype = { column : 'category' for column in options.category }
        input_file = sys.stdin
        input_file_description = "stdin"
        if options.input is not None:
            # Read input from a named file and try to guess separator from filename extension (.csv, .tsv)
            maybe_sep = utils.get_sep_from_extension(options.input)
            if maybe_sep is not None:
                kwargs['sep'] = maybe_sep 
            input_file = options.input
            input_file_description = options.input
        if options.sep is not None:
            # If the user specifies a separator to use it overrides anything else, including whatever may
            # be inferred from the name of the file
            kwargs['sep'] = utils.decode_escapes(options.sep)
        try:
            df = pd.read_csv(input_file, **kwargs)
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
            parents=[io_args.file_sep, io_args.na], add_help=True)
        parser.add_argument('out', metavar='FILE', type=str, nargs='?',
            help=f'Write data to a file. If this argument is absent output will be written to standard output (stdout)')

        self.options = parser.parse_args(args)

    def run(self, df):
        options = self.options
        kwargs = {}
        kwargs['sep'] = const.DEFAULT_SEP
        kwargs['na_rep'] = options.na
        kwargs['index'] = False
        if options.out is not None:
            # Write output from a named file and try to guess separator from filename extension (.csv, .tsv)
            maybe_sep = utils.get_sep_from_extension(options.out)
            if maybe_sep is not None:
                kwargs['sep'] = maybe_sep
            output_file = options.out
            output_file_description = options.out
        else:
            output_file = sys.stdout
        if options.sep is not None:
            # If the user specifies a separator to use it overrides anything else, including whatever may
            # be inferred from the name of the file
            kwargs['sep'] = utils.decode_escapes(options.sep)
        try:
            df.to_csv(output_file, **kwargs)
        except IOError:
            utils.exit_with_error(f"Could not open or write to file: {output_file_description}", const.EXIT_FILE_IO_ERROR)
        return df
