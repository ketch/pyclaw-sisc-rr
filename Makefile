BUILD_DIR=./build

all: $(BUILD_DIR) table_1 figure_5.1 table_2 \
     figure_4 figure_5 figure_6 figure_7

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

figure_5.1: source/figure_5.1/makefig.py 
	@mkdir -p $(BUILD_DIR)/$@
	@cat source/figure_5.1/README.txt
	@cp source/figure_5.1/README.txt $(BUILD_DIR)/$@
	@echo "Building figure 5.1 from raw data"
	python $^ $(BUILD_DIR)/$@
	@echo "***\nmanually crop image vertically and save in .pdf format\n***"

figure_5.1/experiment: source/ 
	@mkdir -p $(BUILD_DIR)/$@	
	@cat source/figure_5.1/experiment/README.txt
	@cp source/figure_5.1/experiment/README.txt $(BUILD_DIR)/$@

#catch all for unimplemented targets
%: source/%/placeholder.txt 
	@cat $^
	@mkdir -p $(BUILD_DIR)/$@
	@cp $^ $(BUILD_DIR)/$@/

#catch all for unimplemented target experiments
%/experiment: source/%/experiment/placeholder.txt
	@cat $^	
	@mkdir -p $(BUILD_DIR)/$@
	@cp $^ $(BUILD_DIR)/$@

# example
table_1/experiment: source/table_1/experiment/placeholder.txt
	@cat $^	
	@mkdir -p $(BUILD_DIR)/$@
	@cp $^ $(BUILD_DIR)/$@/

