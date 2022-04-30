.. _input_output: 

Input and output
*****************

Hatch works on tabular input data in `CSV (comma separated values) <https://en.wikipedia.org/wiki/Comma-separated_values>`_ or `TSV (tab separated values) <https://en.wikipedia.org/wiki/Tab-separated_values>`_ format.

Input data is read from the standard input device (stdin) or a named input file.

Rows in the input file are considered to be "observations" (or cases) and columns are considered to be "features" (or variables). 
That is, each data row is a discrete observation of some thing (a data point), and each observation is described by the values of its features.
The names of the features are given in the first row of the input file (the heading row).

Below is a small example of the kind of input data accepted by Hatch. In this case it is in CSV format with five columns, one heading row and three data rows.
The first row contains the names of each feature (column) in the dataset. The remaining three rows are data rows,
where each row has a value associated with each feature column. 


.. code-block:: bash

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,setosa
    4.9,3.0,1.4,0.2,setosa
    4.7,3.2,1.3,0.2,setosa

.. note::

   Hatch requires that the input data is **rectangular** in shape. In other words, every row must contain the same number of columns.
   Missing values are allowed, and are indicated by leaving a particular column blank (empty) on a given row; nonetheless the column
   must still be present.

.. _input_files:

Input data 
==========

Hatch can read data from standard input (stdin) or a named input file.

Input from standard input device (stdin)
----------------------------------------

By default Hatch will read from standard input. For example you can
redirect input from a file on the command line:

.. code-block:: bash

    hatch count -x class < titanic.csv

In the above example the notation ``< titanic.csv`` causes the contents of the file ``titantic.csv`` to be fed into the standard input of Hatch.
This is called *input redirection*, and is a feature of the command line.

Instead of using input redirection, it is also possible to *pipe* the output from another command to the standard input of Hatch:

.. code-block:: bash

    cat titanic.csv | hatch count -x class

In the above example the command ``cat titanic.csv`` outputs the contents of the file ``titanic.csv`` to standard output which is then fed through a pipe using the ``|`` (vertical bar) operator
into the standard input of Hatch.

Reading from standard input is particularly useful when you want to use Hatch as part of a command pipeline: 

.. code-block:: bash

    example_command | hatch count -x class

.. warning::

   **standard input defaults to CSV format**

   For performance reasons Hatch does not try to detect the format of the input file when reading from standard input. 

   Therefore, when reading from standard input, unless otherwise specified, Hatch assumes that the file is in CSV format.

   This can be overridden by using the ``stdin`` command and supplying the ``--format tsv`` argument. 

   Alternatively you can use the ``in`` command to read the file directly by its name (thus avoiding the use of standard input).
   When reading from a file by name Hatch can use the file name extension to guess the file format. For instance, if
   the file name is ``titanic.tsv`` it will assume the file is in TSV format. Note carefully, file format guessing only works
   with the ``in`` command.

   See below for details on each approach.


Specifying input file type when reading from standard input 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When reading input from standard input, Hatch will assume that the data is in CSV format unless you tell it otherwise.

The ``stdin`` command lets you specify the format of the input file explicitly.

In the following examples we use ``...`` to indicate that the remainder of the example hatch command is unspecified.

Request for TSV file format:

.. code-block:: bash

    cat titanic.tsv | hatch stdin --format tsv ... 

If, for example, you wanted to generate a count plot of the ``class`` feature in the ``titanic.tsv`` file, the ``...`` in the above example could be expanded like so:

.. code-block:: bash

    cat titanic.tsv | hatch stdin --format tsv + count -x class 

Request for CSV file format: 

.. code-block:: bash

    cat titanic.csv | hatch stdin --format csv ...

The above example is redundant because the default behaviour of Hatch is to assume CSV format when reading from standard input. 

Input from a named file 
-----------------------

The ``in`` command allows you to specify an input file by name, instead of reading from standard input:

.. code-block:: bash

    hatch in titanic.tsv ... 

When reading input from a named file (and not from stdin) Hatch will look at the file extension and assume CSV format if the extension is ``.csv`` and TSV format if the extension is ``.tsv``. This behaviour can be overridden with the
``--format <type>`` option. 

Output files 
============

Hatch's default behaviour for plotting commands is to save the resulting image to a file (but it can also do interactive plots, see :ref:`the show command <show>`).

For example, the following command generates a count plot of the ``class`` feature from the input file ``titanic.csv`` and saves the resulting plot to a file called ``titanic.class.count.png``:

.. code-block:: bash

    hatch count -x class titanic.csv

.. _out:

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

.. _show:

Interactive plots
=================

The ``--show`` option overrides the default behaviour and causes the plot to be displayed in an interactive window (and not saved to a file). This assumes you are using Hatch in an environment with a graphics display.

This is illustrated below:

.. code-block:: bash

    hatch count -x class --show titanic.csv

.. _save:

Transforming input data and saving to a file
============================================

Hatch supports a number of data manipulation options, such as :doc:`row filtering <filter/>`, :doc:`random sampling <sample/>`, :doc:`feature selection <features/>`, and :doc:`computation of new columns <eval/>`.

These manipulations are optionally performed prior to plotting or computing statistics.

However, it is also possible to apply these transformations and save the result back to a new file. This is achieved with the :doc:`transform <transform/>` command. For example, the following command randomly samples 100 rows
from the input file ``iris.csv``, and saves the result to ``iris.trans.csv`` (preserving the header row):

.. code-block:: bash

    hatch transform --sample 100 iris.csv

The default output file name can be overridden with ``-o`` (``--out``) like so: 

.. code-block:: bash

    hatch transform --sample 100 -o iris.sample100.csv iris.csv

.. _log:

Logging progress
================

The ``--logfile <filename>`` option causes Hatch to record a timestamped log of program progress to a file. Logging information includes the command line used to invoke the program and key program events.
The log file can be useful for debugging Hatch's behaviour.

In the following example we add logging to a plotting command, such that the output log data is written to a file called ``hatch.log``:

.. code-block:: bash

   hatch count -x class --logfile hatch.log titanic.csv

.. _verbose:

Verbose execution
=================

By default Hatch does not display any messages on the standard output during normal program execution. This can be overridden with 
the ``--verbose`` option which causes Hatch to become more chatty. In particular, when generating any output files, the verbose
mode will cause Hatch to specify the names of any files it has created. This is useful when you want to immediately open the file
for further inspection.

.. code-block:: bash

    hatch count -x class --verbose titanic.csv 

The outut of the above command is:

.. code-block:: text 

    Plot written to titanic.class.count.png

.. _navalues:

NA values
=========
