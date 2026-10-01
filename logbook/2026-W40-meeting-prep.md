# Week 40 meeting preparation (Friday 2 Oct 2026, 11:00)

Task for this week: go through the Tiny Tapeout videos. Notes on them are in [docs/tiny-tapeout.md](../docs/tiny-tapeout.md); the log to email before the meeting is [2026-W40.md](2026-W40.md).

## Before the meeting

- [ ] Watch the four short videos in full and the webinar's 26:00–52:00 (see the viewing table in `docs/tiny-tapeout.md`).
- [ ] Build the four-flip-flop shift register from the webinar (about 15:00–20:00) in the Wokwi template, save it, and take a screenshot to show.
- [ ] Open the [IHP Verilog template](https://github.com/TinyTapeout/ttihp-verilog-template) and read `info.yaml`, `src/project.v` and `test/test.py`.
- [ ] Check and correct `2026-W40.md`, then email it.
- [ ] Bring: the Wokwi screenshot, the counter layout (`docs/counter-sky130A.png`) and the sign-off table.

## One-minute summary to open with

> I went through the Tiny Tapeout videos. Tiny Tapeout puts hundreds of small designs on one shared chip, so a tile is cheap. You design in Wokwi or Verilog in a GitHub template, and GitHub Actions build the layout with LibreLane, which is the same tool my repository already runs. My counter is already sign-off clean on SKY130 and IHP locally. The videos are from 2023–24: Efabless has since closed and the shuttles now run on IHP, GF180 and SKY130, so I checked everything against the current IHP template. I also built a small shift register in Wokwi. Next I would like to put my counter on the IHP template, without submitting. I have five questions to agree the scope.

## Questions he may ask

| Question | Answer |
|---|---|
| What is Tiny Tapeout, and why is it cheap? | Many small designs share one die through an on-chip multiplexer, so the mask and fabrication cost is split. Open tools mean no licences. |
| What are the ways to design? | Wokwi (drawing gates; beginners), Verilog or another HDL (what I will use), and analogue (out of scope). All end in a GitHub repository whose actions build the GDS. |
| Which suits next year's students? | Wokwi for a first lab (nothing to install), then the Verilog template for their projects. Tiny Tapeout sells class bundles. |
| What are the limits? | About 1,000 gates per tile (up to 16 tiles), 8 inputs, 8 outputs, 8 bidirectional pins, about 50 MHz. Designs must be open source. Chips take 6 to 12 months to come back. |
| How does it relate to the flow you built? | Same core tool, LibreLane. My repository runs it locally with any die size and PDK; Tiny Tapeout runs it in GitHub with fixed tile settings, a precheck and a gate-level test. Comparing the two could be the "two open flows". Is that what you meant? |
| What was new to you? | Fill cells take up most of the tile; Tiny Tapeout runs a precheck and a gate-level test on every push; why every register needs a reset on silicon; the fixed top-module interface. |
| What next? | The two remaining videos (*Making ASICs*, *Manufacturing ASICs*), the FAQ and SiliWiz; run the flow on my laptop; then the counter on the IHP template in week 42, without submitting. |

## Questions to ask him

The five scope questions are at the end of [2026-W40.md](2026-W40.md), plus the website link he mentioned.

## Notes from the meeting

*(Write his answers and any new tasks here straight after the meeting, then update `AGENTS.md` sections 5, 9 and 10.)*

-
