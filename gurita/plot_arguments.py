'''
Module      : plot_arguments
Description : Common command line arguments used by plotting commands 
Copyright   : (c) Bernie Pope, 25 September 2021
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import argparse
import gurita.constants as const

def make_plot_arguments(default_width=const.DEFAULT_PLOT_WIDTH, default_height=const.DEFAULT_PLOT_HEIGHT):

    plot_arguments = argparse.ArgumentParser(add_help=False)
    plot_arguments_group = plot_arguments.add_argument_group('Plotting', 'arguments that are provided across all gurita plotting sub-commands')
    
    plot_arguments_group.add_argument(
        '--format',  type=str,
        choices=const.ALLOWED_PLOT_FORMATS, default=const.DEFAULT_PLOT_FORMAT,
        help=f'Graphic file format to use for saved plots. Allowed values: %(choices)s. Default: %(default)s.')
    plot_arguments_group.add_argument(
        '--show', action='store_true',
        default=False,
        help=f'Show an interactive plot window instead of saving to a file.')
    plot_arguments_group.add_argument(
        '--nolegend', action='store_true',
        default=False,
        help=f'Turn off the legend in the plot.')
    plot_arguments_group.add_argument(
        '--plotstyle', choices=const.ALLOWED_STYLES, required=False, default=const.DEFAULT_STYLE,
        help=f'Aesthetic style of plot. Allowed values: %(choices)s. Default: %(default)s.')
    plot_arguments_group.add_argument(
        '--context', choices=const.ALLOWED_CONTEXTS, required=False, default=const.DEFAULT_CONTEXT,
        help=f'Aesthetic context of plot. Allowed values: %(choices)s. Default: %(default)s.')
    plot_arguments_group.add_argument(
        '--title', metavar='STR', required=False, type=str,
        help='Plot title. By default no title will be added.')
    plot_arguments_group.add_argument(
        '--width', metavar='SIZE', required=False, type=float,
        default=default_width,
        help=f'Plot width in cm. Default: %(default)s.')
    plot_arguments_group.add_argument(
        '--height', metavar='SIZE', required=False, type=float,
        default=default_height,
        help=f'Plot height in cm. Default: %(default)s.')
    plot_arguments_group.add_argument(
        '--xlabel', metavar='STR', required=False, type=str,
        help=f'Label for horizontal (X) axis.')
    plot_arguments_group.add_argument(
        '--ylabel', metavar='STR', required=False, type=str,
        help=f'Label for vertical (Y) axis.')
    plot_arguments_group.add_argument(
        '--nxtl', '--noxticklabels', action='store_true',
        help=f'Turn of horizontal (X) axis tick labels.')
    plot_arguments_group.add_argument(
        '--nytl', '--noyticklabels', action='store_true',
        help=f'Turn of veritcal (Y) axis tick labels.')
    plot_arguments_group.add_argument(
        '--rxtl', '--rotxticklabels', metavar='ANGLE', required=False, type=float,
        help=f'Rotate X axis tick labels by ANGLE.')
    plot_arguments_group.add_argument(
        '--rytl', '--rotyticklabels', metavar='ANGLE', required=False, type=float,
        help=f'Rotate Y axis tick labels by ANGLE.')
    return plot_arguments

def target(self, required):
    target = self.required
    if not required:
        target = self.optional
    return target

def x_argument(self, required=False):
    target(self, required).add_argument('-x', '--xaxis', metavar='COLUMN',
           required=required, type=str,
           help=f'Feature to plot along the X axis.')

#x_argument = argparse.ArgumentParser(add_help=False)
#x_argument.add_argument(
#    '-x', '--xaxis', metavar='COLUMN', required=False, type=str,
#    help=f'Feature to plot along the X axis.')

def y_argument(self, required=False):
    target(self, required).add_argument('-y', '--yaxis', metavar='COLUMN',
        required=required, type=str,
        help=f'Feature to plot along the Y axis.')

#y_argument = argparse.ArgumentParser(add_help=False)
#y_argument.add_argument(
#    '-y', '--yaxis', metavar='COLUMN', required=False, type=str,
#    help=f'Feature to plot along the Y axis.')

def hue(self, required=False):
    target(self, required).add_argument(
        '--hue',  metavar='COLUMN', type=str, required=required, 
        help=f'Name of feature to use for colouring/grouping the plotted data.')

#hue = argparse.ArgumentParser(add_help=False)
#hue.add_argument(
#    '--hue',  metavar='COLUMN', type=str, required=False, 
#    help=f'Name of feature to use for colouring/grouping the plotted data.')

def row(self, required=False):
    target(self, required).add_argument(
        '-r', '--row', metavar='COLUMN', type=str, required=required, 
        help=f'Name of feature to use for facet rows.')

#row = argparse.ArgumentParser(add_help=False)
#row.add_argument(
#    '-r', '--row', metavar='COLUMN', type=str, required=False, 
#    help=f'Name of feature to use for facet rows.')

def col(self, required=False):
    target(self, required).add_argument(
        '-c', '--col', metavar='COLUMN', type=str, required=required,
        help=f'Name of feature to use for facet columns.')

# col = argparse.ArgumentParser(add_help=False)
# col.add_argument(
#     '-c', '--col', metavar='COLUMN', type=str, required=False, 
#     help=f'Name of feature to use for facet columns.')

def order(self, required=False):
    target(self, required).add_argument(
        '--order', metavar='VALUE', nargs="+", required=required, type=str,
        help=f'Order to display categorical values.')

#order = argparse.ArgumentParser(add_help=False)
#order.add_argument(
#    '--order', metavar='VALUE', nargs="+", required=False, type=str,
#    help=f'Order to display categorical values.')

def hue_order(self, required=False):
    target(self, required).add_argument(
        '--hueorder', metavar='VALUE', nargs="+", required=required, type=str,
        help=f'Order to display categorical values selected for hue.')

#hue_order = argparse.ArgumentParser(add_help=False)
#hue_order.add_argument(
#    '--hueorder', metavar='VALUE', nargs="+", required=False, type=str,
#    help=f'Order to display categorical values selected for hue.')

def orient(self, required=False):
    target(self, required).add_argument(
        '--orient', choices=const.ALLOWED_ORIENTATIONS, required=required, default=const.DEFAULT_ORIENTATION,
        help=f'Orientation of plot. Allowed values: %(choices)s. Default: %(default)s.')

#orient = argparse.ArgumentParser(add_help=False)
#orient.add_argument(
#    '--orient', choices=const.ALLOWED_ORIENTATIONS, required=False, default=const.DEFAULT_ORIENTATION,
#    help=f'Orientation of plot. Allowed values: %(choices)s. Default: %(default)s.')

def logx(self, required=False):
    target(self, required).add_argument(
    '--logx', action='store_true', required=required,
    help=f'Use a log scale on the horizontal (X) axis.')

#logx = argparse.ArgumentParser(add_help=False)
#logx.add_argument(
#    '--logx', action='store_true',
#    help=f'Use a log scale on the horizontal (X) axis.')

def logy(self, required=False):
    target(self, required).add_argument(
        '--logy', action='store_true',
        help=f'Use a log scale on the veritical (Y) axis.')

#logy = argparse.ArgumentParser(add_help=False)
#logy.add_argument(
#    '--logy', action='store_true',
#    help=f'Use a log scale on the veritical (Y) axis.')

def xlim(self, required=False):
    target(self, required).add_argument(
        '--xlim',  metavar='BOUND', nargs=2, required=required, type=float,
        help=f'Limit horizontal axis range to [LOW,HIGH].')

#xlim = argparse.ArgumentParser(add_help=False)
#xlim.add_argument(
#    '--xlim',  metavar='BOUND', nargs=2, required=False, type=float,
#    help=f'Limit horizontal axis range to [LOW,HIGH].')

def ylim(self, required=False):
    target(self, required).add_argument(
        '--ylim',  metavar='BOUND', nargs=2, required=required, type=float,
        help=f'Limit vertical axis range to [LOW,HIGH].')

#ylim = argparse.ArgumentParser(add_help=False)
#ylim.add_argument(
#    '--ylim',  metavar='BOUND', nargs=2, required=False, type=float,
#    help=f'Limit vertical axis range to [LOW,HIGH].')

def dotsize(self, required=False):
    target(self, required).add_argument(
        '--dotsize',  metavar='COLUMN', type=str, required=required, 
        help=f'Name of feature to use for plotted point size.')

#dotsize = argparse.ArgumentParser(add_help=False)
#dotsize.add_argument(
#    '--dotsize',  metavar='COLUMN', type=str, required=False, 
#    help=f'Name of feature to use for plotted point size.')

def dotsizerange(self, required=False):
    target(self, required).add_argument(
        '--dotsizerange',  metavar='BOUND', nargs=2, type=float, required=required, 
        help=f'Size range for plotted point size based on numerical feature [LOW,HIGH].')

#dotsizerange = argparse.ArgumentParser(add_help=False)
#dotsizerange.add_argument(
#    '--dotsizerange',  metavar='BOUND', nargs=2, type=float, required=False, 
#    help=f'Size range for plotted point size based on numerical feature [LOW,HIGH].')

def dotalpha(self, required=False):
    target(self, required).add_argument(
        '--dotalpha',  metavar='ALPHA', type=float, default=const.DEFAULT_ALPHA,
        required=required, help=f'Alpha value for plotted points. Default: %(default)s.')

#dotalpha = argparse.ArgumentParser(add_help=False)
#dotalpha.add_argument(
#    '--dotalpha',  metavar='ALPHA', type=float, default=const.DEFAULT_ALPHA,
#    help=f'Alpha value for plotted points. Default: %(default)s.')

def dotlinewidth(self, required=False):
    target(self, required).add_argument(
        '--dotlinewidth',  metavar='WIDTH', type=float, required=required,
        help=f'Border line width value for plotted points.')

#dotlinewidth = argparse.ArgumentParser(add_help=False)
#dotlinewidth.add_argument(
#    '--dotlinewidth',  metavar='WIDTH', type=float, 
#    help=f'Border line width value for plotted points.')

def dotlinecolour(self, required=False):
    target(self, required).add_argument(
        '--dotlinecolour',  metavar='COLOUR', type=str, required=required,
        help=f'Border line colour plotted points.')

#dotlinecolour = argparse.ArgumentParser(add_help=False)
#dotlinecolour.add_argument(
#    '--dotlinecolour',  metavar='COLOUR', type=str, 
#    help=f'Border line colour plotted points.')

def dotstyle(self, required=False):
    target(self, required).add_argument(
        '--dotstyle', metavar='COLUMN', type=str, required=required,
        help=f'Name of categorical feature to use for plotted dot marker style.')

#dotstyle = argparse.ArgumentParser(add_help=False)
#dotstyle.add_argument(
#    '--dotstyle', metavar='COLUMN', type=str, required=False, 
#    help=f'Name of categorical feature to use for plotted dot marker style.')

def colwrap(self, required=False):
    target(self, required).add_argument(
        '--colwrap',  metavar='INT', type=int, required=required,
        help=f'Wrap the facet column at this width, to span multiple rows.')

#colwrap = argparse.ArgumentParser(add_help=False)
#colwrap.add_argument(
#    '--colwrap',  metavar='INT', type=int, required=False, 
#    help=f'Wrap the facet column at this width, to span multiple rows.')

def dodge(self, required=False):
    target(self, required).add_argument(
        '--dodge', action='store_true', required=required,
        help=f'Separate hue levels along the categorical axis (when --hue is used).')

#dodge = argparse.ArgumentParser(add_help=False)
#dodge.add_argument(
#    '--dodge', action='store_true', required=False,
#    help=f'Separate hue levels along the categorical axis (when --hue is used).')

def vlines(self, required=False):
    target(self, required).add_argument('--vlines', metavar='AXIS_LOCATION',
        type=float, nargs="+", required=required,
        help=f'Draw vertical lines on the plot at specified axes locations.')

#vlines = argparse.ArgumentParser(add_help=False)
#vlines.add_argument('--vlines', metavar='AXIS_LOCATION', type=float, nargs="+", required=False, help=f'Draw vertical lines on the plot at specified axes locations.')

def hlines(self, required=False):
    target(self, required).add_argument('--hlines', metavar='AXIS_LOCATION',
        type=float, nargs="+", required=False,
        help=f'Draw horizontal lines on the plot at specified axes locations.')


#hlines = argparse.ArgumentParser(add_help=False)
#hlines.add_argument('--hlines', metavar='AXIS_LOCATION', type=float, nargs="+", required=False, help=f'Draw horizontal lines on the plot at specified axes locations.')


def strip(self, required=False):
    target(self, required).add_argument('--strip', action='store_true', required=required,
        default=False, help=f'Overlay data points using a strip plot.')

#strip = argparse.ArgumentParser(add_help=False)
#strip.add_argument('--strip', action='store_true', default=False, help=f'Overlay data points using a strip plot.')

def nooutliers(self, required=False):
    target(self, required).add_argument('--nooutliers', action='store_true',
        required=required, default=False, help=f'Do not display outlier data.')

#nooutliers = argparse.ArgumentParser(add_help=False)
#nooutliers.add_argument('--nooutliers', action='store_true', default=False, help=f'Do not display outlier data.')

def estimator(self, required=False):
    target(self, required).add_argument('--estimator', metavar='FUN',
        default=const.DEFAULT_ESTIMATOR, required=required, choices=const.ALLOWED_ESTIMATORS,
        help=f'Function to compute point estimate of numerical feature. Choices: %(choices)s. Default: %(default)s.')

#estimator = argparse.ArgumentParser(add_help=False)
#estimator.add_argument('--estimator', metavar='FUN', default=const.DEFAULT_ESTIMATOR, required=False, choices=const.ALLOWED_ESTIMATORS, help=f'Function to compute point estimate of numerical feature. Choices: %(choices)s. Default: %(default)s.')
