# Supervisor meeting, 23 October 2026

The meeting was held at 11:00 as part of the group meeting. Only the parts about this project are recorded here. The source is an automatic transcript and recording (private Drive folder "23rd Otober 2026"), which is garbled in places; quotations are approximate.

## What Kamrul reported

- TinyQV, Tiny Tapeout's RISC-V, works 4 bits at a time, so one instruction takes 8 clocks. It has no memory of its own: code and data sit in external flash and RAM.
- Other blocks can be attached to it, and someone has already attached an NPU. His plan was to run a machine-learning model on it.
- Before the meeting he ran TinyQV's own tests in simulation; all of them passed ([week-04.md](week-04.md)).

## What Prof. Popovici suggested

- **A RISC-V on an FPGA, with the accelerator on the chip.**
  - The RISC-V runs on an FPGA. The Tiny Tapeout chip is a separate accelerator.
  - The two are connected "through whatever interfaces, maybe even directly", using the chip's digital I/O.
- **TinyQV is "too small … not that useful"** for this.
  - First check which RISC-V designs already exist on Tiny Tapeout.
  - If none suits, choose "a proper RISC-V, which is 32-bit … but not one of the largest".
- **An alternative he gave:** take that 32-bit RISC-V and "look … how you can reduce the power consumption", first on the FPGA, then put it onto the ASIC.
- **What to accelerate:** "a little bit of research".
  - Find what "would work much faster in 130 nanometer compared to FPGA, which is … 7 nanometer".
  - His examples: convolution, or nonlinear functions such as tanh or sigmoid.
- **The link between the two:**
  - Kamrul said the bandwidth of the transfer would be very important.
  - Prof. Popovici: keep it fully digital and model the delay, so you can say "if this would have been on the chip, you don't lose this".
- **Fabrication is the main aim:** "one of the things which I would like to do is to do the fabrication of the ASIC".
  - Tiny Tapeout is used because it is low cost.
  - "It doesn't matter what accelerator", but he wants to show "quite a lot of acceleration" from moving that part onto the ASIC.
- **Literature:** accelerators for RISC-V, and the usual kinds of AI and machine-learning accelerators ("quite a lot of them nowadays").

## What this changes

- The "A then B" plan of 18 October (an ML instruction extension inside TinyQV) **is not what he asked for**. The research becomes a RISC-V on an FPGA plus an accelerator chip made through Tiny Tapeout, with fabrication as the goal.
- **Still useful:**
  - Running TinyQV taught the Tiny Tapeout simulation tools.
  - TinyQV's NPU is a worked example of a small ML accelerator.
  - Data movement is still the main cost. Here the data crosses the chip's pins, so the accelerator must do a lot of work for little data.
- **A possible link to part B:** stochastic computing fits his tanh/sigmoid example. His group's IEEE ASAP 2019 paper is on stochastic tanh and sigmoid (reading list #10). This is an idea to check, not something he said.
- **Earlier scope note:** the 2 October scope listed FPGA work as out of scope. That no longer holds for the host CPU.

## Not discussed

These are still open:
- which shuttle, and how many tiles;
- whether EE6008 continues the design;
- the report and seminar dates;
- the benchmark;
- whether stochastic computing stays in the plan.

## Actions

- [ ] List the RISC-V designs already on Tiny Tapeout. For each: 32-bit or not, size, licence, whether it runs on an FPGA.
- [ ] Choose a small 32-bit RISC-V for the FPGA (candidates to check: PicoRV32, SERV, VexRiscv, Ibex), and find out which FPGA board is available at UCC.
- [ ] Literature survey on RISC-V accelerators and ML accelerators: what each speeds up, how much data it needs, and the speed-up it reports.
- [ ] Shortlist two or three functions to accelerate (convolution, tanh/sigmoid and others). Estimate the work per byte sent over the pins, against the Tiny Tapeout I/O limits.
- [ ] Choose between the supervisor's two options: an accelerator chip (his main suggestion) or a lower-power 32-bit RISC-V.
- [ ] Email Prof. Popovici a short summary, to check it was understood correctly, together with the open questions.
