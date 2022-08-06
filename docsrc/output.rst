.. _output_files:

Writing output data 
===================

Gurita can write data to a named output file or standard output (stdout).

Output to a named file 
----------------------

The ``out`` command allows you to specify an output file by name:

.. code-block:: text 

    gurita ... + out newfile.csv

As before, we use ``...`` to indicate that part of the example Gurita command is omitted for the sake of simplifying the discussion.

You should imagine that ``...`` would be replaced by more text to complete the command.
For example, the following command reads the file ``titanic.csv`` from standard input and then saves the header row and first ten data rows to an output file called ``newfile.csv``:

.. code-block:: text 

    cat titanic.csv | gurita head 10 + out newfile.csv 

Again we see :ref:`command chaining <command_chain>` in action, where the first command ``head 10`` transforms the input data before it is passed along to the ``out newfile.csv`` command.

When writing output to a named file (and not to standard output) Gurita will look at the file extension and assume CSV format if the extension is ``.csv`` and TSV format if the extension is ``.tsv``. This behaviour can be overridden with the
``--sep <str>`` option as noted below. 

.. warning:: 

   When writing to a named file, if the file already exists,  the ``out`` command will overwrite its contents. The original contents of the file will be lost.

Specifying the field separator explicitly 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``out`` command lets you specify the field separator of the output file explicitly. This will override any default behaviour that Gurita would otherwise have when determining the output file type.
This mimics the behaviour of the ``in`` command for reading input from files, as discussed previously.

Request for CSV file format: 

.. code-block:: text 

    gurita ... out --sep ',' ...

Note: comma is the default separator used by Gurita, so you don't need to specify it explicitly. Therefore the above example is redundant, and only shown for the sake of illustration.

Request for TSV file format:

.. code-block:: text 

    gurita ... out --sep '\t' ...

Be sure to enclose the ``\t`` in quote characters to ensure that it is treated as a single string.

Elaborating the above example to a full command:

.. code-block:: text 

    cat titanic.csv | gurita head 10 + out --sep '\t' example_filename 

Using a vertical bar character as the field separator:

.. code-block:: text 

    gurita ... out --sep '|' ... 

.. note::

    ``out --sep <str>``  forces Gurita to use the specified field separator regardless of the filename extension or contents of the file. 

Output to standard output (stdout) 
----------------------------------

If you don't specify a file name when using the ``out`` command Gurita will assume that the output should be written to standard output (stdout):

.. code-block:: text

    gurita ... out

For example:

.. code-block:: text

    cat titanic.csv | gurita head 10 + out

Writing to standard output is particularly useful when you want to use Gurita as part of a command pipeline: 

.. code-block:: text

    gurita ... + out | example_command

Here ``example_command`` is supposed to represent an arbitrary command, possibly itself a series of commands piped together, whose input comes from the standard output of Gurita.

.. note::

   **Standard output defaults to CSV format**

   When writing to standard output, unless otherwise specified, Gurita assumes that the file is in CSV format.

   This can be overridden by ``out --sep <str>`` 

   As previously noted, when writing to a named file Gurita will try to use the file name extension to determine the file format, avoiding the need to specify ``--sep``.


Implicit CSV output to standard output (stdout)
-----------------------------------------------

In some circumstances, for convenience, Gurita will implicitly write the final state of the data to standard output. It chooses to do this in precisely two circumstances, when
the last command in a chain is either:

   * a data transformation
   * an input command (including implicitly reading from standard input)

However, Gurita will *not* implicitly write the final state of the data to standard output when the last command in a chain is either:

   * a plotting command
   * a data summary command 
   * an ``out`` command

The logic for this behaviour is as follows.

If the last command in a chain is a transformation or just an input command, Gurita assumes that you must have read/transformed the data for a reason and you probably
want to save/use the result. If a command chain does not explicitly end with an ``out`` command the final state of the data would be lost. So Gurita writes it to standard output in CSV format for you.

If the last command in a chain is a plotting command, then Gurita assumes that your main purpose must have been to generate the plot, and therefore you are not interested in saving/using the final state of the data. 
Similarly for situations when the last command shows summary information about the data, such as ``pretty``.
If you want to make a plot or see summary information *and* save the final state of the data you can always achieve this by ending a chain with an explicit ``out`` command. 

Therefore:

.. code-block:: text

    gurita <transformation or input command> + out

can be simplified to:

.. code-block:: text

    gurita <transformation or input command>

As a concrete example, the following command:

.. code-block:: text

    cat titanic.csv | gurita head 10 + out

can be simplified to:

.. code-block:: text

    cat titanic.csv | gurita head 10

or, of course, you could achieve the same result with input redirection, again dropping the ``+ out`` from the original command:

.. code-block:: text

    gurita head 10 < titanic.csv

Note carefully that when implicitly writing to standard output Gurita will always assume the output file should be written in CSV format. If you want to read a different format from standard input you must explicitly specify
the type using: ``out --sep <str> ...``

Writing output to more than one file in a command chain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may write output to more than one file in a command chain, both to named files and standard output. 

For example you can do something like this:

.. code-block:: text

    gurita ... out newfile1.csv + ... + out newfile2.tsv + ... 

In the above example, output is written to ``newfile1.csv`` in CSV format, then some unspecified commands are run, and later output is written to ``newfile2.tsv`` in TSV format, and some more unspecified commands are run.

Each invocation of ``out`` causes the current data set to be written to a file or standard output. When used in a chain of commands ``out`` also passes the current data set along unmodified to the next command in the chain. This allows
the data to be passed along from left to right in the chain with further processing of the data occurring after the ``out`` command has been executed.

This is most useful when you want to save different states of the data as it undergoes various transformations in a command chain.

Warning: if you have two separate ``out`` commands that write to the same named output file, the last occurrence will overwrite any earlier output that that file. 

However, if multiple different writes to standard output are used, they will form a single concatenated stream of data. 

The following command is a more concrete example:

.. code-block:: text

   gurita in iris.csv + sample 0.6 + out samp.csv + cut -c sepal_length + out len.tsv

There are five parts to the above command chain:

1. input is read from the ``iris.csv`` file, this becomes the current data set
2. 60% of the data rows in the current data set are randomly sampled, the remaining 40% of the rows are discareded
3. the current (sampled) data set is written to the output file ``samp.csv`` in CSV format
4. the ``sepal_length`` column is selected from the current (sampled) data set and the remaining columns are discareded 
5. the final (cut and sampled) data set is written to the output file ``len.tsv`` in TSV format 


Converting between TSV and CSV formats
--------------------------------------

Gurita can read and write data in both CSV and TSV formats. Therefore, one simple but useful thing it can easily do is convert data files
between those formats. Notably, in such conversions it will handle corner cases correctly, such as proper quotation of data values, and
appropriate formatting of missing (NA) values. 

For example, the following commands all convert the ``iris.csv`` file (in CSV format) into TSV format, and save the result in a file called ``iris.tsv``:

.. code-block:: text

   gurita in iris.csv + out iris.tsv

.. code-block:: text

   cat iris.csv | gurita out iris.tsv

.. code-block:: text

   cat iris.csv | gurita out --sep '\t' > iris.tsv

Conversely, the following commands all convert the ``iris.tsv`` file (in TSV format) into CSV format, and save the result in a file called ``iris.csv``:

.. code-block:: text

   gurita in iris.tsv + out iris.csv

.. code-block:: text

   cat iris.tsv | gurita in --sep '\t' + out iris.csv

.. code-block:: text

   cat iris.tsv | gurita in --sep '\t' + out > iris.csv

Note that in the above example there is no need to specify that the output file is in CSV format because that is the default behaviour of the ``out`` command.

