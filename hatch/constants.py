'''
Module      : Constants 
Description : Constant values for the Hatch program 
Copyright   : (c) Bernie Pope, 16 Oct 2019
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import pkg_resources
import matplotlib.pyplot as plt

PROGRAM_NAME = "hatch"

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
DEFAULT_ZSCORE_SUFFIX= '_zscore'
DEFAULT_CLUSTER_PREFIX = 'cluster'
DEFAULT_PCA_N_COMPONENTS = 2 
DEFAULT_KMEANS_N_CLUSTERS = 2
DEFAULT_GMM_N_CLUSTERS = 2
DEFAULT_GMM_MAX_ITER = 1000
DEFAULT_PLOT_WIDTH = 20 
DEFAULT_PLOT_HEIGHT = 20 
DEFAULT_PAIR_PLOT_WIDTH = 5 
DEFAULT_PAIR_PLOT_HEIGHT = 5
DEFAULT_OUTPUT_NAME = "hatch"
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
DEFAULT_HEATMAP_STRING_FORMAT = ".2g"

ALLOWED_FILETYPES = ['csv', 'tsv']
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


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"
