<p align="center">
  <img src="docs/_images/gurita_using_computer.png" width="250" alt="fun image of octopus using a computer">
</p>

# Gurita: a command line data analytics and plotting tool 


Gurita is a command line tool for analysing and visualising tabular data in CSV or TSV format.

At its core Gurita provides a suite of commands, each of which carries out a common data analytics or plotting task.

**A unique and powerful feature of Gurita** is that commands to be chained together into flexible analysis pipelines. See the advanced example below.

It is designed to be fast and convenient, and is particularly suited to data exploration tasks. Input files with large numbers of rows (> millions) are readily supported.

Gurita commands are highly customisable, however sensible defaults are applied. Therefore simple tasks are easy to express
and complex tasks are possible.

Gurita is implemented in [Python](http://www.python.org/) and makes extensive use of the [Pandas](https://pandas.pydata.org/), [Seaborn](https://seaborn.pydata.org/), and [Scikit-learn](https://scikit-learn.org/) libraries for data processing and plot generation.

# Documentation

Please consult the [Gurita Documentation](https://bjpop.github.io/gurita/index.html) for detailed information about installation and usage.

# Examples

### Simple example

Box plot of `sepal_length` for each species in the classic [iris dataset](https://github.com/mwaskom/seaborn-data/blob/master/iris.csv/):

```bash
cat iris.csv | gurita box -x species -y sepal_length
```

<p align="center">
  <img src="docs/_images/box.species.sepal_length.png" width="400" alt="example box plot of sepal_length for each species in the classic iris dataset">
</p>

### Advanced example 

The following example illustrates Gurita's ability to chain commands together. 

Commands in a chain are separated by the plus sign (+) and data flows from left to right in the chain.

```bash
cat iris.csv | gurita filter 'species != "virginica"' \
                      + sample 0.9 \
                      + pca \
                      + scatter -x pc1 -y pc2 --hue species
```

<p align="center">
  <img src="docs/_images/scatter.pc1.pc2.species.png" width="500" alt="Scatter plot comparing principal components pc1 and pc2 from a filtered iris dataset">
</p>

In this example there are 4 commands that are executed in the following order:

1. The ``filter`` command selects all rows where ``species`` is not equal to ``virginica``.
2. The filtered rows are then passed to the ``sample`` command which randomly selects 90% of the remaining rows.
3. The sampled rows are then passed to the ``pca`` command which performs principal component analysis (PCA) as a data reduction step, yielding two extra columns in the data called ``pc1`` and ``pc2``.
4. Finally the pca-transformed data is passed to the `scatter` command which generates a scatter plot of ``pc1`` and ``pc2`` (the first two principal components).

# Licence

This program is released as open source software under the terms of [MIT License](https://raw.githubusercontent.com/bjpop/gurita/master/LICENSE).

# Authors

 * [Bernie Pope](http://www.berniepope.id.au/)
