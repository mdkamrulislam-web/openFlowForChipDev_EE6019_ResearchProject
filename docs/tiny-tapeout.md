# Tiny Tapeout: how it works, and what it means for this flow

Notes from the Tiny Tapeout videos, checked against the current IHP Verilog template ([TinyTapeout/ttihp-verilog-template](https://github.com/TinyTapeout/ttihp-verilog-template), as of 30 Sep 2026). The videos date from Tiny Tapeout 4 to 6 (2023–24), and several details have changed since; those are listed in [What has changed since the videos](#what-has-changed-since-the-videos).

## The videos, and how to watch them

| Video | Length | Main point | How to watch |
|---|---|---|---|
| [From idea to chip design in minutes](https://www.youtube.com/watch?v=qVWq_XZko-M) | 3 min | What Tiny Tapeout is and why it is cheap | In full |
| [Getting started with Wokwi](https://www.youtube.com/watch?v=F1SwXF2ny4g) | 3 min | Drawing and simulating gates in the browser | In full |
| [Working with an HDL](https://www.youtube.com/watch?v=KbWb6xd9jFE) | 3 min | Verilog projects: `info.yaml`, the fixed top module, cocotb tests | In full |
| [Getting your design ready to submit](https://www.youtube.com/watch?v=fCGPKdmM3Dc) | 6 min | The GitHub template, its actions, and submitting | In full |
| [Webinar: Build your first chip with Tiny Tapeout](https://www.youtube.com/watch?v=UVZK-kmN7wc) | 57 min | All of the above, plus design tips | 26:00–52:00 closely (GitHub, submission, Verilog, design tips); skim 6:00–25:00 (logic-gate basics in Wokwi) |

Still to watch from the study path: *Making ASICs* and *Manufacturing ASICs*. These are the most relevant to physical design.

If you read the auto-generated transcripts, some names are misheard: "tiny PayPal" is Tiny Tapeout, "walkway" or "WWE" is Wokwi, "e-fabulous" or "EAB" is Efabless, "Coco DB" is cocotb, "ttk wave" is GTKWave, "icus" is Icarus.

### What each video says

**From idea to chip design in minutes.** A custom chip normally costs tens of thousands for fabrication, plus about $100k for tool licences, under an NDA that stops you sharing the design. Tiny Tapeout combines many small designs into one chip, with an on-chip multiplexer to select which one drives the pins, so each project costs little. You receive everyone's designs as well as your own.

**Getting started with Wokwi.** Wokwi is a browser editor and simulator for gates and flip-flops.
- The electrical rule check (ERC) flags two outputs driving one wire and inputs left unconnected; these must be fixed before the design can be made.
- A `truth_table.md` file turns a truth table into an automatic test.
- Only logic between the input and output blocks is manufactured, so debug LEDs outside them are ignored.
- Saving a copy gives the project a new ID, which is what you put in `info.yaml`.

**Working with an HDL.**
- In `info.yaml`, set the Wokwi ID to 0, list every source file, and name a top module `tt_um_<github user>_<name>`.
- The top module's ports are fixed and cannot change.
- Tests use cocotb: a small `tb.v` instantiates the design, and `test.py` starts the clock, applies reset and checks the outputs. The `test` action runs it on every push.
- A gate-level test (the same test on the synthesised netlist) is strongly recommended, because nothing can be changed after manufacture.

**Getting your design ready to submit.**
1. Create a repository from the template.
2. Set GitHub Pages to GitHub Actions.
3. Fill in `info.yaml` (Wokwi ID or source files, tiles, title, pins) and `docs/info.md`.
4. Commit. The actions build the datasheet, run the tests and build the GDS, and `gds` must be green to submit.
5. If `gds` fails, read the synthesis log first. A design that is too large fails in placement or routing, so reduce it or add tiles.
6. Submit in the app: sign in with GitHub, paste the repository URL, pay, then **submit a revision**.

**Webinar: Build your first chip with Tiny Tapeout.** It repeats the process above in full, then adds:
- **Demo board:** switches on the inputs, a seven-segment display on the outputs, PMOD connectors, and an RP2040 running MicroPython.
- **Limits:** about 1,000 gates per tile, up to 16 tiles, 8 inputs, 8 outputs, 8 bidirectional pins, and roughly 50–66 MHz I/O.
- **The `gds` result page:** shows utilisation (the example used about 2% of a tile), the cells used and a 3D viewer. Most of the tile is filler cells.
- **Design tips:** reset every register, synchronise or debounce external inputs, avoid ripple counters, mind setup and hold timing and clock-domain crossings, and test with Icarus, Verilator, cocotb and a gate-level simulation.
- **Q&A:** compares Tiny Tapeout (a shared die, open source, one demo board) with a full-chip shuttle (the whole die, any tools, many copies of your chip).

## How Tiny Tapeout works

- **Shared die.** Hundreds of small projects are combined into one chip. Each project gets one or more **tiles**, and an on-chip multiplexer connects the selected project to the pins. That is why it is cheap: everyone shares one mask set.
- **Everyone gets everything.** Every chip carries every project from that shuttle, so all designs must be open source.
- **One tile** is about 0.1 mm tall and holds roughly 1,000 standard cells. Larger designs buy more tiles (up to 16).
- **Pins per project:** `clk`, `rst_n` (active low), 8 inputs `ui_in`, 8 outputs `uo_out`, 8 bidirectional `uio_*` with an output-enable `uio_oe`. Expect I/O up to about 50 MHz; see the [specs](https://tinytapeout.com/specs/) for the current figure.
- **Demo board:** DIP switches on the inputs, a seven-segment display on the outputs, PMOD headers, and a Raspberry Pi RP2040 running MicroPython that selects the project and can drive tests from a PC.
- **Ways to design:** Wokwi (gates in a browser, for beginners), Verilog or another HDL (what this project uses), and analogue (out of scope here).

## The Verilog route, step by step

1. Create a repository from the template ("Use this template"). It must be **public**.
2. In the repository settings, set **Pages → Build and deployment → Source** to **GitHub Actions**, otherwise the results page cannot be published.
3. Put the RTL in `src/`. The top module must be named `tt_um_<github user>_<name>` and have **exactly** the template's ports; names cannot change and nothing can be added or removed.
4. Fill in `info.yaml`: title, author, description, `clock_hz`, `tiles`, `top_module`, every file in `source_files` (a missing file breaks the build), and the pin descriptions (they become the datasheet).
5. Write `docs/info.md`: how the design works and how to test it. Every chip owner receives it, and so does your future self.
6. Adapt the cocotb test in `test/` (`test.py`, `tb.v`, `Makefile`), then push. The actions run.
7. When the `gds` and `docs` badges are green (and `test` too; strongly recommended), submit at [app.tinytapeout.com](https://app.tinytapeout.com/): sign in with GitHub, paste the repository URL, pay or apply a coupon, then **submit a revision**. Only a submitted revision is on the shuttle; later changes need a new revision before the deadline.

**Do not do step 7 for this project without Prof. Popovici's approval.** Submitting reserves a paid tile.

### The actions in the current IHP template

| Workflow | What it does |
|---|---|
| `test` | RTL simulation of the cocotb test (Icarus); fails if any test fails |
| `gds` | Hardens the design with LibreLane, runs the Tiny Tapeout **precheck**, a **gate-level test** of the synthesised netlist, and publishes the 2D/3D **viewer** |
| `docs` | Builds the datasheet page from `info.yaml` and `docs/info.md` |
| `fpga` | Builds a bitstream for an iCE40UP5K FPGA board, to try the design before silicon (manual run only) |

The `gds` result page shows warnings, utilisation and the standard cells used. In the 3D viewer, keys 1, 2 and 3 hide filler cells, hide wiring, and isolate the selected cell.

### When `gds` fails

- First read the synthesis log in the `gds` logs artifact; a design error usually shows up there.
- If the design is too big, placement or routing fails. Shrink the design or increase `tiles`.
- Placement error `GPL-0302`: raise `PL_TARGET_DENSITY_PCT` in `src/config.json` (the template says values up to 80 have worked).
- Setup violations: raise `CLOCK_PERIOD`. Hold violations: raise the hold slack margins. Both are in `src/config.json`.

## Design rules the videos stress

As a verification engineer you know most of these. The new part is why they matter on silicon.

- **Unknown start-up state.** Flip-flops power up in a random state on a real chip (an FPGA initialises them). Every register that matters needs a reset from `rst_n`, which is **active low**.
- **Asynchronous inputs.** `ui_in` comes from switches or another board, not from your clock. Pass it through a two-flop synchroniser (and debounce buttons) to avoid metastability.
- **Multiple drivers and floating inputs** are errors (Wokwi's ERC, Verilator lint in the HDL flow). Assign every output, including `uio_out` and `uio_oe`, to 0 if unused.
- **Propagation delay.** Long logic paths limit the clock; this is what setup slack in the timing report measures.
- **Prefer synchronous counters and dividers** to ripple counters, which glitch.
- **Clock-domain crossings** need care if a design uses more than one clock.
- **Test before you submit,** including a gate-level simulation: once a chip is made, nothing can be changed.

## What has changed since the videos

| In the videos | Now |
|---|---|
| Fabrication through Efabless on SKY130; tickets bought from the Efabless store | Efabless closed in 2025. Shuttles now run on IHP SG13G2, GF180 and SKY130 (see [tinytapeout.com/chips](https://tinytapeout.com/chips/)); payment is in the submission app |
| About $100 per project, $50 per extra tile | Check the current prices on the website; class bundles are on [tinytapeout.com/teaching](https://tinytapeout.com/teaching/) |
| Flow settings in `config.tcl` (OpenLane 1) | `src/config.json`, read by **LibreLane**, the same tool this repository's `make harden` runs |
| Tile about 160 × 100 µm | About 167 × 108 µm on IHP; tile options `1x1` up to `8x2` |
| Three actions: docs, test, gds | Four workflows; `gds` now includes precheck, gate-level test and viewer |

The template's actions are pinned to a shuttle tag (`ttihp26b` in the current template). Check that the tag matches the shuttle you aim for before relying on it.

## What this means for our flow

1. **Same core tool.** The Tiny Tapeout `gds` action runs LibreLane, like `make harden` here. The differences are Tiny Tapeout's fixed die (the tile), fixed pin positions and power grid, and some checks it turns off to save time (KLayout DRC and XOR). It then adds its own precheck. Running one design both ways and comparing the results is a natural "two flows" comparison.
2. **Gate-level simulation is missing from our flow.** Tiny Tapeout runs it in CI; we should add a `make gl-sim` target that re-runs the testbench on `final/nl/` (and later with SDF timing).
3. **cocotb.** Tiny Tapeout tests are cocotb (`cocotb==2.0.1` in the template). Our flow should accept a design's `test/` folder as it stands.
4. **Putting the counter on the template** (planned for week 42) needs these changes:
   - a wrapper `tt_um_mdkamrulislam_counter` with the fixed ports;
   - reset from `rst_n`, inverted (our counter's `rst` is active high);
   - `en` from `ui_in[0]`, `count` on `uo_out`, `wrap` on `uio_out[0]` with `uio_oe = 8'b0000_0001`, all other outputs tied to 0;
   - `info.yaml` (`top_module`, `source_files`, `clock_hz: 50000000`, pin names), `docs/info.md`, and `PROJECT_SOURCES` in `test/Makefile`;
   - our self-checking testbench ported to `test/test.py`;
   - GitHub Pages set to GitHub Actions.
