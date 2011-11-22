#!/usr/bin/env python
# This code is originally taken from
# http://matplotlib.sourceforge.net/mpl_examples/pylab_examples/table_demo.py
# It is modified here to generate the required plot.
import matplotlib

from pylab import *
from matplotlib.colors import colorConverter


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



axes([0.3, 0.25, 0.65, 0.65])   # leave room below the axes for the table

data = [[  0.001, 0.6, 4.1, 4, 3.9, 3.8, 3.8, 4, 4.2],
        [  2, 1.5, 1.5, 1.5, 1.5, 1.6, 1.9, 2.9, 6.6],
        [  5.9, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6, 3.6],
        [  4.9, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
        [  88.199, 94.8, 92.7, 92.5, 92.6, 92.7, 92.7, 92.6, 92.8]]


colLabels = ['1','4', '16', '64', '256', '1024', '4096', '16384', '65536']
rowLabels = ['CFL Reduce', 'Parallel Initialization', 'Global to Local', 'Local to Global', 'Serial Computations']
# Get some pastel shades for the colours
colours = get_colours(len(rowLabels))
rows = len(data)

ind = arange(len(colLabels)) + 0.3  # the x locations for the groups
cellText = []
width = 0.4     # the width of the bars
yoff = array([0.0] * len(colLabels)) # the bottom values for stacked bar chart
for row in xrange(rows):
    bar(ind, data[rows-row-1], width, bottom=yoff, color=colours[rows-row-1])
    yoff = yoff + data[rows-row-1]

cellText = data
# Add total efficiency to the data
data.append( [sum([row[i] for row in data]) for i in range(9)])
data[-1] = data[-1][0]/data[-1]
data[-1] = [round(x,2) for x in data [-1]]
rowLabels.append('Total Efficiency')
colours.append([1,1,1])

# Add a table at the bottom of the axes
table(cellText=cellText,
                  rowLabels=rowLabels, rowColours=colours,
                  colLabels=colLabels,
                  loc='bottom')
ylabel("Execution Time Per Core in Seconds")
figtext(.5, .02, "Number of Cores")
vals = arange(0, 121, 20)
yticks(vals, ['%d' % val for val in vals])
xticks([])
import os
try:
    os.makedirs('build')
except OSError:
    print "directory already exists, ignoring"  

savefig("./build/euler_weak_scaling.pdf")

#show()


