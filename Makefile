CWD := $(shell pwd)
export BUILD_DIR := $(CWD)/build

all: $(BUILD_DIR) table_5.1/experiment figure_5.1/experiment table_7.1/experiment figure_7.1/experiment figure_7.2/experiment figure_7.3/experiment figure_7.4/experiment figure_7.5/experiment table_5.1 figure_5.1 table_7.1 figure_7.1 figure_7.2 figure_7.3 figure_7.4 figure_7.5 

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

table_5.1: source/table_5.1/README.txt
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/table_5.1/README.txt
	@cp source/table_5.1/README.txt $(BUILD_DIR)/$@

table_5.1/experiment: source/table_5.1/experiment/*
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/table_5.1/experiment/README.txt
	@cp source/table_5.1/experiment/README.txt $(BUILD_DIR)/$@
	@echo "Copying table 5.1 experiment source files to $(BUILD_DIR)/$@"
	@cp -r $^ $(BUILD_DIR)/$@

table_7.1: source/table_7.1/README.txt
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/table_7.1/README.txt
	@cp source/table_7.1/README.txt $(BUILD_DIR)/$@

table_7.1/experiment: source/table_7.1/experiment/*
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/table_7.1/experiment/README.txt
	@cp source/table_7.1/experiment/README.txt $(BUILD_DIR)/$@
	@echo "Copying table 7.1 experiment source files to $(BUILD_DIR)/$@"
	@cp -r $^ $(BUILD_DIR)/$@

figure_5.1: source/figure_5.1/makefig.py source/figure_5.1/README.txt
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/figure_5.1/README.txt
	@cp source/figure_5.1/README.txt $(BUILD_DIR)/$@
	@echo "Building figure 5.1 from raw data"
	(cd source/figure_5.1 && python makefig.py $(BUILD_DIR)/$@)
	@echo "***\nMANUAL STEP: crop image vertically and save in .pdf format\n***"

figure_5.1/experiment: source/figure_5.1/experiment/src2.f source/figure_5.1/experiment/shockbubble.py source/figure_5.1/experiment/Makefile
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/figure_5.1/experiment/README.txt
	@cp source/figure_5.1/experiment/README.txt $(BUILD_DIR)/$@
	@cp $^ $(BUILD_DIR)/$@

figure_7.1: source/figure_7.1/README.txt
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/figure_7.1/README.txt
	@cp source/figure_7.1/README.txt $(BUILD_DIR)/$@

figure_7.1/experiment: source/figure_7.1/experiment/shallow_4_Rossby_Haurwitz_wave.py source/figure_7.1/experiment/Makefile 
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/figure_7.1/README.txt
	@cp source/figure_7.1/README.txt $(BUILD_DIR)/$@
	@echo "Re-running Rossby-Haurwitz experiment"
	(cd source/figure_7.1/experiment && time $(MAKE) data)
	@cp $^ $(BUILD_DIR)/$@

figure_7.2: source/figure_7.2/makefig.py source/figure_7.2/setplot.py source/figure_7.2/README.txt
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/figure_7.2/experiment/README.txt
	@cp source/figure_7.2/experiment/README.txt $(BUILD_DIR)/$@
	@echo "Building figure 7.2 from pyclaw output"
	(cd source/figure_7.2 && $(MAKE) $@)

figure_7.2/experiment: source/figure_7.2/experiment/shockbubble.py source/figure_7.2/experiment/Makefile 
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/figure_7.2/README.txt
	@cp source/figure_7.2/README.txt $(BUILD_DIR)/$@
	@echo "Re-running shock-bubble interaction"
	(cd source/figure_7.2/experiment && time $(MAKE) data)
	@cp $^ $(BUILD_DIR)/$@

figure_7.3: source/figure_7.3/makefig.py source/figure_7.3/setplot.py source/figure_7.3/README.txt
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/figure_7.3/experiment/README.txt
	@cp source/figure_7.3/experiment/README.txt $(BUILD_DIR)/$@
	@echo "Building figure 7.3 from pyclaw output"
	(cd source/figure_7.3 && $(MAKE) $@)

figure_7.3/experiment: source/figure_7.3/experiment/shockbubble.py source/figure_7.3/experiment/Makefile 
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/figure_7.3/experiment/README.txt
	@cp source/figure_7.3/experiment/README.txt $(BUILD_DIR)/$@
	@echo "Re-running WENO comparison of shock-bubble interaction"
	(cd source/figure_7.3/experiment && time $(MAKE) data)
	@cp $^ $(BUILD_DIR)/$@

figure_7.4: source/figure_7.4/plots.py source/figure_7.4/README.txt
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/figure_7.4/README.txt
	@cp source/figure_7.4/README.txt $(BUILD_DIR)/$@
	@echo "Building figure 7.4 from pyclaw output"
	(cd source/figure_7.4 && $(MAKE) $@)

figure_7.4/experiment: source/figure_7.4/experiment/psystem.py 
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/figure_7.4/experiment/README.txt
	@cp source/figure_7.4/experiment/README.txt $(BUILD_DIR)/$@
	@cp $^ $(BUILD_DIR)/$@

figure_7.5: source/figure_7.5/plots.py source/figure_7.5/README.txt
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/figure_7.5/README.txt
	@cp source/figure_7.5/README.txt $(BUILD_DIR)/$@
	@echo "Building figure 7.5 from pyclaw output"
	(cd source/figure_7.5 && $(MAKE) $@)

figure_7.5/experiment: source/figure_7.5/experiment/psystem.py 
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/figure_7.5/experiment/README.txt
	@cp source/figure_7.5/experiment/README.txt $(BUILD_DIR)/$@
	@cp $^ $(BUILD_DIR)/$@

