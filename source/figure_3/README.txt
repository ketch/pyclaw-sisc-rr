Figure 3 shows the profiling results of a weak scaling experiment for an Euler application. The experiment was run on 1, 4, 16, 64, 256, 1024, 4096, 16384 and 65536 cores.

Hardware:
Blue Gene/P Shaheen supercomputer which has 16 racks of Quad-Core PowerPC 450 nodes with 4GB of available RAM for each.

Software:
Python 2.6
numpy 2.0.0dev8672
PETSc 3.1.8
petsc4py 1.1.2 **(dev-june2011)
XLF 11.1 for compiling
Pyclaw github repository: ec035e4f06e93100590d branch: scaling_shaheen
Riemann github repository: 184798b81bcc38e7ab4d  branch: master


Application:
The Euler application to run is found under the ./experiment directory.

Environment Variables:
export CLAW=<path_to>/clawpack
export RIEMANN=$CLAW/riemann
export PYCLAW=$CLAW/pyclaw
source <path_to>//prod.sh # a copy of prod.sh is in this directory.


Building:
Check https://github.com/clawpack/pyclaw/wiki/Running-on-shaheen/2328cbd968ede04f28e07bcecf5827b13fbf99a3 for details 
$ cd ./experiment
$ make_f2py

Running:
Check https://github.com/clawpack/pyclaw/wiki/Running-on-shaheen/2328cbd968ede04f28e07bcecf5827b13fbf99a3 for details 
$ cd ./experiment
$ kslrun -a <account_number> -n <number_of_processes> -t <wall_time> -p <partition_size> -m VN -r  "/bgsys/drivers/ppcfloor/gnu-linux/bin/python shockbubble.py"

Profiling:
Each time you run the application, cProfile profiles will be generated for process 0 and (process 5 if applicable). 

Note about the timing results in the figure:
Local to Global: The execution time of method localToGlobal
Global to Local: The execution time of method globalToLocal
CFL Reduce: The execution time of method max of petsc4py.PETSc.Vec class
Parallel Initialization: The execution time of methods init_q_da and init_aux_da **
Serial Computations: The execution time for  evolve_to_time method excluding the execution time of localToGlobal, GlobalToLocal and petsc4py.PETSc.Vec max methods
Total Efficiency (for n processes): is the total execution time for one process over the total execution time for n processes.
