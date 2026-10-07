# Week 1 meeting preparation (Friday 2 Oct 2026, 11:00)

Task for this week: go through the Tiny Tapeout videos. Notes on them are in [docs/tiny-tapeout.md](../docs/tiny-tapeout.md); the log to email before the meeting is [week-01.md](week-01.md).

## Before the meeting

- [ ] Watch the four short videos in full and the webinar's 26:00–52:00 (see the viewing table in `docs/tiny-tapeout.md`).
- [ ] Build the four-flip-flop shift register from the webinar (about 15:00–20:00) in the Wokwi template, save it, and take a screenshot to show.
- [ ] Open the [IHP Verilog template](https://github.com/TinyTapeout/ttihp-verilog-template) and read `info.yaml`, `src/project.v` and `test/test.py`.
- [ ] Check and correct `week-01.md`, then email it.
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
| What next? | The two remaining videos (*Making ASICs*, *Manufacturing ASICs*), the FAQ and SiliWiz; run the flow on my laptop; then the counter on the IHP template in week 3, without submitting. |

## Questions to ask him

The scope questions and the website link are at the end of [week-01.md](week-01.md). Start with question 1: whether I should build a flow like Tiny Tapeout's or use it as it is. Tiny Tapeout is mainly a service (shared die, GitHub template, route to the fab) that runs LibreLane, the same tool as `make harden`; my reading is that the project adds the survey, a local flow students can see and debug, the guide, and the demonstrator, with Tiny Tapeout as the last step. His answer may also settle question 2 (which two open flows).

## Notes from the meeting

From the meeting transcripts (2 Oct 2026) and his answers to the follow-up email.

- **Build a flow like Tiny Tapeout's?** No. Use the Tiny Tapeout flow to design. He wants to run that flow with undergraduate students next year, so document it step by step for a Verilog design: write the code, simulate and test it, build the GDS, up to the point of submission.
- **Task for next week:** document the flow as PowerPoint slides. Any format and length.
- **Research part:** a larger template with a RISC-V core ("carousel" as heard; possibly Caravel or Croc, asked by email), used to explore neural-network accelerators, taken through the full flow to a layout ready for submission.
- **Technology:** whichever is available at that point, SkyWater 130 nm or IHP 130 nm.
- **Tile size:** he asked what fits in one tile (about 1,000 cells, 8 inputs, 8 outputs, 8 bidirectional pins, clock and reset); "not bad, I was thinking it will be much worse".
- **Next year:** he plans a batch of student chips; students who go through the flow now may become demonstrators.
- **Website link** from 25 Sep: it was Tiny Tapeout.
- **Report and presentation dates:** to be given later.
- **Still open:** which RISC-V template he meant, and whether there is a type of neural network or paper to start from (email sent 2 Oct).
