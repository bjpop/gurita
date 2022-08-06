'''
Module      : io_arguments 
Description : Common I/O command line arguments for Gurita commands
Copyright   : (c) Bernie Pope, 16 Oct 2019-2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import gurita.constants as const

io_arguments = argparse.ArgumentParser()
io_arguments_group = io_arguments.add_argument_group('Input and Output', 'input/output related arguments that are provided across all gurita sub-commands') 

io_arguments_group.add_argument(
    '-o', '--out', metavar='FILE', type=str, nargs='?', required=False,
    help=f'Write output to a file. Use filename if provided, otherwise a filename will be automatically chosen.')

#io_arguments_group.add_argument(
#    '--prefix',  metavar='NAME', type=str,
#    required=False, 
#    help=f'Prefix for output file')

file_sep = argparse.ArgumentParser(add_help=False)
file_sep.add_argument(
    '--sep', metavar='STR', type=str, required=False, 
    help=f"Use STR as field separator for input/output tabular file. For TAB delimiter, use --sep '\\t'")

na = argparse.ArgumentParser(add_help=False)
na.add_argument(
    '--na', metavar='STR', type=str, required=False, default=const.DEFAULT_NA,
    help=f"Use STR as NA indicator when writing data to CSV or TSV file. Default: '%(default)s' (empty string)")

navalues = argparse.ArgumentParser(add_help=False)
navalues.add_argument(
    '--navalues', metavar='STR', required=False, type=str, nargs='+',
    help="Treat values in this space separated list as NA values. Example: --navalues '.' '-' '!'")
