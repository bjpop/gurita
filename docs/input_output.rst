Input and output
*****************

.. _input_files:

Input files
===========

Hatch can read data from a named input file, or if no file is specified, then it will read input from the standard input device (stdin).

The example below illustrates reading input from a named file. Note the use of double-dash ``--`` just before the file name. The double-dash indicates the end of the regular command line arguments, and tells hatch that the following arugment is the input file name:

.. code-block:: bash

    hatch count --x class embark_town -- titanic.csv

Read from stdin:

.. code-block:: bash

    hatch count --cols class embark_town < titanic.csv

Reading from stdin is particularly useful for pipeline commands:

.. code-block:: bash

    some_command | hatch ...

.. _filetype:

File type
---------

The input file type must be either CSV or TSV. The first row of the input file must be column headings.

By default hatch will assume the data is in CSV format, but you can change the format with the ``--filetype TSV`` argument, and choose TSV instead.

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
