# RISC-V designs on Tiny Tapeout: characterisation and gap

*Prepared 5 November 2026 for the 6 November meeting. This answers the task set on 30 October ([meeting record](../../logbook/week-05-meeting.md)): characterise every RISC-V on Tiny Tapeout (size, tiles, bits, frequency, parameters, papers) and find what is missing.*

## How the numbers were collected

- **List of designs:** the official [Tiny Tapeout index](https://github.com/TinyTapeout/tinytapeout-index) holds every project taped out since TT02 (29 shuttles on SKY130, IHP SG13G2 and GF180). A text search for RISC-V names gave 114 entries; after removing ALUs, hazard units and peripherals, 102 entries remain from 65 differently named projects. Many were taped out more than once, and many share a core (TinyQV, KianV, SERV).
- **Measured flow results:** every shuttle repository keeps each project's `stats/metrics.csv` and `stats/synthesis-stats.txt`, which come from the real Tiny Tapeout hardening run. They give cell count, cell area, flip-flops, die area, utilisation, estimated power and timing slack. The project's own `src/config.json` gives the clock period the flow used.
- **Description:** each project's datasheet (`docs/info.md`) gives the ISA, datapath and memory.
- **All rows:** [data/tt-riscv-metrics.csv](data/tt-riscv-metrics.csv). Scripts: [tools/tt-riscv-survey/](../../tools/tt-riscv-survey/README.md).

### What the columns mean

- **Tiles:** Tiny Tapeout sells area in tiles. One SKY130 tile is about 0.018 mm² of die (about 161 × 111 µm); one IHP tile is about 0.031 mm². The largest SKY130 slot is 8×4 tiles (0.70 mm²).
- **Gate equivalents (kGE):** the synthesised standard-cell area divided by the area of the smallest two-input NAND gate (SKY130 `nand2_1` = 3.75 µm²; IHP `sg13g2_nand2_1` = 7.26 µm²). It lets designs on different processes be compared. Check: the same SERV design gives 5.6 kGE on both SKY130 and IHP, and TinyQV gives 17.6 and 18.5 kGE.
- **kGE includes the whole Tiny Tapeout project**: the CPU plus its SPI/QSPI memory controller, UART and other peripherals. It is not the bare core.
- **Fmax (estimate):** 1 / (flow clock period − setup slack), at the typical corner (SKY130: 25 °C, 1.8 V; slow corner in brackets where reported). This comes from the layout tool, not from measured silicon. Tiny Tapeout's own clocking also limits the usable clock (most designs ask for 20–64 MHz). TT06/TT07 used the older flow, which stores no usable slack, so these show "n/a".
- **Power:** the flow's estimate at its own switching assumption, not a measurement.

## Main 32-bit designs

SKY130 entries unless marked IHP. Where a core was taped out several times, the newest SKY130 version is shown.

| Design (author) | Shuttle | ISA | How it computes | Memory | Tiles (mm²) | kGE | Flip-flops | Fmax est., MHz | Power est., mW | Paper |
|---|---|---|---|---|---|---|---|---|---|---|
| nanoV one-tile (W. M. Lee, after M. Bell) | TTSKY26c | RV32E | 1 bit per clock | external SPI RAM | 1×1 (0.018) | 3.9 | n/r | 17 (flow clock 12) | 0.2 | none |
| SERV "underserved" (O. Kindgren; versions by others) | TTSKY25b | RV32I | 1 bit per clock, about 32+ clocks per instruction | SPI flash, execute in place | 1×2 (0.036) | 5.6 | 468 | 110 (69) | 1.9 | no peer-reviewed paper found; FPGA size about 125 LUTs (7-series) [1] |
| FemtoRV + compact register file (M. Bell) | TTSKY25b | FemtoRV (variant not stated) | not stated | QSPI flash + PSRAM | 2×2 (0.076) | 8.2 | 343 | 57 (44) | 2.4 | none |
| DUMBRV (Y. Liu), IHP | TTIHP25b | RV32E + Zicond + Zbs | not stated | two SPI memories | 2×2 (0.132) | 12.0 | 414 | 54 | 5.0 | none |
| Wildcat (M. Schoeberl, DTU) | TTCAD25a | RV32I | pipelined (the paper compares 3, 4 and 5 stages) | none on TT (blink demo) | 3×2 (0.115) | 13.3 | 807 | 87 (45) | 5.4 | arXiv 2502.20197 [2] |
| RV32E MinMCU (W. Liu) | TT06 | RV32E | not stated | SPI flash + PSRAM | 2×2 (0.076) | 13.5 | 938 | n/a | n/a | none |
| FazyRV-ExoTiny (M. Kissich, TU Graz) | TT06 | RV32I | **2-bit chunks** (core supports 1, 2, 4 or 8) | QSPI flash + PSRAM | 2×2 (0.076) | 15.0 | 1,306 | n/a (design 50) | n/a | ACM CF '24 [3] |
| LaRVa (J. Arias) | TTCAD25a | RV32 (not stated) | not stated | external, serial bootloader, JTAG | 3×2 (0.115) | 16.6 | 971 | 59 (50) | 0.9 | none |
| TinyQV (M. Bell) | TTSKY25b | RV32EC + Zcb + Zicond | 4 bits per clock (8 clocks per 32-bit step) | QSPI flash + PSRAM | 3×2 (0.115) | 17.6 | 1,146 | 80 (60) | 9.9 | none |
| KianV bare-metal (H. Dabui) | TTSKY25b | RV32E | 32-bit | QSPI flash + PSRAM | 4×2 (0.154) | 18.2 | 1,264 | 83 (43) | 4.6 | none |
| ENSEIRB-MATMECA core, IHP | TTIHP25b | RV32 (not stated) | not stated | UART boot loader | 4×2 (0.268) | 21.9 | 1,637 | 126 | 10.7 | none |
| UART-programmable RV32I (E. Nieman) | TT06 | RV32I (no FENCE/ECALL, word loads only) | 32-bit | 64-byte on-chip program | 4×2 (0.154) | 24.4 | 1,785 | n/a | n/a | none |
| FemtoRV (UNAL) | TTSKY25b | FemtoRV (variant not stated) | not stated | SPI flash + SPI RAM | 4×2 (0.154) | 24.9 | 1,512 | 47 (34) | 6.6 | none |
| 5-stage RV32I (D. Macy) | TT07 | RV32I subset | 5-stage pipeline | 64 B program, 32 B data on chip | 8×2 (0.311) | 27.6 | 1,844 | n/a | n/a | none |
| KianV uLinux, register-file edition | TTSKY26c | RV32IMA | 32-bit | SPI flash + 2 PSRAM | 3×4 (0.260) | 29.3 | n/r | 51 (27) | 5.8 | none |
| Goldcrest (JKU Linz), IHP | TTIHP0p2 | RV32 via microcode on a subleq machine | microcoded | SPI ROM + SPI RAM | 6×2 (0.404) | 30.5 | 2,503 | n/r | n/r | none |
| SotaSoC (SotaTek), IHP | TTIHP26a | RV32IC + Zicsr, FreeRTOS | not stated | QSPI flash + PSRAM | 6×2 (0.404) | 32.3 | 2,537 | 120 | 18.8 | none |
| RISC-V WG "swc1", IHP | TTIHP26a | RV32I | state machine | QSPI PSRAM/flash | 8×2 (0.541) | 36.2 | 2,644 | 69 | 11.4 | none |
| PicoRV32 "Foxworks" (Trinity College Dublin) | TTSKY26c | RV32I | 32-bit, multi-cycle | SPI flash, execute in place; 128 B SRAM | 8×2 (0.311) | 37.0 | n/r | 59 (48) | 11.3 | none for this chip |
| Tiny32 (Tomvdsch) | TTSKY26c | RV32IM + Zicsr, Zephyr target | multi-cycle, iterative M | SPI flash + PSRAM | 8×2 (0.311) | 40.1 | n/r | 58 (30) | 5.1 | none |
| KianV uLinux SoC (H. Dabui) | TTSKY25b | RV32IMA, boots Linux | 32-bit | SPI flash + 2 PSRAM | 8×2 (0.311) | 43.0 | 2,724 | 51 (26) | 7.8 | none |
| KianV Sv32 Linux SoC (H. Dabui, U. Shaked), IHP | TTIHP26a | RV32IMA + Sv32 MMU, I- and D-cache | 32-bit | QSPI PSRAM + caches | 8×4 (1.225) | 85.9 | n/r | 50 | 20.7 | none |

*n/r: not reported in the stored statistics for that shuttle. n/a: older flow, no slack stored.*

### Other RISC-V entries (smaller or special)

- **TinyQV used as a base for other people's SoCs:** the crowdsourced TinyQV SoCs "Asteroids" (8×4, 114 kGE) and "Berzerk" (4×4, 54 kGE); Speck-V (custom instructions for the Speck lightweight cipher); a LoRa edge node SoC (IHP); a CORDIC SoC (IHP); PRISM (a reconfigurable state machine beside TinyQV); Borg (a tiny FP16 GPU beside TinyQV); AlphaOneSoC (a TinyQV copy); a TinyQV with Wishbone bus.
- **The FPGA and chip split already exists once:** authQV (TTSKY26b, 1×1) puts only the QSPI memory controller on the chip, and the RV32I CPU runs on an FPGA.
- **SERV-based SoC on GF180:** serv_soc_wb (TTGF26a, 3×2), SERV changed to RV32E with a flip-flop register file.
- **Accelerators beside a RISC-V:** TinyMOA (compute-in-memory, IHP, unfinished datasheet); a 4×4 ternary (BitNet) matrix multiplier.
- **Teaching cores and 8-bit "RISC-V-like" designs:** schoolRISCV, RISC-V Mini (8-bit, 1 tile), RV8U, TinyRV1 (VHDL, Cornell TinyRV1 ISA), KRV8, the UCLA club core, the CIT core, a single-cycle RV32I subset (N. Perez), and two 1-tile "RISCV Processor Design" copies.
- **Too early for flow statistics:** TT02/TT03 SERV, TT03 scan-chain RISC-V in four blocks, TT04 nanoV (bit-serial RV32E, 1×2), TT05 KianV.

## What the table shows

1. **Size is set by bits per clock and by the register file.** From one bit per clock (SERV, 5.6 kGE; nanoV, 3.9 kGE) to four bits (TinyQV, 17.6 kGE) to full 32-bit cores (PicoRV32, 37 kGE; KianV, 43 kGE). Flip-flops take 30–57% of the area in almost every design. Thirty-two 32-bit registers alone need 1,024 flip-flops, so most designs use RV32E (16 registers) or a custom latch-based register file. KianV's register-file edition is about a third smaller than the standard KianV (29.3 vs 43.0 kGE); the reason still needs checking in its source.
2. **Every 32-bit design that can run real programs fetches code from an external SPI or QSPI chip** (the rest hold only 64 bytes of program, or a fixed demo) through Tiny Tapeout's few pins. Speed is therefore limited by memory, not by the core. Only a few datasheets mention a cache (KianV Sv32 has I- and D-caches).
3. **The flow suggests 50–120 MHz at the typical corner** for most cores, but 25–60 MHz at the slow corner. Measured on-chip speeds are not in the records.

## Gaps: what no Tiny Tapeout RISC-V provides

Checked against all 102 datasheets:

| Gap | Evidence |
|---|---|
| **No performance data.** None reports CoreMark, Dhrystone or Embench, or a measured CPI. Area is known; speed per area is not. | Search of all datasheets: 0 matches. |
| **No low-power design.** None mentions clock gating, sleep, WFI or power-down. The only power numbers are flow estimates. | 0 matches. Prof. Popovici named power optimisation as the summer goal (30 Oct). |
| **No area-versus-width study on silicon.** FazyRV can be built with 1, 2, 4 or 8 bits per clock, but Tiny Tapeout only ever got the 2-bit version. The 4-bit area he asked about is therefore unknown for FazyRV. TinyQV is a different 4-bit core. | ExoTiny datasheet: "Instantiates FazyRV with a chunk size of 2 bits." |
| **Hardly any ISA compliance evidence.** Only one datasheet mentions compliance tests. Several cores are partial (TinyQV hard-wires gp and tp; the Nieman core has word loads only). | 1 match out of 102. |
| **Memory on the chip is rare.** No SKY130 datasheet mentions an SRAM macro; DTU reports OpenRAM DRC problems [2b]. IHP offers SRAM macros (Tiny Tapeout has an IHP SRAM example repository). | 3 datasheets mention SRAM macros or latch arrays; all are IHP. |

## Options to discuss on 6 November (Kamrul decides)

1. **A characterised, scalable 32-bit RISC-V on Tiny Tapeout.**
   - Take FazyRV (open, MIT licence, compliance-tested, published).
   - Run the Tiny Tapeout flow at 1, 2, 4 and 8 bits, and measure area, Fmax and power for each, plus Embench cycles on the FPGA.
   - Then tape out the best point.
   - This directly answers "how much area for 4-bit". Related work to read first: SAILOR (2026), which builds on FazyRV's scalable datapath [4].
2. **A low-power 32-bit RISC-V on Tiny Tapeout.** Add clock gating, a WFI sleep state and operand isolation to a small core, and compare the flow power against the plain version. This leads into his summer goal.
3. **Speed through memory.** Add a small instruction cache or prefetch buffer to a QSPI core (IHP SRAM, or latches on SKY130) and measure the speed-up per added kGE.

These can be combined: option 1 gives the baseline that options 2 and 3 need.

## Next steps after the meeting

- [ ] Put PicoRV32 (or FazyRV) on the lab FPGA board and record LUTs, flip-flops and Fmax from the tools.
- [ ] Run the Tiny Tapeout flow for FazyRV at 1, 2, 4 and 8 bits (GitHub Actions; no local EDA tools needed).
- [ ] Read the FazyRV paper [3], SAILOR [4], the Wildcat paper [2] and the Tiny Tapeout paper [5]; add them to the [reading list](reading-list.md).
- [ ] Check which chips have been tested in silicon (Tiny Tapeout chip pages) before quoting any silicon result.

## References

1. SERV FPGA size from the bit-serial RISC-V overview in the FPGA-Ignite presentation: <https://fpga-ignite.github.io/presentations-pdf/presentation2.pdf>; core: <https://github.com/olofk/serv>.
2. M. Schoeberl, "Wildcat: Educational RISC-V Microprocessors", arXiv:2502.20197, 2025. <https://arxiv.org/abs/2502.20197>. [2b] M. Schoeberl, student tape-out talk, FSiC 2026: <https://wiki.f-si.org/images/6/65/Student-tapeout-fsic2026.pdf>.
3. M. Kissich and M. Baunach, "FazyRV: Closing the Gap between 32-Bit and Bit-Serial RISC-V Cores with a Scalable Implementation", ACM Computing Frontiers (CF '24), 2024. doi:10.1145/3649153.3649195. Code: <https://github.com/meiniKi/FazyRV>.
4. "SAILOR: A Scalable and Energy-Efficient Ultra-Lightweight RISC-V for IoT Security", arXiv:2602.24166, 2026. <https://arxiv.org/abs/2602.24166>.
5. M. Venn, "Tiny Tapeout: A Shared Silicon Tapeout Platform Accessible to Everyone", IEEE Solid-State Circuits Magazine, 2024. <https://ieeexplore.ieee.org/document/10584359>.
6. Tiny Tapeout index (all shuttles): <https://github.com/TinyTapeout/tinytapeout-index>.

*References 1–5 were found by web search on 5 November and have not yet been read in full. Check each against the paper itself before citing it in the interim report.*
