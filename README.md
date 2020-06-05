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

Hatch can generate a number of differnt plot types, each of which can be selected on the command line:

```
$ hatch -h
usage: hatch [-h] {hist,dist,scatter,line,count,heatmap} ...

Generate plots of tabular data

optional arguments:
  -h, --help            show this help message and exit

Plot type:
  {hist,dist,scatter,line,count,heatmap}
                        sub-command help
    hist                Histograms of numerical data
    dist                Distributions of numerical data
    scatter             Scatter plots of numerical data
    line                Line plots of numerical data
    count               Counts (bar plots) of categorical data
    heatmap             Heatmap of two categories with numerical values

```

For example, if you want to plot a histogram, hatch can be invoked like so:

```
hatch hist ...
```

where `...` indicates the remaining arguments to the histogram plot.

Help messages for each plot type can be requested with `-h` or `--help` after the plot type. For example, to get specific help about histogram plots, use:

```
hatch hist -h
```

## Example test data

In the `data` directory in this repository we provide some sample test data for the sake of illustrating the plotting functionality of hatch.

The iris dataset is from the UCI Machine Learning Repository.
The CSV version was obtained from <a href="https://gist.github.com/curran/a08a1080b88344b0c8a7">Iris Data Set</a>, and can be found in the `data/iris.csv` file in this repository.

The flights dataset is from the `seaborn-data` repository that is used in the seaborn Python library documentation. The CSV version was obtaind from <a href="https://github.com/mwaskom/seaborn-data/blob/master/flights.csv">flights data</a>, and can be found in the `data/flights.csv` file in this repository.

The fmri dataset is from the `seaborn-data` repository that is used in the seaborn Python library documentation. The CSV version was obtaind from <a href="https://github.com/mwaskom/seaborn-data/blob/master/fmri.csv">fmri data</a>, and can be found in the `data/fmri.csv` file in this repository.

## Histograms

Plot distributions of selected columns as histograms.

```
$ hatch hist -h
usage: hatch hist [-h] [--outdir DIR] [--filetype FILETYPE] [--name NAME]
                  [--logfile LOG_FILE] [--nolegend] [--filter EXPR]
                  [--navalues STR] [--title STR] [--width SIZE]
                  [--height SIZE] --columns FEATURE [FEATURE ...] [--logy]
                  [--xlim LOW HIGH LOW HIGH] [--ylim LOW HIGH LOW HIGH]
                  [--bins NUMBINS] [--cumulative]
                  DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --outdir DIR          Name of optional output directory.
  --filetype FILETYPE   Type of input file
  --name NAME           Name prefix for output files
  --logfile LOG_FILE    record program progress in LOG_FILE
  --nolegend            Turn off the legend in the plot
  --filter EXPR         Filter rows: only retain rows that make this
                        expression True
  --navalues STR        Treat values in this space separated list as NA
                        values. Example: --navalues ". - !"
  --title STR           Plot title. By default no title will be added.
  --width SIZE          Plot width in inches (default: 10)
  --height SIZE         Plot height in inches (default: 8)
  --columns FEATURE [FEATURE ...]
                        Columns to plot
  --logy                Use a log scale on the veritical axis
  --xlim LOW HIGH LOW HIGH
                        Limit horizontal axis range to [LOW,HIGH]
  --ylim LOW HIGH LOW HIGH
                        Limit vertical axis range to [LOW,HIGH]
  --bins NUMBINS        Number of bins for histogram (default=100)
  --cumulative          Generate cumulative histogram
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

Below is a histogram plot for sepal length for the iris data set (iris.sepal_length.histogram.png):

<img src="images/iris.sepal_length.histogram.png" width="500" height="400">

## Distributions

```
$ hatch dist -h
usage: hatch dist [-h] [--outdir DIR] [--filetype FILETYPE] [--name NAME]
                  [--version] [--logfile LOG_FILE] [--nolegend]
                  [--filter EXPR] [--navalues STR] [--title STR]
                  [--width SIZE] [--height SIZE] --columns FEATURE
                  [FEATURE ...] [--logy] [--ylim LOW HIGH LOW HIGH] --group
                  FEATURE [FEATURE ...] [--type {box,violin}]
                  DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --outdir DIR          Name of optional output directory.
  --filetype FILETYPE   Type of input file
  --name NAME           Name prefix for output files
  --version             show program's version number and exit
  --logfile LOG_FILE    record program progress in LOG_FILE
  --nolegend            Turn off the legend in the plot
  --filter EXPR         Filter rows: only retain rows that make this
                        expression True
  --navalues STR        Treat values in this space separated list as NA
                        values. Example: --navalues ". - !"
  --title STR           Plot title. By default no title will be added.
  --width SIZE          Plot width in inches (default: 10)
  --height SIZE         Plot height in inches (default: 8)
  --columns FEATURE [FEATURE ...]
                        Columns to plot
  --logy                Use a log scale on the veritical axis
  --ylim LOW HIGH LOW HIGH
                        Limit vertical axis range to [LOW,HIGH]
  --group FEATURE [FEATURE ...]
                        Plot distributions of of the columns where data are
                        grouped by these features
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

Below is a distribution plot for sepal length grouped by species for the iris data set (iris.sepal_length.species.dist.png):

<img src="images/iris.sepal_length.species.dist.png" width="500" height="400">

## Scatter plots

```
$ hatch scatter -h
usage: hatch scatter [-h] [--outdir DIR] [--filetype FILETYPE] [--name NAME]
                     [--version] [--logfile LOG_FILE] [--nolegend]
                     [--filter EXPR] [--navalues STR] [--title STR]
                     [--width SIZE] [--height SIZE] --xy X,Y [X,Y ...]
                     [--logx] [--logy] [--xlim LOW HIGH LOW HIGH]
                     [--ylim LOW HIGH LOW HIGH] [--hue FEATURE]
                     [--size FEATURE] [--alpha ALPHA] [--linewidth WIDTH]
                     DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --outdir DIR          Name of optional output directory.
  --filetype FILETYPE   Type of input file
  --name NAME           Name prefix for output files
  --version             show program's version number and exit
  --logfile LOG_FILE    record program progress in LOG_FILE
  --nolegend            Turn off the legend in the plot
  --filter EXPR         Filter rows: only retain rows that make this
                        expression True
  --navalues STR        Treat values in this space separated list as NA
                        values. Example: --navalues ". - !"
  --title STR           Plot title. By default no title will be added.
  --width SIZE          Plot width in inches (default: 10)
  --height SIZE         Plot height in inches (default: 8)
  --xy X,Y [X,Y ...]    Pairs of features to plot, format: name1,name2
  --logx                Use a log scale on the horizontal axis
  --logy                Use a log scale on the veritical axis
  --xlim LOW HIGH LOW HIGH
                        Limit horizontal axis range to [LOW,HIGH]
  --ylim LOW HIGH LOW HIGH
                        Limit vertical axis range to [LOW,HIGH]
  --hue FEATURE         Name of feature (column headings) to use for colouring
                        dots
  --size FEATURE        Name of feature (column headings) to use for dot size
  --alpha ALPHA         Alpha value for plotting points (default: 0.3)
  --linewidth WIDTH     Line width value for plotting points (default: 0)
```

For example, scatter plots of "sepal_length verus sepal_width", "petal_length versus petal_width" and "sepal_length versus petal_length" with hue indicating species:
```
hatch scatter --xy sepal_length,sepal_width petal_length,petal_width sepal_length,petal_length --hue species -- iris.csv 
```

Outputs go to:
```
iris.petal_length.petal_width.scatter.png
iris.sepal_length.petal_length.scatter.png
iris.sepal_length.sepal_width.scatter.png
```

Below is the scatter plot for sepal length versus petal length with hue determined by species for the iris data set (iris.sepal_length.petal_length.scatter.png):

<img src="images/iris.sepal_length.petal_length.scatter.png" width="500" height="400">

## Line plots

```
$ hatch line -h
usage: hatch line [-h] [--outdir DIR] [--filetype FILETYPE] [--name NAME]
                  [--version] [--logfile LOG_FILE] [--nolegend]
                  [--filter EXPR] [--navalues STR] [--title STR]
                  [--width SIZE] [--height SIZE] --xy X,Y [X,Y ...] [--logy]
                  [--xlim LOW HIGH LOW HIGH] [--ylim LOW HIGH LOW HIGH]
                  [--overlay] [--hue FEATURE]
                  DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --outdir DIR          Name of optional output directory.
  --filetype FILETYPE   Type of input file
  --name NAME           Name prefix for output files
  --version             show program's version number and exit
  --logfile LOG_FILE    record program progress in LOG_FILE
  --nolegend            Turn off the legend in the plot
  --filter EXPR         Filter rows: only retain rows that make this
                        expression True
  --navalues STR        Treat values in this space separated list as NA
                        values. Example: --navalues ". - !"
  --title STR           Plot title. By default no title will be added.
  --width SIZE          Plot width in inches (default: 10)
  --height SIZE         Plot height in inches (default: 8)
  --xy X,Y [X,Y ...]    Pairs of features to plot, format: name1,name2
  --logy                Use a log scale on the veritical axis
  --xlim LOW HIGH LOW HIGH
                        Limit horizontal axis range to [LOW,HIGH]
  --ylim LOW HIGH LOW HIGH
                        Limit vertical axis range to [LOW,HIGH]
  --overlay             Overlay line plots on the same axes, otherwise make a
                        separate plot for each
  --hue FEATURE         Name of feature (column headings) to group data for
                        line plot
```

For example, a line plot for the fmri dataset showing the relationship between timepoint and signal with separate lines for the event column: 
```
hatch hatch line --xy timepoint,signal --hue event -- fmri.csv 
```

Outputs go to:
```
fmri.timepoint.signal.line.png
```

Below is the line plot for timepoint versus signal grouped by the even column (fmri.timepoint.signal.line.png):

<img src="images/fmri.timepoint.signal.line.png" width="500" height="400">

## Heatmaps

```
$ hatch heatmap -h
usage: hatch heatmap [-h] [--outdir DIR] [--filetype FILETYPE] [--name NAME]
                     [--version] [--logfile LOG_FILE] [--nolegend]
                     [--filter EXPR] [--navalues STR] [--title STR]
                     [--width SIZE] [--height SIZE] [--cmap COLOR_MAP_NAME]
                     --rows FEATURE --columns FEATURE --values FEATURE [--log]
                     DATA

positional arguments:
  DATA                  Filepaths of input CSV/TSV file

optional arguments:
  -h, --help            show this help message and exit
  --outdir DIR          Name of optional output directory.
  --filetype FILETYPE   Type of input file
  --name NAME           Name prefix for output files
  --version             show program's version number and exit
  --logfile LOG_FILE    record program progress in LOG_FILE
  --nolegend            Turn off the legend in the plot
  --filter EXPR         Filter rows: only retain rows that make this
                        expression True
  --navalues STR        Treat values in this space separated list as NA
                        values. Example: --navalues ". - !"
  --title STR           Plot title. By default no title will be added.
  --width SIZE          Plot width in inches (default: 10)
  --height SIZE         Plot height in inches (default: 8)
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

Below is a heatmap for the flights datset (flights.year.month.passengers.heatmap.png):

<img src="images/flights.year.month.passengers.heatmap.png" width="500" height="400">

# Filtering rows

The `--filter` command line option allows you to select rows to be included in the plot (with unselected rows excluded).
It takes a Python expression as its argument. Any rows that make the expression True are included in the plot, and all other
rows are excluded. The syntax of the expression follows the Pandas style.

Specifically it uses the notation provided by the [pandas.DataFrame.query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html).

In the following command we select only those rows where the value in the `species` column is not equal to `setosa` (that is we exclude all
rows for setosa).

```
hatch scatter --filter 'species != "setosa"' --xy sepal_length,sepal_width --hue species -- iris.csv
```

Note that column names can be written as if they are ordinary variables, such as `species` above. However, if a column name has spaces in it (or other characters not
allowed by Python variables) then it can be surround in back-tick characters, as in:

```
hatch scatter --filter '`species` != "setosa"' --xy sepal_length,sepal_width --hue species -- iris.csv
```

The query syntax also supports complex boolean expressions (essentially anything that can be expressed in Python), for example:

```
hatch count --columns class embark_town --filter 'survived == 0 and sex == "male"' -- titanic.csv 
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
