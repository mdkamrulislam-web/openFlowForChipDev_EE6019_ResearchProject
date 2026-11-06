# Supervisor meeting, 30 October 2026

Held at 11:00 as part of the group meeting. Only this project's part is recorded. The source is three automatic transcripts and a recording (private Drive folder "5. 30th October 2026"). They are garbled in places ("RIGS5" = RISC-V, "tiny table" = Tiny Tapeout), so quotations are approximate.

## What Kamrul reported

- He looked at RISC-V designs available online. PicoRV32 needs about 2,000 LUTs and fits the lab FPGA board. Running it there and trying some instructions would be a good start.
- Tiny Tapeout already has some RISC-V designs, but they are slow compared with designs outside Tiny Tapeout. Examples: a SERV-based 32-bit core that handles one bit at a time (a student implemented it a year or two ago); FazyRV-ExoTiny, whose datapath can be 1, 2, 4 or 8 bits wide to save area.
- He had less time this week because of a mid-term and an assignment. Prof. Popovici: "no problem".

## What Prof. Popovici said

- **FPGA board:** Kamrul asked for one; Prof. Popovici offered to give him a board after the meeting.
- **The task, restated:** "take a RISC-V design and bring it to the full ASIC design … through Tiny Tapeout".
  - First check it on the FPGA: area and "even the gate equivalent", because "from the gate equivalent you can see how much space [it] will require on, say, SKY130".
  - Then, once simulation and the FPGA work, go through the ASIC flow. It is to be implemented as an ASIC, not as LUTs.
  - "On the ASIC flow we will try perhaps to optimise for power consumption … we'll find an optimisation goal over the summer."
- **On "slow":** "not necessarily slow". Characterise them: how big, how many tiles, how many bits. Note which features each has and which it lacks. "Then we'll find out the gap that is not implemented in Tiny Tapeout, and we'll address that. That's the ultimate aim."
- **FazyRV:** "Fully characterise. How much is that area for the 4-bit?"
- **Task for next week (6 Nov):** "try to find all the characteristics of the implementation": size, frequency, all the parameters they were characterised with, and any papers about them. Then identify the gap.

## What this changes

- On 30 October the project was again **a RISC-V taken through the full Tiny Tapeout ASIC flow**. The 23 October accelerator-chip idea was not mentioned. Confirm on 6 November whether the accelerator is dropped or postponed.
- An FPGA run is a check before the ASIC, not the end product.
- Low power is the likely optimisation goal for the summer (EE6008).

## Actions

- [x] Characterise the RISC-V designs on Tiny Tapeout and find the gap: [docs/research/tt-riscv-characterisation.md](../docs/research/tt-riscv-characterisation.md) (5 November).
- [ ] Collect the FPGA board, if not already done; note its exact part number.
- [ ] Put a RISC-V on the FPGA and record area (LUTs, flip-flops) and Fmax.
