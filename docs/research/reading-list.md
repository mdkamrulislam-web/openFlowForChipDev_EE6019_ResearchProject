# Reading list for the literature survey

*Started 18 October 2026. Every entry below was checked to exist on that date. Read each one yourself before citing it: Prof. Popovici's rule is roughly one checked reference per page of report, closely tied to the text.*

**How to use it:**
- Add each source to Zotero, through Google Scholar.
- First pass: abstract, introduction, conclusion and the key figures.
- Write one line on **why it matters for this project** and tick it off.
- Aim for about 30 checked references by the interim report (end of Semester 1).

## The platform

| # | Source | Why it matters | Read |
|---|---|---|:-:|
| 1 | M. Bell, [TinyQV source and README](https://github.com/MichaelBell/tinyQV) | The core you will extend: RV32EC, 4 bits per clock, QSPI memory, existing custom instructions | ☐ |
| 2 | Tiny Tapeout, [TinyQV crowdsourced SoC (TTSKY25a)](https://github.com/TinyTapeout/ttsky25a-tinyqv) and [NPU peripheral documentation](https://github.com/TinyTapeout/ttsky25a-tinyqv/blob/main/docs/user_peripherals/04_npu.md) | The SoC you will build on, and the existing ML peripheral your design will be compared with | ☐ |
| 3 | Tiny Tapeout, [Crowd-sourced RISC-V peripheral competition](https://tinytapeout.com/competitions/risc-v-peripheral/) | Interface rules and tile limits for TinyQV peripherals | ☐ |
| 4 | RISC-V International, [ratified ISA specifications](https://riscv.org/specifications/ratified/) | RV32E, the C extension and the rules for custom instructions | ☐ |

## Part A: ML instructions and quantised inference

| # | Source | Why it matters | Read |
|---|---|---|:-:|
| 5 | A. Garofalo et al., "XpulpNN: Accelerating Quantized Neural Networks on RISC-V Processors Through ISA Extensions", [DATE 2020](https://past.date-conference.com/proceedings-archive/2020/html/0650.html); journal version, [IEEE TETC](https://www.research-collection.ethz.ch/handle/20.500.11850/508241) | The closest work: ML instructions on a (larger) RISC-V core | ☐ |
| 6 | S. Prakash et al., "CFU Playground: Full-Stack Open-Source Framework for Tiny Machine Learning (tinyML) Acceleration on FPGAs", [arXiv:2201.01863](https://arxiv.org/abs/2201.01863) | Custom instruction units for tiny ML, with a method for measuring them | ☐ |
| 7 | B. Jacob et al., "Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference", [arXiv:1712.05877](https://arxiv.org/abs/1712.05877) | The integer quantisation scheme the NPU follows; explains scale, zero point and requantisation | ☐ |
| 8 | C. Banbury et al., "MLPerf Tiny Benchmark", [arXiv:2106.07597](https://arxiv.org/abs/2106.07597) | The standard TinyML benchmark (keyword spotting, anomaly detection and others) | ☐ |

## Part B: stochastic computing

| # | Source | Why it matters | Read |
|---|---|---|:-:|
| 9 | A. Alaghi and J. P. Hayes, "Survey of Stochastic Computing", ACM Trans. Embedded Computing Systems 12(2s), 2013 ([PDF](https://homes.cs.washington.edu/~armin/ACM_TECS_2013.pdf)) | The standard introduction: representation, circuits, trade-offs | ☐ |
| 10 | "Efficient Architectures and Implementation of Arithmetic Functions Approximation Based Stochastic Computing", IEEE ASAP 2019, co-authored by E. Popovici ([CORA](https://cora.ucc.ie/handle/10468/8805)) | Your supervisor's own work: stochastic sigmoid and tanh; cheaper binary-to-stochastic conversion | ☐ |
| 11 | J. Li et al., "Towards Acceleration of Deep Convolutional Neural Networks Using Stochastic Computing", ASP-DAC 2017 ([PDF](https://ywang393.expressions.syr.edu/wp-content/uploads/2016/07/Towards-acceleration-of-deep-convolutional-neural-networks-using-stochastic-computing.pdf)) | Stochastic CNN hardware: large area and power savings for a small accuracy cost | ☐ |
| 12 | Q. Chen et al., "A 16×128 Stochastic-Binary Processing Element Array for Accelerating Stochastic Dot-Product Computation Using 1-16 Bit-Stream Length", [DATE 2020](https://past.date-conference.com/proceedings-archive/2020/pdf/0437.pdf) | A real chip using very short bit streams (1–16) for dot products, close to what part B would test | ☐ |

## Future directions (one paragraph in the survey)

| # | Source | Why it matters | Read |
|---|---|---|:-:|
| 13 | T. Fritzmann, G. Sigl and J. Sepúlveda, "RISQ-V: Tightly Coupled RISC-V Accelerators for Post-Quantum Cryptography", [IACR TCHES 2020(4)](https://tches.iacr.org/index.php/TCHES/article/view/8683) | The same idea (instruction extensions) applied to post-quantum cryptography | ☐ |
| 14 | K. Tiri and I. Verbauwhede, "A Logic Level Design Methodology for a Secure DPA Resistant ASIC or FPGA Implementation", DATE 2004 ([PDF](https://mooney.gatech.edu/Courses/ECE3170/lectures/TiriVerbDATE04.pdf)) | Constant-power logic: the side-channel angle Prof. Popovici mentioned | ☐ |

**Next to find** (Google Scholar): recent ML instruction-extension work on small RISC-V cores, energy measurement in open-source flows (OpenROAD/OpenSTA power analysis), and recent stochastic-computing neural-network accelerators (2022 onwards).
