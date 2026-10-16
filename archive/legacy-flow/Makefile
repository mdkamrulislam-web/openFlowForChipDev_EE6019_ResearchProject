# EE6019 open chip flow: top-level entry points.
#
#   make sim                    simulate DESIGN with Icarus Verilog
#   make sim-verilator          simulate DESIGN with Verilator
#   make lint                   Verilator lint of the RTL
#   make harden                 RTL to GDS with LibreLane on PDK
#   make summary                print sign-off metrics of the last harden
#   make view                   open the final GDS in KLayout (needs a display)
#   make shell                  interactive shell in the tool container
#
# Knobs:  DESIGN=counter  PDK=sky130A | ihp-sg13g2 | gf180mcuD
#
# On the host every command runs inside the pinned container (env/tools.env).
# Inside the container (e.g. `make shell`) the tools are called directly.

DESIGN  ?= counter
PDK     ?= sky130A
RUN_TAG ?= $(PDK)

# Default standard-cell library for each PDK.
SCL_sky130A    := sky130_fd_sc_hd
SCL_ihp-sg13g2 := sg13g2_stdcell
SCL_gf180mcuD  := gf180mcu_fd_sc_mcu7t5v0
SCL     ?= $(SCL_$(PDK))

DESIGN_DIR := designs/$(DESIGN)
BUILD      := build/$(DESIGN)
RUN_DIR    := $(DESIGN_DIR)/runs/$(RUN_TAG)

RTL := $(wildcard $(DESIGN_DIR)/src/*.v)
TB  := $(wildcard $(DESIGN_DIR)/tb/*.v)
TOP_TB := $(DESIGN)_tb

ifeq ($(wildcard /foss/tools),)
  IN := PDK=$(PDK) SCL=$(SCL) scripts/run-in-container.sh
else
  IN :=
endif

.PHONY: all sim sim-verilator lint harden summary view shell clean

all: lint sim harden summary

sim:
	@mkdir -p $(BUILD)
	$(IN) sh -c 'iverilog -g2012 -Wall -s $(TOP_TB) -o $(BUILD)/$(TOP_TB).vvp $(TB) $(RTL) && \
	  cd $(BUILD) && vvp -n $(TOP_TB).vvp +vcd | tee sim_icarus.log && grep -q "^PASS" sim_icarus.log'

sim-verilator:
	@mkdir -p $(BUILD)
	$(IN) sh -c 'verilator --binary --timing -Wno-fatal --top-module $(TOP_TB) -Mdir $(BUILD)/obj_dir $(TB) $(RTL) > $(BUILD)/verilator_build.log && \
	  cd $(BUILD) && ./obj_dir/V$(TOP_TB) | tee sim_verilator.log && grep -q "^PASS" sim_verilator.log'

lint:
	$(IN) verilator --lint-only -Wall $(RTL)

harden:
	$(IN) librelane --manual-pdk --pdk-root /foss/pdks --pdk $(PDK) --scl $(SCL) \
	  --run-tag $(RUN_TAG) --overwrite $(DESIGN_DIR)/config.json

summary:
	@python3 scripts/summary.py $(RUN_DIR)

view:
	$(IN) klayout $(RUN_DIR)/final/gds/$(DESIGN).gds

shell:
	$(IN) bash

clean:
	rm -rf build $(DESIGN_DIR)/runs
