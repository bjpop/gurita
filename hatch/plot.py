'''
Module      : Main
Description : Plotting for Hatch
Copyright   : (c) Bernie Pope, 16 Oct 2019 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import logging
import pkg_resources
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import sklearn.decomposition as sk_decomp 
from sklearn.impute import SimpleImputer
import math
import numpy as np
import scipy
import hatch.utils as utils
import hatch.constants as const

def do_plot(df, options):
    # plotting commands go here
    kwargs = {}
    sns.set_style(options.style)
    sns.set_context(options.context)
    if options.cmd == 'hist':
        Displot(options.cmd, options, df, kwargs).plot()
    elif options.cmd == 'count':
        if options.xaxis is not None and options.yaxis is not None:
            utils.exit_with_error("You cannot use both -x (--xaxis) and -y (--yaxis) at the same time in a count plot", const.EXIT_COMMAND_LINE_ERROR)
        elif options.xaxis is not None:
            Catplot(options.cmd, options, df, kwargs).plot()
        elif options.yaxis is not None:
            Catplot(options.cmd, options, df, kwargs).plot()
        else:
            utils.exit_with_error("A count plot requires either -x (--xaxis) or -y (--yaxis) to be specified", const.EXIT_COMMAND_LINE_ERROR)
    elif options.cmd in ['box', 'violin', 'swarm', 'strip', 'boxen', 'bar', 'point']:
        Catplot(options.cmd, options, df, kwargs).plot()
    elif options.cmd == 'line':
        Relplot(options.cmd, options, df, kwargs).plot()
    elif options.cmd == 'scatter':
        kwargs = { 'size': options.dotsize, 'alpha': options.dotalpha, 'linewidth': options.dotlinewidth }
        Relplot(options.cmd, options, df, kwargs).plot()
    elif options.cmd == 'heatmap':
        Heatmap(options, df).plot()
    elif options.cmd == 'clustermap':
        Clustermap(options, df).plot()
    elif options.cmd == 'pca':
        PCA(options, df).plot()


class Plot:
    def __init__(self, options, df):
        self.options = options
        self.df = df
        self.fig = None
        self.ax = None

    def plot(self):
        options = self.options
        plt.suptitle('')
        self.fig, self.ax = plt.subplots(figsize=(options.width, options.height))
        self.render_data()
        if hasattr(options, 'title') and options.title is not None:
            plt.title(options.title)
        if hasattr(options, 'xlabel') and options.xlabel is not None:
            self.ax.set(xlabel=options.xlabel)
        if hasattr(options, 'ylabel') and options.ylabel is not None:
            self.ax.set(ylabel=options.ylabel)
        if hasattr(options, 'xlim') and options.xlim is not None:
            xlow, xhigh = options.xlim
            plt.xlim(xlow, xhigh)
        if hasattr(options, 'ylim') and options.ylim is not None:
            ylow, yhigh = options.ylim
            plt.ylim(ylow, yhigh)
        if hasattr(options, 'noxticklabels') and options.noxticklabels:
            self.ax.set(xticks=[])
            self.ax.set(xticklabels=[])
        if hasattr(options, 'noyticklabels') and options.noyticklabels:
            self.ax.set(yticks=[])
            self.ax.set(yticklabels=[])
        if hasattr(options, 'rotxticklabels') and options.rotxticklabels is not None:
            self.ax.set_xticklabels(self.ax.get_xticklabels(), rotation=options.rotxticklabels)
        if hasattr(options, 'rotyticklabels') and options.rotyticklabels is not None:
            self.ax.set_yticklabels(self.ax.get_yticklabels(), rotation=options.rotyticklabels)
        if hasattr(options, 'logy') and options.logy:
            self.ax.set(yscale="log")
        if hasattr(options, 'logx') and options.logx:
            self.ax.set(xscale="log")
        #plt.tight_layout()
        if options.show:
            plt.show()
        else:
           output_filename = self.make_output_filename()
           plt.savefig(output_filename, bbox_inches='tight', format=self.options.format)
           if self.options.verbose:
               print(f"Plot written to {output_filename}")
        plt.close()

    def render_data(self):
        raise NotImplementedError

    def make_output_filename(self):
        raise NotImplementedError


class Facetplot(object):
    def __init__(self, kind, options, df, kwargs):
        self.options = options
        self.df = df
        self.kind = kind
        self.x = options.xaxis
        self.y = options.yaxis
        self.hue = options.hue
        self.row = options.row
        self.col = options.col
        self.kwargs = kwargs
        features = [f for f in [self.x, self.y] if f is not None]
        utils.check_df_has_features(self.df, features)

    def plot(self):
        options = self.options
        graph = self.make_graph(self.kwargs)
        if options.logx:
            graph.set(xscale="log")
        if options.logy:
            graph.set(yscale="log")
        if hasattr(options, 'title') and options.title is not None:
            plt.title(options.title)
        if hasattr(options, 'xlim') and options.xlim is not None:
            xlow, xhigh = options.xlim
            plt.xlim(xlow, xhigh)
        if hasattr(options, 'ylim') and options.ylim is not None:
            ylow, yhigh = options.ylim
            plt.ylim(ylow, yhigh)
        if hasattr(options, 'rotxticklabels') and options.rotxticklabels is not None:
            for ax in graph.axes.ravel():
                ax.set_xticklabels(ax.get_xticklabels(), rotation=options.rotxticklabels)
        if options.show:
            plt.show()
        else:
           output_filename = self.make_output_filename()
           plt.savefig(output_filename, bbox_inches='tight', format=self.options.format)
           if self.options.verbose:
               print(f"Plot written to {output_filename}")
        plt.close() 

    def make_graph(self, kwargs):
        raise NotImplementedError

    def make_output_filename(self):
        options = self.options
        if options.out:
            return options.out
        else:
            extension = [options.format]
            output_name = [utils.get_output_name(options)]
            y_str = utils.output_field(self.y)
            x_str = utils.output_field(self.x)
            hue_str = utils.output_field(self.hue)
            row_str = utils.output_field(self.row)
            col_str = utils.output_field(self.col)
            type_str = [self.kind]
            return Path('.'.join(output_name + y_str + x_str +
                                 hue_str + row_str + col_str +
                                 type_str + extension))

# Displots call the displot interface in Seaborn, and thus share common
# functionality https://seaborn.pydata.org/generated/seaborn.displot.html 
class Displot(Facetplot):
    def __init__(self, kind, options, df, kwargs):
        super().__init__(kind, options, df, kwargs)
    

    def make_graph(self, kwargs):
        options = self.options
        facet_kws = { 'legend_out': True }
        aspect = 1
        if options.bins:
            kwargs['bins'] = options.bins
        if options.binwidth:
            kwargs['binwidth'] = options.binwidth
        if options.width > 0:
            aspect = options.width / options.height
        if options.multiple:
            kwargs['multiple'] = options.multiple
        if options.kde:
            kwargs['kde'] = options.kde
        graph = sns.displot(kind=self.kind, data=self.df,
                x=self.x, y=self.y, col=self.col, row=self.row,
                height=options.height, aspect=aspect, hue=self.hue,
                cumulative=options.cumulative,
                hue_order=options.hueorder, 
                facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        return graph


# Catplots call the catplot interface in Seaborn, and thus share common
# functionality https://seaborn.pydata.org/tutorial/categorical.html
class Catplot(Facetplot):
    def __init__(self, kind, options, df, kwargs):
        super().__init__(kind, options, df, kwargs)

    def make_graph(self, kwargs):
        options = self.options
        facet_kws = { 'legend_out': True }
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        graph = sns.catplot(kind=self.kind, data=self.df,
                x=self.x, y=self.y, col=self.col, row=self.row,
                height=options.height, aspect=aspect, hue=self.hue,
                order=options.order, hue_order=options.hueorder,
                orient=options.orient, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        return graph


# Relplots call the relplot interface in Seaborn, and thus share common
# functionality https://seaborn.pydata.org/tutorial/relational.html 
class Relplot(Facetplot):
    def __init__(self, kind, options, df, kwargs):
        super().__init__(kind, options, df, kwargs)

    def make_graph(self, kwargs):
        options = self.options
        aspect = 1
        if options.width > 0:
            aspect = options.width / options.height
        facet_kws = { 'legend_out': True }
        graph = sns.relplot(kind=self.kind, data=self.df,
                x=self.x, y=self.y, col=self.col, row=self.row,
                height=options.height, aspect=aspect, hue=self.hue,
                hue_order=options.hueorder, facet_kws=facet_kws, col_wrap=options.colwrap, **kwargs)
        return graph


class PCA(Plot):
    def __init__(self, options, df):
        super().__init__(options, df)

    def render_data(self):

        # select only numeric features for the PCA
        numeric_df = self.df.select_dtypes(include=np.number)

        # Handle rows in the data that have missing values
        if self.options.missing == 'drop':
            numeric_df = numeric_df.dropna()
        elif self.options.missing == 'imputemean':
            imputer = SimpleImputer(strategy='mean')
            numeric_df = imputer.fit_transform(numeric_df)
        elif self.options.missing == 'imputemedian':
            imputer = SimpleImputer(strategy='median')
            numeric_df = imputer.fit_transform(numeric_df)
        elif self.options.missing == 'imputemostfrequent':
            imputer = SimpleImputer(strategy='most_frequent')
            numeric_df = imputer.fit_transform(numeric_df)
        # Standardize features by removing the mean and scaling to unit variance 
        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(numeric_df)
        # Perform PCA on the standardized data
        pca = sk_decomp.PCA(n_components=2)
        pca_transform = pca.fit_transform(standardized_data)
        # Build a new dataframe for the PCA transformed data, adding columnd headings for the 2 components
        first_two_components = pd.DataFrame(data = pca_transform, columns = ['principal component 1', 'principal component 2'])
        # Optionally select a column to use for colouring the dots in the plot
        if self.options.hue is not None:
            hue_column = self.df[self.options.hue]
            first_two_components = first_two_components.join(hue_column)
        # Generate a scatter plot for the PCA transformed data
        graph=sns.scatterplot(data=first_two_components, x='principal component 1', y='principal component 2', hue=self.options.hue,
                          alpha=self.options.dotalpha, size=self.options.dotsize, linewidth=self.options.dotlinewidth)
        self.ax.set(xlabel='principal component 1', ylabel='principal component 2')
        if self.options.hue is not None:
            graph.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        if self.options.nolegend:
            graph.legend_.remove()

    def make_output_filename(self):
        if self.options.out:
            return self.options.out
        else:
            extension = self.options.format
            output_name = utils.get_output_name(self.options)
            return Path('.'.join([output_name, 'pca', extension])) 


class Heatmap(Plot):
    def __init__(self, options, df):
        if options.xaxis not in df.columns:
            utils.exit_with_error(f"{options.xaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        if options.yaxis not in df.columns:
            utils.exit_with_error(f"{options.yaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)

        if options.val not in df.columns:
            utils.exit_with_error(f"{options.val} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        super().__init__(options, df)
        self.x = options.xaxis 
        self.y = options.yaxis 
        self.val = options.val 

    def render_data(self):
        pivot_data = self.df.pivot(index=self.y, columns=self.x, values=self.val)
        sns.heatmap(data=pivot_data, cmap=self.options.cmap)

    def make_output_filename(self):
        options = self.options
        if options.out:
            return options.out
        else:
            extension = [options.format]
            output_name = [utils.get_output_name(options)]
            x_str = utils.output_field(self.x)
            y_str = utils.output_field(self.y)
            val_str = utils.output_field(self.val)
            type_str = ['heatmap']
            return Path('.'.join(output_name + x_str + y_str + val_str + type_str + extension))


class Clustermap(Plot):
    def __init__(self, options, df):
        if options.xaxis not in df.columns:
            utils.exit_with_error(f"{options.xaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        if options.yaxis not in df.columns:
            utils.exit_with_error(f"{options.yaxis} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)

        if options.val not in df.columns:
            utils.exit_with_error(f"{options.val} is not an attribute of the data set", const.EXIT_COMMAND_LINE_ERROR)
        super().__init__(options, df)
        self.x = options.xaxis 
        self.y = options.yaxis 
        self.val = options.val 

    def render_data(self):
        options = self.options
        pivot_data = self.df.pivot(index=self.y, columns=self.x, values=self.val)
        figsize = (options.width, options.height)
        z_score = None
        if options.zscore == 'y':
            z_score = 0
        elif options.zscore == 'x':
            z_score = 1
        standard_scale = None
        if options.stdscale == 'y':
            standard_scale = 0
        elif options.zscore == 'x':
            standard_scale = 1
        xticklabels = True
        if options.noxticklabels:
            xticklabels = False
        yticklabels = True
        if options.noyticklabels:
            yticklabels = False
        # clustermap does not allow both zscore and standard_scale to be specified at the
        # same time, even if only one is None. 
        if standard_scale is not None:
            sns.clustermap(data=pivot_data, cmap=options.cmap, figsize=figsize,
                dendrogram_ratio=options.dendroratio, row_cluster=options.rowclust,
                col_cluster=options.colclust, yticklabels=yticklabels, xticklabels=xticklabels,
                standard_scale=standard_scale, method=options.method, metric=options.metric)
        elif z_score is not None:
            sns.clustermap(data=pivot_data, cmap=options.cmap, figsize=figsize,
                dendrogram_ratio=options.dendroratio, row_cluster=options.rowclust,
                col_cluster=options.colclust, z_score=z_score, yticklabels=yticklabels,
                xticklabels=xticklabels, method=options.method, metric=options.metric)
        else:
            sns.clustermap(data=pivot_data, cmap=options.cmap, figsize=figsize,
                dendrogram_ratio=options.dendroratio, row_cluster=options.rowclust,
                col_cluster=options.colclust, yticklabels=yticklabels, xticklabels=xticklabels,
                method=options.method, metric=options.metric)

    def make_output_filename(self):
        options = self.options
        if options.out:
            return options.out
        else:
            extension = [options.format]
            output_name = [utils.get_output_name(options)]
            x_str = utils.output_field(self.x)
            y_str = utils.output_field(self.y)
            val_str = utils.output_field(self.val)
            type_str = ['clustermap']
            return Path('.'.join(output_name + x_str + y_str + val_str + type_str + extension))
