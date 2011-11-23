BUILD_DIR=./build

all: $(BUILD_DIR) table_1 figure_5.1 table_2 \
     figure_4 figure_5 figure_6 figure_7

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

#catch all for unimplemented targets
%: source/%/placeholder.txt 
	@cat $^
	@mkdir -p $(BUILD_DIR)/$@
	@cp $^ $(BUILD_DIR)/$@/

figure_5.1: source/figure_5.1/makefig.py 
	@mkdir -p $(BUILD_DIR)/$@
	python $^ $(BUILD_DIR)/$@
	convert $(BUILD_DIR)/$@/euler_weak_scaling.png -gravity South \
          -background white -splice 0x1  -background black -splice 0x1 \
          -trim  +repage -chop 0x1 $(BUILD_DIR)/$@/euler_weak_scaling.png
	convert $(BUILD_DIR)/$@/euler_weak_scaling.png -gravity West \
          -background white -splice 1x0  -background black -splice 1x0 \
          -trim  +repage -chop 1x0 $(BUILD_DIR)/$@/euler_weak_scaling.png

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

