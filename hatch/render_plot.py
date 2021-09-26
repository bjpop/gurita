'''
Module      : Main
Description : Utilities for rendering plots 
Copyright   : (c) Bernie Pope, 25 September 2021 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX
'''

import sys
import matplotlib.pyplot as plt
from pathlib import Path
import hatch.utils as utils
import seaborn as sns

def facet_plot(options, graph, kind):
    if options.logx:
        graph.set(xscale="log")
    if options.logy:
        graph.set(yscale="log")
    if hasattr(options, 'title') and options.title is not None:
        plt.title(options.title)
    if hasattr(options, 'xlabel') and options.xlabel is not None:
        graph.set(xlabel=options.xlabel)
    if hasattr(options, 'ylabel') and options.ylabel is not None:
        graph.set(ylabel=options.ylabel)
    if hasattr(options, 'xlim') and options.xlim is not None:
        xlow, xhigh = options.xlim
        plt.xlim(xlow, xhigh)
    if hasattr(options, 'ylim') and options.ylim is not None:
        ylow, yhigh = options.ylim
        plt.ylim(ylow, yhigh)
    if hasattr(options, 'rotxticklabels') and options.rotxticklabels is not None:
        for ax in graph.axes.ravel():
            ax.set_xticklabels(ax.get_xticklabels(), rotation=options.rotxticklabels)
    if hasattr(options, 'noxticklabels') and options.noxticklabels:
        graph.set(xticks=[])
        graph.set(xticklabels=[])
    if hasattr(options, 'noyticklabels') and options.noyticklabels:
        graph.set(yticks=[])
        graph.set(yticklabels=[])
    if options.show:
        plt.show()
    else:
       output_filename = make_output_filename(options, kind)
       plt.savefig(output_filename, bbox_inches='tight', format=options.format)
       #if options.verbose:
       #    print(f"Plot written to {output_filename}")

    # write to stdout by default
    #else:
    #   plt.savefig(sys.stdout.buffer, bbox_inches='tight', format=options.format)
    plt.close() 

def make_output_filename(options, kind):
    if options.out is not None:
        # don't try to make this unique, just use what user specified, they may want to overwrite the old file
        return Path(options.out)
    else:
        extension = [options.format]
        output_name = [utils.get_output_name(options)]
        y_str = utils.output_field(options.yaxis)
        x_str = utils.output_field(options.xaxis)
        hue_str = utils.output_field(options.hue)
        row_str = utils.output_field(options.row)
        col_str = utils.output_field(options.col)
        path = Path('.'.join(output_name + x_str + y_str +
                             hue_str + row_str + col_str +
                             [kind] + extension))
        return utils.make_unique_numbered_filepath(path)
