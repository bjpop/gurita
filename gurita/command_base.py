'''
Module      : command_base
Description : base class for command classes, allows plugin-style definition of new commands 
Copyright   : (c) Bernie Pope, 26 September 2021 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import gurita.constants as const
import argparse 

class CommandBase:
    command_map = {}

    def __init_subclass__(cls, name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.name = name
        cls.command_map[name] = cls

    def __init__(self, parser_parents=[]):
        self.options = None
        self.parser = argparse.ArgumentParser(prog=f'{const.PROGRAM_NAME} {self.name}', description=self.description, add_help=False, parents=parser_parents)
        self.required = self.parser.add_argument_group('required arguments')
        self.optional = self.parser.add_argument_group('optional arguments')
        self.optional.add_argument( '-h', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')

    def parse_args(self, args=[]):
        self.options = self.parser.parse_args(args)
