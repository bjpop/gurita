#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''
Plot and analyse tabular data on the comand line.
'''


setup(
    name='gurita',
    version='1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['gurita'],
    package_dir={'gurita': 'gurita'},
    entry_points={
        'console_scripts': ['gurita = gurita.gurita:main']
    },
    url='https://github.com/bjpop/gurita',
    license='LICENSE',
    description=('Plot and analyse tabular data on the comand line.'),
    long_description=(LONG_DESCRIPTION),
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "seaborn",
        "matplotlib",
        "numexpr",
        "scikit-learn",
    ]
)
