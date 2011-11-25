PYCLAWMAKE = $(PYCLAW)/Makefile.common

include $(PYCLAWMAKE)

RP_SOURCE =   $(RIEMANN)/src/rpn2_euler_5wave.f $(RIEMANN)/src/rpt2_euler_5wave.f

code: classic2.so sharpclaw2.so

data: code
	python run.py

