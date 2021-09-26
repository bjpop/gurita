'''
Module      : command_base
Description : base class for command classes, allows plugin-style definition of new commands 
Copyright   : (c) Bernie Pope, 26 September 2021 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

class CommandBase:
    command_map = {}

    def __init_subclass__(cls, name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.name = name
        cls.command_map[name] = cls
