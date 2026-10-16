# Week 3 (12 to 16 October 2026)

*The 9 October meeting was cancelled, so this log is sent together with [week 2](week-02.md).*

## Tasks Done

- **Rewrote the tutorial as a short, learner-first lesson.** The 85-page manual was too long for a beginner, so the new lesson starts from an existing design: a serial-in, parallel-out shift register adapted to the official SKY130 template. It comes with a 15-page guide, slides, an offline interactive page and a starter pack ([docs/shift-register-quickstart](../docs/shift-register-quickstart/)).
- **Added a gate-level test (GLS) section.** Two pages explain the gate-level test, and a connected diagram shows how each push starts the RTL, documentation and GDS workflows.
- **Reorganised the repository.** The project root now matches the Tiny Tapeout template ([PR #9](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/pull/9)); the earlier stand-alone LibreLane counter flow is kept in `archive/legacy-flow`.
- **Took the shift register through the complete Tiny Tapeout flow.** At commit `66475c7`, GDS, precheck, gate-level test and viewer all pass ([run](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/actions/runs/38924144510), [layout viewer](https://mdkamrulislam-web.github.io/openFlowForChipDev_EE6019_ResearchProject/)). The same example has its own repository, [tt-shift-register](https://github.com/mdkamrulislam-web/tt-shift-register), where every workflow passes.
- **Merged earlier work:** the week 2 teaching material ([PR #8](https://github.com/mdkamrulislam-web/openFlowForChipDev_EE6019_ResearchProject/pull/8)) and the counter worked example ([tt-sky130-counter PR #1](https://github.com/mdkamrulislam-web/tt-sky130-counter/pull/1)).
- **Supervisor email, 12 October:** get familiar with the flow and with published chips, take a simple circuit through the full flow, and aim for a submission towards the end of the master's.
- **Supervisor meeting, 16 October:** [notes](week-03-meeting.md). I then compared research angles and drafted a recommendation ([options note](../docs/research/riscv-research-angles.md)).

## Problems and how I fixed them

- **The layout-viewer step failed four times** because GitHub Pages could not be used while the repository was private. I made the repository public and enabled Pages; the next run passed every step.
- **The long manual and course were too much for a beginner.** I wrote a short lesson that starts from an existing design, and checked it step by step as a learner would.
- **The workflow diagram did not show how the jobs connect, and gate-level testing was not explained.** I added the connected diagram and the two GLS pages, and restored a missing step on the GitHub Pages screenshot.
- **The repository layout did not match the lesson.** I moved the template files to the root, archived the old flow, and checked the moved files byte for byte.

## Remaining Tasks

- Send Prof. Popovici the tutorial.
- Agree the research angle; start the literature survey (about 30 checked references for the interim report).
- Confirm the interim-report, seminar and dissertation dates with the module coordinator.
- Watch *Making ASICs* and *Manufacturing ASICs*.
- Check the risk assessment against the department's form.
- Set up the project laptop (software and remote access requested).

## Questions

1. Is a machine-learning instruction extension for TinyQV, Tiny Tapeout's RISC-V SoC, a good research direction? (See the options note.)
2. Which shuttle should the January class aim for, and could the group support a multi-tile submission for my design?
3. Should my summer research project (EE6008) continue this design?
4. Which licence should the now-public repository and the student material use?
