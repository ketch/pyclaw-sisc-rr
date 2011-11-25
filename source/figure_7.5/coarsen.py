from pyclaw.solution import Solution
from petclaw.io.petsc import read_petsc
from petclaw.io.petsc import write_petsc
from petsc4py import PETSc
import petclaw
import numpy as np
import os

def read_original_solution(frame,file_prefix='claw_p',path='./experiment/_output/_p'):
    sol = Solution()
    read_petsc(sol,frame=frame,path=path,file_prefix=file_prefix)
    return sol

def coarsen_xhalf(sol):
    # Interpolation
    sol.state.q_da.setBoundaryType(PETSc.DA.BoundaryType.NONE)
    sol.state.q_da.setRefinementFactor(refine_x=2,refine_y=2)
    qda_coarsen = sol.state.q_da.coarsen()
    gqVec_coarsen = qda_coarsen.createGlobalVec()
    qda_coarsen.setInterpolationType(interp_type=0)
    mat,scale = qda_coarsen.getInterpolation(sol.state.q_da)
    mat.multTranspose(sol.state.gqVec,gqVec_coarsen)
    gqVec_coarsen = scale*gqVec_coarsen
    qda_coarsen.setBoundaryType(PETSc.DA.BoundaryType.PERIODIC)

    # get coarsened ng
    ranges = qda_coarsen.getRanges()
    ng = np.zeros(2)
    for i,nrange in enumerate(ranges):
        ng[i]=nrange[1]-nrange[0]

    # reshape the coarsened vector
    q_dim = [sol.state.meqn]
    q_dim.extend(ng)
    q_coarsen = gqVec_coarsen.getArray().copy().reshape(q_dim,order = 'F')
    
    # Create coarsen grid        
    lower = sol.grid.lower; upper = sol.grid.upper
    mx = qda_coarsen.getSizes()[0]; my = qda_coarsen.getSizes()[1]
    x = petclaw.Dimension('x',lower[0],upper[0],mx)
    y = petclaw.Dimension('y',lower[1],upper[1],my)
    grid = petclaw.Grid([x,y])

    # Creat coarsened state
    state = petclaw.State(grid)
    state.meqn = sol.state.meqn
    state.t = sol.state.t
    state.q = q_coarsen

    return petclaw.Solution(state)

if __name__== "__main__":
    path='./experiment/_output/'
    first_frame = 0
    last_frame = 200
    
    coarsening_level = 3
    
    for frame in range(first_frame,last_frame+1):
        print 'coarsening frame '+str(frame)
        if frame<10:
            filenumber=str(frame)
            filenumber='000'+filenumber
        elif frame<100:
            filenumber=str(frame)
            filenumber='00'+filenumber
        elif frame<1000:
            filenumber=str(frame)
            filenumber='0'+filenumber
        elif frame <10000:
            filenumber=str(frame)

        filename = ["claw_p.pkl%s" %filenumber,"claw_p.ptc%s" %filenumber,"claw_p.ptc%s.info" %filenumber]

        original_sol = Solution()
        read_petsc(original_sol,frame=frame,path=path,file_prefix='claw_p')
        coarsened_sol = original_sol

        for i in xrange(coarsening_level):
            coarsened_sol = coarsen_xhalf(coarsened_sol)

        # Write coarsened solution
        #if not os.path.exists('./_output/_p/coarsened/'): 
        #    os.mkdir('./_output/_p/coarsened/')
        write_petsc(coarsened_sol,frame,'./',file_prefix='claw_p_coarsened')
