Input and output
*****************

.. _input_files:

Input files
===========

Hatch can read data from a named input file or the standard input device (stdin). 

The example below illustrates reading input from a named file. This command produces a :doc:`count plot <count/>` for the ``class`` feature in the ``titantic.csv`` dataset:

.. code-block:: bash

    hatch count -x class titanic.csv

In some instances it is useful to clearly separate the optional command line arguments from the name of the input file. Following standard command line conventions, Hatch provides a double-dash ``--``
marker to be used for this purpose. The double-dash (surrounded by whitespace) indicates the end of the regular command line arguments, and tells Hatch that the following arugment is the input file name:

.. code-block:: bash

    hatch count -x class -- titanic.csv

If no input file name is provided, Hatch will read from stdin instead. For example you can
redirect input from a file on the Unix command line:

.. code-block:: bash

    hatch count -x class < titanic.csv

Reading from stdin is particularly useful when you want to use Hatch as part of a command pipeline: 

.. code-block:: bash

    example_command | hatch count -x class

.. _filetype:

File type
---------

The input file type must be either CSV or TSV. The first row of the input file must be column headings.

By default Hatch will assume the data is in CSV format, but you can change the format with the ``--filetype TSV`` argument, and choose TSV instead.

Output files
============

Hatch produces PNG (graphics) files as its output. A single plot command may produce one or more such files, depending on how Hatch is used. By default Hatch names the output files based on the following information:

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

.. _prefix:

Output prefix
-------------

The output prefix can be overridden with the ``--prefix`` command line option (regardless of whether the input comes from a named file or from stdin). For example:

.. code-block:: bash

    hatch dist --cols sepal_length --groups species --prefix flower < iris.csv

produces an output file called ``flower.sepal_length.species.box.png``.

.. _outdir:

Output directory
================

.. _save:

Saving data to a file
=====================

.. _log:

Logging progress
================

.. _info:

Input data summary
==================

.. _verbose:

Verbose execution
=================

.. _navalues:

NA values
=========
