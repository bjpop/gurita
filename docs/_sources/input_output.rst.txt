.. _input_output: 

Input and output data
*********************

Hatch works on tabular data in `CSV (comma separated values) <https://en.wikipedia.org/wiki/Comma-separated_values>`_ or `TSV (tab separated values) <https://en.wikipedia.org/wiki/Tab-separated_values>`_ format.

Input data is read from a named file or the standard input (stdin). Data can be written to a named file or standard output (stdout).

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
   :ref:`Missing values <missing_values>` are allowed, and are indicated by leaving a particular entry blank (empty) or marking it with a special value. 

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

When reading input from a named file (and not from standard input) Hatch will look at the file extension and assume CSV format if the extension is ``.csv`` and TSV format if the extension is ``.tsv``. This behaviour can be overridden with the
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

.. note::

   **Standard input defaults to CSV format**

   For performance reasons Hatch does not try to detect the format of the input file when reading from standard input. 

   Therefore, when reading from standard input, unless otherwise specified, Hatch assumes that the file is in CSV format.

   This can be overridden by ``in --format tsv ...`` 

   As previously noted, when reading from a named file Hatch will try to use the file name extension to determine the file format, avoiding the need to specify ``--format``.

   **Standard input can only be read once in a Hatch command**

   A Hatch command can only read from standard input at most once in a command. An attempt to read from standard input more than once will result in an error: 

   .. code-block:: text

       hatch in + count -x class + in < titanic.csv
       hatch ERROR: stdin may only be used at most once, and only as the first command; exiting

   **Standard input can only be read at the start of a command**

   Hatch will only permit standard input to be read at the start of a command chain. Therefore it is an error to request to read
   from standard input in any position other then the first command in the chain:

   .. code-block:: text

      hatch count -x class + in < titanic.csv
      hatch ERROR: stdin may only be used at most once, and only as the first command; exiting

   Note that this restriction is only a concern when using the ``in`` command to read from standard input, and does
   not apply when reading from standard input implicitly (as noted below).


Implicit CSV input from standard input (stdin)
-----------------------------------------------------

For convenience, if you don't specify how to read input, Hatch will assume you wanted to read from standard input in CSV format.

Therefore:

.. code-block:: text

    hatch in + <rest of command>

can be simplified to:

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

Reading input from more than one file in a command chain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may read input from more than one file in a command chain, but only when each of those files is read from a named file (and not standard input). 

For example you can do something like this:

.. code-block:: text

    hatch in titanic.csv + ... + in iris.csv + ... 

In the above example, first ``titanic.csv`` is read as input, then some unspecified commands are run, and later ``iris.csv`` is read as input, and some more unspecified commands are run.

Whenever a new input is read from a named file the contents of that file become the current data set, and any previous data set in the command chain is discarded.

The following command is a more concrete example:

.. code-block:: text

   hatch in titanic.csv + hist -x fare + in iris.csv + count -x species

There are four parts to the above command chain:

1. input is read from the ``titanic.csv`` file, this becomes the current data set
2. a histogram is plotted of the ``fare`` column from the current (titanic) data set, generating an output file called ``hist.fare.png`` 
3. input is read from the ``iris.csv`` file, this becomes the new current data set, replacing the titanic data set, which is now discarded 
4. a count plot is created using the ``species`` column for the X axis from the current (iris) data set, generating an output file called ``count.species.png``

.. _output_files:

Output data 
===========

Hatch can write data to a named output file or standard output (stdout).

Output to a named file 
----------------------

The ``out`` command allows you to specify an output file by name:

.. code-block:: text 

    hatch ... + out newfile.csv

As before, we use ``...`` to indicate that part of the example Hatch command is omitted for the sake of simplifying the discussion.

You should imagine that ``...`` would be replaced by more text to complete the command.
For example, the following command reads the file ``titanic.csv`` from standard input and then saves the header row and first ten data rows to an output file called ``newfile.csv``:

.. code-block:: text 

    cat titanic.csv | hatch head 10 + out newfile.csv 

Again we see :ref:`command chaining <command_chain>` in action, where the first command ``head 10`` transforms the input data before it is passed along to the ``out newfile.csv`` command.

When writing output to a named file (and not to standard output) Hatch will look at the file extension and assume CSV format if the extension is ``.csv`` and TSV format if the extension is ``.tsv``. This behaviour can be overridden with the
``--format <type>`` option as noted below. This mimics the behaviour of the ``in`` command for reading input from files, as discussed previously.

Specifying output file type explicitly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``out`` command lets you specify the format of the output file explicitly. This will override any default behaviour that Hatch would otherwise have when determining the output file type.

Request for CSV file format: 

.. code-block:: text 

    hatch ... out --format csv ...

Request for TSV file format:

.. code-block:: text 

    hatch ... out --format tsv ...

Elaborating the above example to a full command:

.. code-block:: text 

    cat titanic.csv | hatch head 10 + out --format tsv example_filename 

.. note::

    ``out --format <type> ...`` forces Hatch to use the specified output type regardless of the filename extension or contents of the file. 

Output to standard output (stdout) 
----------------------------------

If you don't specify a file name when using the ``out`` command Hatch will assume that the output should be written to standard output (stdout).

.. code-block:: text

    cat titanic.csv | hatch head 10 + out

Writing to standard output is particularly useful when you want to use Hatch as part of a command pipeline: 

.. code-block:: text

    hatch ... + out | example_command

Here ``example_command`` is supposed to represent an arbitrary command, possibly itself a series of commands piped together, whose input comes from the standard output of Hatch.

.. note::

   **Standard output defaults to CSV format**

   When writing to standard output, unless otherwise specified, Hatch assumes that the file is in CSV format.

   This can be overridden by ``out --format tsv`` 

   As previously noted, when writing to a named file Hatch will try to use the file name extension to determine the file format, avoiding the need to specify ``--format``.


Implicit CSV output to standard output (stdout)
-----------------------------------------------

In some circumstances, for convenience, Hatch will implicitly write the final state of the data to standard output. It chooses to do this in precisely two circumstances, when
the last command in a chain is either:

   * a data transformation
   * an input command (including implicitly reading from standard input)

However, Hatch will *not* implicitly write the final state of the data to standard output when the last command in a chain is either:

   * a plotting command
   * a data summary command 
   * an ``out`` command

The logic for this behaviour is as follows.

If the last command in a chain is a transformation or just an input command, Hatch assumes that you must have read/transformed the data for a reason and you probably
want to save/use the result. And because you didn't explicitly end the chain with an ``out`` command, the final state of the data would otherwise be lost. So Hatch writes it to standard output in CSV format for you.

If the last command in a chain is a plotting command, then Hatch assumes that your main purpose must have been to generate the plot, and therefore you are not interested in saving/using the final state of the data. 
Similarly for situations when the last command shows summary information about the data, such as ``pretty``.
If you want to make a plot or see summary information *and* save the final state of the data you can always achieve this by ending a chain with an explicit ``out`` command. 

If the last command in a chain is an ``out`` command there is no need for implicit output.

Therefore:

.. code-block:: text

    hatch <transformation or input command> + out

can be simplified to:

.. code-block:: text

    hatch <transformation or input command>

As a concrete example, the following command:

.. code-block:: text

    cat titanic.csv | hatch head 10 + out

can be simplified to:

.. code-block:: text

    cat titanic.csv | hatch head 10

or, of course, you could achieve the same result with input redirection, again dropping the ``+ out`` from the original command:

.. code-block:: text

    hatch head 10 < titanic.csv

Note carefully that when implicitly writing to standard output Hatch will always assume the output file should be written in CSV format. If you want to read a different format from standard input you must explicitly specify
the type using: ``out --format <type> ...``

Writing output to more than one file in a command chain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may write output to more than one file in a command chain, both to named files and standard output. 

For example you can do something like this:

.. code-block:: text

    hatch ... out newfile1.csv + ... + out newfile2.tsv + ... 

In the above example, output is written to ``newfile1.csv`` in CSV format, then some unspecified commands are run, and later output is written to ``newfile2.tsv`` in TSV format, and some more unspecified commands are run.

Each invocation of ``out`` causes the current data set to be output to a file or standard output. When used in a chain of commands ``out`` also passes the current data set along unmodified to the next command in the chain. This allows
the data to be passed along from left to right in the chain with further processing of the data occurring after the ``out`` command has been executed.

This is most useful when you want to save different states of the data as it undergoes various transformations in a command chain.

Note that if multiple different writes to standard output are used, they will form a single concatenated stream of data. 

The following command is a more concrete example:

.. code-block:: text

   hatch in iris.csv + sample 0.6 + out samp.csv + cut -c sepal_length + out len.tsv

There are five parts to the above command chain:

1. input is read from the ``iris.csv`` file, this becomes the current data set
2. 60% of the data rows in the current data set are randomly sampled, the remaining 40% of the rows are discareded
3. the current (sampled) data set is written to the output file ``sample.csv`` in CSV format
4. the ``sepal_length`` column is selected from the current (sampled) data set and the remaining columns are discareded 
5. the final (cut and sampled) data set is written to the output file ``len.tsv`` in TSV format 


Using Hatch to convert between TSV and CSV formats
==================================================

Hatch can read and write data in both CSV and TSV formats. Therefore, one simple, but useful thing it can easily do is convert data files
between those formats. Notably, in such conversions it will handle corner cases correctly, such as proper quotation of data values, and
appropriate formatting of missing (NA) values. 

For example, the following commands all convert the ``iris.csv`` file (in CSV format) into TSV format, and save the result in a file called ``iris.tsv``:

.. code-block:: text

   cat iris.csv | hatch out --format tsv > iris.tsv

.. code-block:: text

   cat iris.csv | hatch out iris.tsv

.. code-block:: text

   hatch in iris.csv + out iris.tsv

Conversely, the following commands all convert the ``iris.tsv`` file (in TSV format) into CSV format, and save the result in a file called ``iris.csv``:

.. code-block:: text

   cat iris.tsv | hatch out > iris.csv

Note that in the above example there is no need to specify that the output file is in CSV format because that is the default behaviour of the ``out`` command.

.. code-block:: text

   cat iris.csv | hatch out iris.csv

.. code-block:: text

   hatch in iris.tsv + out iris.csv

.. _missing_values:

Missing (NA) values
===================
