'''
Module      : Args 
Description : Command line argument parsing for Gurita
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
import gurita.constants as const
import gurita.utils as utils
from gurita.command_base import CommandBase

# the special characer used to separate commainds in a chain
SUBCOMMAND_SEPARATOR = "+"

USAGE_HEADER = '''Gurita is a data analytics and plotting program.

Display a help message or the version number and exit:

    gurita [-h|--help] [-v|--version]

Display the help message for a command and exit:

    gurita command -h

Run a single command with optional arguments:

    gurita command <args>

Run a chain of commands from left to right, each separated by '+' character:

    gurita command_1 <args> + ... + command_n <args>
'''

def display_usage():
    print(USAGE_HEADER)
    display_commands()

JUSTIFY_WIDTH = 20

def display_commands():
    category_map = {cat : [] for cat in const.COMMAND_CATEGORIES}
    # Group any commands that are not in the standard categories into 'other'
    category_map['other'] = []

    for this_name, this_command in CommandBase.command_map.items():
        this_category = this_command.category
        this_description = this_command.description

        if this_category in category_map:
            category_map[this_category].append((this_name, this_description))
        else:
            category_map['other'].append((this_name, this_description))

    print("Available commands:")
    print()

    for this_category in const.COMMAND_CATEGORIES:
        print(f"    {this_category}")
        print(f"    {'-' * len(this_category)}")
        print()
        for this_name, this_description in sorted(category_map[this_category], key=lambda pair: pair[0]):
            print(f"    {this_name.ljust(JUSTIFY_WIDTH, ' ')}{this_description}")
        print()
        if category_map['other']:
            for this_name, this_description in sorted(category_map['other'], key=lambda pair: pair[0]):
                print(f"{    this_name.ljust(JUSTIFY_WIDTH, ' ')}{this_description}")
            print()

def display_version():
    print(f"{const.PROGRAM_NAME} {const.PROGRAM_VERSION}")


'''
Command line syntax is:

    gurita [-h] [-v]

    gurita subcommand -h

    gurita subcommand <args>

    gurita subcommand <args> + subcommand <args> + ... + subcommand <args>

    Example:

    gurita filter 'size >= 10' + \
          pca -n 3 + \
          cluster -f pc1 pc2 + \
          scatter -x pc1 -y pc2 --hue cluster1 < data.csv
'''

# split list into non-empty sublists based on seperator
def split_list(this_list, sep):
   return [list(group) for is_sep, group in itertools.groupby(this_list, lambda word: word == sep) if not is_sep]


def parse_commandline(cmdline_args):
    fields = cmdline_args 
    command_map = CommandBase.command_map

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
                x = command_map[command_name]
                this_command = command_map[command_name]()
                this_command.parse_args(command_args)
                result.append(this_command)
            else:
                utils.exit_with_error(f"Unrecognised subcommand: {command_name}", const.EXIT_COMMAND_LINE_ERROR)
        return result 
    else:
        # An empty command line is ok
        return []
