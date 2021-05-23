'''
Module      : Stats 
Description : Statistical calculations for Hatch 
Copyright   : (c) Bernie Pope, 16 Oct 2019-2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import logging
import pandas as pd
import numpy as np
from itertools import combinations
import math
import scipy
import hatch.utils as utils


def norm_test(df, options):
    if options.features is not None:
        features = options.features
        utils.check_df_has_features(df, features)
    else:
        numeric_df = df.select_dtypes(include=np.number)
        features = list(numeric_df.columns)
    print("feature,statistic,p-value")
    for f in features:
        k2, p_value = scipy.stats.normaltest(df[f]) 
        print(f"{f},{k2},{p_value}")


def correlation(df, options):
    print("feature1,feature2,coefficient,p-value")
    if options.method == 'pearson':
        corr_fun = scipy.stats.pearsonr
    elif options.method == 'spearman':
        corr_fun = scipy.stats.spearmanr
    elif options.method == 'kendall':
        corr_fun = scipy.stats.kendalltau
    if options.features is not None:
        features = options.features
        utils.check_df_has_features(df, features)
    else:
        numeric_df = df.select_dtypes(include=np.number)
        features = list(numeric_df.columns)
    for f1, f2 in combinations(features, 2): 
       coeff, p_value = corr_fun(df[f1], df[f2])
       print(f"{f1},{f2},{coeff},{p_value}")


def display_info(df, options):
    rows, cols = df.shape 
    pd.set_option('display.max_columns', None)
    # optionally select only certain columns to display
    if options.features is not None:
        df = df[options.features]
    print(df.describe(include='all'))
    print(f"rows: {rows}, cols: {cols}")
