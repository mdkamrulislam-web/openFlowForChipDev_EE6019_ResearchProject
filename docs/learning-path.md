# Learning path: from RTL to layout with the open flow

This is for someone who can write and verify Verilog but has never done physical design (the steps that turn a netlist into a layout). It is a set of hands-on exercises on this repository, in order. Each one takes an hour or two. Write down what you see in each exercise; those notes become your Friday log and, later, the student guide.

## What "developing an open flow" means

You do not write any EDA tools. Yosys, OpenROAD, Magic, KLayout and the rest already exist. A *flow* is the layer around them:

| Layer | What it is | Where it lives here |
|---|---|---|
| Tools and PDKs | The programs and the foundry data, at fixed versions | `env/tools.env` (one container image) |
| Glue | Commands that run the tools in the right order with the right settings | `Makefile`, `scripts/`, LibreLane, `designs/*/config.json` |
| Checks | Proof that a run worked: tests pass, DRC and LVS clean, timing met | Testbenches, `scripts/summary.py`, `.github/workflows/flow.yml` |
| Documentation | How someone else installs it, runs it and fixes problems | `README.md`, `docs/` |

LibreLane already chains the physical-design tools. The project's work is to choose and pin the tools, make the flow easy and reproducible, add what is missing (gate-level simulation, cocotb, Tiny Tapeout compatibility, a second flow for comparison), measure it, and document it well enough for a student to follow alone.

## A map from verification to physical design

| You already know | The physical-design equivalent |
|---|---|
| RTL simulation proves the function | Synthesis, place and route must keep that function; LVS and gate-level simulation prove it did |
| A testbench that prints PASS | Sign-off checks that report zero: DRC, LVS, antenna, setup and hold violations |
| Simulator and its compile options | The PDK and its standard-cell library, chosen by `PDK=` and `SCL=` |
| Regression in CI | `make harden summary` on each PDK in CI |
| Gate-level sim with SDF | The same, using the routed netlist and SDF that the flow writes to `final/` |

## Words you will meet

- **PDK** (process design kit): the foundry's rules and data for one manufacturing process (SKY130, IHP SG13G2, GF180).
- **Standard cell**: a pre-drawn logic gate or flip-flop of fixed height. Synthesis maps your RTL onto these.
- **Liberty (`.lib`)**: timing and power of each cell. **LEF**: each cell's outline and pins. **GDS**: the final layout, the file a foundry manufactures.
- **Floorplan**: the die size, the rows cells sit in, and where the pins go. **Utilisation / density**: how full the rows are.
- **PDN** (power distribution network): the metal grid that carries power and ground to every cell.
- **CTS** (clock tree synthesis): buffers inserted so the clock reaches every flip-flop at nearly the same time (low *skew*).
- **Routing**: drawing the metal wires and vias that connect the cells.
- **Parasitics (SPEF)**: the resistance and capacitance of the real wires, used for accurate timing.
- **Slack**: how much timing margin is left. Positive is good; negative is a violation. **Setup** is "is the data there in time", **hold** is "did it stay stable long enough".
- **Corners**: timing checked at slow, typical and fast process, voltage and temperature.
- **DRC** (design-rule check): the layout obeys the foundry's geometry rules. **LVS** (layout versus schematic): the layout is the same circuit as the netlist. **Antenna**: long wires that could damage transistor gates during manufacture.

## Exercise 0: a warm-up in Wokwi (no install)

Open the Wokwi template from [tinytapeout.com](https://tinytapeout.com/) in a browser. Build a four-flip-flop shift register: chain the flip-flops Q to D, connect every clock to the clock input, take the first D from a switch, and drive four display segments from the Q outputs. Simulate it with the single-step clock, then with the clock generator at 2 Hz. Press restart a few times and notice that the flip-flops start in a random state: on silicon nothing is initialised unless you reset it. [tiny-tapeout.md](tiny-tapeout.md) summarises the videos that go with this.

## Exercise 1: install and run the counter

Follow [setup.md](setup.md), then:

```bash
make sim                       # expect: PASS: counter_tb (8-bit), 0 errors
make harden summary            # SKY130, a few minutes
make harden summary PDK=ihp-sg13g2
```

Record: how long each command took, the disk space used, and anything that went wrong and how you fixed it.

## Exercise 2: walk through a run folder

Open `designs/counter/runs/sky130A/` and read [flow.md](flow.md) beside it. Each numbered folder is one step. For each stage in flow.md, find its folder and open one report:

- `06-yosys-synthesis/reports/stat.rpt`: which cells did Yosys use, and how many flip-flops? Does that match 8 bits of count?
- `55-openroad-stapostpnr/summary.rpt`: worst setup and hold slack at each corner. Which corner is the worst, and why would that be?
- `final/metrics.json`: the numbers `make summary` prints.

## Exercise 3: look at the layout

Install KLayout on your own machine and open `final/gds/counter.gds` (or look at `final/render/`). Find the power stripes, the standard-cell rows, the pins on the edge, and the empty space filled with filler and tap cells. Compare the SKY130 and IHP layouts: why does IHP need far fewer cells for the same design?

## Exercise 4: break it on purpose

Each change below makes one check fail. Make the change, run `make harden summary`, read the error, then undo it. Write down what failed and where the flow reported it.

1. **Timing.** In `config.json`, lower `CLOCK_PERIOD` (20 ns now) step by step until setup slack goes negative. That is roughly the counter's maximum clock. Then try `PDK=ihp-sg13g2` at the same period.
2. **Area.** Shrink `DIE_AREA` from 150 × 150 µm until placement fails.
3. **Function.** Add a bug to `counter.v` and check that `make sim` fails before you run `harden`. (Synthesis and DRC will not notice a logic bug; only verification does.)

This is the most useful exercise: most of a physical designer's job is reading these failures and fixing them.

## Exercise 5: your own small design

Follow [Adding your own design](flow.md#adding-your-own-design) with something small that you choose: a shift register, a PWM generator or a UART transmitter. Write the testbench first. Take it through `sim`, `harden` and `summary` on both PDKs, and record the area and slack.

## After that

The project plan in [AGENTS.md](../AGENTS.md) takes over: the Tiny Tapeout IHP template (week 3), local hardening with `tt_tool`, the second flow (OpenROAD-flow-scripts), and the comparison between them.

## Further reading

- LibreLane documentation, especially the configuration variables: <https://librelane.readthedocs.io/>
- Tiny Tapeout, *Making ASICs* and the digital design lessons: <https://tinytapeout.com/making_asics/>
- OpenROAD documentation: <https://openroad.readthedocs.io/>
