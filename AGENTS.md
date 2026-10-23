# AGENTS.md: context for any AI assistant (or person) continuing this project

Read this file first. It is the full handover for the EE6019 research project, written so that any tool (Claude, ChatGPT, Gemini, Copilot, Cursor, Codex and so on) can carry on without access to earlier chats. Links to claude.ai documents are kept as references, but they only open for the owner's account, so everything you need is copied in here.

*Last updated: 23 October 2026 (supervisor redirected the research: RISC-V on an FPGA plus an accelerator chip; TinyQV simulation run).*

**Supervisor meeting, 23 October (11:00): the research direction changed.**
- **His suggestion:** put a RISC-V on an **FPGA** and build an **accelerator as the Tiny Tapeout chip**. The two talk over the chip's digital I/O.
- **The link:** model the link delay, so the result can say what an on-chip version would gain.
- **TinyQV:** "too small … not that useful".
  - First check which RISC-V designs already exist on Tiny Tapeout.
  - Otherwise use a "proper" 32-bit RISC-V that is not one of the largest.
- **Alternative:** lower the power of that 32-bit RISC-V, then tape it out.
- **What to accelerate:** research what runs much faster on a 130 nm chip than on a modern FPGA. His examples: convolution, tanh or sigmoid.
- **His main aim:** fabricate the chip and show a large speed-up. The choice of accelerator is open.
- **Literature:** RISC-V accelerators and ML accelerators.
- **Records:** notes in `logbook/week-04-meeting.md`. That day's TinyQV simulation (all tests pass; problems and fixes) is in `logbook/week-04.md`.
- **Effect on the plan:** the 18 October "A then B" plan below (an instruction extension inside TinyQV) is **superseded**. Kamrul has yet to choose between the supervisor's two options; see section 10.

**Supervisor meeting, 16 October (15:00):**
- **Teaching:** the shift-register tutorial is "exactly what I need". About 70 third-year students will use it from January 2027, each taking a small design through the full flow to tape-out. Send him the tutorial.
- **Research:** a larger, multi-tile design that follows the Tiny Tapeout flow, based on RISC-V and contributing something new rather than re-implementing an open core. Use what Tiny Tapeout offers as an SoC backbone.
- **Angles he suggested:**
  - ultra-low power
  - instruction extensions for machine learning or for (post-quantum) cryptography
  - constant power whatever the instruction
  - earlier group work: a small stochastic-computing RISC-V
- **Reports:** about one checked reference per page; presentations with at most two lines per bullet.
- **Records:** notes in `logbook/week-03-meeting.md`. The options and recommendation (an ML instruction extension for TinyQV, Tiny Tapeout's RISC-V SoC, compared with its existing NPU peripheral) are in `docs/research/riscv-research-angles.md`.
- **Chosen 18 October (Kamrul):** A then B. A is an ML instruction extension for TinyQV, by April. B is a stochastic-computing version over the summer, compared with A in one paper. To be confirmed with Prof. Popovici on 23 October. Start here: `docs/research/getting-started.md` (TinyQV in simulation) and `docs/research/reading-list.md`.

**Root layout correction, 16 October:** Kamrul explicitly requested that this checkout use the directory structure shown in the short lesson. The canonical project files now live at the repository root: `src/project.v`, `src/shift_register.v`, `src/config.json`, `test/{Makefile,tb.v,test.py,requirements.txt}`, `docs/info.md`, `info.yaml`, and four official Tiny Tapeout workflows. `.devcontainer`, `.vscode` and the upstream template licence are retained. The old standalone counter flow and its original CI/README/docs/images were preserved together in `archive/legacy-flow`; 14 original files were byte-checked after moving. Do not restore the old root layout. The starter ZIP is now generated from the canonical seven root design files. Current guide/slide copies use `*-root-layout.*`, leaving open Office documents undisturbed. Root RTL simulation passed and the deliberate wrong-shift mutation was caught. Later on 16 October, once GitHub Pages was enabled, the full Tiny Tapeout run passed at `66475c7`: GDS, precheck, gate-level test and viewer ([run 38924144510](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/actions/runs/38924144510)).

**Teaching revision, 16 October:** following Kamrul's review, the short guide now has a common commit/push node with arrows to independent RTL, docs and GDS workflows, then GDS arrows to precheck, GLS and viewer. Two dedicated GLS pages explain the netlist, shared port-level test, `GL_TEST` power-pin fixture, exact `gl_test` job/log/result/artifact route, failure checks and the distinction from timing sign-off. Current review editions are `docs/shift-register-quickstart/quickstart-revised.{docx,pdf}` (15 pages), `lesson-revised.{pptx,pdf}` (24 slides), the updated HTML and learning-pack ZIP. Earlier open Office files are retained. A genuine successful COUNTER GLS screenshot/log excerpt is explicitly labelled; the shift register's own physical and GLS run passed later on 16 October (see above). Learner/supervisor approval remains pending.

**Supervisor email, 12 October:** first become familiar with Tiny Tapeout's existing flow and chips/submissions, then take a simple circuit through the full design flow; he suggests an adder or a sequential circuit such as a counter. He aims for some submissions towards the end of the master's, with no particular shuttle, count, budget or exact date approved. He calls the former SoC backbone "carousel" and says he needs to check whether it is still available; do not treat this as confirmation of Caravel or Croc. The earlier accelerator direction is not cancelled or newly specified. The existing counter's full template run is relevant evidence; the newer shift register has since passed the full template run (16 October). Its suitability as a sequential example is an inference, pending his acceptance. The source PDF is retained in the private project's Drive Emails folder, titled `12th October 2026.pdf`; the detailed record is in the private tracker.

**Latest teaching direction (11 October):** Kamrul said the earlier manual and slides were too long and unhelpful from a learner's perspective. He requested a completely new, short walkthrough with simple language, clear steps, diagrams/screenshots and interaction, starting from an already-developed Verilog design. The new primary review candidate is `docs/shift-register-quickstart/`: an offline interactive HTML guide, a 13-page Word/PDF guide, a 20-slide PowerPoint/PDF lesson and an exact seven-file shift-register adaptation ZIP. It starts from an existing serial-in, parallel-out register and teaches pin mapping, wrapping, metadata/source lists, cocotb tests, template upload and workflow checks. Old materials remain historical references; their technical checks do not imply learner acceptance.

**New example verification:** the real shift-register RTL passes Icarus/cocotb simulation, and the test catches a deliberately reversed shift direction. Source lists and top-module names agree. On 16 October it also passed the physical build and gate-level test, here and in [tt-shift-register](https://github.com/mdkamrulislam-web/tt-shift-register); nothing has been submitted or fabricated. The HTML was checked on desktop/mobile and exports were rendered and visually checked. User/supervisor review of the new teaching approach remains pending.

**Current project record:** [private Project view](https://track.whoiskamrul.com/#/project). This holds the current progress, timeline, logs, meeting records, supervisor questions and deliverable status. Sign in with the existing tracker password. Keep the teaching files, code, evidence and logbook copies in this repository. Older plans below are historical where they disagree with a later confirmed decision.

**During future authorised project work:** read the tracker record before changing status, then record meaningful dated progress and update the affected deliverable, question or meeting. Use the authenticated agent interface described in the private tracker repository, preserve existing user notes, and read changes back. Do not include credentials or private calendar details here. Drafts, verified results and supervisor approval are distinct; record a meeting or sent email only when confirmed. Calendar scheduling remains in the existing calendar.

---

## 1. The project in one paragraph

EE6019 is the MEngSc (Electrical and Electronic Engineering) research project at University College Cork, 2026–27, supervised by **Prof. Emanuel Popovici**. The student is Kamrul (GitHub `mdkamrulislam-web`). Since the 2 Oct 2026 meeting the project has two parts. **Teaching:** document the existing **Tiny Tapeout** Verilog flow step by step so that UCC undergraduates can use it next year to make their own chips; Kamrul does *not* build a new flow. On 8 October Kamrul requested a comprehensive DOCX beginner manual with screenshots, reasons, instructions, checks and examples, without a length limit, then explicitly asked for the slides too. The 85-page manual and complete 195-slide course now support independent learning and teaching. The earlier 26-slide overview is preserved for history. **Research:** design a **neural-network accelerator** on a larger open template with a **RISC-V** core and take it through the full open flow to a layout ready for submission. **The project must be finished by 30 April 2027**; that date is fixed and cannot slip.

### How the scope got here

- **21 Sep 2026 (email):** Prof. Popovici suggested starting from Bo Yang's PhD thesis (UCC 2020, EDA for VLSI reliability) and mentioned other directions, including "a completely open flow for digital and use tinytapeouts".
- **24 Sep (options note):** Kamrul proposed four options from the thesis. Option C combined an open flow (Yosys, ABC, LibreLane, Tiny Tapeout on SKY130 or IHP SG13G2) with reliability-driven synthesis.
- **25 Sep (group meeting):** the project became the open flow: survey the free alternatives to Cadence and Synopsys, install an open flow, and build an ASIC with it. The group hopes to make chips for students next year with this flow, so this project is the first through it. He may let Kamrul build a chip "using both those open flows" (which two is unclear). He said he would send a website link (not yet received). Weekly Friday log entries feed the logbook in the final report; record mistakes and how they were fixed. Every project needs a short risk assessment.
- **30 Sep:** Prof. Popovici asked Kamrul to start exploring the flows and videos on **tinytapeout.com** (study path in section 6).
- **2 Oct (weekly meeting, plus his answers to the follow-up email):** no new flow: use the Tiny Tapeout flow and document it step by step for undergraduates, as PowerPoint slides (any format and length), up to the submission step. For the research, a larger template with a RISC-V core (heard as "carousel"; probably Caravel, possibly Croc; asked by email) to explore neural-network accelerators, taken through the full flow. Technology: whichever is available at that point (SkyWater 130 nm or IHP 130 nm). The website he meant on 25 Sep is Tiny Tapeout. Report dates to follow. He plans a batch of student chips next year; students who learn the flow now may become demonstrators. Notes: `logbook/week-01-meeting-prep.md`.

The thesis work (reliability-aware synthesis) is **out of scope** unless the supervisor asks for it; it is kept as an optional research extension. Analogue/mixed-signal and PCB work are also out of scope. FPGA work was out of scope too, until the 23 Oct meeting proposed an FPGA-hosted RISC-V driving the accelerator chip. The supervisor's other students' projects (FPGA place and route, PCB, option pricing, smart glasses) are unrelated; ignore them.

---

## 2. Deliverables and definition of done

Revised after the 2 Oct 2026 meeting.

| Deliverable | What it is | Where | Needed by |
|---|---|---|---|
| Tiny Tapeout beginner guide and slide course | Comprehensive DOCX/PDF manual and editable PowerPoint/PDF course: fundamentals, complete example, screenshots, browser steps, tests, checked layout and free stopping point; later submission and fabrication explained. | `docs/beginner-guide/`, `docs/slides/` | First version 9 Oct 2026 |
| Open-tool survey | Each flow stage mapped to its commercial tool and its open replacement | Report chapter 2 | To agree |
| Research design | Neural-network accelerator on the RISC-V template, verified and taken through the full flow to a submission-ready layout | Repo | Mar 2027 |
| Report, logbook, presentation | EE6019 submission, with weekly Friday logs and the risk assessment | UCC submission | Dates to follow |

**Background, not a deliverable:** the repo's own LibreLane flow (`make harden`, the counter) and the planned comparison with OpenROAD-flow-scripts were set up before 2 Oct. He did not ask for a separate flow; keep it only where it helps (understanding the stages, or hardening the research design locally).

**Done means:** an undergraduate can use the manual from first principles through a tested, checked and archived layout, explaining why each step is needed. Technical and visual checks have been completed; a trial with a new student and supervisor review are still required to establish usability. The research accelerator must pass simulation, synthesis, place and route, timing, DRC and LVS with no errors; Prof. Popovici must sign off the report and logbook.

---

## 3. Current repository layout (16 October 2026)

This checkout itself is now a Tiny Tapeout SKY Verilog project. Open its root,
not the documentation's portable starter folder, when following the lesson.

```text
.github/workflows/{test,docs,gds,fpga}.yaml   official template workflows
src/shift_register.v                       reusable eight-bit circuit
src/project.v                              fixed-port wrapper
src/config.json                            upstream physical-build settings
test/Makefile                              RTL/GLS source selection
test/tb.v                                  fixture, including GL_TEST power pins
test/test.py                               shared cocotb checks
test/requirements.txt                      upstream Python requirements
docs/info.md                               shift-register datasheet
info.yaml                                  metadata, pin map, module and sources
docs/shift-register-quickstart/             current lesson, exports and evidence
logbook/                                   weekly project records
archive/legacy-flow/                       preserved earlier standalone flow
```

The canonical seven adaptation files match the portable starter. The documentation
builders synchronise the portable copy from the root. Keep the three top-module
names and two source lists consistent. The wrapper is
`tt_um_student_shift_register`; serial data uses `ui_in[0]`, shift enable uses
`ui_in[1]`, and the output is `uo_out`. All bidirectional pins remain inputs.

The official template baseline is `68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a`.
Root infrastructure is copied from this baseline, including the 20 ns configuration
and cocotb 2.1.0 requirements. Project and documentation licensing beyond the
upstream template remains a supervisor question.

Local root RTL simulation has passed (one test, zero failures), and a reversed
shift direction fails as expected. Physical layout, precheck, timing and GLS
have not run for this shift register. The successful counter GLS screenshot
and earlier counter results remain clearly identified reference evidence.

Current review copies: `quickstart-root-layout.{docx,pdf}` (15 pages),
`lesson-root-layout.{pptx,pdf}` (24 slides), offline HTML and starter/learning ZIPs
under `docs/shift-register-quickstart`. User/supervisor acceptance remains pending.

The old `make sim`, `make harden`, two-PDK container and counter live together
under `archive/legacy-flow`. Their working directory is that archive folder.
Historical setup, flow notes, results and the previous handover are preserved
there. The archived CI definition is not an active root workflow.

---

## 4. Tool chain (open tool vs commercial equivalent)

This table is the core of the survey chapter.

| Stage | Open tool | Commercial equivalent |
|---|---|---|
| RTL simulation and testbench | Icarus Verilog or Verilator, with cocotb | Cadence Xcelium, Synopsys VCS |
| Lint | Verilator lint | Synopsys SpyGlass |
| Synthesis | Yosys with ABC | Synopsys Design Compiler, Cadence Genus |
| Floorplan, placement, CTS, routing | OpenROAD (driven by LibreLane or ORFS) | Cadence Innovus, Synopsys IC Compiler II |
| Parasitics and static timing | OpenRCX, OpenSTA | Cadence Tempus, Synopsys PrimeTime |
| DRC | Magic and KLayout (KLayout decks for IHP) | Siemens Calibre |
| LVS | Netgen (SKY130), KLayout (IHP) | Siemens Calibre |
| Gate-level simulation | Icarus Verilog with PDK cell models | Xcelium, VCS |
| Layout viewing | KLayout | Cadence Virtuoso |
| Packaging for tapeout | Tiny Tapeout template and GitHub Actions | Foundry sign-off kit |

Before 2 Oct the plan was to compare LibreLane with **OpenROAD-flow-scripts (ORFS)**; that is now optional (section 2).

---

## 5. PDK and shuttle

**Teaching example:** the root uses the official SKY130 template. The research process choice is still open. On 16 October the research was set as a multi-tile Tiny Tapeout design. The options note proposes TinyQV, which has been taped out on SKY130, IHP and GF180.

**Decided 2 Oct 2026:** the technology is whichever is available at that point, SkyWater 130 nm (SKY130) or IHP 130 nm (SG13G2); no preference. The research template may fix it (Caravel runs on SKY130; Croc targets IHP). Whether the accelerator is actually submitted to a shuttle is not decided; the deliverable is a submission-ready layout.

Shuttle dates from <https://tinytapeout.com/chips/>, read 30 Sep 2026. Re-check before committing to dates.

| Shuttle | PDK | Closes | Fit |
|---|---|---|---|
| TTSKY26d | SKY130 | 30 Nov 2026 | Too early for the demonstrator |
| TTGF26c | GF180 | 7 Dec 2026 | Too early (TTGF26d, same date, is reserved for the ArtScience Museum Singapore) |
| **TTIHP27a** | IHP SG13G2 | **March 2027** (day not published; delivery Q1 2028) | Target |
| TTGF27a | GF180 | April 2027 | Fallback |
| TTSKY27a | SKY130 | May 2027 | After the project ends |

- Fabs and MPW services behind each shuttle (IHP direct; SkyWater via ChipFoundry; GlobalFoundries via wafer.space) are in `docs/tiny-tapeout.md`, "Who makes the chips now".
- IHP also runs its own low-cost open-source MPW (about 2,800 EUR/mm², roughly 8-month turnaround), possibly useful for next year's student chips.
- Chips take 6 to 9 months, up to a year, so no silicon will come back before 30 Apr 2027. The deliverable is a verified, submitted (or submission-ready) GDS.
- Do **not** submit anything at app.tinytapeout.com without the supervisor's go-ahead: a submission reserves a paid tile.

---

## 6. Tiny Tapeout: what we learned

Study path doc (owner-only link): <https://claude.ai/code/artifact/919efaa6-7ecf-43b1-a6d9-5c519e6cfcb3>

- **Four flows**, all ending in a GitHub repo whose Actions build the GDS, submitted at app.tinytapeout.com: **Wokwi** (gates in a browser; beginners), **Verilog/HDL** (`src/`, cocotb tests in `test/`, `info.yaml`; Actions `test`, `gds` via LibreLane, `docs`, `fpga`; this is the one we use), **local hardening** (`tt/tt_tool.py` with LibreLane 3.0.3 via pip), and **analogue** (out of scope).
- **IHP template:** <https://github.com/TinyTapeout/ttihp-verilog-template>. As of 30 Sep 2026 it has `src/config.json` (LibreLane settings, 50 MHz default), four workflows (`test`; `gds` with precheck, gate-level test and viewer; `docs`; `fpga`, manual), actions pinned to tag `ttihp26b`, and `cocotb==2.0.1`. Notes from the videos, what has changed since they were made, and the counter-to-template checklist are in `docs/tiny-tapeout.md`.
- **Tile limits:** about 167 × 108 µm on IHP (160 × 100 µm in older material), roughly 1,000 gates, 8 inputs, 8 outputs, 8 bidirectional pins, `clk` and `rst_n`, at least 50 MHz. The top module must be named `tt_um_<user>_<name>` with the fixed port list `ui_in, uo_out, uio_in, uio_out, uio_oe, ena, clk, rst_n`. The demonstrator must fit this or use extra tiles.
- **Version gap:** checked 7 Oct, the SKY130 `ttsky26d` action defaults to LibreLane 3.0.14 and IHP `ttihp26b` to 3.0.5; this repo's image ships 3.1.0.dev3. See the dated source links in `docs/tiny-tapeout.md`. Record each actual run's versions; support-tool branches may move even when the action tag is unchanged.
- **IHP terms:** chips stay IHP's property, lent for 2 years, no resale, shipping only within the EU and Switzerland (Ireland is fine).
- **Class bundles** (likely route for next year's students): 5 projects + 1 board EUR 565; 25 + 3 EUR 2,195; 75 + 5 EUR 5,325 (<https://tinytapeout.com/teaching/>).
- **"Both open flows"** (25 Sep): after the 2 Oct meeting, most likely Tiny Tapeout (small designs; teaching) and the larger RISC-V template (research). Not yet confirmed in those words.

**Videos, in watching order:** [From idea to chip design in minutes](https://www.youtube.com/watch?v=qVWq_XZko-M); [Making ASICs](https://www.youtube.com/watch?v=dckPKyO2nSo); [Manufacturing ASICs](https://www.youtube.com/watch?v=aBDJQ9NYTEU); [Getting started with Wokwi](https://www.youtube.com/watch?v=F1SwXF2ny4g); [Working with an HDL](https://www.youtube.com/watch?v=KbWb6xd9jFE); [Get your submission ready](https://www.youtube.com/watch?v=fCGPKdmM3Dc); optional [Build Your First Chip with Tiny Tapeout](https://www.youtube.com/watch?v=UVZK-kmN7wc). Reading: [Making ASICs](https://tinytapeout.com/making_asics/), [FAQ](https://tinytapeout.com/faq/), [SiliWiz](https://tinytapeout.com/siliwiz/), [Digital design lessons 1–3](https://tinytapeout.com/digital_design/), [HDL rules](https://tinytapeout.com/hdl/important/), [Testing](https://tinytapeout.com/hdl/testing/), [Local hardening](https://tinytapeout.com/guides/local-hardening/), [Specs](https://tinytapeout.com/specs/), [basic](https://tinytapeout.com/guides/workshop/) and [advanced](https://tinytapeout.com/guides/advanced-workshop/) workshops.

**Worked example (moved into week 2):** the counter is prepared in the official SKY130 template at [tt-sky130-counter](https://github.com/mdkamrulislam-web/tt-sky130-counter), without submitting. The wrapper is `tt_um_mdkamrulislam_counter`, with enable on `ui_in[0]`, count on `uo_out`, and wrap on `uio_out[0]`. Its cocotb test uses only top-level ports. Get `test`, `gds` (including precheck and gate-level test), and `docs` green before calling it complete. The minimal counter assumes synchronous enable; physical buttons need synchronisation and debouncing.

Optional local IHP hardening reference, separate from the week 2 SKY130 example; the commands have not been run in this session:

```bash
export PDK_ROOT=~/ttsetup/pdk PDK=ihp-sg13g2 LIBRELANE_TAG=3.0.5
pip install librelane==$LIBRELANE_TAG
./tt/tt_tool.py --create-user-config --ihp
./tt/tt_tool.py --harden --ihp
./tt/tt_tool.py --print-warnings --ihp
```

A comparison with this repository's local flow is optional background work; confirm whether the tool survey is still a report deliverable.

---

## 7. Timeline

**Needs re-planning.** The provisional plan in `docs/research/riscv-research-angles.md` (section 4) was superseded on 23 October (FPGA RISC-V plus an accelerator chip). Re-plan once Kamrul chooses the option and the accelerator. The tables below were written before the 2 Oct meeting changed the scope (section 1). Weeks 2 and 3 are updated; from week 4 on, re-plan around the research template once Prof. Popovici confirms which one he meant.

Month-level milestones (pre-2 Oct):

| Month | Milestone that shows it is done |
|---|---|
| Oct 2026 | Counter clean on SKY130 and IHP (done 30 Sep); survey table drafted; container installs on a laptop and a lab PC |
| Nov 2026 | LibreLane and ORFS compared; flow accepts Tiny Tapeout projects; demonstrator chosen |
| Dec 2026 | Student guide v0 tested by a classmate; interim note sent |
| Feb 2027 | Demonstrator passes its testbench and fits the tile |
| Mar 2027 | Clean DRC, LVS and timing; Tiny Tapeout submission (if approved) |
| Apr 2027 | A classmate follows the guide on a clean machine; report submitted |

Week by week (one row per Friday log; weeks are counted from the project start, week 1 = 28 Sep to 2 Oct 2026; exam and break weeks are guesses at the UCC calendar):

| Friday | Project week | Focus | What the log reports |
|---|---|---|---|
| 2 Oct | 1 | Plan, scope questions, first counter run (PR #1) | Send plan and scope questions; ask for the website link; first log |
| 9 Oct | 2 | Tiny Tapeout flow slides; remaining videos; risk assessment | First version of the slides; screenshots from Kamrul's template fork; risk assessment drafted |
| 16 Oct | 3 | Finish the slides from his feedback; read up on the research template once confirmed | Slides v2; template's example running |
| 23 Oct | 4 | Local hardening with `tt_tool`; start tool survey | LibreLane 3.0.3 vs 3.1: same result or not |
| 30 Oct | 5 | Survey write-up; PDK and shuttle decision | Report ch. 2 draft; decision recorded |
| 6 Nov | 6 | Second flow: ORFS runs the counter | ORFS clean on IHP (and SKY130) in the same container |
| 13 Nov | 7 | Compare LibreLane with ORFS | Table: area, slack, run time, set-up effort |
| 20 Nov | 8 | Flow accepts a TT project as it stands | `src/`, `test/`, `info.yaml`; cocotb + gate-level tests in CI |
| 27 Nov | 9 | Choose the demonstrator | Three candidates, one agreed; spec with pin map, 1,000-gate budget |
| 4 Dec | 10 | Student guide v0: install and first run | Classmate follows it on a clean machine; interim note |
| 11, 18 Dec | 11–12 | Exams: light weeks | Short logs; tidy docs |
| 25 Dec, 1 Jan | 13–14 | Christmas break | No log expected (confirm) |
| 8 Jan | 15 | Re-run the flow; begin demonstrator RTL | Flow still clean; RTL skeleton |
| 15 Jan | 16 | Demonstrator RTL core | Core blocks with cocotb unit tests |
| 22 Jan | 17 | Full testbench; first harden on IHP | Every spec feature tested; first area/timing |
| 29 Jan | 18 | Fit the tile and meet timing | Fits planned tiles at target clock |
| 5 Feb | 19 | Gate-level sim clean; guide ch. 2–3 | GL tests pass; guide covers reports, DRC and timing fixes |
| 12 Feb | 20 | Design freeze candidate | `docs/info.md`; freeze tag |
| 19 Feb | 21 | Sign-off round 1 on IHP | DRC, LVS, antenna, timing across corners |
| 26 Feb | 22 | Fix sign-off issues | All closed; TT actions green on the submission repo |
| 5 Mar | 23 | Final checks; confirm TTIHP27a date and budget | Go / no-go from supervisor |
| 12 Mar | 24 | Submit to TTIHP27a, if approved | Submission confirmed, or tagged release of the verified GDS |
| 19 Mar | 25 | Buffer for a shuttle slip; start report | Methods chapter |
| 26 Mar | 26 | Report: results | Flow comparison and demonstrator results |
| 2 Apr | 27 | Student guide complete; dry runs | Classmates run the guide on clean machines |
| 9 Apr | 28 | Fix the guide; full report draft | Draft sent to supervisor |
| 16 Apr | 29 | Revise report; compile logbook | Feedback addressed |
| 23 Apr | 30 | Presentation and demo | Slides and demo rehearsed |
| 30 Apr | 31 | Submit | Report, logbook, v1.0 release of the repo |

Current status and milestones are in the [private Project view](https://track.whoiskamrul.com/#/project). The older owner-only plan <https://claude.ai/code/artifact/a8f92d4e-ab03-4128-aa07-d5932dd6f512> is a historical reference; it does not override later recorded decisions. Retain section 10 as a repository summary and check the tracker before updating it.

---

## 8. Weekly routine: Friday log and meeting

- Kamrul meets Prof. Popovici **every Friday, 11:00–12:00**. The week's log must be written and the work pushed **before** the meeting.
- Save each log as `logbook/week-<nn>.md`, numbered by project week from the start on 28 Sep 2026 (e.g. `logbook/week-02.md` for 5 to 9 Oct), with the dates in the heading, and email the same text to the supervisor before the meeting. Failed runs count: he asked for mistakes and fixes to be recorded.
- Bring one screenshot or report (layout, timing summary, DRC count) to each meeting.

Template:

```markdown
# Week 2 (5 to 9 Oct 2026)

## Done
-

## Problems and how I fixed them
-

## Evidence
- Commit or PR link, screenshot, report numbers

## Next week
-

## Questions for Prof. Popovici
-
```

---

## 9. Questions for the supervisor

**Answered on 2 Oct 2026:** build a new flow? No, use and document Tiny Tapeout's. Main deliverables? Section 2. Accelerator scope? Full flow to a submission-ready layout. Technology? Whichever is available (SKY130 or IHP). Slides? Any format and length. Website link? Tiny Tapeout. Report dates? To be given later.

**Answered on 16 Oct 2026 (meeting):**
- **When:** the class uses the flow from January 2027 (about 70 designs).
- **Research platform:** what Tiny Tapeout offers, on RISC-V, using several tiles.
- **Angle:** to be chosen by Kamrul from the suggested list.

**Answered on 23 Oct 2026 (meeting):**
- **TinyQV as the backbone?** No, it is too small.
- **What instead?** A RISC-V on an FPGA plus an accelerator chip (or, alternatively, a lower-power 32-bit RISC-V).
- **Is fabrication wanted?** Yes, through Tiny Tapeout.

**Still open:**

1. Which accelerator? He left it to research (convolution, tanh/sigmoid were examples). Does stochastic computing (his group's ASAP 2019 work) fit?
2. Which shuttle for the January class, and what tile budget for this design?
3. The exact interim-report, seminar and dissertation dates. He referred these to the module coordinator.
4. Should the summer research project (EE6008) continue this design?

Also open: whether the open-tool survey (section 4) is still wanted as a report chapter; licence for this (now public) repository and the student material.

---

## 10. Next steps (updated 23 October 2026)

- [x] Correct the local project root to match the short guide's Tiny Tapeout tree.
- [x] Preserve the earlier standalone flow under `archive/legacy-flow` and check its original file bytes.
- [x] Verify the real root shift register with local RTL simulation and a wrong-direction mutation.
- [x] Add GLS pages, connected workflow arrows and visible screenshot step 2; refresh review copies and downloads.
- [ ] Kamrul completes his hands-on template adaptation and checks RTL/docs/GDS/GLS for the same final commit.
- [ ] User/supervisor review and a beginner trial of the short lesson.
- [x] Record the 16 October meeting (`logbook/week-03-meeting.md`) and draft the week 3 log (sent together with week 2).
- [x] Compare research angles; recommendation in `docs/research/riscv-research-angles.md`.
- [ ] Send Prof. Popovici the tutorial (he asked for it on 16 October).
- [x] Discuss the research angle and backbone on 23 October. He redirected the research (top of this file).
- [x] Run TinyQV in simulation (`docs/research/getting-started.md`, steps 1–2), 23 October: CPU 11/11, hello, NPU 2/2 pass (`logbook/week-04.md`). The toolchain and software-baseline steps are paused, because TinyQV is no longer the backbone.

**From 23 October:**
- [ ] List the RISC-V designs already on Tiny Tapeout: 32-bit or not, size, licence, FPGA-ready.
- [ ] Choose a small 32-bit RISC-V for the FPGA (PicoRV32, SERV, VexRiscv, Ibex …); find which FPGA board UCC has.
- [ ] Literature survey: RISC-V accelerators and ML accelerators (what is accelerated, data needed, speed-up). Extend `docs/research/reading-list.md`; about 30 checked references for the interim report.
- [ ] Shortlist two or three functions to accelerate and estimate the work per byte over the Tiny Tapeout I/O.
- [ ] Kamrul chooses between the accelerator chip and the low-power RISC-V, then revise the timeline (section 7).
- [ ] Email Prof. Popovici a summary of the 23 October direction to confirm it was understood.
- [ ] Confirm the interim-report, seminar and dissertation dates with the module coordinator.
- [ ] Finish the remaining ASIC videos and review the risk assessment.

The 12 October email confirms a full simple-design flow as the immediate task
and an aim for submissions near the end of the master's; it sets no exact
submission count, shuttle, budget or fabrication date.

---

## 11. Risks

| Risk | Fallback |
|---|---|
| TTIHP27a slips, or no budget for a tile | Deliver a verified, tapeout-ready GDS; submit to a later shuttle |
| Tools do not install cleanly on lab PCs or laptops | One pinned container for everything; test the guide on a clean machine monthly |
| IHP support less mature than SKY130 | Bring up on SKY130 first; PDK stays one setting; ask on the IHP and LibreLane forums |
| Design too large for the tile or misses timing | Choose a small design early; run the full flow weekly from January |
| Tool versions change | Pin versions; upgrade only on purpose, with a log entry |
| Exams in December and January | Front-load the survey and first full runs into October and November |
| Laptop or disk failure | Push to GitHub at least every Friday |

---

## 12. Working conventions for whoever continues

- **British English** in all writing (optimisation, analogue, behaviour, modelling).
- Every flow change goes through a **pull request**; CI runs the reference design so a broken flow is caught at once.
- The current Tiny Tapeout infrastructure baseline and action tags are recorded in the root README and workflows. Keep upstream template settings intact during this lesson. The archived standalone flow pins its own image in `archive/legacy-flow/env/tools.env`.
- Each time a step works, write the **student-guide paragraph** for it that same week.
- When showing Kamrul code changes, show only the relevant changes and say where they go.
- Kamrul has industry design-verification experience (UVM, SystemVerilog, gate-level sim), so verification is his strength; physical design is the new part. Explain PD steps, not testbench basics.
- **This repo may become public:** keep personal details (contact details, ID numbers, coursework, private schedule) out of it.
- Keep this file current: when a decision is made or a milestone lands, update sections 3, 5, 9 and 10 and the "Last updated" date.

## 13. Sources

- Supervisor email (19–21 Sep 2026), options note (24 Sep), meeting transcripts (25 Sep; 2 Oct, with audio), Bo Yang's thesis: Kamrul's Google Drive folder "EE6019 - Research Project" (owner-only link): <https://drive.google.com/drive/folders/1W5qhFknb5gOf17Vi74A2wL_OdaEEyaIn>. Subfolders: Documentations, Emails, Papers, Weekly Project Meetings.
- Research template candidates: Caravel <https://github.com/chipfoundry/caravel_user_project>; Croc / HyperCroc (ETH Zurich PULP group, IHP 130 nm) <https://arxiv.org/abs/2603.12308>.
- Tiny Tapeout: <https://tinytapeout.com/chips/>, <https://tinytapeout.com/faq/>, <https://tinytapeout.com/teaching/>, Hackster article on the IHP shuttle terms.
- IHP low-cost open-source MPW: <https://www.ihp-microelectronics.com/services/research-and-prototyping-service/mpw-prototyping-service/low-cost-open-source-mpw-access-1>
- LibreLane: <https://github.com/librelane/librelane>; IIC-OSIC-TOOLS: <https://github.com/iic-jku/IIC-OSIC-TOOLS>
