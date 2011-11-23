pyclaw_build() {
    export KSL_PROCESS_MODULES=/project/k47/prod/process/modules
    export MODULE_HOME=/project/k47/modules
    export MODULEPATH=$KSL_PROCESS_MODULES/shared/tools:$KSL_PROCESS_MODULES/ppc64/compilers:$KSL_PROCESS_MODULES/ppc64/targets:$MODULE_HOME/ppc64:$MODULE_HOME/ppc450d
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/share/ksl/tcl/8.5.8/ppc64/lib
    export PYTHONPATH=/project/k47/prod/numpy/dev-aug29/ppc450d/lib/python
    module load init genie ibm python numpy
    if [ -z $CLAW ]
    then 
        echo "CLAW Environment variable not set!  Please set before compiling." 1>&2
    fi
    if [ -z $PYCLAW ]
    then 
        echo "PYCLAW Environment variable not set!  Please set before compiling." 1>&2
    fi
    if [ -z $RIEMANN ]
    then 
        echo "RIEMANN Environment variable not set!  Please set before compiling." 1>&2
    fi
    alias make_f2py='make F2PY="f2py -L/opt/ibmcmp/xlsmp/bg/1.7/lib -L/opt/ibmcmp/xlmass/bg/4.4/bglib -L/opt/ibmcmp/xlf/bg/11.1/bglib -lxlf90_r -lxlopt -lxlsmp -lxl -lxlfmath" FC="/bgsys/drivers/ppcfloor/comm/bin/mpixlf77_r -qextname -I/project/k47/prod/python/2.6/ppc64/include -I/project/k47/prod/readline/6.1/ppc64/include -I/project/k47/prod/numpy/dev-aug29/ppc450d/lib/python/numpy/core/include -O3 -qpic=small"'
    echo "*****************************************************************"
    echo "make_f2py alias initialized"
    echo "please use" 
    echo 'make F2PY="f2py -L/opt/ibmcmp/xlsmp/bg/1.7/lib -L/opt/ibmcmp/xlmass/bg/4.4/bglib -L/opt/ibmcmp/xlf/bg/11.1/bglib -lxlf90_r -lxlopt -lxlsmp -lxl -lxlfmath" FC="/bgsys/drivers/ppcfloor/comm/bin/mpixlf77_r -qextname -I/project/k47/prod/python/2.6/ppc64/include -I/project/k47/prod/readline/6.1/ppc64/include -I/project/k47/prod/numpy/dev-aug29/ppc450d/lib/python/numpy/core/include -O3 -qpic=small"'
    echo "or" 
    echo 'make_f2py'
    echo "*****************************************************************"
    echo "the following commands are available:"
    echo "make_f2py    - calls make with the appropriate F2PY variable set"
    echo "*****************************************************************"
    echo "Example:"
    echo 'cd $PYCLAW/apps/advection/1d/constant'
    echo 'make_f2py'
    echo "*****************************************************************"
    echo "numpy/f2py/xlf/python2.6 build environment initialized"
    echo "*****************************************************************"
 }

pyclaw_run() {
    err=0
    if [ -z $CLAW ]
    then 
        echo "CLAW Environment variable not set!  Please set and then re-run this script." 1>&2
        err=1
    fi
    if [ -z $PYCLAW ]
    then 
        echo "PYCLAW Environment variable not set!  Please set and then re-run this script." 1>&2
        err=1
    fi
    if [ -z $RIEMANN ]
    then 
        echo "RIEMANN Environment variable not set!  Please set and then re-run this script." 1>&2
        err=1
    fi
    if [ err = 1 ]
    then
        return 1
    fi
    export PATH=$PATH:/opt/share/ksl/python3/3.2/ppc64/bin
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/share/ksl/readline/6.1/ppc64/lib:/opt/share/ksl/python3/3.2/ppc64/lib
    export KSL_PPC450D_PYTHONPATH=$KSL_PPC450D_PYTHONPATH:/project/k47/prod/petsc4py/dev-jun2011/ppc450d-3.1.8_64/lib/python:/project/k47/prod/numpy/dev-aug29/ppc450d/lib/python:$PYCLAW/src:$RIEMANN
    export KSL_PPC450D_LD_LIBRARY_PATH=$KSL_PPC450D_LD_LIBRARY_PATH:/project/k47/prod/petsc/3.1.8/ppc450d-bgp_gnu_shared_64/lib:/project/k47/prod/numpy/dev-aug29/ppc450d/lib:/project/k47/prod/petsc4py/dev-jun2011/ppc450d-3.1.8_64/lib/python/petsc4py/lib:/opt/ibmcmp/xlsmp/bg/1.7/lib:/opt/ibmcmp/xlmass/bg/4.4/bglib:/opt/ibmcmp/xlf/bg/11.1/bglib
    export BGP_PYTHON=/bgsys/drivers/ppcfloor/gnu-linux/bin/python
    echo "*****************************************************************"
    echo "the following commands are available:"
    echo "kslrun    - simplifies launching jobs on Shaheen"
    echo "*****************************************************************"
    echo "Example:"
    echo 'cd $PYCLAW/apps/advection/1d/constant'
    echo 'kslrun -a k47 -n 4 "$BGP_PYTHON advection.py kernel_language=Fortran use_petsc=True"'
    echo ''
    echo 'type kslrun -h for configuration options'
    echo "*****************************************************************"
    echo "pyclaw execution environment initialized"
    echo "*****************************************************************"
}

echo "pyclaw production execution environment on Shaheen initialized"
echo "the following commands are available:"
echo "pyclaw_build - enables compiling/building Fortran kernel modules"
echo "pyclaw_run   - enables launching jobs using kslrun or loadleveler scripts"