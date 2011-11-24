"""
This script runs after the simulation.  It produces plots from the output.
"""


import sys, os
import os.path
if len(sys.argv) > 1:
    build_dir=sys.argv[1]
else:
    build_dir=os.path.join(os.path.curdir,'_plots')

from visclaw.plotters import plotclaw

plotclaw.plotclaw(outdir='./experiment/_output',format='ascii', plotdir=build_dir)

