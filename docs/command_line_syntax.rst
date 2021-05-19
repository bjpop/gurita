Command line syntax
*******************

The command line syntax for Hatch follows the pattern:

.. code-block:: bash

    hatch <subcommand> <arguments>

where ``subcommand`` selects the plot type (e.g. ``hist``) and ``arguments`` controls the behaviour of the plot and specifies input data.

As a simple example, if you want to plot a histogram of the ``passengers`` column from the file ``flights.csv`` you can run the following command:

.. code-block:: bash

    hatch hist -x passengers flights.csv 

In the above example ``hist`` selects the histogram plot type, ``-x passengers`` specifies that the ``passengers`` feature in the data set should be plotted on the X-axis
and ``flights.csv`` specifies that the input data set should be read from the file ``flights.csv``. See :doc:`input_output` for more information about input and output files.

Each type of plot accepts optional arguments that control its behaviour. Some of these are common across all plot types, and some are limited to specific plot types.

.. _help:

Getting help
============

The ``-h`` or ``--help`` command line arguments give an overview of Hatch's command line syntax:

.. code-block:: bash

    hatch -h

The usage message is displayed as follows:

.. code-block:: text 

    usage: hatch [-h] [-v] {corr,pca,hist,noplot,box,violin,swarm,strip,boxen,count,bar,point,scatter,line,heatmap,clustermap} ...
    
    Generate plots of tabular data
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
    
    Sub command:
      {corr,pca,hist,noplot,box,violin,swarm,strip,boxen,count,bar,point,scatter,line,heatmap,clustermap}
                            sub-command help
        corr                Correlation between two numerical features
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
        clustermap          Clustered heatmap of two categories with numerical values

Help information for each sub-command can be requested with ``-h`` or ``--help``
after the sub-command name. For example, to get specific help about histogram plots, use:

.. code-block:: bash

    hatch hist -h

Common arguments
================

Hatch provides a number of command line arguments that operate over most types of plots.

The following command line options apply generally across most of the plotting sub-commands: 

.. list-table:: 
   :widths: 1 2 1
   :header-rows: 1

   * - Argument
     - Description
     - Reference
   * - ``-h, --help``
     - generate a help message
     - :ref:`help`
   * - ``--outdir DIR``
     - write output files to the DIR directory (default is the current working directory)
     - :ref:`outdir`
   * - ``--filetype {CSV,TSV}``
     - specify the type of input file, allowed values are ``CSV`` (default) and ``TSV``
     - :ref:`filetype`
   * - ``-o FILE, --out FILE``
     - save output plot to FILE (and override the default file name) 
     - :ref:`out`
   * - ``--format {png,jpg,pdf,svg}``
     - file format to use for saved plots, allowed values are ``png`` (default) and ``jpg``, ``pdf``, ``svg``
     - :ref:`format`
   * - ``--prefix NAME``
     - use NAME as the prefix of the output file (default is to use the prefix of the input data file name)
     - :ref:`prefix`
   * - ``--logfile LOG_FILE``
     - write progress information and messages to LOG_FILE 
     - :ref:`log`
   * - ``--filter EXPR``
     - filter the rows of the input data file using the expression EXPR
     - :doc:`filter` 
   * - ``--eval EXPR [EXPR ...]``
     - dynamically create new columns in the input data based on the expressions EXPR [EXPR ...], each expression creates a new column
     - :doc:`eval` 
   * - ``--navalues STR``
     - use STR to represent NA values in the input file 
     - :ref:`navalues` 
   * - ``--info, -i``
     - output a summary of the input data set (including types, an simple statistics where possible)
     - :ref:`info` 
   * - ``--verbose``
     - turn on verbose output mode, this will cause Hatch to be more chatty about its behaviour, and in particular it will print the name of any output file created 
     - :ref:`verbose` 
   * - ``--save FILEPATH, -s FILEPATH``
     - Save the data set to a CSV file after running ``filter``, ``eval`` and ``sample`` commands
     - :ref:`save` 
   * - ``--sample NUM``
     - use a random sample of NUM rows from the input data instead of the full data set
     - :doc:`sample`
   * - ``--title STR``
     - use STR for the title of the plot, by default plots do not have titles
     - :ref:`title` 
   * - ``--width SIZE``
     - specify the width of the plot (in inches) with SIZE
     - :ref:`width` 
   * - ``--height SIZE``
     - specify the height of the plot (in inches) with SIZE
     - :ref:`height` 
   * - ``--xlabel STR``
     - use STR for the X-axis label (otherwise label will be chosen automatically)
     - :ref:`xlabel` 
   * - ``--ylabel STR``
     - use STR for the Y-axis label (otherwise label will be chosen automatically)
     - :ref:`ylabel` 
   * - ``--noxticklabels``
     - turn off tick labels on the X-axix (by default tick labels are shown on the X-axis where appropriate)
     - :ref:`noxticklabels` 
   * - ``--noyticklabels`` 
     - turn off tick labels on the Y-axix (by default tick labels are shown on the Y-axis where appropriate)
     - :ref:`noyticklabels` 
   * - ``--nolegend``
     - turn off the plot legend (only relevant for plots that generate a legend by default)
     - :ref:`nolegend` 
   * - ``--style {darkgrid,whitegrid,dark,white,ticks}``
     - Aesthetic style of plot. Allowed values: darkgrid, whitegrid, dark, white, ticks. Default: darkgrid.
     - :ref:`style` 
   * - ``--context {paper,notebook,talk,poster}``
     - Aesthetic context of plot. Allowed values: paper, notebook, talk, poster.  Default: notebook.
     - :ref:`context` 
   * - ``--show``
     - display an interactive plot window instead of saving the plot to a file 
     - :ref:`show <show>` 
