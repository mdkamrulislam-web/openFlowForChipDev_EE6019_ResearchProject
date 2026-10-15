# Week 2 (5 to 9 Oct 2026)

*Review draft, updated 8 October. Check the wording and add any work not recorded in the repositories before emailing.*

## Tasks Done

- Recorded the previous meeting and revised the project scope: use Tiny Tapeout's existing flow for the teaching slides, and investigate a RISC-V template for neural-network accelerator research. [PR #7](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/pull/7) was merged this week; [the resulting CI run](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/actions/runs/37684836890) passed on SKY130 and IHP.
- Prepared [slides v1](../docs/slides/tiny-tapeout-flow-v1.pptx) and a [PDF copy](../docs/slides/tiny-tapeout-flow-v1.pdf): 22 teaching slides plus a staff appendix, with lecturer notes, sources and a [rebuild script](../docs/slides/build_slides.py). The counter is the running example, covering binary outputs, count/hold/reset, Verilog, cocotb and actual layout results. All 26 slides were rendered in PowerPoint and visually checked.
- Expanded the teaching material into a [complete beginner DOCX](../docs/beginner-guide/tiny-tapeout-beginner-guide.docx) and [PDF](../docs/beginner-guide/tiny-tapeout-beginner-guide.pdf), with approximately 23,000 words across 85 pages. It starts with bits, hardware logic, clocks and reset, then explains each browser step, test, physical-flow stage and result. Includes 30 genuine figure placements, actual FST waveform captures, answered exercises and a seven-file starter ZIP matching the verified counter. The practical route ends at a free checked layout; submission and fabrication are explained as later steps. All pages were rendered and reviewed.
- Made a [complete beginner PowerPoint course](../docs/slides/tiny-tapeout-beginner-course.pptx) and [PDF](../docs/slides/tiny-tapeout-beginner-course.pdf): 195 slides with 39 genuine screenshot placements and approximately 26,500 words of teaching notes. It follows the manual's full learning sequence, with readable code excerpts, editable clock/layout/fabrication diagrams, step-by-step browser instructions, chapter links and twelve longer exercises with separate answer slides. All slides were rendered and visually reviewed; text bounds, sources and PDF pages were checked.
- Prepared a [first look at RISC-V and the candidate research templates](../docs/research/riscv-template-first-look.md). Caravel and Croc are the main candidates; HyperCroc needs further availability checks. A small memory-mapped int8 engine is the provisional starting point, subject to confirmation.
- Prepared a [desk and computer-work risk assessment](../docs/risk-assessment.md) for review. The required departmental form and local controls still need confirmation.
- Added [website-based notes on making and manufacturing ASICs](../docs/tiny-tapeout.md#website-notes-for-the-two-remaining-videos), and checked current template settings against the older video material.
- Prepared and verified the [Tiny Tapeout SKY130 counter example](https://github.com/mdkamrulislam-web/tt-sky130-counter/pull/1), with the fixed interface, pin descriptions, datasheet and a cocotb reference-model test. [RTL tests](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100752), [documentation](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100755) and [GDS, precheck, gate-level test and viewer](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100748) all passed at commit `61ef06b`. The counter uses 4.96% of one tile, with 47 synthesis cells; the [layout viewer](https://mdkamrulislam-web.github.io/tt-sky130-counter/) is live. No design was submitted to a shuttle.

## Problems and how I fixed them

- The earlier counter GDS came from the repository's separate LibreLane flow, on a 150 × 150 µm die. It was not a Tiny Tapeout tile result. Checked the repository structure and prepared a genuine template example, keeping the earlier layout labelled as background evidence.
- The initial template copy had blank project metadata and placeholder documentation, so its first documentation build failed validation. Filled in the title, author, description, pinout and datasheet; the worked-example documentation build passed.
- Docker and the local EDA tools are not installed. Used the template's GitHub Actions for the example instead of a local hardening run.
- Some earlier notes used old template versions and board details. Checked the current sources and recorded version-specific limits rather than treating the videos as current specifications.
- The first slide draft had repeated layouts and some clipped text. Redesigned it around worked examples, then checked every rendered slide and corrected the layout and notes.
- The revised slides still gave too little detail for an independent beginner. Built a comprehensive Word manual with why/do/check instructions, full source explanations, troubleshooting and exercises. The review identified small screenshots, code breaks and a missing optional PDK path; enlarged the figures and corrected the layout and setup instructions.
- Expanded the full guide into a course-sized slide deck after the request for slides. The rendered review caught small binary digits, omitted exercise conditions, code captions touching dark cards and source screenshots that were too small. Corrected these, added enlarged native screenshot details and checked the final export.

## Remaining Tasks

- Review the beginner manual and full slide course with the supervisor, then trial the learning sequence with a new student. Study/lab time has not yet been measured. The earlier overview's capture checklist is preserved separately in [the deck README](../docs/slides/README.md).
- Confirm the research template and neural-network scope, reproduce its example and revise the project timeline.
- Watch *Making ASICs* and *Manufacturing ASICs*. Website reading has been done; the videos remain pending.
- Review the risk assessment and confirm any required departmental form.
- Review and merge the teaching-example and weekly-work pull requests.

## Questions

1. Will the undergraduates use the flow in Semester 2 from January 2027, or in 2027–28? Which process and shuttle should the class target?
2. Is the manual and full slide course sequence suitable for beginners? Which sections should be taught in a lab and which studied independently?
3. Is the research template Caravel, Croc or another platform?
4. Which neural-network type, application or starting paper should I use?
5. Is a submission-ready verified layout sufficient, or should the accelerator be fabricated? If fabrication is required, which funded route and deadline apply?
6. Is the open-tool survey still wanted as a report chapter?
7. What are the interim-report, final-report and presentation deadlines?
8. Which licence should the repository and student slides use?
