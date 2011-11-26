ABOUT THIS REPOSITORY
================

This is the reproducibility repository for "Accessible, Extensible, Scalable Tools for Wave Propagation Problems", a manuscript submitted in 2011 by Ketcheson et al. to the SIAM Journal for Scientific Computing (SISC).  This repository serves two purposes:

- Establish and maintain provenance for all data, charts, and tables presented in the manuscript.  

In particular, the raw data for all visualizations in the paper and their source is archived here along with, where possible, the scripts used to generate their manuscript-ready forms.  Quite a bit of latitude is given to authors in choosing how to archive experimental data, but preference is given to minimizing the size of the repository while providing complete data sets and provenance for all data visualizations in the manuscript.  Consequently, compact post-processed data sets are the preferred archival format for this repository.  For example, if a simulation contains many time steps before arriving at a final solution, and computational gauges are only monitoring a small slice of the simulated domain, it is only expected that the raw data actually used directly used in generating the figures themselves is archived.

- Assist and automate reproducibility.  

The hardware/software environment along with the software used to produce every experimental result reported in the manuscript is described in this repository.  On systems with the prerequisite software installed, the Makefile in the root directory documents and automates reproduction of the experiments described in the paper.  

Automation of this repository relies on an, at minimum, an implementation of the make utility on a POSIX-compatible system.  Additionally, you will need the prerequisites for a functioning PyClaw installation to reproduce many of the experiments as well as several post-processing tools (some of which, are unfortunately not freely available) to generate the manuscript-ready charts and figures.

Finally, the REPRODUCED file maintains a list of readers who were able to reproduce the experiments in this repository, with notes on any found discrepancies.

HOW TO USE THIS REPOSITORY TO EXAMINE RAW DATA AND ITS PROVENANCE
==================================================

The source/ directory organizes data and information for each of the tables and graphs in the manuscript.  Each subdirectory within source/ contains a README.txt file describing the provenance of the data used in the figure or chart.

HOW TO USE THIS REPOSITORY TO GENERATE A FIGURE OR CHART FROM SOURCE
=====================================================

When possible, every figure/table in the paper that reports experimental data is generated from its raw source into a build/ subdirectory by a make command from the reproducibility repository.  When the figure or table cannot be automatically constructed from the data because, for example, it is generated from a non-scriptable tool or the process is too complicated, the postprocessed data is instead stored in an appropriate format in the corresponding build/ subdirectory. 

By default, "make $experiment_name" assembles recorded data into figures/graphs. For example: 

   make table_1 

will assemble/parse data from archived logs or raw data in source/ into build/.  

HOW TO USE THIS REPOSITORY TO REPRODUCE RAW EXPERIMENTAL DATA
===============================================

Appending /experiment to the make target will try to reproduce the experiment on the computer it is being run from.  For example, if you wished to attempt to re-run the experiment that generated the data in table_1, you would run:

   make table_1/experiment

You will need a functioning PyClaw 1.0 installation to run these experiments.  Instructions for installing PyClaw are available at http://numerics.kaust.edu.sa/pyclaw.  Additional dependencies for some of the experiments include PETSc (to enable the parallel petclaw features for scalability testing) and scipy (to enable numerical integration in the Shock-Bubble interaction experiment).

Sometimes it is not possible to automate reproduction of a computational experiment due to dependencies on a specific hardware or software configuration.  In this situation, complete, detailed instructions and any needed scripts for reproducing the archived data are simultaneously printed to the screen and copied to the build/ directory in lieu of an automated experimental run.  

CLOSING NOTES
===========

You may wish to attempt to reproduce every experimental result in this paper.  Those familiar with make will recognize the following idiom:

   make all

If you reproduce any of this data, please let me or another author of this paper know so we can add your results to the REPRODUCED file. 

Aron Ahmadia, King Abdullah University of Science & Technology
aron@ahmadia.net

