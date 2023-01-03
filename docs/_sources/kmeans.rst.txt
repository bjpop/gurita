.. _kmeans:

kmeans
======

The `k-means clustering algorithm <https://en.wikipedia.org/wiki/K-means_clustering>`_  identifies clusters in numerical data 
where individual data points are assigned to the cluster with the nearest mean (cluster centroid).

The number of clusters to detect is specified as an optional parameter (default is 2).

The ``kmeans`` command adds a new column to the dataset storing the cluster label for the corresponding datapoint on each row.  

Clustering does not work with missing values, so rows with missing (NA) values in the clustered columns are automatically removed before clustering.

Usage
-----

.. code-block:: text

    gurita kmeans [-h] [-c COLUMN [COLUMN ...]] [--name NAME] [-n NCLUSTERS]

Arguments
---------

.. list-table::
   :widths: 25 20 10
   :header-rows: 1
   :class: tight-table

   * - Argument
     - Description
     - Reference
   * - * ``-h``
       * ``--help``
     - display help for this command
     - :ref:`help <kmeans_help>`
   * - * ``-c COLUMN [COLUMN...]``
       * ``--columns COLUMN [COLUMN...]``
     - apply clustering to specified numerical columns
     - :ref:`kmeans columns <kmeans_columns>`
   * - * ``-n NCLUSTERS``
       * ``--nclusters NCLUSTERS``
     - identify this many clusters in the data 
     - :ref:`number of clusters <kmeans_num_clusters>`
   * - ``--name NAME``
     - choose a column name for the new cluster label column (default: cluster)
     - :ref:`new column name <kmeans_name>`

See also
--------

:doc:`Gaussian Mixture Models <gmm/>` provide another way to cluster data. 

Simple example
--------------

The following command clusters the numerical columns in the ``iris.csv`` file: 

.. code-block:: text

   gurita kmeans < iris.csv

The output is quite long so we can adjust the command to look at only the first few rows using the :doc:`head <head>` command:

.. code-block:: text

   gurita kmeans + head < iris.csv 

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species,cluster
    5.1,3.5,1.4,0.2,setosa,0
    4.9,3.0,1.4,0.2,setosa,0
    4.7,3.2,1.3,0.2,setosa,0
    4.6,3.1,1.5,0.2,setosa,0
    5.0,3.6,1.4,0.2,setosa,0

A new categorical column called ``cluster`` is added to the dataset, this holds the cluster labels for the datapoint on each row.  

Each cluster is labelled using a natural number (0,1,2 ...).

We can get an overview of the new ``cluster`` column by using the ``describe`` command after clustering:

.. code-block:: text

    gurita kmeans + describe -c cluster < iris.csv

The output of the above command is shown below:

.. code-block:: text

            cluster
    count       150
    unique        2
    top           0
    freq         97

We can see that there are 150 data points (150 rows) and 2 unique values in the ``cluster`` column (these are the labels 0 and 1). The most frequent
label is 0 which occurs 97 times (and thus the label 1 must occur 150-97=53 times).

.. note::

   Despite the use of numbers for cluster labels, Gurita treats them as categorical values. 

   This is beneficial when it comes to plotting data using cluster labels because it means that the plots will correctly
   interpret the labels as catergorical values and render them accordingly.

For example we might like to make a box plot comparing the ``petal_length`` across the two clusters:

.. code-block:: text

    gurita kmeans + box -x cluster -y petal_length < iris.csv 

The output of the above command is written to ``box.cluster.petal_length.png``:

.. image:: ../images/box.cluster.petal_length.png
       :width: 600px
       :height: 600px
       :align: center
       :alt: Box plot comparing petal length across two k-means clusters in the iris.csv dataset 

|


.. _kmeans_help:

Getting help
------------

The full set of command line arguments for ``kmeans`` can be obtained with the ``-h`` or ``--help``
arguments:

.. code-block:: text

    gurita kmeans -h

.. _kmeans_columns:

Cluster data from specified numerical columns
---------------------------------------------

.. code-block:: text

   -c NAME [NAME ...], --columns NAME [NAME ...]

By default, if no column names are specified, clustering is performed on all of the numerical columns in the dataset.

However it is possible to perform clustering on a specific subset of columns via the ``-c/--columns`` argument.

For example, the following command performs k-means clustering on just the columns ``sepal_length``, ``sepal_width``,  and ``petal_length`` (and hence ignores the ``petal_width`` column):

.. code-block:: text

    gurita kmeans -c sepal_length sepal_width petal_length < iris.csv

.. note::

   Non-numeric columns will be ignored by ``kmeans`` even if they are specified as arguments to ``-c/--columns``.

.. _kmeans_num_clusters:

Choose number of clusters to identify
-------------------------------------

.. code-block:: text

   -n NCLUSTERS, --nclusters NCLUSTERS  

By default ``kmeans`` identifies two clusters in the data. However, this can be changed with the ``-n/--nclusters`` argument.

For example, the following command finds three clusters in the ``iris.csv`` file:

.. code-block:: text

   gurita kmeans -n 3 < iris.csv

We can check the number of values in each cluster using the ``grouby`` command:

.. code-block:: text

    gurita kmeans -n 3 + groupby -k cluster < iris.csv  

The output of the above command is shown below:

.. code-block:: text

   cluster,size
   0,50
   1,62
   2,38

We can observe three clusters labelled 0,1,2 with 50,62,38 members respectively.

.. _kmeans_name:

Choose a name for the new cluster label column
----------------------------------------------

.. code-block:: text

    --name NAME 

The ``kmeans`` command adds an extra categorical column called ``cluster`` to the dataset to store the cluster labels for each row. 

The cluster labels are natural numbers (non-negative integers) from 0 upwards (0, 1, 2, ...).

The name of the extra column can be changed with the ``--name`` argument.

The following command specifies that ``group`` should be used as the prefix for the newly added columns:

.. code-block:: text

   gurita kmeans --name group < iris.csv

By chaining this command with ``head`` we can inspect the first few rows of the output:

.. code-block:: text

   gurita kmeans --name group + head < iris.csv

The output of the above command is as follows:

.. code-block:: text

    sepal_length,sepal_width,petal_length,petal_width,species,group
    5.1,3.5,1.4,0.2,setosa,1
    4.9,3.0,1.4,0.2,setosa,1
    4.7,3.2,1.3,0.2,setosa,1
    4.6,3.1,1.5,0.2,setosa,1
    5.0,3.6,1.4,0.2,setosa,1

Observe that the new cluster label column is called ``group``.
