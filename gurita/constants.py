'''
Module      : Constants 
Description : Constant values for the Gurita program 
Copyright   : (c) Bernie Pope, 16 Oct 2019
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import pkg_resources
import matplotlib.pyplot as plt
import numpy as np
import pandas

PROGRAM_NAME = "gurita"

COMMAND_CATEGORIES = ["input/output", "plotting", "transformation", "summary information"]

# exit status values
EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2

# default constants
DEFAULT_ALPHA = 0.8
DEFAULT_LINEWIDTH = 0
DEFAULT_FILETYPE = 'csv'
DEFAULT_PCA_MISSING = 'drop'
DEFAULT_PCA_PREFIX = 'pc'
DEFAULT_ZSCORE_SUFFIX= 'zscore'
DEFAULT_CLUSTER_COLUMN_NAME = 'cluster'
DEFAULT_PCA_N_COMPONENTS = 2 
DEFAULT_KMEANS_N_CLUSTERS = 2
DEFAULT_GMM_N_CLUSTERS = 2
DEFAULT_GMM_MAX_ITER = 100
DEFAULT_PLOT_WIDTH = 20 
DEFAULT_PLOT_HEIGHT = 20 
DEFAULT_PAIR_PLOT_WIDTH = 5 
DEFAULT_PAIR_PLOT_HEIGHT = 5
DEFAULT_OUTPUT_NAME = "gurita"
DEFAULT_ORIENTATION = "v"
DEFAULT_STYLE = "darkgrid"
DEFAULT_CONTEXT = "notebook"
DEFAULT_CORR_METHOD = "pearson"
DEFAULT_PLOT_FORMAT = plt.rcParams["savefig.format"] 
DEFAULT_DENDRO_RATIO = 0.1
DEFAULT_ISNORM_NANPOLICY = 'propagate'
DEFAULT_CLUSTERMAP_METHOD = 'average'
DEFAULT_CLUSTERMAP_METRIC = 'euclidean' 
DEFAULT_NA = ''
DEFAULT_MELT_VALNAME = "value"
DEFAULT_MELT_VARNAME = "variable"
DEFAULT_SORT_NAPOS = "last"
# use ascending order by default
DEFAULT_SORT_ORDER = "a"
DEFAULT_TAIL_NUM = 5
DEFAULT_HEAD_NUM = 5
DEFAULT_PRETTY_MAX_ROWS = 10
DEFAULT_PRETTY_MAX_COLS = 10
DEFAULT_HISTOGRAM_BINS = 10 
DEFAULT_PAIR_PLOT_KIND = 'scatter'
DEFAULT_DROPNA_AXIS = 'rows'
DEFAULT_DROPNA_HOW = 'any'
DEFAULT_OUTLIER_COLUMN = 'outlier'
DEFAULT_OUTLIER_IQR_SCALE = 1.5
DEFAULT_HEATMAP_STRING_FORMAT = "d"
DEFAULT_HISTOGRAM_ELEMENT = 'bars'
DEFAULT_HISTOGRAM_STAT = 'count'
DEFAULT_GROUPBY_FUN = 'count'
DEFAULT_SEP = ','
DEFAULT_ESTIMATOR = 'mean'
DEFAULT_CI = 95
DEFAULT_SORT_ALGORITHM = 'quicksort'
DEFAULT_NORMTEST_ALPHA = 0.05
DEFAULT_NORMTEST_METHOD = 'dagostino'

#ALLOWED_FILETYPES = ['csv', 'tsv', 'CSV', 'TSV']
ALLOWED_PLOT_FORMATS = ['png', 'jpg', 'pdf', 'svg']
ALLOWED_STYLES = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
ALLOWED_CONTEXTS = ['paper', 'notebook', 'talk', 'poster'] 
ALLOWED_ORIENTATIONS = ['v', 'h']
ALLOWED_CLUSTERMAP_METHODS = ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward'] 
ALLOWED_CLUSTERMAP_METRICS = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean', 'hamming', 'jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'] 
ALLOWED_CORR_METHODS = ['pearson', 'kendall', 'spearman']
ALLOWED_HIST_MULTIPLES = ['layer', 'dodge', 'stack', 'fill']
ALLOWED_ISNORM_NAN_POLICIES = ['propagate', 'raise', 'omit']
ALLOWED_PCA_MISSING = ['drop', 'imputemean', 'imputemedian', 'imputemostfrequent']
ALLOWED_SORT_NAPOS = ['first', 'last']
# a = ascend, d = descend
ALLOWED_SORT_ORDER = ['a', 'd']
ALLOWED_PAIRPLOT_KINDS = ['scatter', 'kde', 'hist', 'reg']
ALLOWED_DROPNA_AXIS = ['rows', 'columns']
ALLOWED_DROPNA_HOW = ['any', 'all']
ALLOWED_HISTOGRAM_ELEMENTS = ['bars', 'step', 'poly']
ALLOWED_HISTOGRAM_STATS = ['count', 'frequency', 'probability', 'proportion', 'percent', 'density']
ALLOWED_GROUPBY_FUN = ['sample', 'size', 'sum', 'mean', 'mad', 'median', 'min', 'max', 'prod', 'std', 'var', 'sem', 'skew', 'quantile']
ALLOWED_PIVOT_FUN = ['sample', 'size', 'sum', 'mean', 'mad', 'median', 'min', 'max', 'prod', 'std', 'var', 'sem', 'skew', 'quantile'] 
ESTIMATOR_FUNS = {'mean': np.mean, 'median': np.median, 'max': np.max, 'min': np.min,
  'sum': np.sum, 'std': np.std, 'var': np.var }
ALLOWED_ESTIMATORS = list(ESTIMATOR_FUNS.keys())
ALLOWED_SORT_ALGORITHMS = ['quicksort', 'mergesort', 'heapsort', 'stable']
ALLOWED_NORMTEST_METHODS = ['dagostino', 'shapiro']


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"
