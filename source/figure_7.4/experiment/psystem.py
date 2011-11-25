#!/usr/bin/env python
# encoding: utf-8

import numpy as np

# material parameters
E1=1.;   p1=1.
E2=5.;   p2=5.
# interface parameters
alphax=0.5; deltax=1.
alphay=0.5; deltay=1.
# Linearity parameters
linearity_mat1=2; linearity_mat2=2
# heterogeneity type
het_type='checkerboard'
#het_type='sinusoidal'
#het_type='smooth_checkerboard'
sharpness=10

def qinit(state,A,x0,y0,varx,vary):
    r""" Set initial conditions for q."""
    x =state.grid.x.center; y =state.grid.y.center
    # Create meshgrid
    [yy,xx]=np.meshgrid(y,x)
    s=A*np.exp(-(xx-x0)**2/(2*varx)-(yy-y0)**2/(2*vary)) #sigma(@t=0)
    #parameters from aux
    linearity_mat=state.aux[2,:]
    E=state.aux[1,:]
    #initial condition
    state.q[0,:,:]=np.where(linearity_mat==1,1,0)*s/E+np.where(linearity_mat==2,1,0)*np.log(s+1)/E
    state.q[1,:,:]=0; state.q[2,:,:]=0

def setaux(x,y):
    r"""Creates a matrix representing every grid cell in the domain, 
    whose size is len(x),len(y)
    Each entry of the matrix contains a vector of size 3 with:
    The material density p
    The young modulus E
    A flag indicating which material the grid is made of.
    The domain pattern is a checkerboard."""

    aux = np.empty((4,len(x),len(y)), order='F')
    if het_type == 'checkerboard':
        # xfrac and yfrac are x and y relative to deltax and deltay resp.
        xfrac=x-np.floor(x/deltax)*deltax
        yfrac=y-np.floor(y/deltay)*deltay
        # create a meshgrid out of xfrac and yfrac
        [yyfrac,xxfrac]=np.meshgrid(yfrac,xfrac)
        # density 
        aux[0,:,:]=p1*(xxfrac<=alphax*deltax)*(yyfrac<=alphay*deltay)\
            +p1*(xxfrac >alphax*deltax)*(yyfrac >alphay*deltay)\
            +p2*(xxfrac >alphax*deltax)*(yyfrac<=alphay*deltay)\
            +p2*(xxfrac<=alphax*deltax)*(yyfrac >alphay*deltay)
        #Young modulus
        aux[1,:,:]=E1*(xxfrac<=alphax*deltax)*(yyfrac<=alphay*deltay)\
            +E1*(xxfrac >alphax*deltax)*(yyfrac >alphay*deltay)\
            +E2*(xxfrac >alphax*deltax)*(yyfrac<=alphay*deltay)\
            +E2*(xxfrac<=alphax*deltax)*(yyfrac >alphay*deltay)
        # linearity of material
        aux[2,:,:]=linearity_mat1*(xxfrac<=alphax*deltax)*(yyfrac<=alphay*deltay)\
            +linearity_mat1*(xxfrac >alphax*deltax)*(yyfrac >alphay*deltay)\
            +linearity_mat2*(xxfrac >alphax*deltax)*(yyfrac<=alphay*deltay)\
            +linearity_mat2*(xxfrac<=alphax*deltax)*(yyfrac >alphay*deltay)
    elif het_type == 'sinusoidal' or het_type == 'smooth_checkerboard':
        [yy,xx]=np.meshgrid(y,x)
        Amp_p=np.abs(p1-p2)/2; offset_p=(p1+p2)/2
        Amp_E=np.abs(E1-E2)/2; offset_E=(E1+E2)/2
        if het_type == 'sinusoidal':
            frec_x=2*np.pi/deltax; frec_y=2*np.pi/deltay
            fun=np.sin(frec_x*xx)*np.sin(frec_y*yy)
        else:
            fun_x=xx*0; fun_y=yy*0
            for i in xrange(0,1+int(np.ceil((x[-1]-x[0])/(deltax*0.5)))):
                fun_x=fun_x+(-1)**i*np.tanh(sharpness*(xx-deltax*i*0.5))
            for i in xrange(0,1+int(np.ceil((y[-1]-y[0])/(deltay*0.5)))):
                fun_y=fun_y+(-1)**i*np.tanh(sharpness*(yy-deltay*i*0.5))
            fun=fun_x*fun_y
        aux[0,:,:]=Amp_p*fun+offset_p
        aux[1,:,:]=Amp_E*fun+offset_E
        aux[2,:,:]=linearity_mat1
    return aux

def b4step(solver,solutions):
    r"""put in aux[3,:,:] the value of q[0,:,:] (eps). This is required in rptpv.f"""
    state = solutions['n'].states[0]   
    state.aux[3,:,:] = state.q[0,:,:]

    # To set to 0 1st 1/2 of the domain. Used in rect domains with PBC in x
    if state.aux_global['turnZero_half_2D']==1:
        if state.t>=state.aux_global['t_turnZero'] and state.t<=state.aux_global['t_turnZero']+1:
            if state.grid.x.nend <= np.floor(state.grid.x.n/2):
                state.q[:,:,:]=0

def compute_p(state):
    state.p[0,:,:]=np.exp(state.q[0,:,:]*state.aux[1,:,:])-1

def compute_F(state):
    rho = state.aux[0,:,:]; E = state.aux[1,:,:]
    
    #Compute the entropy
    u = state.q[1,:,:]/rho
    v = state.q[2,:,:]/rho

    nrg=rho * (u**2 + v**2)/2.

    eps = state.q[0,:,:]
    sigma = np.exp(E*eps) - 1.
    sigint = (sigma-np.log(sigma+1.))/E

    dx=state.grid.d[0]; dy=state.grid.d[1]
    
    state.F[0,:,:] = (sigint+nrg)*dx*dy 

def gauge_pfunction(q,aux):
    p = np.exp(q[0]*aux[1])-1
    return [p]

def gauges(radii,thetas):
    gauges_list=[]
    for radius in radii:
        for theta in thetas: 
            gauges_list.append([radius,theta])
    return gauges_list

def psystem2D(use_petsc=True,solver_type='classic',iplot=False,htmlplot=False):
    """
    Solve the p-system in 2D with variable coefficients
    """
    if use_petsc:
        import petclaw as pyclaw
    else:
        import pyclaw

    ####################################
    ######### MAIN PARAMETERS ##########
    ####################################
    # Domain
    x_lower=0.25; x_upper=200.25
    y_lower=0.25; y_upper=200.25
    # Grid cells per layer
    Ng=240
    mx=(x_upper-x_lower)*Ng; my=(y_upper-y_lower)*Ng
    # Initial condition parameters
    A=5.
    x0=0.25 # Center of initial perturbation
    y0=0.25 # Center of initial perturbation
    varx=5.0; vary=5.0 # Width of initial perturbation
    # Boundary conditions
    mthbc_x_lower=pyclaw.BC.reflecting; mthbc_x_upper=pyclaw.BC.outflow
    mthbc_y_lower=pyclaw.BC.reflecting; mthbc_y_upper=pyclaw.BC.outflow
    # Turning off 1st half of the domain. Useful in rect domains
    turnZero_half_2D=0 #flag
    t_turnZero=50
    # Regarding time
    tfinal=200.0
    nout=200
    t0=0.0
    # restart options
    restart_from_frame = None
    #solver = pyclaw.ClawSolver2D()
    solver = pyclaw.SharpClawSolver2D()
    solver.mwaves = 2
    solver.limiters = pyclaw.limiters.tvd.MC

    solver.mthbc_lower[0]=mthbc_x_lower
    solver.mthbc_upper[0]=mthbc_x_upper
    solver.mthbc_lower[1]=mthbc_y_lower
    solver.mthbc_upper[1]=mthbc_y_upper
    solver.mthauxbc_lower[0]=mthbc_x_lower
    solver.mthauxbc_upper[0]=mthbc_x_upper
    solver.mthauxbc_lower[1]=mthbc_y_lower
    solver.mthauxbc_upper[1]=mthbc_y_upper

    solver.fwave = True
    solver.cfl_max = 2.5
    solver.cfl_desired = 2.45
    solver.start_step = b4step
    solver.dim_split=False
    solver.max_steps = 1000000000
    
    #controller
    claw = pyclaw.Controller()
    claw.tfinal = tfinal
    claw.solver = solver

    if restart_from_frame is not None:
        claw.solution = pyclaw.Solution(restart_from_frame, format='petsc',read_aux=False)
        claw.solution.state.mp = 1
        claw.solution.state.mF = 1
        grid = claw.solution.grid
        claw.solution.state.aux = setaux(grid.x.center,grid.y.center)
        claw.nout = nout - restart_from_frame
        claw.start_frame = restart_from_frame
    else:
        ####################################
        ####################################
        ####################################
        #Creation of grid
        x = pyclaw.Dimension('x',x_lower,x_upper,mx)
        y = pyclaw.Dimension('y',y_lower,y_upper,my)
        grid = pyclaw.Grid([x,y])
        state = pyclaw.State(grid)
        state.meqn = 3
        state.mF = 1
        state.mp = 1
        state.t=t0
        #Set global parameters
        state.aux_global = {}
        state.aux_global['turnZero_half_2D'] = turnZero_half_2D
        state.aux_global['t_turnZero'] = t_turnZero

        state.aux = setaux(grid.x.center,grid.y.center)
        #Initial condition
        qinit(state,A,x0,y0,varx,vary)

        claw.solution = pyclaw.Solution(state)
        claw.nout = nout

    claw.compute_p = compute_p
    claw.compute_F = compute_F
    gauges_radii=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    gauges_thetas=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
    grid.add_gauges(gauges(gauges_radii,gauges_thetas))
    solver.compute_gauge_values = gauge_pfunction
    claw.write_aux_init = False

    #Solve
    status = claw.run()
    
    #strain=claw.frames[claw.nout].state.gqVec.getArray().reshape([grid.ng[0],grid.ng[1],state.meqn])[:,:,0]
    #return strain

    if iplot:    pyclaw.plot.plotInteractive()
    if htmlplot: pyclaw.plot.plotHTML()

if __name__=="__main__":
    import sys
    from pyclaw.util import _info_from_argv
    args, kwargs = _info_from_argv(sys.argv)
    psystem2D(*args,**kwargs)
