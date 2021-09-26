'''
Module      : pca 
Description : Principal Components Analysis (PCA) 
Copyright   : (c) Bernie Pope, 22 September 2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import sys
import logging
import pandas as pd
from sklearn.preprocessing import StandardScaler
import sklearn.decomposition as sk_decomp 
from sklearn.impute import SimpleImputer
import numpy as np
import argparse
import hatch.constants as const
from hatch.command_base import CommandBase

class PCA(CommandBase, name="pca"):
    description = "Principal component analysis (PCA)."
    category = "transformation"

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument(
            '--missing', required=False, default=const.DEFAULT_PCA_MISSING, choices=const.ALLOWED_PCA_MISSING,
            help=f'How to deal with rows that contain missing data. Allowed values: %(choices)s. Default: %(default)s.')
        parser.add_argument(
            '--pcaprefix', required=False, default=const.DEFAULT_PCA_PREFIX,
            help=f'Column label prefix for principal component axes. Default: %(default)s.')
        parser.add_argument(
            '-n', '--ncomps', type=int, required=False, default=const.DEFAULT_PCA_N_COMPONENTS,
            help=f'Number of principal components to generate. Default: %(default)s.')
        self.options = parser.parse_args(args)
    
    def run(self, df):
        # select only numeric features for the PCA
        numeric_df = df.select_dtypes(include=np.number)

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
        pca = sk_decomp.PCA(n_components=self.options.ncomps)
        pca_transform = pca.fit_transform(standardized_data)
        # Build a new dataframe for the PCA transformed data, adding column headings for the new components
        new_column_headers = [self.options.pcaprefix + str(n) for n in range(1, self.options.ncomps + 1)]
        pca_components = pd.DataFrame(data = pca_transform, columns = new_column_headers)
        return df.join(pca_components)
