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
        "numpy==1.22.2",
        "scipy==1.8.0",
        "pandas==1.5.2",
        "seaborn==0.11.2",
        "matplotlib==3.4.2",
        "numexpr==2.7.3",
        "scikit-learn==0.24.2",
    ]
)
