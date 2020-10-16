General behaviour
*****************

Use the ``-h`` or ``--help`` command line arguments to get an overview of hatch's command line syntax:

.. code-block:: bash

    hatch -h

The usage message is displayed as follows:

.. code-block::

    usage: hatch [-h] [-v] {pca,hist,noplot,box,violin,swarm,strip,boxen,count,bar,point,scatter,line,heatmap} ...
    
    Generate plots of tabular data
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
    
    Plot type:
      {pca,hist,noplot,box,violin,swarm,strip,boxen,count,bar,point,scatter,line,heatmap}
                            sub-command help
        pca                 Principal components analysis
        hist                Histograms of numerical data
        noplot              Do not generate a plot, but run filter and eval commands
        box                 Box plot of numerical feature, optionally grouped by categorical features
        violin              Violin plot of numerical feature, optionally grouped by categorical features
        swarm               Swarm plot of numerical feature, optionally grouped by categorical features
        strip               Strip plot of numerical feature, optionally grouped by categorical features
        boxen               Boxen plot of numerical feature, optionally grouped by categorical features
        count               Count plot of categorical feature
        bar                 Bar plot of categorical feature
        point               Point plot of numerical feature, optionally grouped by categorical features
        scatter             Scatter plot of two numerical features
        line                Line plot of numerical feature
        heatmap             Heatmap of two categories with numerical values

In general, the command line syntax for hatch follows the pattern:

.. code-block:: bash

    hatch <subcommand> <arguments>

where ``subcommand`` selects the plot type (e.g. ``bar``) and ``arguments`` controls the behaviour of the plot and specifies input data.

As a simple example, if you want to plot a histogram of the ``passengers`` column from the file ``flights.csv`` you can run the following command:

.. code-block:: bash

    hatch hist -x passengers -- flights.csv 

In the above example ``hist`` selects the histogram plot type, ``-x passengers`` specifies that the ``passengers`` feature in the data set should be plotted on the X-axis
and ``-- flights.csv`` specifies that the input data set should be read from the file ``flights.csv``.

Each type of plot accepts optional arguments that control its behaviour. Some of these are common across all plot types, and some are limited to specific plot types.

Help messages for each plot type can be requested with ``-h`` or ``--help`` after the plot type. For example, to get specific help about histogram plots, use:

.. code-block:: bash

    hatch hist -h

Input files
===========

Hatch can either read data from a named input file, or if no file is specified, then it will read input from the standard input device (stdin).
The input file type must be either CSV or TSV. By default hatch will assume the data is in CSV format, but you can change the format with the ``--filetype`` argument, and choose TSV instead.
Hatch requires that the first row of the input file is the column headings.

Both of the usages below are valid

Read from a named input file:

.. code-block:: bash

    hatch count --x class embark_town -- titanic.csv

Read from stdin:

.. code-block:: bash

    hatch count --cols class embark_town < titanic.csv

Reading from stdin is particularly useful for pipeline commands:

.. code-block:: bash

    some_command | hatch ...

Output files
============

Hatch produces PNG (graphics) files as its output. A single plot command may produce one or more such files, depending on how hatch is used. By default hatch names the output files based on the following information:

 * The prefix of the input data file name (this can be overridden).
 * The name(s) of the columns that have been selected for plotting.
 * Optionally the names of columns that have been selected for grouping.
 * The type of plot being produced.

For example, the following command:

.. code-block:: bash

    hatch dist --cols sepal_length --groups species -- iris.csv

produces an output file called ``iris.sepal_length.species.box.png`` by default, because:

 * ``iris`` is the prefix of the name of the input file `iris.csv`
 * ``sepal_length`` is the column that has been selected for plotting
 * ``species`` is the column that has been selected for grouping
 * ``box`` is the type of plot

If the input data is read from the standard input (stdin) instead of a named file, then the prefix of the output defaults to ``plot``. For example, the following command:

.. code-block:: bash

    hatch dist --cols sepal_length --groups species < iris.csv

produces an output file called ``plot.sepal_length.species.box.png`` because the input data is read (redirected) from stdin.

The output prefix can be overridden with the ``--prefix`` command line option (regardless of whether the input comes from a named file or from stdin). For example:

.. code-block:: bash

    hatch dist --cols sepal_length --groups species --prefix flower < iris.csv

produces an output file called ``flower.sepal_length.species.box.png``.

Command line options for all types of plots
===========================================

The following command line options apply to all types of plots.

.. code-block:: bash

    usage: hatch <plotype>
                      [-h] [--outdir DIR] [--filetype FILETYPE] [--prefix NAME] [--logfile LOG_FILE]
                      [--nolegend] [--filter EXPR] [--eval EXPR [EXPR ...]] [--navalues STR]
                      [--title STR] [--width SIZE] [--height SIZE] [--xlabel STR] [--ylabel STR]
                      [--noxticklabels] [--noyticklabels] 
                      [DATA]
    
    positional arguments:
      DATA                  Filepaths of input CSV/TSV file
    
    optional arguments:
      -h, --help            show this help message and exit
      --outdir DIR          Name of optional output directory.
      --filetype FILETYPE   Type of input file. Allowed values: CSV, TSV. Otherwise inferred from
                            filename extension.
      --prefix NAME         Name prefix for output files
      --logfile LOG_FILE    record program progress in LOG_FILE
      --nolegend            Turn off the legend in the plot
      --filter EXPR         Filter rows: only retain rows that make this expression True
      --eval EXPR [EXPR ...]
                            Construct new columns based on an expression
      --navalues STR        Treat values in this space separated list as NA values. Example: --navalues
                            ". - !"
      --title STR           Plot title. By default no title will be added.
      --width SIZE          Plot width in inches. Default: 10
      --height SIZE         Plot height in inches. Default: 8
      --xlabel STR          Label for horizontal (X) axis
      --ylabel STR          Label for vertical (Y) axis
      --noxticklabels       Turn of horizontal (X) axis tick labels
      --noyticklabels       Turn of veritcal (Y) axis tick labels

Example test data
=================

In the ``data`` directory in this repository we provide some sample test data for the sake of illustrating the plotting functionality of hatch. These data sets have been obtained from the `seaborn-data <https://github.com/mwaskom/seaborn-data/>`_ repository that is used in the seaborn Python library documentation.

 * `iris.csv <https://github.com/mwaskom/seaborn-data/blob/master/iris.csv/>`_
 * `flights.csv <https://github.com/mwaskom/seaborn-data/blob/master/flights.csv/>`_
 * `fmri.csv <https://github.com/mwaskom/seaborn-data/blob/master/fmri.csv/>`_
 * `titanic.csv <https://github.com/mwaskom/seaborn-data/blob/master/titanic.csv>`_
 * `tips.csv <https://github.com/mwaskom/seaborn-data/blob/master/titanic.csv>`_
