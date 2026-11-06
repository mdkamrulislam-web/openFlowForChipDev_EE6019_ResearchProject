# Week 6 meeting preparation (Friday 6 November 2026, 11:00)

Main item: [RISC-V designs on Tiny Tapeout: characterisation and gap](../docs/research/tt-riscv-characterisation.md), the task set on [30 October](week-05-meeting.md).

## Before the meeting

- [ ] Read the characterisation once. Know the five gaps, and the three numbers below.
- [ ] Have the page open on the laptop (GitHub renders the tables).
- [ ] Note the FPGA board's part number, if you have it.

## One-minute summary to open with

> I went through every Tiny Tapeout shuttle since TT02 using the official index. About 65 RISC-V projects have been taped out; many reuse the same few cores, such as TinyQV, KianV and SERV. For each one I took the real flow results: area in gate equivalents, tiles, flip-flops, the flow's frequency estimate and its power estimate. Size depends mainly on how many bits the core handles per clock. SERV at 1 bit is 5.6 thousand gate equivalents on one-by-two tiles; TinyQV at 4 bits is 17.6 thousand on three-by-two; PicoRV32 at 32 bits is 37 thousand on eight-by-two. Every one that can run real programs fetches its code from an external SPI flash chip. The gaps: none publishes benchmark results or CPI; none has any low-power feature; FazyRV was only taped out at 2 bits, so the 4-bit area you asked about is unknown; almost none shows compliance tests. My suggestion: run FazyRV through the Tiny Tapeout flow at 1, 2, 4 and 8 bits on the FPGA and in the ASIC flow, add benchmarks, and use that as the baseline for a low-power version.

## Three numbers to remember

| | kGE | Tiles (SKY130) | Fmax est. (typical) |
|---|---|---|---|
| SERV, 1 bit per clock | 5.6 | 1×2 | 110 MHz |
| TinyQV, 4 bits per clock | 17.6 | 3×2 | 80 MHz |
| PicoRV32, 32 bits | 37.0 | 8×2 | 59 MHz |

A gate equivalent (GE) is the cell area divided by the area of one two-input NAND gate.

## Questions he may ask

| Question | Short answer |
|---|---|
| Where do the numbers come from? | The stored results of the real Tiny Tapeout layout runs (each shuttle repository keeps `metrics.csv` and the synthesis report), not the authors' claims. |
| Are the frequencies measured? | No. They are layout-tool estimates at the typical corner. The slow corner is about half. Silicon results are not in the records. |
| Why is the register file so big? | 32 registers × 32 bits = 1,024 flip-flops. Flip-flops take 30–57% of the area, so most designs use RV32E (16 registers) or a latch-based register file. |
| Papers? | FazyRV (ACM CF '24), Wildcat (arXiv 2025), and the Tiny Tapeout paper (IEEE SSC Magazine 2024). SERV, TinyQV, KianV and PicoRV32 have no peer-reviewed paper. A 2026 paper, SAILOR, builds on FazyRV. Read it before claiming the width study is new. |

## Questions to ask him

1. **Which gap should I take forward:** the width sweep, low power, or memory and speed? (Recommendation: the width sweep first, as the baseline for low power.)
2. **Accelerator:** on 23 October the plan was an accelerator chip; on 30 October, a RISC-V through the full ASIC flow. Is the accelerator dropped, or later?
3. **Core:** FazyRV (scalable, compliance-tested, published, MIT licence) or another core?
4. **The 13 November meeting** is postponed for the Dublin trip. What new time suits?
5. **Interim report:** due 15 January 2027. Should it include this characterisation as the literature-survey part?
