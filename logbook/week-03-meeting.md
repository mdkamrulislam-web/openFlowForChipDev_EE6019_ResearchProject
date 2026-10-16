# Supervisor meeting, 16 October 2026

The meeting was held at 15:00, moved from the usual morning slot, as part of a group meeting. Only the parts about this project are recorded here. The source is an automatic transcript, which is garbled in places; quotations are approximate.

## Teaching material

- Kamrul reported that he had taken a shift register through the whole Tiny Tapeout flow and generated the GDS, and that he had made a slide tutorial for the flow.
- Prof. Popovici said this is exactly what he needs. From January 2027, about 70 third-year students will each make a small design and take it through the full flow to tape-out.
- **Action:** send Prof. Popovici the tutorial.

## Research direction

- Kamrul's part is research: a larger design using several tiles ("not one tile as they would use"), still following the Tiny Tapeout flow.
  - Look at the open projects others have taped out on Tiny Tapeout, and at what Tiny Tapeout offers as an SoC backbone (recalled as "carousel"), then follow that route.
  - The steps: first know the flow, then take a design through it, then implement your own design.
- RISC-V is recommended: it is popular, the architecture is open, and many companies nearby work on it.
- Do not re-implement a design that is already in the open domain. Read what exists and find where we can contribute.
- Angles suggested:
  - an ultra-low-power RISC-V
  - instruction extensions that make a core more suitable for machine learning, or for cryptography and post-quantum cryptography
  - a processor, or digital logic in general, whose power is constant whatever the instruction (an earlier interest of the group)
  - earlier group work: a very small RISC-V using stochastic computing
- **Action:** choose the angle. Options and a recommendation are in [docs/research/riscv-research-angles.md](../docs/research/riscv-research-angles.md).

## Reports and presentations

- **Dates, as Prof. Popovici recalls them** (to be confirmed with the module coordinator): a preliminary report before Christmas, then a presentation, then the final report around April. The rough plan is a working design by April, with more work over the summer.
- **The official module outline:**
  - interim progress report and literature survey at the end of Semester 1 (40 marks; includes the risk assessment)
  - attendance and participation (40 marks)
  - seminar to an independent panel in the middle of Semester 2 (20 marks)
  - dissertation at the end of Semester 2 (100 marks)
- **References:** roughly one reference per page, so about 30 for a 30-page report.
  - Every reference must be real and closely tied to the text.
  - Use scientific sources found through Google Scholar and read what each paper actually says.
  - Unchecked AI-generated references are easy to spot and are marked down.
- **Presentations:**
  - use little text, no more than two lines per bullet
  - use colourful, readable figures
  - be able to explain every word, line and label on every slide

## Actions

- [ ] Send Prof. Popovici the tutorial.
- [ ] Choose the research angle and confirm it at the next meeting.
- [ ] Start the literature survey on Google Scholar, checking every reference.
- [ ] Confirm the interim-report, seminar and dissertation dates with the module coordinator.
