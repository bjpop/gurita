'''
Module      : Args 
Description : Command line argument parsing for Hatch
Copyright   : (c) Bernie Pope, 16 Oct 2019-2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import sys
import logging
import os
from pathlib import Path
import itertools
import hatch.constants as const
import hatch.utils as utils

# the special characer used to separate commainds in a chain
SUBCOMMAND_SEPARATOR = "+"

USAGE_MESSAGE = '''Hatch is a data analytics and plotting program.

Display a help message or the version number and exit:

    hatch [-h|--help] [-v|--version]

Display the help message for a subcommand and exit:

    hatch subcommand -h

Run a single subcommand with optional arguments:

    hatch subcommand <args>

Run a chain of subcommands from left to right:

    hatch subcommand <args> + ... + subcommand <args>

Available subcommands:

    Input / output
    --------------

    in                  Read data from a named file
    out                 Save data to a named file
    stdout              Print data to the standard output (stdout)

    Plotting: 
    ---------

    bar                 Bar plot of categorical feature
    box                 Box plot of numerical feature
    boxen               Boxen plot of numerical feature
    clustermap          Clustered heatmap of two numerical features 
    count               Count plot of categorical feature
    heatmap             Heatmap of two numerical features 
    hist                Histogram of numerical or categorical feature 
    line                Line plot of numerical feature
    point               Point plot of numerical feature
    scatter             Scatter plot of two numerical features
    strip               Strip plot of numerical feature
    swarm               Swarm plot of numerical feature
    violin              Violin plot of numerical feature

    Transformation:
    ---------------

    filter              filter rows with a logical expression
    sample              randomly sample rows
    eval                compute new columns for each row based on existing columns
    features            select columns (features) to retain by name and discard the rest 

    Data reduction:
    ------------------

    pca                 Principal component analysis (PCA)

    Statistics:
    -----------

    correlation         Correlation between numerical features
    info                Show summary information about features in the input data set
    normtest            Test whether numerical features differ from a normal distribution 
    stdev               Compute the standard deviation of numerical features
'''

def display_usage():
    print(USAGE_MESSAGE)

def display_version():
    pring("version")


'''
Command line syntax is:

    hatch [-h] [-v]

    hatch subcommand -h

    hatch subcommand <args>

    hatch subcommand <args> + subcommand <args> + ... + subcommand <args>

    Example:

    hatch filter 'size >= 10' + \
          pca -f size class type age pos + \
          cluster -f pc1 pc2 + \
          scatter -x pc1 -y pc2 --hue chrom < data.csv
'''

# split list into non-empty sublists based on seperator
def split_list(this_list, sep):
   return [list(group) for is_sep, group in itertools.groupby(this_list, lambda word: word == sep) if not is_sep]

def parse_commandline(command_map):
    fields = sys.argv[1:]

    if len(fields) >= 1:

        if fields[0] in ['-h', '--help']:
            display_usage()
            exit(0)

        if fields[0] in ['-v', '--version']:
            display_version()
            exit(0)

        result = []
        for command_fields in split_list(fields, SUBCOMMAND_SEPARATOR):
            if len(command_fields) > 0:
                command_name = command_fields[0]
                command_args = command_fields[1:]
            if command_name in command_map:
                # this could raise a parse error, need to handle it here
                this_command = command_map[command_name]()
                this_command.parse_args(command_args)
                result.append(this_command)
            else:
                utils.exit_with_error(f"Unrecognised subcommand: {command_name}", const.EXIT_COMMAND_LINE_ERROR)
        return result 

    else:
        display_usage()
        exit(0)
