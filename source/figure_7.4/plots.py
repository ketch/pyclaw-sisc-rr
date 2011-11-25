from pyclaw.solution import Solution
from petclaw.io.petsc import read_petsc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as pl
from matplotlib import rc
rc('text', usetex=True)
import matplotlib.cm as cm
import numpy as np
import os

def plot_checker(Ka=5,Kb=1,length=10.25):
    x = np.linspace(0.25,length,1000)
    y = np.linspace(0.25,length,1000)
    yy,xx = np.meshgrid(y,x)
    #checker                                                      
    xfrac=x-np.floor(x);
    yfrac=y-np.floor(y);
    [yyfrac,xxfrac]=np.meshgrid(yfrac,xfrac);

    checker = Ka*(xxfrac<=0.5)*(yyfrac<=0.5)+Ka*(xxfrac>0.5)*(yyfrac>0.5)+Kb*(xxfrac>0.5)*(yyfrac<=0.5)+Kb*(xxfrac<=0.5)*(yyfrac>0.5);
    pl.pcolormesh(xx,yy,checker,cmap=cm.gray)
    pl.xlabel('x',fontsize=20); pl.ylabel('y',fontsize=20)
    pl.xticks(size=20); pl.yticks(size=20)
    pl.axis('scaled')
    pl.axis([np.min(x),np.max(x),np.min(y),np.max(y)])
    pl.savefig('checker.png')
    pl.close()


def plot_p(frame,skip=1,file_prefix='claw_p',path='./_output/_p',title='',axis=None,file_name='fig',axis_slices=None):
    sol=Solution()
    read_petsc(sol,frame=frame,path=path,file_prefix=file_prefix)
    x=sol.grid.x.center; y=sol.grid.y.center
    mx=len(x); my=len(y)
    subx=range(0,mx,skip)
    suby=range(0,my,skip)

    mp=sol.state.meqn

    yy,xx = np.meshgrid(y[suby],x[subx])

    for i in xrange(mp):
        p=sol.state.q[i,:,:]
        p_subx=p[subx,:]
        p_subxy=p_subx[:,suby]
        
        pl.pcolormesh(xx,yy,p_subxy,cmap=cm.OrRd)
        #pl.pcolormesh(xx,yy,p_subxy)
        pl.title(title,fontsize=20)
        pl.xticks(size=20); pl.yticks(size=20)
        cb = pl.colorbar();
        imaxes = pl.gca(); pl.axes(cb.ax)
        pl.yticks(fontsize=20); pl.axes(imaxes)
        if axis is not None:
            pl.axis([axis[0],axis[1],axis[0],axis[1]])
        else:
            pl.axis([np.min(x),np.max(x),np.min(y),np.max(y)])
        pl.savefig(file_name+'.png')
        pl.close()
        if axis_slices is not None:
            p_45=np.zeros(my)
            for j in xrange(0,my):
                p_45[j]=p[j,j]
            x_45=x*np.sqrt(2)
            pl.plot(x_45,p_45,'-k')
            pl.plot(x,p[:,2],'--r')
            pl.xlabel('Radial distance',fontsize=20)
            pl.ylabel('Stress',fontsize=20)
            pl.xticks(size=20); pl.yticks(size=20)
            pl.axis([axis_slices[0],axis_slices[1],np.min(p),np.max(p)])
            pl.savefig(file_name+'_slices.png')
            pl.close()

if __name__== "__main__":
    plot_initial_condition = True
    plot_medium = True
    plot_steg = False

    path='./experiment/_output'

    if plot_initial_condition:
        print('**********************')
        print('**********************')
        print('Plotting initial condition ...')
        plot_p(frame=0,skip=1,path=path,file_prefix='claw_p_coarsened',title='Initial Condition',axis=[0.25,10.25],file_name='initial_condition')

    if plot_medium:
        print('**********************')
        print('**********************')
        print('Plotting medium ...')
        plot_checker()

    if plot_steg:
        print('**********************')
        print('**********************')
        print('Plotting stegoton ...')
        plot_p(frame=200,skip=1,path=path,file_prefix='claw_p_coarsened',title='t=90.0',file_name='stress_checker',axis_slices=[160,190])
