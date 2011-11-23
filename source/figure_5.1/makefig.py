#!/usr/bin/env python
# This code is originally taken from
# http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/table_demo.py
# It is modified here to generate the required plot.
import matplotlib

from pylab import *
from matplotlib.colors import colorConverter

params = {'backend': 'ps',
          'axes.labelsize': 10,
          'text.fontsize': 10,
          'legend.fontsize': 10,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,}
rcParams.update(params)


#Some simple functions to generate colours.
def pastel(colour, weight=2.4):
    """ Convert colour into a nice pastel shade"""
    rgb = asarray(colorConverter.to_rgb(colour))
    # scale colour
    maxc = max(rgb)
    if maxc < 1.0 and maxc > 0:
        # scale colour
        scale = 1.0 / maxc
        rgb = rgb * scale
    # now decrease saturation
    total = sum(rgb)
    slack = 0
    for x in rgb:
        slack += 1.0 - x

    # want to increase weight from total to weight
    # pick x s.t.  slack * x == weight - total
    # x = (weight - total) / slack
    x = (weight - total) / slack

    rgb = [c + (x * (1.0-c)) for c in rgb]

    return rgb

def get_colours(n):
    """ Return n pastel colours. """
    base = asarray([[1,0,0], [0,1,0], [0,0,1]])

    if n <= 3:
        return base[0:n]

    # how many new colours to we need to insert between
    # red and green and between green and blue?
    needed = (((n - 3) + 1) / 2, (n - 3) / 2)
    
    colours = []
    for start in (0, 1):
        for x in linspace(0, 1-(1.0/(needed[start]+1)), needed[start]+1):
            colours.append((base[start] * (1.0 - x)) +
                           (base[start+1] * x))
    colours.append([0,0,1])

    return [pastel(c) for c in colours[0:n]]



axes([0.35, 0.25, 0.55, 0.35])   # leave room below the axes for the table



import pstats

cflReduce = []
parallelInit = []
globalToLocal = []
localToGlobal = []
evolveToTime = []
serialComputations = []


for i in [1,16,256,4096,65536]:
    p = pstats.Stats('profile/profile0_'+str(i))
    prof = {}
    for x in p.stats:
        prof[x[2]] = p.stats[x]
    cflReduce.append(round(prof["<method 'max' of 'petsc4py.PETSc.Vec' objects>"][3],3))
    parallelInit.append(round(prof["init_q_da"][3],3) + round(prof["init_aux_da"][3],3))
    globalToLocal.append(round(prof["<method 'globalToLocal' of 'petsc4py.PETSc.DM' objects>"][3],3))
    localToGlobal.append(round(prof["<method 'localToGlobal' of 'petsc4py.PETSc.DM' objects>"][3],3))
    evolveToTime.append(round(prof["evolve_to_time"][3],3))

serialComputations =[ evolveToTime[i]- cflReduce[i]- globalToLocal[i]- localToGlobal[i] for i in range(len(evolveToTime))]


#data = [[  0.001, 0.6, 4.1, 4, 3.9, 3.8, 3.8, 4, 4.2],
#        [  2, 1.5, 1.5, 1.5, 1.5, 1.6, 1.9, 2.9, 6.6],
#        [  5.9, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6],
#        [  4.9, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#        [  88.199, 94.8, 92.7, 92.5, 92.6, 92.7, 92.7, 92.6, 92.8]]
data = [ cflReduce ,parallelInit , globalToLocal , localToGlobal , serialComputations ]


colLabels = ['1','16', '256', '4096', '65536']

rowLabels = ['CFL Reduce', 'Parallel Initialization', 'Global to Local', 'Local to Global', 'Serial Computations']
# Get some pastel shades for the colours
colours = get_colours(len(rowLabels))
rows = len(data)

ind = arange(len(colLabels)) + 0.3  # the x locations for the groups
cellText = []
width = 0.4     # the width of the bars
yoff = array([0.0] * len(colLabels)) # the bottom values for stacked bar chart
for row in xrange(rows):
    bar(ind, data[rows-row-1], width, bottom=yoff, color=colours[rows-row-1], linewidth=0)
    yoff = yoff + data[rows-row-1]

cellText = data
# Add total efficiency to the data
data.append( [sum([row[i] for row in data]) for i in range(len(colLabels))])
data[-1] = data[-1][0]/data[-1]
data[-1] = [round(x,2) for x in data [-1]]
rowLabels.append('Total Efficiency')
colours.append([1,1,1])

# Add a table at the bottom of the axes
table(cellText=cellText,
      rowLabels=rowLabels, rowColours=colours,
      colLabels=colLabels,
      loc='bottom')
ylabel("Execution Time Per Core (s)")
figtext(.5, .02, "Number of Cores")
vals = arange(0, 121, 20)
yticks(vals, ['%d' % val for val in vals])
xticks([])

#show()

import sys, os
import os.path
if len(sys.argv) > 1:
    build_dir=sys.argv[1]
else:
    build_dir=os.path.curdir

f=gcf()
f.set_figheight(8) 
f.set_figwidth(5.5) 

savefig(os.path.join(build_dir,'euler_weak_scaling.eps'))
