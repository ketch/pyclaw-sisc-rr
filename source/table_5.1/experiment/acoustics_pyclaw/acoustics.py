#!/usr/bin/env python
# encoding: utf-8

import numpy as np

def acoustics2D(iplot=False,htmlplot=False,use_petsc=False,outdir='./_output',solver_type='classic'):
    """
    Example python script for solving the 2d acoustics equations.
    """
    if use_petsc:
        import petclaw as pyclaw
    else:
        import pyclaw
    
    if solver_type=='classic':
        solver=pyclaw.ClawSolver2D()
    elif solver_type=='sharpclaw':
        solver=pyclaw.SharpClawSolver2D()

    solver.dim_split=True
    solver.order = 2
    solver.mwaves = 2
    solver.mthlim = [4]*solver.mwaves
    solver.kernel_language = 'Fortran'
    solver.mthbc_lower[0]=pyclaw.BC.outflow
    solver.mthbc_upper[0]=pyclaw.BC.outflow
    solver.mthbc_lower[1]=pyclaw.BC.outflow
    solver.mthbc_upper[1]=pyclaw.BC.outflow
    solver.cfl_max = .5
    solver.cfl_desired = 0.45
    # Initialize grid
    mx=500; my=500
    x = pyclaw.Dimension('x',-1.0,1.0,mx)#,mthbc_lower=1,mthbc_upper=1)
    y = pyclaw.Dimension('y',-1.0,1.0,my)#, mthbc_lower=1,mthbc_upper=1)
    grid = pyclaw.Grid([x,y])
    state = pyclaw.State(grid)

    rho = 1.0
    bulk = 4.0
    cc = np.sqrt(bulk/rho)
    zz = rho*cc
    state.aux_global['rho']= rho
    state.aux_global['bulk']=bulk
    state.aux_global['zz']= zz
    state.aux_global['cc']=cc

    state.meqn = 3

    Y,X = np.meshgrid(grid.y.center,grid.x.center)
    r = np.sqrt(X**2 + Y**2)
    width=0.2
    state.q[0,:,:] = (np.abs(r-0.5)<=width)*(1.+np.cos(np.pi*(r-0.5)/width))
    state.q[1,:,:] = 0.
    state.q[2,:,:] = 0.
    claw = pyclaw.Controller()
    claw.keep_copy = True
    claw.solution = pyclaw.Solution(state)
    claw.solver = solver
    claw.outdir=outdir
    claw.output_format = None
    claw.nout = 1

    # Solve
    claw.tfinal = 0.4
    status = claw.run()
    print 'number of steps: '+ str(status.get('numsteps')) 

    pressure=0
    return pressure


if __name__=="__main__":
    import sys
    from time import time
    if len(sys.argv)>1:
        from pyclaw.util import _info_from_argv
        args, kwargs = _info_from_argv(sys.argv)
        t1 = time()
        acoustics2D(*args,**kwargs)
        t2 = time
        acoustics2D(*args,**kwargs)
    else:
        t1 = time()
        acoustics2D()
        t2 = time()
        acoustics2D()
    t3 = time()
    print "first call", t2-t1, "second call", t3-t2
