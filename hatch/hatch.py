'''
Module      : Main
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX

A plotting and data analytics program for the command line
'''

import sys
import logging
import pandas as pd
from hatch.command_base import CommandBase
import hatch.args as args
import hatch.utils as utils
import hatch.constants as const
import hatch.plot
import hatch.transform
import hatch.io
import hatch.pca
import hatch.info
import hatch.stats
import hatch.cluster

def init_logging(log_filename=None):
    '''If the log_filename is defined, then
    initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: either None, if logging is not required, or the
            string name of the log file to write to
    Result:
        None
    '''
    if log_filename is not None:
        logging.basicConfig(filename=log_filename,
                            #level=logging.INFO,
                            level=logging.CRITICAL,
                            filemode='w',
                            format='%(asctime)s %(levelname)s - %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S')
        logging.info('program started')
        logging.info('command line: %s', ' '.join(sys.argv))
    else:
        logging.basicConfig(level=logging.CRITICAL)


def is_first_command_input(commands):
    if len(commands) > 0:
        first_command = commands[0]
        type_first_command = type(first_command)
        return (type_first_command is hatch.io.In) or (type_first_command is hatch.io.Stdin)
    else:
        return False


def is_last_command_transform_or_input(commands):
    if len(commands) > 0:
        last_command = commands[-1]
        type_last_command = type(last_command)
        return (last_command.category == 'transformation') or (type_last_command is hatch.io.In) or (type_last_command is hatch.io.Stdin)
    else:
        return False

# stdin may only be used at most once, and only at the beginning of the command sequence
def stdin_used_safely(commands):
    count = 0
    for command in commands:
        if type(command) is hatch.io.Stdin:
            count += 1
    if count == 0:
        return True
    elif count == 1:
        return type(commands[0] is hatch.io.Stdin)
    else:
        return False

def main():
    df = None
    original_commands = args.parse_commandline()
    new_commands = original_commands
    init_logging()
    if not is_first_command_input(original_commands):
        # If the first command is not an explict read of input data
        # either from stdin or a file then we add an implicit read from 
        # stdin to the command stream
        stdin_reader = hatch.io.Stdin()
        stdin_reader.parse_args()
        new_commands = [stdin_reader] + new_commands 
    if (len(original_commands) == 0) or is_last_command_transform_or_input(original_commands):
        # If the last command is a data transformation command or an input command then
        # we add an implicit print to stdout to the command stream
        stdout_writer = hatch.io.Stdout()
        stdout_writer.parse_args()
        new_commands = new_commands + [stdout_writer]
    if not stdin_used_safely(new_commands):
        utils.exit_with_error(f"stdin may only be used at most once, and only as the first command", const.EXIT_COMMAND_LINE_ERROR)
    else:
        for command in new_commands:
            try:
                df = command.run(df)
            except ValueError as e:
                utils.exit_with_error(f"Error: {str(e)}", const.EXIT_COMMAND_LINE_ERROR)
            if df is None:
                break
        logging.info("Completed")
        exit(0)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
