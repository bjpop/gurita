[![travis](https://travis-ci.org/bjpop/hatch.svg?branch=master)](https://travis-ci.org/bjpop/hatch)

# Overview 

This program plots tabular data from input CSV (or TSV) files. Output plots are in PNG format. 

In the examples below, `$` indicates the command line prompt.

# Licence

This program is released as open source software under the terms of [MIT License](https://raw.githubusercontent.com/bjpop/hatch/master/LICENSE).

# Installing

You can install hatch directly from the source code or build and run it from within Docker container.

## Installing directly from source code

Clone this repository: 
```
$ git clone https://github.com/bjpop/hatch
```

Move into the repository directory:
```
$ cd hatch
```

Python 3 is required for this software.

Base_counter can be installed using `pip` in a variety of ways (`$` indicates the command line prompt):

1. Inside a virtual environment:
```
$ python3 -m venv hatch_dev
$ source hatch_dev/bin/activate
$ pip install -U /path/to/hatch
```
2. Into the global package database for all users:
```
$ pip install -U /path/to/hatch
```
3. Into the user package database (for the current user only):
```
$ pip install -U --user /path/to/hatch
```


## Building the Docker container 

The file `Dockerfile` contains instructions for building a Docker container for hatch.

If you have Docker installed on your computer you can build the container like so:
```
$ docker build -t hatch .
```
See below for information about running hatch within the Docker container.

# General behaviour


# Running within the Docker container

The following section describes how to run hatch within the Docker container. It assumes you have Docker installed on your computer and have built the container as described above. 
The container behaves in the same way as the normal version of hatch, however there are some Docker-specific details that you must be aware of.

The general syntax for running hatch within Docker is as follows:
```
$ docker run -i hatch CMD
```
where CMD should be replaced by the specific command line invocation of hatch. Specific examples are below.

Display the help message:
```
$ docker run -i hatch hatch -h
```
Note: it may seem strange that `hatch` is mentioned twice in the command. The first instance is the name of the Docker container and the second instance is the name of the hatch executable that you want to run inside the container.

Display the version number:
```
$ docker run -i hatch hatch --version
```

Read from a single input FASTA file redirected from standard input:
```
$ docker run -i hatch hatch < file.CSV
```

Read from multuple input FASTA files named on the command line, where all the files are in the same directory. You must replace `DATA` with the absolute file path of the directory containing the FASTA files:  
```
$ docker run -i -v DATA:/in hatch hatch /in/file1.fasta /in/file2.fasta /in/file3.fasta
```
The argument `DATA:/in` maps the directory called DATA on your local machine into the `/in` directory within the Docker container.

Logging progress to a file in the directory OUT: 
```
$ docker run -i -v DATA:/in -v OUT:/out hatch-c hatch --log /out/logfile.txt /in/file1.fasta /in/file2.fasta /in/file3.fasta
```
Replace `OUT` with the absolute path of the directory to write the log file. For example, if you want the log file written to the current working directory, replace `OUT` with `$PWD`.
As above, you will also need to replace `DATA` with the absolite path to the directory containing your input FASTA files.

# Testing

## Unit tests

You can run the unit tests for hatch with the following commands:
```
$ cd hatch/python/hatch
$ python -m unittest -v hatch_test
```

## Test suite


# Bug reporting and feature requests

Please submit bug reports and feature requests to the issue tracker on GitHub:

[hatch issue tracker](https://github.com/bjpop/hatch/issues)
