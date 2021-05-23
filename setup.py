#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''
Plot taular data on the comand line.
'''


setup(
    name='hatch',
    version='0.1.0.0',
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
    install_requires=["numpy==1.18.2", "scipy==1.4.1", "pandas==0.25.2",
        "seaborn==0.11.0", "matplotlib==3.3.2", "numexpr==2.7.1", "scikit-learn==0.23.1"]
)
