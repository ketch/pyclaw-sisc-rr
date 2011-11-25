
import os.path
import subprocess

def run(outdir, order=-1):
    """Run the shockbubble example."""

    if os.path.exists(outdir):
        print "directory '%s' already exists, skipping..." % outdir
        return

    args = [ 'mpirun', '-n', '16', 'python', 'shockbubble.py', 'use_petsc=True' ]

    if order > 0:
        args += [ 'solver_type=sharpclaw', 'weno_order=%d' % order ]
    else:
        args += [ 'solver_type=classic' ]

    args += [ 'outdir=%s' % outdir ]

    subprocess.call(args)


# cfl_desired=0.5, cfl_max=0.8
run('reference', order=-1)
run('weno05', order=5)
run('weno07', order=7)
#run('weno09', order=9)

# cfl_desired=0.2, cfl_max=0.3
#run('weno09_2', order=9)

