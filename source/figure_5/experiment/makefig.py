"""
This script runs after the simulation.  It produces plots from the output.
"""
from visclaw.plotters import plotclaw

plotclaw.plotclaw(outdir='./_output',format='ascii')
