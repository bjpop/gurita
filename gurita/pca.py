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
import gurita.constants as const
from gurita.command_base import CommandBase
import gurita.utils as utils

class PCA(CommandBase, name="pca"):
    description = "Principal component analysis (PCA)."
    category = "transformation"

    def __init__(self):
        super().__init__()
        self.optional.add_argument(
            '-c', '--columns', metavar='NAME', nargs="+", type=str, required=False,
            help=f'Select only these named columns')
        self.optional.add_argument(
            '--prefix', required=False, default=const.DEFAULT_PCA_PREFIX,
            help=f'Column label prefix for principal component axes. Default: %(default)s.')
        self.optional.add_argument(
            '-n', '--ncomps', metavar='COMPONENTS', type=int, required=False, default=const.DEFAULT_PCA_N_COMPONENTS,
            help=f'Number of principal components to generate. Default: %(default)s.')

    
    def run(self, df):
        options = self.options
        selected_df = df

        if options.columns is not None:
            utils.validate_columns_error(df, options.columns)
            selected_df = df[options.columns]

        # select only numeric columns for the PCA
        selected_df = selected_df.select_dtypes(include=np.number)

        # drop rows with missing values in any column 
        selected_df = selected_df.dropna()

        # Standardize columns by removing the mean and scaling to unit variance 
        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(selected_df)

        # Perform PCA on the standardized data
        pca = sk_decomp.PCA(n_components=self.options.ncomps)
        pca_transform = pca.fit_transform(standardized_data)

        # Build a new dataframe for the PCA transformed data, adding column headings for the new components
        new_column_headers = [self.options.prefix + str(n) for n in range(1, self.options.ncomps + 1)]
        pca_components = pd.DataFrame(data=pca_transform, columns=new_column_headers, index=selected_df.index)

        return df.join(pca_components)
