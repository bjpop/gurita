#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''
Plot taular data on the comand line.
'''


setup(
    name='hatch',
    version='1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['hatch'],
    package_dir={'hatch': 'hatch'},
    entry_points={
        'console_scripts': ['hatch = hatch.hatch:main']
    },
    url='https://github.com/bjpop/hatch',
    license='LICENSE',
    description=('Plot taular data on the comand line.'),
    long_description=(LONG_DESCRIPTION),
    install_requires=[
        "numpy==1.22.2",
        "scipy==1.8.0",
        "pandas==1.4.1",
        "seaborn==0.11.2",
        "matplotlib==3.4.2",
        "numexpr==2.7.3",
        "scikit-learn==0.24.2",
    ]
)
