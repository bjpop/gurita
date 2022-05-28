.. _list_of_commands:

List of commands
****************

.. _input_output_command_list:

Input and output commands
=========================

.. list-table::
   :widths: 1 2
   :header-rows: 1

   * - Command
     - Description
   * - :doc:`in <in>`
     - Read CSV/TSV data from a named input file or standard input
   * - :doc:`out <out>`
     - Write data to a file or standard output in CSV/TSV format

.. _plotting_command_list:

Plotting commands
=================

.. list-table::
   :widths: 1 2
   :header-rows: 1

   * - Command 
     - Description
   * - :doc:`bar <bar>`
     - Bar plot of categorical feature
   * - :doc:`box <box>`
     - Plot distrbution of numerical column using box-and-whiskers
   * - :doc:`boxen <boxen>`
     - Plot distrbution of numerical column using boxes for quantiles
   * - :doc:`clustermap <clustermap>`
     - Clustered heatmap of two categorical columns
   * - :doc:`count <count>`
     - Plot count of categorical columns using bars
   * - :doc:`heatmap <heatmap>`
     - Heatmap of two categorical columns
   * - :doc:`hist <histogram>`
     - Histogram of numerical or categorical feature
   * - :doc:`line <line>`
     - Line plot of numerical feature
   * - :doc:`lmplot <lmplot>`
     - Regression plot (linear model)
   * - :doc:`pair <pair>`
     - Pair plot of numerical features
   * - :doc:`point <point>`
     - Point plot of numerical feature
   * - :doc:`scatter <scatter>`
     - Scatter plot of two numerical columns
   * - :doc:`strip <strip>`
     - Plot distrbution of numerical column using dotted strip
   * - :doc:`swarm <swarm>`
     - Plot distrbution of numerical column using dot swarm
   * - :doc:`violin <violin>`
     - Plot distrbution of numerical column using violin

.. _transformation_command_list:

Transformation commands
=======================

.. list-table::
   :widths: 1 2
   :header-rows: 1

   * - Command 
     - Description
   * - :doc:`corr <corr>`
     - Pairwise correlation between numerical columns
   * - :doc:`cut <cut>`
     - Select a subset of columns by name
   * - :doc:`dropna <dropna>`
     - Drop rows or columns containing missing values (NA)
   * - :doc:`eval <eval>`
     - Compute new columns for each row with an expression
   * - :doc:`filter <filter>`
     - Filter rows with a logical expression
   * - :doc:`gmm <gmm>`
     - Gaussian mixture model clustering
   * - :doc:`head <head>`
     - Select the first N rows in the data
   * - :doc:`isnorm <isnorm>`
     - Test whether numerical features differ from a normal distribution
   * - :doc:`kmeans <kmeans>`
     - k-means clustering
   * - :doc:`melt <melt>`
     - Reshape a wide format dataset into a long format dataset
   * - :doc:`outlier <outlier>`
     - Detect outliers in numerical columns using interquartile range
   * - :doc:`pca <pca>`
     - Principal component analysis (PCA)
   * - :doc:`pivot <pivot>`
     - Reshape a long format dataset into a wide format dataset
   * - :doc:`sample <sample>`
     - Randomly sample rows
   * - :doc:`sort <sort>`
     - Sort based on columns in precedence from left to right
   * - :doc:`tail <tail>`
     - Select the last N rows in the data
   * - :doc:`zscore <zscore>`
     - Compute Z-score for numerical columns

.. _summary_command_list:

Summary information commands
============================

.. list-table::
   :widths: 1 2
   :header-rows: 1

   * - Command 
     - Description
   * - :doc:`describe <describe>`
     - Show summary information about the input data set
   * - :doc:`pretty <pretty>`
     - Pretty print a fragment of the data set
   * - :doc:`unique <unique>`
     - Print the unique values from a column
