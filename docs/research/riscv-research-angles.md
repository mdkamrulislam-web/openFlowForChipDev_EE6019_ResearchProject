# Choosing the RISC-V research angle

*16 October 2026. Written after the supervisor meeting that day, for discussion on 23 October. Recommendation pending Prof. Popovici's agreement.*

## 1. What was asked on 16 October

- **Scope:** a larger design than the one-tile student projects, using several tiles, but still following the Tiny Tapeout flow from start to finish.
- **Base:** RISC-V. Do not re-implement a core that is already open; read what exists and find where we can contribute.
- **Directions suggested:**
  - an ultra-low-power RISC-V
  - instruction extensions suited to machine learning, or to cryptography and post-quantum cryptography
  - a processor (or logic) whose power stays constant whatever the instruction
  - earlier group work: a very small RISC-V using stochastic computing
- **Backbone:** check what Tiny Tapeout offers as an SoC backbone (the "carousel" in the 12 October email), then follow that route.

## 2. Which backbone?

| | Caravel (most likely the "carousel") | TinyQV |
|---|---|---|
| **What it is** | Efabless harness for SKY130. A PicoRV32 (RV32IMC) management SoC plus a fixed 2.92 × 3.52 mm user area and 38 I/O pads. | Tiny Tapeout's own RISC-V SoC, by Michael Bell. RV32EC with Zcb and Zicond. Processes 4 bits per clock. Code runs from QSPI flash; data lives in QSPI PSRAM. |
| **Status** | Efabless closed in 2025; ChipFoundry continues its shuttles. I found no sign that it is part of today's Tiny Tapeout flow. | Taped out on Tiny Tapeout shuttles since TT06, on SKY130, IHP and GF180. A 2025 community SoC on TTSKY25a added 50 peripherals of up to 2 tiles each. |
| **How you extend it** | A user project in a full-chip slot, not in tiles. | Custom instructions: it already has `mul16`, `lw2`/`lw4` and `sw2`/`sw4`, and its toolchain supports them. Or a memory-mapped peripheral built from the official 1-tile or 2-tile templates. |

**Proposal:** use TinyQV as the backbone. It is what Tiny Tapeout offers now, it fits the tile model, and it is open source (Apache-2.0).

## 3. The options compared

Each option is scored 1–5 on five criteria, with weights in brackets. "Novelty" includes how well the topic could lead to a PhD.

| Option | Novelty (×3) | Feasible and measurable by April (×3) | Fit with the group's work (×2) | Fit with my aims (×2) | Path to summer and tape-out (×1) | **Total** |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| **A. ML instruction extension for TinyQV** | 3 | 5 | 4 | 5 | 5 | **47** |
| B. Stochastic-computing ML unit | 3 | 4 | 5 | 4 | 4 | 43 |
| C. Constant-power (side-channel-resistant) datapath | 5 | 2 | 5 | 3 | 3 | 40 |
| D. Soft-error-tolerant RISC-V, checked by fault injection | 3 | 4 | 3 | 4 | 3 | 38 |
| E. Post-quantum instruction extension (Kyber NTT) | 4 | 3 | 4 | 2 | 4 | 37 |
| F. Ultra-low-power core redesign | 2 | 4 | 4 | 2 | 3 | 33 |

- **A.** One of Prof. Popovici's own suggestions, and it continues my neural-network aim. A 2025 TinyQV "Neural Processing Unit" peripheral already exists, so the new part is the instruction extension and a measured comparison with that peripheral.
- **B.** Builds on the group's stochastic-computing work (an IEEE ASAP 2019 paper co-authored by Prof. Popovici) and needs very little area. The open question is accuracy against bitstream length. It works best as phase 2 of A.
- **C.** The most original topic and the most PhD-shaped. However:
  - the open flow has no built-in per-cycle power traces or leakage tests;
  - dual-rail logic at least doubles the area;
  - silicon would arrive after the project ends.
- **D.** Suits my verification background (fault-injection campaigns) and the group's "reliable computing" theme. It was not raised on 16 October.
- **E.** A strong field, and there is no post-quantum peripheral on TinyQV yet. But modular arithmetic and NTT verification would be a steep learning curve for me.
- **F.** Hard to show a contribution: tiny low-power cores already exist, TinyQV among them. The strongest low-power levers, supply scaling and power gating, are not in the designer's hands on a shared die.

## 4. Recommendation: A, with B as its second phase

**Working title:** energy-efficient machine-learning instructions for a tiny RISC-V on Tiny Tapeout.

**Research question:** TinyQV handles 4 bits per clock and keeps its memory behind QSPI. What is the most energy-efficient way to add neural-network support to such a core: tightly coupled custom instructions, or a memory-mapped accelerator? And how far do low-bit (int8, int4) and stochastic arithmetic change the answer?

**Why this angle:**
- **Supervisor's suggestion:** it is one of the two instruction extensions Prof. Popovici named, and it keeps the original neural-network aim.
- **A plausible gap:**
  - the ML extensions I found target larger cores (XpulpNN) or FPGAs (CFU Playground);
  - on TinyQV, each internal cycle takes 8 clocks and a word load from memory takes 9–10 of those cycles;
  - the literature survey has to confirm the gap.
- **Measurable before silicon:**
  - cycles from simulation
  - energy from post-layout power analysis using simulated switching activity
  - area in tiles
  - accuracy from a Python model
- **Low risk:** TinyQV has been taped out on several shuttles and already has custom instructions, and the 2025 NPU peripheral gives a ready comparison point.
- **Low power stays central:** energy per inference is the main metric, and phase 2 brings in the group's stochastic computing.
- **Relevance:** the topic matters for industrial edge AI and leads naturally into a PhD.

**Plan:**

| When | Milestone |
|---|---|
| Oct–Nov 2026 | Literature survey (about 30 checked references). Run TinyQV in simulation. Choose a small benchmark, for example a 64-input MLP on 8 × 8 digits, and measure the software-only baseline. |
| By end of Semester 1 | Interim report and literature survey, including the risk assessment. |
| Jan–Feb 2027 | Design and verify the custom instructions: a packed int8/int4 dot product with accumulate. Software support through `.insn`. |
| Feb–Mar 2027 | Harden TinyQV plus the extension through the Tiny Tapeout flow on several tiles. Compare energy, latency, area and accuracy against the baseline and the NPU peripheral. Seminar. |
| Apr 2027 | Dissertation, with a submission-ready layout: TTSKY27a (May) or TTIHP27a (March) if approved. |
| Summer 2027 (EE6008) | A stochastic or bit-serial MAC variant, the comparison, and a conference-style paper. |

**Risks and fallbacks:**

| Risk | Fallback |
|---|---|
| Changing TinyQV's serial datapath is too hard | Build the same function first as a 2-tile peripheral from the official template, then compare. |
| QSPI memory traffic dominates every option | Report that as a finding; add a small on-chip weight buffer. |
| Power figures are estimates without silicon | State the method and its limits, and compare every design with the same method. |
| Tile cost | Use the fewest tiles that work. Any submission needs the supervisor's approval. |

## 5. To confirm with Prof. Popovici on 23 October

1. Is the ML instruction extension on TinyQV the right direction, or would you prefer the constant-power or post-quantum angle?
2. Is TinyQV acceptable as the "SoC backbone", since Caravel now sits outside the Tiny Tapeout flow?
3. Is simulated post-layout energy per inference acceptable as the main metric, given that no silicon will arrive before the project ends?
4. Which shuttle and how many tiles could the group support towards the end of the master's?
5. Should the summer research project (EE6008) continue this design?

## Sources (checked 16 October 2026)

These are starting points. Read each one before citing it in the report.

- [TinyQV source and README](https://github.com/MichaelBell/tinyQV) (ISA, nibble-serial datapath, custom instructions, Apache-2.0)
- [TinyQV on TT06](https://tinytapeout.com/chips/tt06/tt_um_MichaelBell_tinyQV)
- Crowd-sourced RISC-V peripheral competition: [rules and templates](https://tinytapeout.com/competitions/risc-v-peripheral/); [entries and winners](https://tinytapeout.com/competitions/risc-v-peripheral-winners/) (includes the Neural Processing Unit)
- [Caravel harness documentation](https://caravel-docs.readthedocs.io/en/moving-to-rst/)
- [Tiny Tapeout shuttle list](https://tinytapeout.com/chips/)
- A. Garofalo et al., "XpulpNN: Accelerating Quantized Neural Networks on RISC-V Processors Through ISA Extensions", [DATE 2020](https://past.date-conference.com/proceedings-archive/2020/html/0650.html); journal version, [IEEE TETC](https://www.research-collection.ethz.ch/handle/20.500.11850/508241)
- S. Prakash et al., "CFU Playground: Full-Stack Open-Source Framework for Tiny Machine Learning (tinyML) Acceleration on FPGAs", [arXiv:2201.01863](https://arxiv.org/abs/2201.01863)
- T. Fritzmann, G. Sigl and J. Sepúlveda, "RISQ-V: Tightly Coupled RISC-V Accelerators for Post-Quantum Cryptography", [IACR TCHES 2020(4)](https://tches.iacr.org/index.php/TCHES/article/view/8683)
- K. Tiri and I. Verbauwhede, "A Logic Level Design Methodology for a Secure DPA Resistant ASIC or FPGA Implementation", [DATE 2004](https://mooney.gatech.edu/Courses/ECE3170/lectures/TiriVerbDATE04.pdf); their VLSI design flow, [arXiv:0710.4806](https://arxiv.org/abs/0710.4806)
- "Efficient Architectures and Implementation of Arithmetic Functions Approximation Based Stochastic Computing", IEEE ASAP 2019, co-authored by E. Popovici ([CORA](https://cora.ucc.ie/handle/10468/8805))
