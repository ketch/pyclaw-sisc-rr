coarsen_data: experiment/_output/claw_p.pkl0000 experiment/_output/claw_p.ptc0000
	python coarsen.py 

compress_data: claw_p_coarsened.pkl0000 claw_p_coarsened.ptc0000
	bzip2 claw_p_coarsened.pkl0000 claw_p_coarsened.ptc0000

figure_7.4: experiment/_output/claw_p_coarsened.pkl0000.bz2 experiment/_output/claw_p_coarsened.ptc0000.bz2 plots.py
	bunzip2 experiment/_output/claw_p_coarsened.pkl0000.bz2 experiment/_output/claw_p_coarsened.ptc0000.bz2 
	python plots.py
