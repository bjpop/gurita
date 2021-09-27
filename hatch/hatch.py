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
import hatch.box_plot
import hatch.boxen_plot
import hatch.violin_plot
import hatch.swarm_plot
import hatch.strip_plot
import hatch.bar_plot
import hatch.point_plot
import hatch.scatter_plot
import hatch.histogram_plot
import hatch.count_plot
import hatch.line_plot
import hatch.filter_rows
import hatch.sample_rows
import hatch.output
import hatch.input
import hatch.pca
import hatch.eval
import hatch.describe
import hatch.cut
import hatch.stats

def init_logging(log_filename):
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
                            level=logging.INFO,
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
        return (type_first_command is hatch.input.In) or (type_first_command is hatch.input.Stdin)
    else:
        return False


def is_last_command_transform(commands):
    if len(commands) > 0:
        return commands[-1].category == 'transformation'
    else:
        return False


def main():
    df = None
    commands = args.parse_commandline()
    if not is_first_command_input(commands):
        # If the first command is not an explict read of input data
        # either from stdin or a file then we add an implicit read from 
        # stdin to the command stream
        stdin_reader = hatch.input.Stdin()
        stdin_reader.parse_args()
        commands = [stdin_reader] + commands
    if is_last_command_transform(commands):
        # If the last command is a data transformation command then
        # we add an implicit print to stdout to the command stream
        stdout_writer = hatch.output.Stdout()
        stdout_writer.parse_args()
        commands = commands + [stdout_writer]
    for command in commands:
        try:
            df = command.run(df)
        except ValueError as e:
            utils.exit_with_error(f"Error: {str(e)}", const.EXIT_COMMAND_LINE_ERROR)
    logging.info("Completed")
    exit(0)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
