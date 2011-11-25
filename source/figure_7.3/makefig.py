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

plotclaw.plotclaw(outdir='./experiment/reference',format='petsc', plotdir='./reference')
plotclaw.plotclaw(outdir='./experiment/weno05',format='petsc', plotdir='./weno05'
plotclaw.plotclaw(outdir='./experiment/weno07',format='petsc', plotdir='./weno07')
plotclaw.plotclaw(outdir='./experiment/weno09',format='petsc', plotdir='./weno09')

