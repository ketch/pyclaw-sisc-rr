PYCLAWMAKE = $(PYCLAW)/Makefile.common

include $(PYCLAWMAKE)

RP_SOURCE =   $(RIEMANN)/src/rpn2_euler_5wave.f $(RIEMANN)/src/rpt2_euler_5wave.f

code: classic2.so 

data: code
    python shockbubble.py
    
figure: data
    python makefig.py
    cp _plots/frame0000fig1.png ./fig5a.png
    cp _plots/frame0009fig1.png ./fig5b.png
    cp _plots/frame0009fig0.png ./fig5c.png
