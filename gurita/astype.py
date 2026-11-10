'''
Module      : astype
Description : Force column type conversions in the pipeline for Gurita
Copyright   : (c) Bernie Pope, 16 Oct 2019-2021
License     : MIT
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''


import pandas as pd
from gurita.command_base import CommandBase

class Astype(CommandBase, name="astype"):
    name = "astype"
    category = "data transformation"
    description = "Force column type conversions"

    def __init__(self):
        super().__init__()
        self.columns = []
        self.target_type = None

    def parse_args(self, args):
        """
        Parse command line arguments for astype.
        Supports both positional arguments (e.g., astype patient_group categorical)
        and named arguments (e.g., astype --column patient_group --type categorical).
        """
        parser = self.parser
        
        # Named arguments
        parser.add_argument(
            '-c', '--column', 
            dest='named_columns', 
            action='append', 
            help='Target column name (can be specified multiple times)'
        )
        parser.add_argument(
            '-t', '--type', 
            dest='target_type_named', 
            choices=['categorical', 'numerical', 'datetime'],
            help='Target data type (named)'
        )

        # Catch all remaining positional arguments
        parser.add_argument(
            'pos_args', 
            nargs='*', 
            help='Positional columns followed by target data type'
        )

        parsed_args = parser.parse_args(args)

        # 1. Determine target type (prioritize named type)
        self.target_type = parsed_args.target_type_named

        # 2. Collect columns
        self.columns = []
        if parsed_args.named_columns:
            self.columns.extend(parsed_args.named_columns)

        # 3. Parse positional arguments robustly
        # If target_type not set via flags, check if the last positional arg is a valid type
        valid_types = {'categorical', 'numerical', 'datetime'}
        pos_args = parsed_args.pos_args

        if pos_args:
            if not self.target_type and pos_args[-1] in valid_types:
                self.target_type = pos_args[-1]
                cols = pos_args[:-1]
            else:
                cols = pos_args
            self.columns.extend(cols)
            
    def run(self, df):
        """
        Convert specified columns to a target type with robust error handling (errors='coerce').
        """
        if not self.target_type or not self.columns:
            return df

        for col in self.columns:
            if col in df.columns:
                if self.target_type == 'categorical':
                    df[col] = df[col].astype('category')
                elif self.target_type == 'numerical':
                    # Convert to numeric, forcing unconvertible values to NaN instead of dropping rows
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                elif self.target_type == 'datetime':
                    # Convert to datetime, forcing unconvertible values to NaT (NaN)
                    df[col] = pd.to_datetime(df[col], errors='coerce')
        return df