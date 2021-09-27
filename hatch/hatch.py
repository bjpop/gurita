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
import hatch.info
import hatch.columns

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


def read_data(commands):
    input_file = sys.stdin
    sep = ","
    na_values = None
    try:
        dtype = None
        #if options.category:
        #   dtype = { column : 'category' for column in options.category }
        data = pd.read_csv(input_file, sep=sep, keep_default_na=True, na_values=na_values, dtype=dtype)
        return data
    except IOError:
        utils.exit_with_error(f"Could not open file: {options.data}", const.EXIT_FILE_IO_ERROR)

'''
def read_data(options):
    if options.navalues:
        na_values = options.navalues.split()
    else:
        na_values = None

    if options.data is not None:
        input_file = options.data
        maybe_filetype = utils.get_filetype_from_extension(input_file)
        if options.filetype == 'TSV':
            sep = "\t"
        elif options.filetype == 'CSV':
            sep = ','
        elif maybe_filetype == 'TSV':
            sep = "\t"
        elif maybe_filetype == 'CSV':
            sep = ","
        else: 
            utils.exit_with_error(f'Cannot deduce input file type: {input_file}. Either rename file or use the --filetype flag', const.EXIT_FILE_IO_ERROR)
    else:
        input_file = sys.stdin
        sep = ","
        if options.filetype == "TSV":
           sep = "\t"
    try:
        dtype = None
        #if options.category:
        #   dtype = { column : 'category' for column in options.category }
        data = pd.read_csv(input_file, sep=sep, keep_default_na=True, na_values=na_values, dtype=dtype)
    except IOError:
        utils.exit_with_error(f"Could not open file: {options.data}", const.EXIT_FILE_IO_ERROR)
    if options.eval:
        try:
            eval_str = '\n'.join(options.eval)
            data = data.eval(eval_str)
        except:
            utils.exit_with_error(f"Bad eval expression: {options.eval}", const.EXIT_COMMAND_LINE_ERROR)
    # optionally filter rows of the data
    if options.filter:
        try:
            data = data.query(options.filter)
        except:
            utils.exit_with_error(f"Bad filter expression: {options.filter}", const.EXIT_COMMAND_LINE_ERROR)
    # optionally randomly sample the rows of data
    if options.sample is not None:
        if options.sample >= 1:
            # clamp the sample size to be within the number of rows in the table
            # the sample method returns an empty result otherwise
            sample_size = min(math.trunc(options.sample), len(data.index))
            data = data.sample(n = sample_size)
        elif 0 < options.sample < 1:
            data = data.sample(frac = options.sample)
        else:
            utils.exit_with_error(f"Sample argument {options.sample} out of range. Must be > 0", const.EXIT_COMMAND_LINE_ERROR)
    # optionally select only certain columns
    # we do this at the end so that filter expressions can refer to the full set of columns
    if options.features is not None:
        bad_features = []
        for f in options.features: 
            if f not in data.columns:
                bad_features.append(f)
        if bad_features:
            bad_features_str = ",".join(bad_features)
            utils.exit_with_error(f"These features are not in the input: {bad_features_str}", const.EXIT_COMMAND_LINE_ERROR)
        else:
            data = data[options.features]
    return data 
'''

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
        stdin_reader.parse_args([])
        commands = [stdin_reader] + commands
    if is_last_command_transform(commands):
        # If the last command is a data transformation command then
        # we add an implicit print to stdout to the command stream
        stdout_writer = hatch.output.Stdout()
        stdout_writer.parse_args([])
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
