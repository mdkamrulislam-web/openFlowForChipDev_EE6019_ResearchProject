# Tiny Tapeout: how it works, and what it means for this flow

Earlier video notes, plus website-based notes added on 7 October 2026. Current details were checked against the official [templates](https://tinytapeout.com/hdl/templates/), [SKY130 template](https://github.com/TinyTapeout/ttsky-verilog-template) and [IHP template](https://github.com/TinyTapeout/ttihp-verilog-template). The earlier videos date from Tiny Tapeout 4 to 6 (2023–24); changes are listed in [What has changed since the videos](#what-has-changed-since-the-videos). The two remaining videos have not been watched or transcribed for these notes.

## The videos, and how to watch them

| Video | Length | Main point | How to watch |
|---|---|---|---|
| [From idea to chip design in minutes](https://www.youtube.com/watch?v=qVWq_XZko-M) | 3 min | What Tiny Tapeout is and why it is cheap | In full |
| [Getting started with Wokwi](https://www.youtube.com/watch?v=F1SwXF2ny4g) | 3 min | Drawing and simulating gates in the browser | In full |
| [Working with an HDL](https://www.youtube.com/watch?v=KbWb6xd9jFE) | 3 min | Verilog projects: `info.yaml`, the fixed top module, cocotb tests | In full |
| [Getting your design ready to submit](https://www.youtube.com/watch?v=fCGPKdmM3Dc) | 6 min | The GitHub template, its actions, and submitting | In full |
| [Webinar: Build your first chip with Tiny Tapeout](https://www.youtube.com/watch?v=UVZK-kmN7wc) | 57 min | All of the above, plus design tips | 26:00–52:00 closely (GitHub, submission, Verilog, design tips); skim 6:00–25:00 (logic-gate basics in Wokwi) |

Still to watch from the study path: [Making ASICs](https://www.youtube.com/watch?v=dckPKyO2nSo) and [Manufacturing ASICs](https://www.youtube.com/watch?v=aBDJQ9NYTEU). These are the most relevant to physical design. Their transcripts have not been supplied; the website notes below do not count as watching them.

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

### Website notes for the two remaining videos

**Making ASICs — website-based notes, checked 7 October 2026.** The [official page](https://tinytapeout.com/making_asics/) describes converting a Verilog netlist to GDS, the layout files used for manufacture, and running the tools on GitHub's servers. It introduces the flow logs as evidence to inspect. The page still names OpenLane; the current template actions use LibreLane. For the slides, explain synthesis and physical design, then show where the template publishes logs and layout results. This is a teaching outline from the website and template, not a summary of an unseen video.

**Manufacturing ASICs — website-based notes, checked 7 October 2026.** The [same page](https://tinytapeout.com/making_asics/) links a factory tour showing the move from GDS to a physical chip, but does not provide a transcript. The [FAQ](https://tinytapeout.com/faq/#when-will-the-chips-get-manufactured) gives a general 6–9-month manufacturing estimate, with board assembly, testing and fulfilment afterwards; delivery can take up to a year. Use the [chips page](https://tinytapeout.com/chips/) for the chosen shuttle's estimate. The [devkit FAQ](https://tinytapeout.com/faq/#what-is-a-devkit) distinguishes the ASIC breakout board from the demo board. Detailed factory steps remain for the video review.

**Avoid carrying old specifications into the slides.** The FAQ's tile/gate figures are under “Chip Specs for TT04 to TT10”, so they are a historical guide. Current SKY130 and IHP template `info.yaml` files describe a tile as about **167 × 108 µm** and list the available tile sizes. A gate estimate does not guarantee that a design will route. Sources: [SKY130 metadata](https://github.com/TinyTapeout/ttsky-verilog-template/blob/main/info.yaml), [IHP metadata](https://github.com/TinyTapeout/ttihp-verilog-template/blob/main/info.yaml).

## How Tiny Tapeout works

- **Shared die.** Hundreds of small projects are combined into one chip. Each project gets one or more **tiles**, and an on-chip multiplexer connects the selected project to the pins. That is why it is cheap: everyone shares one mask set.
- **Everyone gets everything.** Every chip carries every project from that shuttle, so all designs must be open source.
- **One tile:** the current SKY130 and IHP templates describe about 167 × 108 µm. The older FAQ's roughly 1,000 logic gates is only a guide; cell mix and routing decide what fits. Larger designs can use the tile sizes allowed by their template.
- **Fixed interface:** `clk`, `rst_n` (active low), `ena`, 8 inputs `ui_in`, 8 outputs `uo_out`, and 8 bidirectional `uio_*` with output-enable `uio_oe`. Copy the template's complete port declaration.
- **Timing limits differ.** The [GPIO specs](https://tinytapeout.com/specs/gpio/) give SKY130 pad ratings of 66 MHz input and 33 MHz output. The [clock page](https://tinytapeout.com/specs/clock/) bases its roughly 66 MHz clock estimate on SKY130 pads. These are separate from the design's internal timing limit and do not establish IHP or GF180 limits.
- **Demo board:** switches, displays and connectors expose the project signals; an onboard microcontroller selects the project and can drive tests from a PC. Hardware differs by board generation: follow the [quickstart for the current ETR board](https://tinytapeout.com/guides/get-started-demoboard-etr/) or the guide for the board supplied with the shuttle.
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

The templates' actions are pinned to shuttle tags: `ttsky26d` for SKY130 and `ttihp26b` for IHP, checked 7 October 2026 ([SKY130 workflow](https://github.com/TinyTapeout/ttsky-verilog-template/blob/main/.github/workflows/gds.yaml), [IHP workflow](https://github.com/TinyTapeout/ttihp-verilog-template/blob/main/.github/workflows/gds.yaml)). Check the tag and PDK again before choosing a shuttle.

**LibreLane versions differ by action tag.** The current [SKY130 action](https://github.com/TinyTapeout/tt-gds-action/blob/ttsky26d/action.yml) defaults to **3.0.14**; the [IHP action](https://github.com/TinyTapeout/tt-gds-action/blob/ttihp26b/action.yml) defaults to **3.0.5**. Earlier notes saying 3.0.3 are stale. Both actions fetch `tt-support-tools` from `main` by default, so keep the actual run logs and revisions with the example; a shuttle tag alone does not freeze every dependency.

### Who makes the chips now

Since Efabless closed, each Tiny Tapeout shuttle goes to one of three fabs through a different multi-project wafer (MPW) service. The run codes come from [tinytapeout.com/chips](https://tinytapeout.com/chips/) (read 1 Oct 2026); the nodes come from the PDKs.

| Shuttle prefix | Fab | Process node (open PDK) | MPW service | Run code on the chips page |
|---|---|---|---|---|
| TTIHP | IHP, Frankfurt (Oder), Germany | 130 nm SiGe BiCMOS (`ihp-sg13g2`) | IHP's own open-source MPW | `IHP-2609`, `IHP-2603`, … |
| TTSKY | SkyWater Technology, USA | 130 nm CMOS (`sky130A`) | ChipFoundry chipIgnite | `CI-2612`, `CI-2609`, … |
| TTGF | GlobalFoundries | 180 nm CMOS (`gf180mcuD`) | wafer.space | `w.s Run #3` |

All three are mature nodes: cheap, with open PDKs, and far from the advanced nodes that commercial Cadence and Synopsys flows usually target. IHP SG13G2 also has fast SiGe bipolar transistors (HBTs) for RF and high-speed analogue; a digital Tiny Tapeout design uses only its CMOS standard cells.

## What this means for the project

The supervisor confirmed on 2 October that the teaching task uses and documents Tiny Tapeout's existing flow. The repo's separate LibreLane counter flow is background material; building another flow or adding targets to it is not a teaching deliverable.

1. **Teach the template's flow.** Follow its RTL tests, LibreLane hardening, precheck, gate-level test, viewer and documentation. Explain the tile and fixed interface as physical constraints.
2. **Use gate-level simulation already provided.** Adapt the counter's cocotb test so the template can exercise both RTL and its generated netlist. Keep an explicit gate-level pass as evidence; a layout picture alone is not verification.
3. **Keep versions with the example.** Use the selected template's own requirements and workflow tags. Any local comparison with this repo's LibreLane flow is optional background work.
4. **Putting the counter on the template — completed in week 2:** the genuine [SKY130 counter example](https://github.com/mdkamrulislam-web/tt-sky130-counter/pull/1) passes RTL, docs, GDS, precheck and gate-level tests at commit `61ef06b` ([GDS run](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100748)). It uses 4.96% of one tile and 47 synthesis cells; [the viewer](https://mdkamrulislam-web.github.io/tt-sky130-counter/) is live. The PR awaits review/merge; no shuttle submission was made. The earlier counter GDS was from this repo's separate flow. The template changes were:
   - a wrapper `tt_um_mdkamrulislam_counter` with the fixed ports;
   - reset from `rst_n`, inverted (our counter's `rst` is active high);
   - `en` from `ui_in[0]`, `count` on `uo_out`, `wrap` on `uio_out[0]` with `uio_oe = 8'b0000_0001`, all other outputs tied to 0;
   - `info.yaml` (`top_module`, `source_files`, `clock_hz: 50000000`, pin names), `docs/info.md`, and `PROJECT_SOURCES` in `test/Makefile`;
   - our self-checking testbench ported to `test/test.py`;
   - GitHub Pages set to GitHub Actions.

The counter example assumes `ui_in[0]` is synchronous to `clk`. A real switch or button is asynchronous: synchronise it, and debounce it if its mechanical transitions matter, before using it as the enable.
