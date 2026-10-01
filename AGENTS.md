# AGENTS.md: context for any AI assistant (or person) continuing this project

Read this file first. It is the full handover for the EE6019 research project, written so that any tool (Claude, ChatGPT, Gemini, Copilot, Cursor, Codex and so on) can carry on without access to earlier chats. Links to claude.ai documents are kept as references, but they only open for the owner's account, so everything you need is copied in here.

*Last updated: 1 October 2026 (project week 1).*

---

## 1. The project in one paragraph

EE6019 is the MEngSc (Electrical and Electronic Engineering) research project at University College Cork, 2026–27, supervised by **Prof. Emanuel Popovici**. The student is Kamrul (GitHub `mdkamrulislam-web`). The goal is an **open-source chip-development flow**: a documented, reproducible, fully open digital flow from Verilog RTL to a sign-off-clean GDSII layout, which next year's UCC students can install and follow to make their own chips (most likely through Tiny Tapeout). Kamrul's own design is the first one through the flow and proves that it works. **The project must be finished by 30 April 2027**; that date is fixed and cannot slip.

### How the scope got here

- **21 Sep 2026 (email):** Prof. Popovici suggested starting from Bo Yang's PhD thesis (UCC 2020, EDA for VLSI reliability) and mentioned other directions, including "a completely open flow for digital and use tinytapeouts".
- **24 Sep (options note):** Kamrul proposed four options from the thesis. Option C combined an open flow (Yosys, ABC, LibreLane, Tiny Tapeout on SKY130 or IHP SG13G2) with reliability-driven synthesis.
- **25 Sep (group meeting):** the project became the open flow: survey the free alternatives to Cadence and Synopsys, install an open flow, and build an ASIC with it. The group hopes to make chips for students next year with this flow, so this project is the first through it. He may let Kamrul build a chip "using both those open flows" (which two is unclear). He said he would send a website link (not yet received). Weekly Friday log entries feed the logbook in the final report; record mistakes and how they were fixed. Every project needs a short risk assessment.
- **30 Sep:** Prof. Popovici asked Kamrul to start exploring the flows and videos on **tinytapeout.com** (study path in section 6).

The thesis work (reliability-aware synthesis) is **out of scope** unless the supervisor asks for it; it is kept as an optional research extension. Analogue/mixed-signal, FPGA and PCB work are also out of scope. The supervisor's other students' projects (FPGA place and route, PCB, option pricing, smart glasses) are unrelated; ignore them.

---

## 2. Deliverables and definition of done

| Deliverable | What it is | Where | Needed by |
|---|---|---|---|
| Open-tool survey | Each flow stage mapped to its commercial tool and its open replacement, with maturity notes | Report chapter 2 | End Oct 2026 |
| Reproducible environment | One pinned container plus install notes for laptops and lab PCs | This repo | Mid Oct 2026 |
| Reference flow | Make targets for simulate, synthesise, place and route, timing, DRC, LVS, gate-level sim; PDK chosen by one setting | This repo | Nov 2026 |
| Worked example | A small design through every stage with reports kept | This repo | Nov 2026 (counter), Mar 2027 (real design) |
| Demonstrator design | A useful block, verified and tapeout-ready; submitted to Tiny Tapeout if approved | Repo, then shuttle | Mar 2027 |
| Student guide | Lab-style handouts: install, first run, reading reports, fixing DRC and timing errors | `docs/`, later a website | Apr 2027 |
| Report, logbook, presentation | EE6019 submission, with weekly Friday logs and the risk assessment | UCC submission | Dates to confirm |

**Done means:** a student who has never used the tools can follow the guide from a clean machine to a GDS in one lab session; Kamrul's design passes simulation, synthesis, place and route, timing, DRC and LVS with no errors; and Prof. Popovici has signed off the report and logbook.

**Research angle for the report:** a survey of open tools against Cadence and Synopsys, plus one measured comparison (for example LibreLane vs OpenROAD-flow-scripts, or SKY130 vs IHP SG13G2: area, slack, run time, set-up effort).

---

## 3. Current state of the repository (1 Oct 2026)

- `main` holds the working flow. [PR #1](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/pull/1) (the flow) and [PR #2](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/pull/2) (this file) were merged on 1 Oct 2026, and CI is green on `main` for both PDKs. `README.md`, `docs/setup.md` and `docs/flow.md` are the user-facing documentation.
- Kamrul is new to physical design. `docs/learning-path.md` is his hands-on route through the flow (install, read the reports, break it on purpose, a small design of his own), and is also the start of the student guide.
- Friday logs live in `logbook/`; `logbook/week-01.md` is the first.

### What the flow contains

```
Makefile                     entry points (below)
env/tools.env                pinned container image (tag + digest)
scripts/run-in-container.sh  runs each command inside the container as the host user
scripts/summary.py           prints the DRC / LVS / timing sign-off table of a run
designs/counter/src/counter.v      8-bit counter with enable and wrap flag
designs/counter/tb/counter_tb.v    self-checking testbench, prints "PASS" on success
designs/counter/config.json        LibreLane config (50 MHz, 150 x 150 um die)
docs/setup.md, docs/flow.md        install guide (Linux, macOS, WSL2, Podman), stage-by-stage walkthrough
docs/counter-*.png                 layout renders
docs/learning-path.md              hands-on exercises for someone new to physical design
docs/tiny-tapeout.md               Tiny Tapeout notes: how it works, changes since the videos, what it means for the flow
logbook/week-<nn>.md               Friday logs (project week number)
logbook/week-01-meeting-prep.md    checklist, summary and likely questions for the 2 Oct meeting; meeting notes go at its end
.github/workflows/flow.yml         CI: lint + Icarus + Verilator sim, then harden on sky130A and ihp-sg13g2
```

### Tool environment

Every tool and PDK comes from one Docker image, **IIC-OSIC-TOOLS `hpretl/iic-osic-tools:2026.09`**, pinned by digest in `env/tools.env` (about 3.9 GB download, 17 GB on disk, amd64 and arm64). Nothing but Docker (or Podman), `make`, `python3` and `git` is installed on the host.

| Tool | Version in the image |
|---|---|
| LibreLane (successor to OpenLane 2, FOSSi Foundation) | 3.1.0.dev3 |
| Yosys | 0.69 |
| OpenROAD | 26Q3-2443 |
| Magic | 8.3.684 |
| KLayout | 0.30.5 |
| Icarus Verilog | 14.0 (devel) |
| Verilator | 5.052 |
| PDKs | `sky130A`, `ihp-sg13g2`, `gf180mcuD` |

### How to run it

```bash
make sim                             # Icarus simulation of DESIGN (default: counter)
make sim-verilator                   # same testbench, Verilator
make lint                            # Verilator lint
make harden                          # RTL to GDS with LibreLane, PDK=sky130A by default
make summary                         # sign-off table for the last harden
make harden summary PDK=ihp-sg13g2   # same design on IHP
make shell                           # shell inside the tool container
# knobs: DESIGN=<name>  PDK=sky130A | ihp-sg13g2 | gf180mcuD
```

New designs go in `designs/<name>/{src,tb,config.json}`; outputs land in `designs/<name>/runs/<pdk>/` (not committed). The Makefile passes `--pdk/--scl` explicitly because the image defaults to IHP.

### First result (30 Sep 2026): the counter is sign-off clean on both PDKs

| Check | SKY130 (`sky130_fd_sc_hd`) | IHP SG13G2 (`sg13g2_stdcell`) |
|---|---|---|
| Simulation (Icarus, Verilator) | pass | pass |
| DRC (Magic, KLayout) / LVS / antenna | 0 / 0 / 0 | 0 / 0 / 0 |
| Setup / hold violations | 0 / 0 | 0 / 0 |
| Worst setup / hold slack | 9.17 ns / 0.11 ns | 10.34 ns / 0.13 ns |
| Standard cells (incl. fill, taps) | 298 | 68 |

### Notes for cloud or sandboxed AI sessions

- Start `dockerd` yourself if no daemon is running.
- Docker Hub works but rate-limits anonymous pulls; ghcr.io blob downloads (the official OpenLane 2 image) and cachix may be blocked by proxies. The pinned IIC-OSIC-TOOLS image from Docker Hub is the route that worked.
- You need about 20 GB of free disk for the image.
- YouTube pages generally cannot be fetched from cloud sessions.

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

Plan: build on LibreLane in the pinned container, keep the PDK a single setting, and run the same design through **OpenROAD-flow-scripts (ORFS)** as the second flow for comparison.

---

## 5. PDK and shuttle decision (open)

**Recommendation (not yet approved): IHP SG13G2 as the target, SKY130 for bring-up.** GF180 is the fallback.

Shuttle dates from <https://tinytapeout.com/chips/>, read 30 Sep 2026. Re-check before committing to dates.

| Shuttle | PDK | Closes | Fit |
|---|---|---|---|
| TTSKY26d | SKY130 | 30 Nov 2026 | Too early for the demonstrator |
| TTGF26c / TTGF26d | GF180 | 7 Dec 2026 | Too early |
| **TTIHP27a** | IHP SG13G2 | **March 2027** (day not published; delivery Q1 2028) | Target |
| TTGF27a | GF180 | April 2027 | Fallback |
| TTSKY27a | SKY130 | May 2027 | After the project ends |

- IHP also runs its own low-cost open-source MPW (about 2,800 EUR/mm², roughly 8-month turnaround), possibly useful for next year's student chips.
- Chips take 6 to 9 months, up to a year, so no silicon will come back before 30 Apr 2027. The deliverable is a verified, submitted (or submission-ready) GDS.
- Do **not** submit anything at app.tinytapeout.com without the supervisor's go-ahead: a submission reserves a paid tile.

---

## 6. Tiny Tapeout: what we learned

Study path doc (owner-only link): <https://claude.ai/code/artifact/919efaa6-7ecf-43b1-a6d9-5c519e6cfcb3>

- **Four flows**, all ending in a GitHub repo whose Actions build the GDS, submitted at app.tinytapeout.com: **Wokwi** (gates in a browser; beginners), **Verilog/HDL** (`src/`, cocotb tests in `test/`, `info.yaml`; Actions `test`, `gds` via LibreLane, `docs`, `fpga`; this is the one we use), **local hardening** (`tt/tt_tool.py` with LibreLane 3.0.3 via pip), and **analogue** (out of scope).
- **IHP template:** <https://github.com/TinyTapeout/ttihp-verilog-template>. As of 30 Sep 2026 it has `src/config.json` (LibreLane settings, 50 MHz default), four workflows (`test`; `gds` with precheck, gate-level test and viewer; `docs`; `fpga`, manual), actions pinned to tag `ttihp26b`, and `cocotb==2.0.1`. Notes from the videos, what has changed since they were made, and the counter-to-template checklist are in `docs/tiny-tapeout.md`.
- **Tile limits:** about 167 × 108 µm on IHP (160 × 100 µm in older material), roughly 1,000 gates, 8 inputs, 8 outputs, 8 bidirectional pins, `clk` and `rst_n`, at least 50 MHz. The top module must be named `tt_um_<user>_<name>` with the fixed port list `ui_in, uo_out, uio_in, uio_out, uio_oe, ena, clk, rst_n`. The demonstrator must fit this or use extra tiles.
- **Version gap:** Tiny Tapeout pins LibreLane 3.0.3; our image ships 3.1. Check that a design clean in one is clean in the other.
- **IHP terms:** chips stay IHP's property, lent for 2 years, no resale, shipping only within the EU and Switzerland (Ireland is fine).
- **Class bundles** (likely route for next year's students): 5 projects + 1 board EUR 565; 25 + 3 EUR 2,195; 75 + 5 EUR 5,325 (<https://tinytapeout.com/teaching/>).
- **"Both open flows"** might mean LibreLane + ORFS, or Tiny Tapeout's GitHub Actions flow + local LibreLane. Ask the supervisor.

**Videos, in watching order:** [From idea to chip design in minutes](https://www.youtube.com/watch?v=qVWq_XZko-M); [Making ASICs](https://www.youtube.com/watch?v=dckPKyO2nSo); [Manufacturing ASICs](https://www.youtube.com/watch?v=aBDJQ9NYTEU); [Getting started with Wokwi](https://www.youtube.com/watch?v=F1SwXF2ny4g); [Working with an HDL](https://www.youtube.com/watch?v=KbWb6xd9jFE); [Get your submission ready](https://www.youtube.com/watch?v=fCGPKdmM3Dc); optional [Build Your First Chip with Tiny Tapeout](https://www.youtube.com/watch?v=UVZK-kmN7wc). Reading: [Making ASICs](https://tinytapeout.com/making_asics/), [FAQ](https://tinytapeout.com/faq/), [SiliWiz](https://tinytapeout.com/siliwiz/), [Digital design lessons 1–3](https://tinytapeout.com/digital_design/), [HDL rules](https://tinytapeout.com/hdl/important/), [Testing](https://tinytapeout.com/hdl/testing/), [Local hardening](https://tinytapeout.com/guides/local-hardening/), [Specs](https://tinytapeout.com/specs/), [basic](https://tinytapeout.com/guides/workshop/) and [advanced](https://tinytapeout.com/guides/advanced-workshop/) workshops.

**Planned exercise (week 3):** put the counter through the IHP template without submitting. Use the template, copy the RTL into `src/`, rename the top to `tt_um_mdkamrulislam_counter` with the fixed ports, fill in `info.yaml` and `docs/info.md`, adapt `test/test.py` (cocotb; `cd test && pip install -r requirements.txt && make -B`), push and get `test`, `gds`, `docs` green. Then harden locally:

```bash
export PDK_ROOT=~/ttsetup/pdk PDK=ihp-sg13g2 LIBRELANE_TAG=3.0.3
pip install librelane==$LIBRELANE_TAG
./tt/tt_tool.py --create-user-config --ihp
./tt/tt_tool.py --harden --ihp
./tt/tt_tool.py --print-warnings --ihp
```

Compare area, cell count, slack and run time with `make harden PDK=ihp-sg13g2` here. That is the first entry of the tool survey.

---

## 7. Timeline

Month-level milestones:

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
| 9 Oct | 2 | Merge PR #1; Tiny Tapeout study path parts 1–2 | Notes from videos, FAQ, SiliWiz, Wokwi; risk assessment drafted |
| 16 Oct | 3 | Counter on the TT IHP Verilog template | Actions green (test, gds, docs); GDS screenshot |
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

The full plan doc (owner-only link) has a Status column per week: <https://claude.ai/code/artifact/a8f92d4e-ab03-4128-aa07-d5932dd6f512>. If you cannot open it, track status in this file instead (section 10).

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

## 9. Open questions for the supervisor

Five answers would lock the plan:

1. Is the documented, reusable flow the main deliverable, with Kamrul's chip as the first worked example? *(default: yes)*
2. Which two "open flows" did he mean? *(guess: LibreLane and ORFS; or TT Actions flow + local LibreLane)*
3. Is a real Tiny Tapeout submission expected, and is there budget for a tile on TTIHP27a?
4. Which PDK does he prefer, and does the group have links with IHP? *(default: IHP target, SKY130 bring-up)*
5. What are the fixed dates for the interim report, final report and presentation?

Also open: the website link he promised; whether the thesis's reliability work should carry over (default: optional extension only); how students should install the flow (container, lab image, or GitHub template with CI); which example design; which machine to use (laptop, lab PC or server account); licence for this repository.

---

## 10. Next steps (as of 1 Oct 2026, evening)

- [ ] Send the plan and scope questions to Prof. Popovici; ask for the website link.
- [ ] 2 Oct meeting: prepare with `logbook/week-01-meeting-prep.md`; afterwards record his answers there and update sections 5, 9 and 10.
- [x] Draft the first Friday log (`logbook/week-01.md`) for the 2 Oct meeting; Kamrul to check it and email it.
- [x] Review and merge PR #1 (merged 1 Oct).
- [ ] Work through `docs/learning-path.md` exercises 1 to 4 on his own laptop (week 2).
- [ ] Work through the Tiny Tapeout study path, then start the open-tool survey table. *(1 Oct: five videos done from transcripts, notes in `docs/tiny-tapeout.md`; still to do: Making ASICs, Manufacturing ASICs, FAQ, SiliWiz, Wokwi.)*
- [ ] Add a gate-level simulation target (`make gl-sim`) on the routed netlist; Tiny Tapeout already runs one in CI.
- [ ] Draft the one-page risk assessment (desk and computer work: display-screen use, laptop batteries and chargers, fire exits).
- [ ] After that: gate-level simulation and cocotb testbenches in the flow; counter on the TT IHP template (week 3).

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
- Tool and PDK versions are **pinned** in `env/tools.env` and listed in the README. Upgrade only on purpose and record it.
- Each time a step works, write the **student-guide paragraph** for it that same week.
- When showing Kamrul code changes, show only the relevant changes and say where they go.
- Kamrul has industry design-verification experience (UVM, SystemVerilog, gate-level sim), so verification is his strength; physical design is the new part. Explain PD steps, not testbench basics.
- **This repo may become public:** keep personal details (contact details, ID numbers, coursework, private schedule) out of it.
- Keep this file current: when a decision is made or a milestone lands, update sections 3, 5, 9 and 10 and the "Last updated" date.

## 13. Sources

- Supervisor email (19–21 Sep 2026), options note (24 Sep), group meeting auto-transcript (25 Sep), Bo Yang's thesis: Kamrul's Google Drive folder "EE6019 - Research Project".
- Tiny Tapeout: <https://tinytapeout.com/chips/>, <https://tinytapeout.com/faq/>, <https://tinytapeout.com/teaching/>, Hackster article on the IHP shuttle terms.
- IHP low-cost open-source MPW: <https://www.ihp-microelectronics.com/services/research-and-prototyping-service/mpw-prototyping-service/low-cost-open-source-mpw-access-1>
- LibreLane: <https://github.com/librelane/librelane>; IIC-OSIC-TOOLS: <https://github.com/iic-jku/IIC-OSIC-TOOLS>
