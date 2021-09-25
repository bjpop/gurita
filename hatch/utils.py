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

def check_df_has_features(df, features):
    bad_features = set()
    for f in features:
        if f not in df.columns:
            bad_features.add(f)
    if bad_features:
        feature_str = ", ".join(bad_features)
        exit_with_error(f"Feature(s) not in data: {feature_str}",
                const.EXIT_COMMAND_LINE_ERROR)


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
    elif options.file is not None:
        return options.file 
    else:
        return const.DEFAULT_OUTPUT_NAME

def output_field(field):
    return [field.replace(' ', '_')] if field is not None else []


def make_unique_numbered_filepath(path):
    stem = path.stem
    ext = path.suffix 

    print((stem, ext))
    counter = 1

    while path.exists():
        path = Path(stem + "_" + str(counter) + ext)
        counter += 1

    return path
