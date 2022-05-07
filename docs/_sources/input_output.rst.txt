.. _input_output: 

Input and output
*****************

Hatch works on tabular input data in `CSV (comma separated values) <https://en.wikipedia.org/wiki/Comma-separated_values>`_ or `TSV (tab separated values) <https://en.wikipedia.org/wiki/Tab-separated_values>`_ format.

Input data is read from the standard input device (stdin) or a named input file.

Rows in the input file are considered to be "observations" and columns are considered to be "features" (or variables). 
That is, each data row is a discrete observation of some thing (a data point), and each observation is described by the values of its features.
The names of the features are given in the first row of the input file (the heading row).

Below is a small example of the kind of input data accepted by Hatch. In this case it is in CSV format with five columns, one heading row and three data rows.
The first row contains the names of each column. The remaining three rows are data rows,
where each row has a value associated with each column:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,setosa
    4.9,3.0,1.4,0.2,virginica
    4.7,3.2,1.3,0.2,setosa

.. note::

   Hatch requires that the input data is **rectangular** in shape. In other words, every row must contain the same number of columns.
   Missing values are allowed, and are indicated by leaving a particular column blank (empty) on a given row; nonetheless the column
   must still be present.

.. _input_files:

Input data 
==========

Hatch can read data from a named input file or standard input (stdin).

Input from a named file 
-----------------------

The ``in`` command allows you to specify an input file by name: 

.. code-block:: text 

    hatch in titanic.csv ... 

We use ``...`` to indicate that the remainder of the example Hatch command is omitted for the sake of simplifying the discussion.

You should imagine that ``...`` would be replaced by more text to complete the command.
For example, if you wanted to generate a count plot of the ``class`` feature in the ``titanic.csv`` file, the ``...`` in the above example could be expanded like so:

.. code-block:: text 

    hatch in titanic.csv + count -x class 

In the above example data is read from the input file and then passed along the :ref:`command chain <command_chain>` from left to right into the ``count`` command to make a plot.

When reading input from a named file (and not from stdin) Hatch will look at the file extension and assume CSV format if the extension is ``.csv`` and TSV format if the extension is ``.tsv``. This behaviour can be overridden with the
``--format <type>`` option as noted below.

Specifying input file type explicitly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``in`` command lets you specify the format of the input file explicitly. This will override any default behaviour that Hatch would otherwise have when determining the input file type.

Request for CSV file format: 

.. code-block:: text 

    hatch in --format csv ...

Request for TSV file format:

.. code-block:: text 

    hatch in --format tsv ... 

Elaborating the above example to a full command:

.. code-block:: text 

    hatch in --format tsv example_filename + count -x class 

.. note::

    ``in --format <type> ...`` forces Hatch to use the specified input type regardless of the filename extension or contents of the file. 

Input from standard input (stdin) 
---------------------------------

If you don't specify a file name when using the ``in`` command Hatch will assume that the input should be read from standard input (stdin).

.. code-block:: text

    hatch in + count -x class < titanic.csv

In the above example the notation ``< titanic.csv`` causes the contents of the file ``titantic.csv`` to be fed into the standard input of Hatch.
This is called *input redirection*. 

Instead of using input redirection, it is also possible to *pipe* the output from another command to the standard input of Hatch:

.. code-block:: text 

    cat titanic.csv | hatch in + count -x class

In the above example the command ``cat titanic.csv`` outputs the contents of the file ``titanic.csv`` to standard output which is then fed through a pipe using the ``|`` (vertical bar) operator
into the standard input of Hatch.

Reading from standard input is particularly useful when you want to use Hatch as part of a command pipeline: 

.. code-block:: text

    example_command | hatch in + count -x class

Here ``example_command`` is supposed to represent an arbitrary command, possibly itself a series of commands piped together, whose ouput is sent as input into Hatch.

.. warning::

   **Standard input defaults to CSV format**

   For performance reasons Hatch does not try to detect the format of the input file when reading from standard input. 

   Therefore, when reading from standard input, unless otherwise specified, Hatch assumes that the file is in CSV format.

   This can be overridden by ``in --format tsv ...`` 

   As previously noted, when reading from a named file Hatch will try to use the file name extension to determine the file format, avoiding the need to specify ``--format``.


Implicit CSV input from standard input device (stdin)
-----------------------------------------------------

For convenience, if you don't specify how to read input, Hatch will assume you wanted to read from standard input in CSV format.

Therefore:

.. code-block:: text

    hatch in + <rest of command>

is equivalent to:

.. code-block:: text

    hatch <rest of command>

In other words, if a Hatch command starts with ``in +`` you can simply omit that part, and Hatch will implicitly read from standard input using CSV format. This saves you a bit of typing and makes the command line tidier.

As a concrete example, the following command:

.. code-block:: text

    cat titanic.csv | hatch in + count -x class

can be simplified to:

.. code-block:: text

    cat titanic.csv | hatch count -x class

or, of course, you could achieve the same result with input redirection, again dropping the ``in +`` from the original command:

.. code-block:: text

    hatch count -x class < titanic.csv

Note carefully that when implicitly reading from standard input Hatch will always assume the input file is in CSV format. If you want to read a different format from standard input you must explicitly specify
the type using: ``in --format <type> ...``

Output files 
============

Hatch's default behaviour for plotting commands is to save the resulting image to a file (but it can also do interactive plots, see :ref:`the show command <show>`).

For example, the following command generates a count plot of the ``class`` feature from the input file ``titanic.csv`` and saves the resulting plot to a file called ``titanic.class.count.png``:

.. code-block:: text

    hatch count -x class titanic.csv

.. _out:

Output plot file name
---------------------

When saving a plot to a file, you can specify the name of the file to use with the ``-o <filename>`` or ``--out <filename>`` option. 

For example, the following command saves the output plot to a file called ``example.png``:

.. code-block:: text

    hatch count -x class -o example.png titanic.csv

If you do not specify an output file name, Hatch will choose an appropriate file name based on various input parameters:

 * The prefix of the input data file name (this can be overridden).
 * The name(s) of the columns that have been selected for plotting.
 * Optionally the names of columns that have been selected for grouping (for example by using ``--hue`` where applicable).
 * The type of plot being produced.

For example, the following command:

.. code-block:: text

    hatch hist -x sepal_length --hue species iris.csv

automatically produces an output file called ``iris.sepal_length.species.hist.png`` by default, because:

 * ``iris`` is the prefix of the name of the input file `iris.csv`
 * ``sepal_length`` is the column that has been selected for plotting
 * ``species`` is the column that has been selected for grouping via the ``--hue`` argument
 * ``hist`` is the type of plot (a histogram)

If the input data is read from the standard input (stdin) instead of a named file, then the prefix of the output defaults to ``plot``. For example, the following command:

.. code-block:: text

    hatch hist -x sepal_length --hue species < iris.csv 

produces an output file called ``plot.sepal_length.species.hist.png`` because the input data is read (redirected) from stdin.

.. _prefix:

Output prefix
-------------

The output prefix can be overridden with the ``--prefix`` command line option (regardless of whether the input comes from a named file or from stdin). For example:

.. code-block:: text

    hatch hist -x sepal_length --hue species --prefix flower < iris.csv

produces an output file called ``flower.sepal_length.species.hist.png``.

.. _format:

Output plot graphics file format 
--------------------------------

By default Hatch will save output plots in the PNG file format. However, this can be overridden with the ``--format {png,jpg,pdf,svg}`` option.

For example, the following command saves the output plot in SVG format, to a file called ``titanic.class.count.svg``:

.. code-block:: text

    hatch count -x class --format svg titanic.csv

.. note::

    If you do not specify an output file name, Hatch will choose one for you. This includes the addition of a file name suffix indicating the type of graphics format used (``png``, ``pdf``, ``svg``, or ``jpg``). 

    If you use ``-o`` (or ``--out``) to specify an output file name, Hatch will use that name verbatim and will not append suffix to the file name indicating the file type. Of course you may include a suffix in your own chosen name, however, this suffix does not influence the type of graphics format used. The only way to change the output graphics file format is with the ``--format`` option (otherwise the default ``png`` type is used).

.. _show:

Interactive plots
=================

The ``--show`` option overrides the default behaviour and causes the plot to be displayed in an interactive window (and not saved to a file). This assumes you are using Hatch in an environment with a graphics display.

This is illustrated below:

.. code-block:: text

    hatch count -x class --show titanic.csv

.. _save:

Transforming input data and saving to a file
============================================

Hatch supports a number of data manipulation options, such as :doc:`row filtering <filter/>`, :doc:`random sampling <sample/>`, :doc:`feature selection <features/>`, and :doc:`computation of new columns <eval/>`.

These manipulations are optionally performed prior to plotting or computing statistics.

However, it is also possible to apply these transformations and save the result back to a new file. This is achieved with the :doc:`transform <transform/>` command. For example, the following command randomly samples 100 rows
from the input file ``iris.csv``, and saves the result to ``iris.trans.csv`` (preserving the header row):

.. code-block:: text

    hatch transform --sample 100 iris.csv

The default output file name can be overridden with ``-o`` (``--out``) like so: 

.. code-block:: text

    hatch transform --sample 100 -o iris.sample100.csv iris.csv

.. _log:

Logging progress
================

The ``--logfile <filename>`` option causes Hatch to record a timestamped log of program progress to a file. Logging information includes the command line used to invoke the program and key program events.
The log file can be useful for debugging Hatch's behaviour.

In the following example we add logging to a plotting command, such that the output log data is written to a file called ``hatch.log``:

.. code-block:: text

   hatch count -x class --logfile hatch.log titanic.csv

.. _verbose:

Verbose execution
=================

By default Hatch does not display any messages on the standard output during normal program execution. This can be overridden with 
the ``--verbose`` option which causes Hatch to become more chatty. In particular, when generating any output files, the verbose
mode will cause Hatch to specify the names of any files it has created. This is useful when you want to immediately open the file
for further inspection.

.. code-block:: text

    hatch count -x class --verbose titanic.csv 

The outut of the above command is:

.. code-block:: text 

    Plot written to titanic.class.count.png

.. _navalues:

NA values
=========
