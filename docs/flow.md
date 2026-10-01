# The flow, stage by stage

This walks through what happens when you run `make sim` and `make harden`, using the counter as the example. Paths are relative to `designs/counter/runs/<pdk>/`, where each numbered folder is one step of the LibreLane flow with its own logs and reports.

## 1. Simulation (`make sim`, `make sim-verilator`)

The testbench drives the counter and compares it on every cycle with a behavioural reference model. It checks counting, the wrap pulse, holding when `en` is low, and synchronous reset, and prints `PASS` only if nothing mismatched. The same testbench runs on two simulators:

- **Icarus Verilog**: event-driven, closest to the language standard, quick to start.
- **Verilator**: compiles Verilog to C++, much faster on large designs, stricter lint.

Passing both catches simulator-dependent code early. `+vcd` writes `build/<design>/<design>_tb.vcd`, which you can open in GTKWave (in the container: `make shell`, then `gtkwave build/counter/counter_tb.vcd`).

## 2. Lint (`make lint`, and steps 01–04)

Verilator with `-Wall` flags width mismatches, unused signals, latches and similar mistakes before synthesis.

## 3. Synthesis (step 06, Yosys)

Yosys turns the RTL into a netlist of the PDK's standard cells (`sky130_fd_sc_hd__dfxtp_1` flip-flops, adders built from logic gates, and so on). Look at `06-yosys-synthesis/reports/stat.rpt` for the cell count and area.

## 4. Floorplan and power grid (steps 13–22, OpenROAD)

Sets the die (150 × 150 µm here, from `DIE_AREA` in `config.json`), cuts standard-cell rows, inserts tap and end-cap cells, and builds the power distribution network (the metal stripes in the layout render).

## 5. Placement (steps 24–34)

Global placement spreads cells to minimise wire length at the target density (`PL_TARGET_DENSITY_PCT`), I/O placement puts the pins on the die edge, then detailed placement snaps cells legally into rows.

## 6. Clock tree synthesis (step 35)

Builds a buffered tree so the clock reaches every flip-flop with low skew, then repairs any timing problems the new buffers caused.

## 7. Routing (steps 39–46)

Global routing plans which metal layers and regions each net uses; detailed routing (TritonRoute) draws the actual wires and vias and iterates until there are no routing DRC errors. Antenna diodes are inserted where long wires could damage transistor gates during manufacture.

## 8. Parasitic extraction and timing (steps 54–55)

OpenRCX extracts the resistance and capacitance of every wire. OpenSTA then checks setup and hold timing at every process, voltage and temperature corner. Reports are in `55-openroad-stapostpnr/`; `summary.rpt` there lists the worst slack per corner.

## 9. GDS and sign-off (steps 57–76)

- **Stream-out**: Magic and KLayout each write a GDS; an XOR check confirms they agree.
- **DRC**: Magic and KLayout check the layout against the foundry's design rules.
- **LVS**: Magic extracts a SPICE netlist from the layout and Netgen compares it with the synthesised netlist.
- **Checkers**: the flow stops with an error if any DRC, LVS, antenna, timing, slew or capacitance check fails.

`76-misc-reportmanufacturability/` has the one-page verdict, and `make summary` prints the key numbers from `final/metrics.json`.

## Outputs

`final/` holds every view of the finished block: `gds/` (layout for fabrication), `lef/` (abstract for use as a macro), `nl/` and `pnl/` (netlists without and with power pins), `sdf/` (delays for gate-level simulation), `lib/` (timing model), `spef/` (parasitics) and `render/` (PNG).

## Switching PDK

The PDK is a make variable, not part of the design:

```bash
make harden summary PDK=sky130A       # default
make harden summary PDK=ihp-sg13g2
make harden summary PDK=gf180mcuD     # installed in the image, not yet tested with the counter
```

The Makefile picks the default standard-cell library for each PDK; override it with `SCL=<library>`. If a design needs PDK-specific settings, put them in `config.json` under a `"pdk::<name>"` key, for example:

```json
"pdk::ihp-sg13g2": { "PL_TARGET_DENSITY_PCT": 60 }
```

## Adding your own design

1. `cp -r designs/counter designs/<name>`
2. Put your RTL in `designs/<name>/src/`. The top module name must match `DESIGN_NAME` in `config.json`.
3. Write `designs/<name>/tb/<name>_tb.v` so that it prints a line starting `PASS` when every check succeeds.
4. Edit `config.json`: `DESIGN_NAME`, `CLOCK_PORT`, `CLOCK_PERIOD` (ns), and `DIE_AREA` (µm) large enough for your cells. A good starting point is a die area of about three times the synthesised cell area.
5. `make sim harden summary DESIGN=<name>`

The full list of configuration variables is in the [LibreLane documentation](https://librelane.readthedocs.io/).
