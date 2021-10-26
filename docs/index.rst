.. hatch documentation master file, created by
   sphinx-quickstart on Wed Oct 14 18:01:41 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Hatch: a command line data analytics and plotting tool
******************************************************

Hatch is a command line tool for analysing and visualising data taking input from tabular data in CSV or TSV format.

At its core, Hatch provides a suite of commands, each of which carries out a common data analytics or plotting task.
Additionally, Hatch allows commands to be chained together into flexible analysis pipelines.

It is designed to be fast and convenient, and is particularly suited to data exploration tasks. Input files with large numbers of rows (> millions) are readily supported.

Hatch commands are highly customisable, however sensible defaults are applied. Therefore simple tasks are easy to express
and complex tasks are possible.

Hatch is implemented in `Python <http://www.python.org/>`_ and makes extensive use of the `Pandas <https://pandas.pydata.org/>`_, `Seaborn <https://seaborn.pydata.org/>`_, and `Scikit-learn <https://scikit-learn.org/>`_ libraries for data processing and plot generation.

Simple example
--------------

The following examples use the ``iris.csv`` dataset as input. The file contains 150 data rows (plus one heading row) and 5 columns.
A pretty display of the first and last 5 rows of the data can be viewed using the ``hatch pretty`` command:

.. code-block:: bash

   cat iris.csv | hatch pretty
   sepal_length  sepal_width  petal_length  petal_width   species
            5.1          3.5           1.4          0.2    setosa
            4.9          3.0           1.4          0.2    setosa
            4.7          3.2           1.3          0.2    setosa
            4.6          3.1           1.5          0.2    setosa
            5.0          3.6           1.4          0.2    setosa
  ...                    ...           ...          ...       ...
            6.7          3.0           5.2          2.3 virginica
            6.3          2.5           5.0          1.9 virginica
            6.5          3.0           5.2          2.0 virginica
            6.2          3.4           5.4          2.3 virginica
            5.9          3.0           5.1          1.8 virginica

  [150 rows x 5 columns]

The following Hatch command generates a box plot of data from a file called ``iris.csv``, the Y-axis
represents the ``sepal_length`` numerical feature, and the X-axis is grouped by the ``species`` categorical feature.
The goal of this plot is to show the distribution of sepal length of the three different species of iris
flowers contained in the data set.

.. code-block:: bash

   cat iris.csv | hatch box -x species -y sepal_length

The above command generates an output file called ``hatch.species.sepal_length.box.png`` that
contains the following box plot:

.. image:: ../images/iris.sepal_length.species.box.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Box plot showing the distribution of sepal length by species for the iris data set


Advanced example
----------------

The following example illustrates Hatch's ability to chain commands together: 

.. code-block:: bash

    cat iris.csv | hatch filter 'species != "virginica"' + sample 0.9 + pca + scatter -x pc1 -y pc2 --hue species

Input is read from the file called `iris.csv` on standard input and data is passed from left to right in the chain.
Commands can modify the data as it is passed along.

In this example there are 4 commands that are executed in the following order:

1. The `filter` command selects all rows where `species` is not equal to `virginica`.
2. The filtered rows are then passed to the `sample` command which randomly selects 90% of the remaining rows.
3. The sampled rows are then passed to the `pca` command which performs principal component analysis (PCA) as a data reduction step, yielding two extra columns in the data called `pc1` and `pc2`.
4. Finally the pca-transformed data is passed to the `scatter` command which generates a scatter plot of `pc1` and `pc2` (the first two principal components).

.. image:: ../images/iris.pc1.pc2.species.pca.scatter.png
       :width: 700px
       :height: 600px
       :align: center
       :alt: Scatter plot comparing principal components pc1 and pc2 from a filtered iris dataset 

License
-------

Hatch is open source software and is licensed under the terms of the `MIT license <https://raw.githubusercontent.com/bjpop/hatch/master/LICENSE>`_.

.. toctree::
   :caption: Overview
   :hidden:

   self
   license
   installation 
   example_input_data

.. toctree::
   :caption: General behaviour 
   :hidden:

   command_line_syntax 
   input_output 

.. toctree::
   :caption: Plotting 
   :hidden:

   histogram 
   count
   scatter
   box
   violin
   swarm
   strip
   boxen
   point
   bar
   line
   heatmap
   clustermap
   pca

 
.. toctree::
   :caption: Statistics 
   :hidden:

   info 
   correlation 
   normal_test


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Data maniupulation 

   transform 
   features
   filter 
   eval 
   sample


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Facets 

   facets 

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Plot aesthetics 

   aesthetics 

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Advanced topics 

   docker

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Development

   contributing
   bug_reports
   feature_requests
