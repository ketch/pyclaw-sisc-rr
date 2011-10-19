BUILD_DIR=./build

all: $(BUILD_DIR) table_1 figure_3 table_2 \
     figure_4 figure_5 figure_6 figure_7

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

#catch all for unimplemented targets
%: source/%/placeholder.txt 
	@cat $^
	@mkdir -p $(BUILD_DIR)/$@
	@cp $^ $(BUILD_DIR)/$@/

# example
table_1: source/table_1/placeholder.txt
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

