ABOUT THIS EXPERIMENT
================
Figure 7.1 shows the water height of the zonal wave number 4 Rossby-Haurwitz problem at different times over a 400x200
grid, illustrating the ability of PyClaw to handle problems on non-trivial geometries.

Computing this experiment required slightly more than 3.5 hours on a single core of a Xeon X5550 workstation.

REPRODUCING THE FIGURE
=================

The figure in the manuscript relies on 3-D plotting capability currently unavailable in pyclaw.  We used MATLAB based
plotting routines from the Clawpack distribution (available in the matlab/ directory) in the following manner to produce the figure in the paper:

cd _output/
mv fort.q0038 fort.q0001
mv fort.q0045 fort.q0002
mv fort.q0048 fort.q0003

# run plotclaw2d in MATLAB, rotate figure and adjust color.

RESPONSIBLE AUTHORS
==============
Matteo Parsani
David Ketcheson
Aron Ahmadia
