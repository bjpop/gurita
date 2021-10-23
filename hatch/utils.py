'''
Module      : Utils 
Description : General utilities for the Hatch program 
Copyright   : (c) Bernie Pope, 16 Oct 2019
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import sys
import logging
from pathlib import Path
import hatch.constants as const


# convert cm measurement to inches
def plot_dimensions_inches(width, height):
    width_inches = cm_to_inches(width)
    height_inches = cm_to_inches(height)
    aspect = 1
    if width > 0:
         aspect = width / height
    return width_inches, height_inches, aspect

# convert cm measurement to inches
def cm_to_inches(cm):
    return cm * 0.393701

def check_df_has_columns(df, columns):
    bad_columns = set()
    for f in columns:
        if f not in df.columns:
            bad_columns.add(f)
    if bad_columns:
        column_str = ", ".join(bad_columns)
        exit_with_error(f"Feature(s) not in data: {column_str}",
                const.EXIT_COMMAND_LINE_ERROR)

def validate_columns(df, columns):
    valid_columns = []
    invalid_columns = []
    for f in columns:
        if f in df:
           valid_columns.append(f)
        else:
           invalid_columns.append(f)
    return valid_columns, invalid_columns

def validate_columns_error(df, columns):
    invalid_columns = []
    for f in columns:
        if f not in df:
           invalid_columns.append(f)
    if invalid_columns:
        bad_columns_str = ', '.join(invalid_columns)
        exit_with_error(f"The following requested columns are not in the data: {bad_columns_str}", const.EXIT_COMMAND_LINE_ERROR)


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}; exiting".format(const.PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def get_filetype_from_extension(filename):
    path = Path(filename)
    if path.suffix.upper() == '.TSV':
        return 'TSV'
    elif path.suffix.upper() == '.CSV':
        return 'CSV'
    else:
        return None


def get_output_name(options):
    if options.prefix:
        return options.prefix
    elif options.out is not None:
        return options.out
    else:
        return const.DEFAULT_OUTPUT_NAME

def output_field(options, field):
    if hasattr(options, field) and getattr(options, field) is not None:
        return [getattr(options, field).replace(' ', '_')]
    else:
        return [] 


def make_unique_numbered_filepath(path):
    stem = path.stem
    ext = path.suffix 
    counter = 1
    while path.exists():
        path = Path(stem + "_" + str(counter) + ext)
        counter += 1
    return path
