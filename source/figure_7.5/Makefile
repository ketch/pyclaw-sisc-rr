coarsen_data: experiment/_output/claw_p.pkl0200 experiment/_output/claw_p.ptc0200
	python coarsen.py 

compress_data: claw_p_coarsened.pkl0200 claw_p_coarsened.ptc0200
	bzip2 claw_p_coarsened.pkl0200 claw_p_coarsened.ptc0200

figure_7.5: experiment/_output/claw_p_coarsened.pkl0200.bz2 experiment/_output/claw_p_coarsened.ptc0200.bz2 plots.py
	bunzip2 experiment/_output/claw_p_coarsened.pkl0200.bz2 experiment/_output/claw_p_coarsened.ptc0200.bz2 
	python plots.py
