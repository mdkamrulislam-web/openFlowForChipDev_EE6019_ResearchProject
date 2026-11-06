# Week 6 (2 to 6 November 2026)

*Task from the [30 October meeting](week-05-meeting.md): characterise the RISC-V designs on Tiny Tapeout (size, tiles, bits per clock, frequency, parameters, papers), answer "how much is the area for the 4-bit FazyRV?", and identify the gap.*

## Tasks Done

- **Characterised every RISC-V taped out on Tiny Tapeout** ([characterisation](../docs/research/tt-riscv-characterisation.md), [data](../docs/research/data/tt-riscv-metrics.csv)). I used the official Tiny Tapeout index (29 shuttles, TT02 to 2026, SKY130, IHP and GF180): 102 entries from 65 differently named projects. For each one I took the stored results of the real Tiny Tapeout layout run, not the authors' claims: area in gate equivalents (GE), tiles, flip-flops, the flow's frequency estimate and its power estimate. The scripts are in [tools/tt-riscv-survey](../tools/tt-riscv-survey/), so the table can be rebuilt.
- **Main result:** size is set mostly by how many bits the core handles per clock, and by the register file.

  | Core | Bits per clock | Area (kGE) | Tiles (SKY130) | Fmax estimate, typical (slow) corner |
  |---|---|---|---|---|
  | SERV | 1 | 5.6 | 1×2 | 110 (69) MHz |
  | FazyRV-ExoTiny | 2 | 15.0 | 2×2 | not stored (TT06) |
  | TinyQV | 4 | 17.6 | 3×2 | 80 (60) MHz |
  | PicoRV32 (Trinity College Dublin) | 32 | 37.0 | 8×2 | 59 (48) MHz |
  | KianV uLinux SoC | 32 | 43.0 | 8×2 | 51 (26) MHz |

  The largest cores already fill 8×2, the largest SKY130 size, so they leave no room for an addition. Every 32-bit core that runs real programs fetches its code from an external SPI or QSPI chip, so speed is limited by memory as well as by the core.
- **Answered the FazyRV 4-bit question** from the FazyRV paper (Kissich and Baunach, ACM CF '24). The paper measures FPGAs only:
  - iCE40: the 4-bit version uses 593 logic cells, against 515 for 1-bit, 506 for SERV and 1,569 for PicoRV32.
  - Xilinx 7-Series (same family as my board): 87 slices for 4-bit, against 77 for 1-bit; PicoRV32 about 236.
  - In their demo at 20 MHz, 4-bit is about 3.4 times faster than 1-bit for about 15% more area.
  - **No ASIC area and no power are reported for any width**, and Tiny Tapeout has only taped out the 2-bit version. The 4-bit area in the Tiny Tapeout flow is therefore still unknown.
- **Checked FazyRV for low-power features.** The paper names clock gating only as an idea to speed up shift instructions. The current source code (3 November 2026) has no clock gating, sleep or WFI.
- **Received the FPGA board:** TUL PYNQ-Z2 (Zynq-7020, about 53,000 LUTs). Every core above fits easily.

## Gaps found

Checked against all 102 Tiny Tapeout datasheets:

1. **No performance data:** no CoreMark, Dhrystone, Embench or measured CPI on any Tiny Tapeout RISC-V.
2. **No low-power design:** no clock gating, sleep, WFI or power-down. The only power numbers are flow estimates.
3. **No area-versus-width study in the ASIC flow:** FazyRV supports 1, 2, 4 and 8 bits, but only 2-bit was taped out; its paper reports FPGA results only.
4. **Almost no compliance evidence:** one datasheet in 102 mentions compliance tests.
5. **On-chip memory is rare:** SRAM macros appear only on IHP designs.

## Problems and how I fixed them

- **A name search also found ALUs, hazard units and peripherals.** I checked each match and removed those that are not processors (114 matches down to 102).
- **Shuttles store their statistics in two formats** (OpenLane 1 before 2025, OpenLane 2 after), and TT02 to TT05 store none. The script reads both formats; the older entries are listed without numbers.
- **The frequencies are layout-tool estimates, not measurements.** I report both the typical and slow corners and label them as estimates.
- **Gate equivalents need the NAND2 area of each process.** I used 3.75 µm² (SKY130) and 7.26 µm² (IHP); the GF180 value is not yet verified, so GF180 entries have no GE.
- **My first count ("about 45 cores") was wrong.** Recounted from the data: 102 entries from 65 projects.
- **Some first-draft statements were stronger than the sources** (for example a core's ISA and pipeline depth). I checked each against its datasheet or paper and corrected them.

## Evidence

- [PR #14](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/pull/14): characterisation, data, scripts and the 30 October meeting record.
- FazyRV paper: doi:10.1145/3649153.3649195 (Tables 3, 4 and 5).

## Next Week

- Agree which gap to take forward (proposal below).
- Set up Vivado for the PYNQ-Z2 and run FazyRV on it: record LUTs, flip-flops and Fmax, and compare with the paper's 7-Series figures.
- Run FazyRV through the Tiny Tapeout flow at 1, 2, 4 and 8 bits (GitHub Actions) and record area, tiles, Fmax and power for each.
- Read SAILOR (2026, builds on FazyRV), Wildcat and the Tiny Tapeout paper; check the HeiChips 2025 and GF180 "Hachure" FazyRV chips for published results.

**Proposal:** use FazyRV as the core. First measure it at all four widths in the Tiny Tapeout flow (area, tiles, power) and on the FPGA (with benchmarks). Then use that as the baseline for a low-power version with clock gating and a sleep state.

## Questions for Prof. Popovici

1. Which gap should I take forward: the width study, low power, or memory and speed?
2. Is the 23 October accelerator idea dropped, or postponed?
3. Is the plan to fabricate through Tiny Tapeout, or elsewhere? A Tiny Tapeout GDS is one tile block inside their chip, not a complete chip.
4. What size should I aim for (for example, at most about 6 to 8 tiles, to leave room for my addition)?
5. The 13 November meeting is postponed. What new time suits?
