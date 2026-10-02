# Week 1 (28 Sep to 2 Oct 2026)

## Done
- Agreed the project direction at the 25 Sep group meeting: survey the free alternatives to Cadence and Synopsys, set up an open flow, and build an ASIC with it as the first design through the flow.
- Went through five of the Tiny Tapeout videos (from transcripts): *From idea to chip design in minutes*, *Getting started with Wokwi*, *Working with an HDL*, *Getting your design ready to submit*, and the *Build your first chip* webinar. Checked them against the current IHP Verilog template and wrote notes: `docs/tiny-tapeout.md`.
- Main things learned:
  - Tiny Tapeout shares one die between hundreds of projects; one tile (about 167 × 108 µm on IHP) holds roughly 1,000 cells, with 8 inputs, 8 outputs, 8 bidirectional pins, clock and active-low reset.
  - Its GitHub `gds` action runs LibreLane, an open-source RTL-to-GDS flow, with a fixed tile, pins and power grid, plus a precheck and a gate-level test.
  - The videos are from 2023–24: Efabless has since closed, shuttles now run on IHP, GF180 and SKY130, and flow settings moved from `config.tcl` to `src/config.json`.

## Problems and how I fixed them
- None this week.

## Evidence
- Notes on the videos and the current IHP template: `docs/tiny-tapeout.md`.

## Next week
- Install the open-source tools on my laptop and note how the install goes.
- Tiny Tapeout: the two remaining videos (*Making ASICs*, *Manufacturing ASICs*), the FAQ, SiliWiz, and a small Wokwi design.
- Plan putting a small design on the IHP Verilog template (week 3), without submitting.
- Draft the risk assessment.

## Questions for Prof. Popovici
1. Tiny Tapeout already provides a complete flow: a GitHub template whose Actions run LibreLane and build the GDS. Am I meant to build a similar flow, or to use Tiny Tapeout as it is? My understanding is that my work is the survey of open tools against Cadence and Synopsys, a local flow that students can run and debug stage by stage, a student guide, and a demonstrator chip submitted through Tiny Tapeout. Is that right, and is the documented, reusable flow the main deliverable, with my chip as the first worked example?
2. Which two "open flows" did you mean: LibreLane and OpenROAD-flow-scripts, or the Tiny Tapeout GitHub flow and local LibreLane?
3. Is a real Tiny Tapeout submission expected, and is there budget for a tile on the IHP shuttle (TTIHP27a, March 2027)?
4. Which PDK do you prefer? I propose IHP SG13G2 as the target and SKY130 for bring-up.
5. What are the dates for the interim report, final report and presentation?
6. Could you send the website link you mentioned?
