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

PLOT_COMMANDS = ['hist', 'count', 'box', 'violin', 'swarm',
        'strip', 'boxen', 'bar', 'point', 'line', 'scatter',
        'heatmap', 'clustermap', 'pca']

# exit status values
EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2

# default constants
DEFAULT_ALPHA = 0.5
DEFAULT_LINEWIDTH = 0
DEFAULT_FILETYPE = 'csv'
DEFAULT_PCA_MISSING = 'drop'
DEFAULT_PCA_PREFIX = 'pc'
DEFAULT_PCA_N_COMPONENTS = 2 
DEFAULT_PLOT_WIDTH = 8 
DEFAULT_PLOT_HEIGHT = 8 
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

try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"
