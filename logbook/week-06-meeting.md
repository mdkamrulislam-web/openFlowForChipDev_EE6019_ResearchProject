# Supervisor meeting, 6 November 2026

Held at 11:00. Only this project's part is recorded; small talk is left out. The source is five automatic transcripts and two recordings (private Drive folder "6. 6th November 2026"). Version 1 is the clearest and labels the speakers. The transcripts are garbled in places ("risk" = RISC-V, "fuzzy RV" = FazyRV), so quotations are approximate.

## What Kamrul reported

- The [characterisation](../docs/research/tt-riscv-characterisation.md) of the RISC-V designs on Tiny Tapeout ([week 6 log](week-06.md)).
- A 32-bit-per-cycle core fills all 16 tiles, the largest Tiny Tapeout size, which leaves no room for anything else.
- FazyRV is scalable, but Tiny Tapeout only has the 2-bit version. Its paper has FPGA data for every width. Proposal: run the 4- and 8-bit versions through the Tiny Tapeout flow and compare gate equivalents, then add clock gating to reduce power.

## What Prof. Popovici said

- **Cost:** 16 tiles at about €70 each is about €1,000: "That should be okay."
- **On the FazyRV widths:** "Yeah, so they have tried." He did not take up the width study as the research.
- **Clock gating:** "usually works for very large chips. I'm not sure how clock gating would work on a RISC[-V] … a bit of a tricky challenge."
- **Two ideas instead:**
  1. Take a 4-bit or 8-bit RISC-V and change it to be very low power, "maybe having some special registers or things like this".
  2. "How can we build a RISC[-V] device that, regardless of what operation it is doing, the power is constant." This means power that does not depend on the instruction or data (a defence against power-analysis attacks), not power that is the same for every width.
- **The direction:** "Take one architecture, just one, and concentrate on very low power. Any techniques that you can read on lowering power for a microprocessor, and just apply it. And then implement it … through the flow."
- **The FPGA:** using the 4- or 8-bit core on the FPGA for the lab project is fine ("Of course"). Constant power cannot be shown on an FPGA, because its architecture is fixed; the FPGA only checks that the RISC-V works (an emulation).
- **Fabrication:** asked whether the chip would be made through Tiny Tapeout: "Probably, yeah."
- **Size:** "Pick the processor first … a 4-bit processor or an 8-bit processor, and work on that. Don't worry for the moment … at all on the tiles." Then "8 usually. 8 or 16 should be fine". This probably means tiles (the question was about tiles), but it could mean bits; to confirm.
- **Project laptop:** delayed; he will follow it up so that it arrives next week. An external drive would do in the meantime.

## What this changes

- The research is now **one small RISC-V (4- or 8-bit datapath), made low power, taken through the Tiny Tapeout flow**, probably to a real chip. FazyRV at 4 or 8 bits fits this.
- The width sweep is no longer the research question. At most it is a quick baseline.
- Clock gating is not to be the main idea. Read the low-power microprocessor literature first; constant power is the second option.
- The FPGA is a functional check, and may also serve as the EE6043 lab project.

## Not covered

- Whether the 23 October accelerator idea is dropped.
- A new time for the 13 November meeting (postponed for his Dublin trip, which he mentioned cancelling).
- The interim report.

## Actions

- [ ] Find one survey paper on low-power microprocessor design and one on power-analysis countermeasures (constant power); choose the direction.
- [ ] Choose the core and width (FazyRV, 4 or 8 bits).
- [ ] Run it on the PYNQ-Z2 (functional check; LUTs, flip-flops, Fmax).
- [ ] Run the plain core through the Tiny Tapeout flow as the baseline: area, tiles and the flow's power estimate.
- [ ] Email to confirm: "8 or 16" (tiles or bits), the accelerator, and the 13 November meeting.
