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
import os
import math
from pathlib import Path
import numpy as np
import pandas as pd
import hatch.args as args
import hatch.utils as utils
import hatch.plot as plot
import hatch.constants as const
import hatch.stats as stats

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
                            level=logging.DEBUG,
                            filemode='w',
                            format='%(asctime)s %(levelname)s - %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S')
        logging.info('program started')
        logging.info('command line: %s', ' '.join(sys.argv))
    else:
        logging.basicConfig(level=logging.CRITICAL)


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
            data = data.sample(n = math.trunc(options.sample))
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

def save(options, df):
    if options.out:
        output_filename = options.out
    else:
        output_name = utils.get_output_name(options)
        output_filename = Path('.'.join([output_name, "trans", "csv"]))
    df.to_csv(output_filename, header=True, index=False)
    if options.verbose:
        print(f"Data saved to {output_filename}")

PLOT_COMMANDS = ['hist', 'count', 'box', 'violin', 'swarm', 'strip', 'boxen', 'bar', 'point', 'line', 'scatter', 'heatmap', 'clustermap', 'pca']

def main():
    options = args.parse_args()
    init_logging(options.logfile)
    # read and transform the input data (apply filters, sampling etc)
    df = read_data(options)
    if options.cmd == 'trans':
        save(options, df)
    elif options.cmd == 'info':
        stats.display_info(df, options)
    elif options.cmd == 'corr':
        stats.correlation(df, options)
    elif options.cmd == 'normtest':
        stats.norm_test(df, options)
    elif options.cmd in const.PLOT_COMMANDS:
        try:
            plot.do_plot(df, options)
        except TypeError as e:
            utils.exit_with_error(str(e), const.EXIT_COMMAND_LINE_ERROR)
    else:
        utils.exit_with_error(f"Unrecognised plot type: {options.cmd}", const.EXIT_COMMAND_LINE_ERROR)
    logging.info("Completed")


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
