[![travis](https://travis-ci.org/bjpop/hatch.svg?branch=master)](https://travis-ci.org/bjpop/hatch)

# Overview 

This program plots tabular data from input CSV (or TSV) files. Output plots are in PNG format. 

Hatch supports the following plot types:
 * Histograms (regular and cumulative)
 * Distributions (box and violin)
 * Scatter plots (with optional hue)
 * Line plots
 * Heatmaps

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

Common parameters:

```
$ hatch -h
$ hatch --help
usage: hatch [-h] [--outdir DIR] [--filetype FILETYPE] [--name NAME]
             [--version] [--log LOG_FILE] [--nolegend] [--filter EXPR]
             [--navalues STR]
             {hist,dist,scatter,line,heatmap} ...

Generate plots of tabular data

positional arguments:
  {hist,dist,scatter,line,heatmap}
                        sub-command help
    hist                Plot histograms of columns
    dist                Plot distributions of data
    scatter             Plot scatter of two numerical columns in data
    line                Plot line plots of columns
    heatmap             Plot a heatmap of two categories with numerical values

optional arguments:
  -h, --help            show this help message and exit
  --outdir DIR          Name of optional output directory.
  --filetype FILETYPE   Type of input file
  --name NAME           Name prefix for output files
  --version             show program's version number and exit
  --log LOG_FILE        record program progress in LOG_FILE
  --nolegend            Turn off the legend in the plot
  --filter EXPR         Filter rows: only retain rows that make this
                        expression True
  --navalues STR        Treat values in this space separated list as NA
                        values. Example: --navalues ". - !"
```

## Histograms

Plot distributions of selected columns as histograms.

```
$ hatch hist -h
usage: hatch hist [-h] --columns FEATURE [FEATURE ...] [--bins NUMBINS]
                  [--cumulative] [--logy]
                  DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --columns FEATURE [FEATURE ...]
                        Columns to plot
  --bins NUMBINS        Number of bins for histogram (default=100)
  --cumulative          Generate cumulative histogram
  --logy                Use a log scale on the vertical axis
```

For example, plot histograms of selected columns of the example iris.csv dataset using 10 bins. 

```
$ hatch hist --columns sepal_length sepal_width petal_length petal_width --bins 10 -- iris.csv
```

Outputs go to:

```
iris.petal_length.histogram.png
iris.petal_width.histogram.png
iris.sepal_length.histogram.png
iris.sepal_width.histogram.png
```

Below is the histogram plot for sepal length in the iris data set. 

![Example Iris sepal length histogram](images/iris.sepal_length.histogram.png =500x400)

## Distributions

```
$ hatch dist -h
usage: hatch dist [-h] --columns FEATURE [FEATURE ...] --group FEATURE
                  [FEATURE ...] [--logy] [--type {box,violin}]
                  DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --columns FEATURE [FEATURE ...]
                        Columns to plot
  --group FEATURE [FEATURE ...]
                        Plot distributions of of the columns where data are
                        grouped by these features
  --logy                Use a log scale on the vertical axis
  --type {box,violin}   Type of plot, default(box)

```

For example, plot distributions of selected columns, grouped by their species, using violin plots:

```
hatch dist --columns sepal_length sepal_width petal_length petal_width --group species --type violin -- iris.csv
```

Outputs go to:

```
iris.petal_length.species.dist.png
iris.petal_width.species.dist.png
iris.sepal_length.species.dist.png
iris.sepal_width.species.dist.png
```

## Scatter plots

```
$ hatch scatter -h
usage: hatch scatter [-h] --pairs FEATURE,FEATURE [FEATURE,FEATURE ...]
                     [--hue FEATURE] [--size FEATURE] [--alpha ALPHA]
                     [--linewidth WIDTH]
                     DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --pairs FEATURE,FEATURE [FEATURE,FEATURE ...]
                        Pairs of features to plot, format: feature1,feature2
  --hue FEATURE         Name of feature (column headings) to use for colouring
                        dots
  --size FEATURE        Name of feature (column headings) to use for dot size
  --alpha ALPHA         Alpha value for plotting points (default: 0.3)
  --linewidth WIDTH     Line width value for plotting points (default: 0)
```

For example, scatter plots of "sepal_length verus sepal_width", "petal_length versus petal_width" and "sepal_length versus petal_length" with hue indicating species:
```
hatch scatter --pairs sepal_length,sepal_width petal_length,petal_width sepal_length,petal_length --hue species -- iris.csv 
```

Outputs go to:
```
iris.petal_length.petal_width.scatter.png
iris.sepal_length.petal_length.scatter.png
iris.sepal_length.sepal_width.scatter.png
```

## Heatmaps

```
$ hatch heatmap -h
usage: hatch heatmap [-h] [--cmap COLOR_MAP_NAME] --rows FEATURE --columns
                     FEATURE --values FEATURE [--log]
                     DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --cmap COLOR_MAP_NAME
                        Use this color map, will use Seaborn default if not
                        specified
  --rows FEATURE        Interpret this feature (column of data) as the rows of
                        the heatmap
  --columns FEATURE     Interpret this feature (column of data) as the columns
                        of the heatmap
  --values FEATURE      Interpret this feature (column of data) as the values
                        of the heatmap
  --log                 Use a log scale on the numerical data

```

For example, 
```
hatch heatmap --rows year --columns month --values passengers -- flights.csv
```

Output will go to:
```
flights.year.month.passengers.heatmap.png
```

# Filtering rows

The `--filter` command line option allows you to select rows to be included in the plot (with unselected rows excluded).
It takes a Python expression as its argument. Any rows that make the expression True are included in the plot, and all other
rows are excluded. The syntax of the expression follows the Pandas style.

In the following command we select only those rows where the value in the `species` column is not equal to `setosa` (that is we exclude all
rows for setosa).

```
hatch --filter "data.species != 'setosa'" scatter --pairs sepal_length,sepal_width petal_length,petal_width sepal_length,petal_length --hue species -- iris.csv
```

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
