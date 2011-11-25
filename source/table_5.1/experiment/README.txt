ABOUT THIS EXPERIMENT
================
 
Table 5.1 shows timing results (in seconds) for on-core serial experiments solving acoustics and shallow water problems
implemented in both Clawpack and PyClaw on an Intel Xeon and an IBM BlueGene/P.

The following are manual instructions for reproducing the experiment on the BlueGene/P.  Reproducing this experiment is
not automated because it relies on a development version of PyClaw that must be specifically activated.

Common Environment Software (IBM BlueGene/P) 
==========================================
- IBM XL Fortran 11.1 
- IBM BlueGene/P System Driver V1R4M2_200_2010-100508P

PyClaw Software (Acoustics and Shallow Water):
==========================================
- Python 2.6
- PETSc 3.1.8
- petsc4py 1.2
- numpy 1.6.1 (patched on Shaheen to use IBM XL compilers)
- http://github.com/clawpack/pyclaw/commit/ce6fe0164191496b3126d062e3e4997541e32814 
   (use "git reset --hard ce6fe0164191496b3126d062e3e4997541e32814" in a PyClaw repository to switch to this version of
   the code)
- Riemann repository 
- prod.sh script (included in this repository)

Shallow Water Clawpack Software: 
============================================
- Clawpack library: 4.3
- prod_clawpack.sh script (included in this repository)

Acoustics Clawpack Software:
=======================================
- Clawpack library: 4.6.1
- prod_clawpack.sh script (included in this repository)

Profiling:
==========
Timing statements are instrumented in the application script file of PyClaw examples and in the driver.f file of the clawpack examples. Timing results are produced as an output. 

Environment for PyClaw Applications:
====================================
| $ export CLAW=<path_to>/clawpack
| $ export RIEMANN=$CLAW/riemann
| $ export PYCLAW=$CLAW/pyclaw
| $ source <path_to>/prod.sh # a copy of prod.sh is in this directory.

Environment for Clawpack Applications:
========================================

Building and Running PyClaw Applications:
=========================================
| # -O3 flag was used for compilation by adding -O3 to the FFLAGS in $PYCLAW/Makefile.common
| # Check https://github.com/clawpack/pyclaw/wiki/Running-on-shaheen/2328cbd968ede04f28e07bcecf5827b13fbf99a3 for details 
| $ cd ./<experiment_directory>
| $ make_f2py
| $ kslrun -a <account_number> -n 1 -t <wall_time> -p 1 -m SMP -r  "/bgsys/drivers/ppcfloor/gnu-linux/bin/python <application_script_file> use_petsc=True"

Building and Running Clawpack Applications:
===========================================
-O3 flag used for the library and application compilation by adding -O3 to the FFLAGS in the application make file

For Shallow Water Application: ??
----------------------------------
| $ cd ./<experiment_directory>
| $ make_clawpack
| $ kslrun -a <account_number> -n 1 -t <wall_time> -p 1 -m SMP -r  "./xclaw"

For Acoustics Applications: ??
------------------------------
| $ cd ./<experiment_directory>
| $ python setrun.py 
| $ make_clawpack
| $ make_clawpack .data
| $ kslrun -a <account_number> -n 1 -t <wall_time> -p 1 -m SMP -r  "./xclaw"



