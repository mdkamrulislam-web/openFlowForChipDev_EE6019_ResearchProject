# Week 2 meeting preparation (9 October 2026)

This week's main task is the [comprehensive Tiny Tapeout beginner manual](../docs/beginner-guide/README.md) and [complete 195-slide course](../docs/slides/README.md). Supporting material: [weekly log](week-02.md), [research-template comparison](../docs/research/riscv-template-first-look.md) and [risk assessment](../docs/risk-assessment.md).

## Before the meeting

- [ ] Check the weekly log against the work actually completed, add any missing facts and email it from the university account.
- [ ] Open `docs/slides/tiny-tapeout-beginner-course.pptx` or its PDF; keep the Word manual and starter ZIP ready. The older `tiny-tapeout-flow-v1.pptx` is the short overview.
- [ ] Open the [counter worked-example PR](https://github.com/mdkamrulislam-web/tt-sky130-counter/pull/1) and its actual GDS summary or layout viewer.
- [ ] Keep the research comparison and risk draft ready.
- [ ] Check whether the follow-up email has been answered; remove any resolved questions below.

## One-minute summary to open with

> I have prepared an 85-page beginner manual and a complete 195-slide course using the counter as a running example, plus a research-template comparison and risk draft. Both teaching formats start with circuit concepts and give step-by-step browser instructions, screenshots, code explanations, checks and exercises. They reach a free checked-layout package, then explain later submission and fabrication. The genuine Tiny Tapeout SKY130 example passed RTL, layout, precheck and gate-level checks and uses about 5% of one tile. For the research, Caravel and Croc are the main candidates. I suggest starting with a small memory-mapped int8 engine once you confirm the template and application. The main decisions are class timing and shuttle, feedback on the teaching sequence, and research scope.

## Questions he may ask

| Question | Short answer |
|---|---|
| How long will students need? | The manual and full slide course support study over several sessions. Timing has not been measured with students; a beginner trial will establish realistic reading and lab time. Actions run in the background with variable queue/build time. |
| What fits in one tile? | The actual SKY130 counter uses 4.96% utilisation and 47 synthesis cells. Its final tile has 279 non-fill instances including taps, or 4,600 with fillers, so these counts answer different questions. Small state machines and interfaces are plausible examples; each design needs its own routed run. The separate 150 × 150 µm counter-flow figures are background evidence. |
| Can students work without installing anything? | Wokwi provides browser gate design; GitHub Actions provide HDL tests and layout builds. Editing can be done in the browser. Codespaces offers an interactive dev container, subject to memory and account allowances; its suitability for this class still needs a trial. |
| What would a class cost? | Tiny Tapeout publishes teaching bundles; use the current staff appendix and [teaching page](https://tinytapeout.com/teaching/) for the selected shuttle. A bundle is not a confirmed class quote: confirm project sizes, boards, shipping, taxes, timing and IHP ownership terms. |
| Which research template will you use? | Awaiting confirmation. Caravel provides a SKY130 user area and Wishbone interface; Croc offers an educational IHP whole-SoC flow and OBI user domain. The current Croc default is CVE2/SG13CMOS5L, with SG13G2 selectable. The comparison records these differences. |

## Questions to ask him

1. **Class timing and shuttle:** Semester 2 from January 2027, or 2027–28? Which fab/process and shuttle should the students use?
2. **Beginner manual and full slide course:** is the learning sequence appropriate? Which sections should be taught in a lab, and which can be read independently? Plan a beginner trial.
3. **Research template:** Caravel, Croc or another platform? Which maintained source/revision should I start from?
4. **Neural network:** which type, application or paper, and which performance/accuracy criteria?
5. **Fabrication:** is verified submission-ready GDS sufficient, or is a real submission required? Confirm the funded route and deadline before planning payment or a booking.
6. **Tool survey:** still required as a report chapter?
7. **Assessment dates:** interim report, final report and presentation?
8. **Licensing:** which licence for the repository and slides shared with students?

## Notes from the meeting

To be filled from the meeting notes or transcript. Record decisions, actions and unresolved questions here before revising the timeline.
