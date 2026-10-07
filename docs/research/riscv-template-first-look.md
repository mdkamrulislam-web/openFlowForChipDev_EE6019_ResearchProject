# RISC-V research template: first look

*Sources checked 7 October 2026. Desk review only; no template build has been run. The intended template still needs supervisor confirmation.*

RISC-V is an open, royalty-free instruction-set architecture (ISA): the contract between software and a processor. A particular core may be open source or proprietary. RV32I provides 32-bit integer operations and 32 integer registers; RV32E reduces this to 16 registers for smaller embedded cores. Optional extensions include M (multiply/divide), C (compressed instructions) and V (vectors); a core implements only its declared subset. Accelerator research can reuse open cores and software tools, add custom instructions where the core permits, or attach a memory-mapped coprocessor controlled through ordinary loads and stores. ISA extensibility does not itself supply an accelerator interface. Sources: [RISC-V overview][isa], [RV32I][rv32i], [RV32E][rv32e] and [extension names][extensions].

## Candidate comparison

“Carousel” most plausibly means **Caravel**, but this is an interpretation. ChipFoundry now publishes the [Caravel harness][harness] and [user-project template][caravel], and offers fabrication through chipIgnite. Do not assume the former free Efabless OpenMPW programme remains available.

| Template | PDK | CPU core | Bus to attach an accelerator | User area | Flow and tools | Route to fabrication: shuttle, cost, dates | Documentation quality | Fit by April 2027 |
|---|---|---|---|---|---|---|---|---|
| [Caravel][caravel] | SkyWater SKY130, 130 nm | VexRiscv management SoC, generated with LiteX ([TRM][trm]) | 32-bit Wishbone; memory-mapped registers | About 10 mm² ([platforms][platforms]) | ChipFoundry CLI, OpenLane, OpenSTA; cocotb RTL/GL tests | chipIgnite: USD 14,950 base; CI2612 projected tapeout 7 Dec 2026, delivery 25 May 2027 ([price][price], [status][status]) | Detailed template instructions and register manual; harness warns documentation is being updated | Good for a small user macro; December is too early for a spring design. Later shuttle needs confirmation |
| [Croc][croc] (PULP: ETH Zurich/Bologna) | IHP 130 nm; current default SG13CMOS5L, SG13G2 selectable | CVE2 in current RTL; earlier Croc paper used Ibex | 32-bit OBI crossbar; optional CV-X-IF at core wrapper | Editable `user_domain` within the whole-chip floorplan; budget must be measured | Bender, Yosys/Slang, OpenROAD, KLayout; Verilator | IHP MPW; process/area quotation. CMOS5L tape-in listed for 30 Mar 2027; SG13G2 open run listed for 4 Oct 2027 ([schedule][ihp-schedule]) | Readable educational RTL, bring-up commands and extension guidance; tool versions matter | Strong compact research option; SRAM and floorplan constrain scope. A layout is feasible; returned silicon is later |
| [HyperCroc][hypercroc] (additional candidate) | IHP 130 nm in paper | Ibex RV32IMCB in paper | OBI user domain, iDMA and HyperBus | Shared floorplan; added memory-controller/PHY overhead | Croc-derived open RTL-to-GDS flow | IHP route; no project quote or confirmed accessible release established here | Two-page 2026 paper; release and silicon status need checking | Consider only if larger datasets require external memory and the maintained source is available |

**Availability matters.** Croc's [current core wrapper][core] disables M/B and CV-X-IF by default: do not treat the earlier paper's CPU configuration as the current template. The README supports container version 2025.12; reproduce its example in the upstream environment and pin a commit before integration. HyperCroc's paper announces future release/tapeout, so its targets are not proof of a completed release or measured HyperCroc silicon.

**Costs and dates are provisional.** ChipFoundry's [60-day commitment rule][commitment] differs from its projected status-page dates; obtain written deadlines and a quotation. Shuttles can slip or be cancelled. IHP's [open-MPW page][ihp-open] advertises SG13G2 at EUR 2,800/mm² and CMOS5L at EUR 1,500/mm², subject to participation terms and aggregate demand; bare die and packaging differ from chipIgnite's packaged-parts/board offer. These are not total project quotes. The [2027 IHP schedule][ihp-schedule] may change until 1 December 2026. Plan April completion around verified GDS and the report.

## Three manageable accelerator directions

These are proposed starting scopes, not measured area guarantees. Establish an early synthesis and routing budget.

1. **Small int8 MLP engine:** one MAC first, then four parallel MACs; int8 operands, int32 accumulation and at most 1–4 KiB local storage. Attach through Wishbone/OBI. Compare CPU and accelerator inference cycles, transfer overhead and routed area. Start with [Sze et al., *Efficient Processing of Deep Neural Networks*, 2017][sze] and [Gemmini][gemmini] for dataflow ideas. Gemmini's Rocket/Chipyard system is a reference, not a drop-in template block.
2. **Binary dot-product engine:** one 32-bit XNOR/popcount lane, accumulator and threshold, reusing it across a small binarised MLP. Measure accuracy against the int8 baseline as well as area/cycles. Start with [Courbariaux et al., *Binarized Neural Networks*, 2016][bnn] and [Rastegari et al., *XNOR-Net*, 2016][xnor].
3. **Custom packed-int8 instruction:** a two-input unit producing a four-element dot product, with software handling accumulation. Croc's optional CV-X-IF makes this plausible, but enabling it adds core/interface verification. Caravel's fixed management harness favours a Wishbone block. [CFU Playground][cfu] demonstrates the method in FPGA/simulation; it supplies ideas rather than ASIC integration. Use [Croc's wrapper][core] as the integration starting point.

## Provisional recommendation and decisions

Choose the **memory-mapped int8 engine** first: the same datapath can move between Caravel and Croc, and a software baseline makes the benefit testable. If the supervisor meant Caravel, use its user-project wrapper. If the choice is open, Croc is attractive for its readable whole-SoC flow and explicit user domain; confirm the IHP process and reproduce the baseline first. Keep HyperCroc as a later extension.

Confirm: which template and upstream revision; which network/application and success metrics; memory-mapped or custom-instruction scope; whether verified layout or actual fabrication is required; and the funded shuttle, process, licence and deadline. No fabrication booking follows from this review.

[isa]: https://riscv.org/about/
[rv32i]: https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html
[rv32e]: https://docs.riscv.org/reference/isa/unpriv/rv32e.html
[extensions]: https://docs.riscv.org/reference/isa/unpriv/naming.html
[harness]: https://github.com/chipfoundry/caravel
[caravel]: https://github.com/chipfoundry/caravel_user_project
[trm]: https://caravel-mgmt-soc-litex.readthedocs.io/en/latest/
[platforms]: https://chipfoundry.io/soc_platforms
[price]: https://chipfoundry.io/faqs
[status]: https://platform.chipfoundry.io/status
[commitment]: https://chipfoundry.io/how-it-works
[croc]: https://github.com/pulp-platform/croc/blob/main/README.md
[core]: https://github.com/pulp-platform/croc/blob/main/rtl/core_wrap.sv
[hypercroc]: https://arxiv.org/html/2603.12308v1
[ihp-open]: https://dk.ihp-microelectronics.com/OpenSourceRequest.php
[ihp-schedule]: https://www.ihp-microelectronics.com/services/research-and-prototyping-service/mpw-prototyping-service/schedule-price-list
[sze]: https://arxiv.org/abs/1703.09039
[gemmini]: https://github.com/ucb-bar/gemmini
[bnn]: https://arxiv.org/abs/1602.02830
[xnor]: https://arxiv.org/abs/1603.05279
[cfu]: https://github.com/google/CFU-Playground
