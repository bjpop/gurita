.. _input_output: 

Tabular input and output data
*****************************

Gurita reads and writes data in tabular data format.

By default it will use `CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ format, where a comma is used as the field separator. However, upon request, it allows alternative field separators to be used.
For example, `TSV <https://en.wikipedia.org/wiki/Tab-separated_values>`_ files are supported by setting the field separator to a tab character (\\t).

Input data is read from a named file or the standard input (stdin). Data can be written to a named file or standard output (stdout).

Rows in the input file are considered to be "observations" and columns are considered to be "features" (or variables). 
That is, each data row is a discrete observation of some thing (a data point), and each observation is described by the values of its columns.
The names of the columns are given in the first row of the input file (the heading row).

Below is a small example of the kind of input data accepted by Gurita. In this case it is in CSV format with five columns, one heading row and three data rows.
The first row contains the names of each column. The remaining three rows are data rows,
where each row has a value associated with each column:

.. code-block:: text 

    sepal_length,sepal_width,petal_length,petal_width,species
    5.1,3.5,1.4,0.2,setosa
    4.9,3.0,1.4,0.2,virginica
    4.7,3.2,1.3,0.2,setosa

.. note::

   Gurita requires that the input data is **rectangular** in shape. In other words, every row must contain the same number of columns.
   :ref:`Missing values <missing_values>` are allowed, and are indicated by leaving a particular entry blank (empty) or marking it with a special value. 
