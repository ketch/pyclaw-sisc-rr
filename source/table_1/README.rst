Table 1 shows timing results (in seconds) for on-core serial experiments solving acoustics and shallow water problems implemented in both Clawpack and PyClaw on an Intel Xeon and a PowerPC 450 machine.

The following is the experiment reproducibility instructions for the PowerPC 450 machine (on Shaheen supercomputer). The experiment can be similarly reproduced on Intel Xeon machine.


Shallow Water PyClaw Experiment Software:
==========================================
- Python 2.6
- numpy 2.0.0dev8672
- PETSc 3.1.8
- petsc4py 1.1.2 ??(dev-june2011)
- XLF 11.1 for compiling
- Pyclaw github repository: ce6fe0164191496b3126d062e3e4997541e32814 branch: fortran_src
- Riemann github repository: 184798b81bcc38e7ab4dba7ddfff0481734ba0f9  branch: master

Application:
------------
./experiment/shallow_pyclaw



Shallow Water Clawpack Experiment Software: 
============================================
- XLF 11.1 for compiling
- Clawpack library: 4.3

Application:
------------
./experiment/shallow_clawpack 



Acoustics PyClaw Experiment Software:
======================================
- Python 2.6
- numpy 2.0.0dev8672
- PETSc 3.1.8
- petsc4py 1.1.2 ??(dev-june2011)
- XLF 11.1 for compiling
- Pyclaw github repository: 58f691599a4bdfba5783172bf161ebc1d337500b branch: fortran_src
- Riemann github repository: 184798b81bcc38e7ab4dba7ddfff0481734ba0f9 branch: master

Application:
------------
./experiment/acoustics_pyclaw



Acoustics Clawpack Experiment Software:
=======================================
- XLF 11.1 for compiling
- clawpack library: 4.6.1

Application:
------------
./experiment/acoustics_clawpack



Profiling:
==========
Timing statements are instrumented in the application script file of PyClaw examples and in the driver.f file of the clawpack examples. Timing results are produced as an output. 



Environment for PyClaw Applications:
====================================
| $ export CLAW=<path_to>/clawpack
| $ export RIEMANN=$CLAW/riemann
| $ export PYCLAW=$CLAW/pyclaw
| $ source <path_to>/prod.sh # a copy of prod.sh is in this directory.



Environment for Clawpack Applications:??
========================================



Building and Running PyClaw Applications:
=========================================
| -O3 flag was used for compilation by adding -O3 to the FFLAGS in $PYCLAW/Makefile.common
| Check https://github.com/clawpack/pyclaw/wiki/Running-on-shaheen/2328cbd968ede04f28e07bcecf5827b13fbf99a3 for details 
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



