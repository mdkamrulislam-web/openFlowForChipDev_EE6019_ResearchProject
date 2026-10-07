# Week 2 meeting preparation (9 October 2026)

This week's main task is the Tiny Tapeout teaching slides. Supporting material: [weekly log](week-02.md), [research-template comparison](../docs/research/riscv-template-first-look.md) and [risk assessment](../docs/risk-assessment.md).

## Before the meeting

- [ ] Check the weekly log against the work actually completed, add any missing facts and email it from the university account.
- [ ] Open `docs/slides/tiny-tapeout-flow-v1.pptx`; check the remaining screenshot markers.
- [ ] Open the [counter worked-example PR](https://github.com/mdkamrulislam-web/tt-sky130-counter/pull/1) and its actual GDS summary or layout viewer.
- [ ] Keep the research comparison and risk draft ready.
- [ ] Check whether the follow-up email has been answered; remove any resolved questions below.

## One-minute summary to open with

> I have prepared a first teaching deck using the counter as a running example, alongside the research-template comparison and risk draft. The slides explain the steps from behaviour and Verilog to tests, layout and submission, with count, hold, reset and pin-mapping examples. I checked the earlier counter repository: it uses a separate LibreLane flow, so I prepared a real Tiny Tapeout SKY130 example. Its RTL, layout, precheck and gate-level checks all passed, and it uses about 5% of one tile. For the research, Caravel and Croc are the main candidates. I suggest starting with a small memory-mapped int8 engine once you confirm the template and application. The main decisions are the class timing and shuttle, feedback on the slides, and research scope.

## Questions he may ask

| Question | Short answer |
|---|---|
| How long will students need? | Planning estimate: one 2–3-hour introductory lab for a small example in a prepared environment, plus time to design and debug their own project. This has not been measured with students; a dry run will establish the real duration. Actions run in the background and have variable queue/build time. |
| What fits in one tile? | The actual SKY130 counter uses 4.96% utilisation and 47 synthesis cells. Its final tile has 279 non-fill instances including taps, or 4,600 with fillers, so these counts answer different questions. Small state machines and interfaces are plausible examples; each design needs its own routed run. The separate 150 × 150 µm counter-flow figures are background evidence. |
| Can students work without installing anything? | Wokwi provides browser gate design; GitHub Actions provide HDL tests and layout builds. Editing can be done in the browser. Codespaces offers an interactive dev container, subject to memory and account allowances; its suitability for this class still needs a trial. |
| What would a class cost? | Tiny Tapeout publishes teaching bundles; use the current staff appendix and [teaching page](https://tinytapeout.com/teaching/) for the selected shuttle. A bundle is not a confirmed class quote: confirm project sizes, boards, shipping, taxes, timing and IHP ownership terms. |
| Which research template will you use? | Awaiting confirmation. Caravel provides a SKY130 user area and Wishbone interface; Croc offers an educational IHP whole-SoC flow and OBI user domain. The current Croc default is CVE2/SG13CMOS5L, with SG13G2 selectable. The comparison records these differences. |

## Questions to ask him

1. **Class timing and shuttle:** Semester 2 from January 2027, or 2027–28? Which fab/process and shuttle should the students use?
2. **Slides v1:** is the depth and length appropriate? Taught lab or independent reading? Keep Wokwi?
3. **Research template:** Caravel, Croc or another platform? Which maintained source/revision should I start from?
4. **Neural network:** which type, application or paper, and which performance/accuracy criteria?
5. **Fabrication:** is verified submission-ready GDS sufficient, or is a real submission required? Confirm the funded route and deadline before planning payment or a booking.
6. **Tool survey:** still required as a report chapter?
7. **Assessment dates:** interim report, final report and presentation?
8. **Licensing:** which licence for the repository and slides shared with students?

## Notes from the meeting

To be filled from the meeting notes or transcript. Record decisions, actions and unresolved questions here before revising the timeline.
