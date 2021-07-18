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

Input file type
---------------

The input file type must be either CSV or TSV. The first row of the input file must be column headings.

By default Hatch will assume the data is in CSV format, but you can change the format with the ``--filetype TSV`` argument, and choose TSV instead.

Output files 
============

Hatch's default behaviour for plotting commands is to save the resulting image to a file.

For example, the following command generates a count plot of the ``class`` feature from the input file ``titanic.csv`` and saves the resulting plot to a file called ``titanic.class.count.png``:

.. code-block:: bash

    hatch count -x class titanic.csv

Interactive plots
-----------------

.. _show:

The ``--show`` option overrides the default behaviour and causes the plot to be displayed in an interactive window (and not saved to a file). This assumes you are using Hatch in an environment with a graphics display.

We can modify the above command with ``--show`` like so:

.. code-block:: bash

    hatch count -x class --show titanic.csv

Output plot file name
---------------------

When saving a plot to a file, you can specify the name of the file to use with the ``-o <filename>`` or ``--out <filename>`` option. 

For example, the following command saves the output plot to a file called ``example.png``:

.. code-block:: bash

    hatch count -x class -o example.png titanic.csv

If you do not specify an output file name, Hatch will choose an appropriate file name based on various input parameters:

 * The prefix of the input data file name (this can be overridden).
 * The name(s) of the columns that have been selected for plotting.
 * Optionally the names of columns that have been selected for grouping (for example by using ``--hue`` where applicable).
 * The type of plot being produced.

For example, the following command:

.. code-block:: bash

    hatch hist -x sepal_length --hue species iris.csv

automatically produces an output file called ``iris.sepal_length.species.hist.png`` by default, because:

 * ``iris`` is the prefix of the name of the input file `iris.csv`
 * ``sepal_length`` is the column that has been selected for plotting
 * ``species`` is the column that has been selected for grouping via the ``--hue`` argument
 * ``hist`` is the type of plot (a histogram)

If the input data is read from the standard input (stdin) instead of a named file, then the prefix of the output defaults to ``plot``. For example, the following command:

.. code-block:: bash

    hatch hist -x sepal_length --hue species < iris.csv 

produces an output file called ``plot.sepal_length.species.hist.png`` because the input data is read (redirected) from stdin.

.. _prefix:

Output prefix
-------------

The output prefix can be overridden with the ``--prefix`` command line option (regardless of whether the input comes from a named file or from stdin). For example:

.. code-block:: bash

    hatch hist -x sepal_length --hue species --prefix flower < iris.csv

produces an output file called ``flower.sepal_length.species.hist.png``.

.. _format:

Output plot graphics file format 
--------------------------------

By default Hatch will save output plots in the PNG file format. However, this can be overridden with the ``--format {png,jpg,pdf,svg}`` option.

For example, the following command saves the output plot in SVG format, to a file called ``titanic.class.count.svg``:

.. code-block:: bash

    hatch count -x class --format svg titanic.csv

.. note::

    If you do not specify an output file name, Hatch will choose one for you. This includes the addition of a file name suffix indicating the type of graphics format used (``png``, ``pdf``, ``svg``, or ``jpg``). 

    If you use ``-o`` (or ``--out``) to specify an output file name, Hatch will use that name verbatim and will not append suffix to the file name indicating the file type. Of course you may include a suffix in your own chosen name, however, this suffix does not influence the type of graphics format used. The only way to change the output graphics file format is with the ``--format`` option (otherwise the default ``png`` type is used).

.. _save:

Transforming input data and saving to a file
============================================

Hatch supports a number of data manipulation options, such as :doc:`row filtering <filter/>`, :doc:`random sampling <sample/>`, :doc:`feature selection <features/>`, and :doc:`computation of new columns <eval/>`.

These manipulations are optionally performed prior to plotting or computing statistics.

However, it is also possible to apply these transformations and save the result back to a new file. This is achieved with the :doc:`trans` command. For example, the following command randomly samples 100 rows
from the input file ``iris.csv``, and saves the result to ``iris.sample100.csv`` (preserving the header row):

.. code-block:: bash

    hatch trans --sample 100 -o iris.sample100.csv iris.csv


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
