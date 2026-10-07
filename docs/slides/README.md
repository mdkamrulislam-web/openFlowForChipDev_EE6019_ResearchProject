# Tiny Tapeout beginner lecture

[PowerPoint](tiny-tapeout-flow-v1.pptx) · [PDF preview](tiny-tapeout-flow-v1.pdf)

The deck has 22 teaching slides and four staff appendix slides. It follows one real 8-bit counter through pins, RTL, tests, GitHub workflows, layout and the submission process. The diagrams and text are editable PowerPoint shapes; screenshots remain genuine captured evidence. Every slide has lecturer notes and precise source URLs. Source facts were checked on 7 October 2026; the redesigned deck was built and reviewed on 8 October 2026.

## Rebuild

Use Python 3.10 or later; this build was checked with Python 3.13.15 and the pinned packages in [requirements.txt](requirements.txt).

```powershell
python -m venv .venv-slides
.\.venv-slides\Scripts\python -m pip install -r docs/slides/requirements.txt
.\.venv-slides\Scripts\python docs/slides/build_slides.py
```

The builder reads [lecture-notes.json](lecture-notes.json) and local files in [img](img), then writes the PPTX and [slide-sources.json](slide-sources.json). It makes no network calls. Aptos/Aptos Display and Consolas are the intended fonts; they are available in the installed Microsoft Office environment used for review. Rebuilding does not execute the ASIC flow.

To export the PDF, open the PPTX in PowerPoint and use **File → Export → Create PDF/XPS**. The reviewed PDF and slide PNGs were exported by installed PowerPoint through COM. All 26 slides were inspected in rendered contact sheets, with full-size checks on changed code, screenshot and diagram slides. Use the PDF to review visual layout; use the PPTX to read notes, follow links or edit.

## Real worked-example identity

Repository: [tt-sky130-counter](https://github.com/mdkamrulislam-web/tt-sky130-counter), branch `worked-example`, [PR #1](https://github.com/mdkamrulislam-web/tt-sky130-counter/pull/1).

Reviewed commit: `61ef06bed008e76000f9ae46d65182e476d15dd6`.

| Evidence | Exact run or route | Result |
|---|---|---|
| RTL test | [37693100752](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100752) | 1 test, 0 failures, 0 errors |
| Datasheet | [37693100755](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100755) | Generated two-page PDF |
| Layout and checks | [37693100748](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100748) | gds, precheck, gl_test and viewer passed |
| Published layout | [Project viewer](https://mdkamrulislam-web.github.io/tt-sky130-counter/) | Loaded OAS matches that run |
| Initial metadata failure | [37693066241](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693066241) | Empty title/author/description; this is not an RTL assertion failure |

The build used SKY130, a 1x1 tile, a 50 MHz clock target and LibreLane 3.0.14. Reported core utilisation is **4.96131%**; **47 cells after synthesis** differs from **279 non-fill physical instances** and **4,600 total instances including 4,321 fillers**. Worst setup/hold slack was **8.64285 / 0.109636 ns**, with zero timing violations. All 15 prechecks passed. There were 447 `TIMESCALEMOD` lint warnings, not zero warnings. These are flow reports, not measured fabricated-silicon results. No shuttle booking, payment or submission occurred.

`img/counter-sky130-background.png` belongs to the earlier **separate 150 × 150 µm custom LibreLane flow**. It is retained for provenance and is not used as Tiny Tapeout evidence in the deck.

## Capture checklist

Four screenshot tasks remain, plus an optional future failed-assertion example. Slides label them honestly. Anonymous public captures cannot show account-only settings or full job logs; use an authorised signed-in session for those pages. Preserve project/run/commit identity in the capture. Do not draw imitation GitHub UI or label a constructed waveform as a simulation capture.

| Marker | Status and exact capture instructions |
|---|---|
| P1 | **Pending.** Sign in and open [official SKY template](https://github.com/TinyTapeout/ttsky-verilog-template). Capture the repository name and expanded **Use this template → Create a new repository** menu. Anonymous GitHub omits this button; the saved anonymous overview is insufficient. No new repository needs to be created merely for this image. |
| P2 | **Pending.** In [worked-example Pages settings](https://github.com/mdkamrulislam-web/tt-sky130-counter/settings/pages), capture **Build and deployment → Source: GitHub Actions**, with repository identity. |
| P3 | **Captured.** `img/counter-actions-green.png`: [Actions filtered to worked-example](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions?query=branch%3Aworked-example), showing docs/test/gds passes at `61ef06b`. Slide 13 uses native PowerPoint crop to enlarge those genuine rows. |
| P4 | **Partly captured; metrics view pending.** `img/counter-gds-run-summary.png` shows all four passed jobs. Open [GDS run 37693100748](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100748), then its gds job summary/logs or downloaded metrics artifact. Capture the actual utilisation/cell table and timing/precheck results with the run identity. Keep synthesis, non-fill and filler-inclusive counts separately labelled. The anonymous overview does not expose that table. |
| P5 | **Captured.** `img/counter-viewer-full.png` and `img/counter-viewer-no-fill.png` are genuine loaded [3D viewer captures](https://gds-viewer.tinytapeout.com/?pdk=sky130A&model=https%3A%2F%2Fmdkamrulislam-web.github.io%2Ftt-sky130-counter%2Ftinytapeout.oas). Slide 14 uses the native viewer state with **Filler cells** unchecked. The viewer automatically refits; these are not exact pixel-area comparisons. |
| P6 | **Optional future example; no failing assertion captured.** The worked-example tests passed. If a real assertion failure occurs during teaching, capture its assertion, input/expected/observed context and later passing correction. No failing run is needed to review this deck. The genuine initial metadata failure on slide 17 is clearly labelled and does not substitute for a failed-assertion capture. |
| P7 | **Captured.** `img/counter-datasheet-page-1.png` is page 1 of the two-page datasheet from [docs run 37693100755](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100755). It shows counter behaviour, testing and synchronous-enable assumptions. |
| P8 | **Pending.** Download `test-results` from [RTL run 37693100752](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100752), then open the genuine `tb.fst` in GTKWave or Surfer. Add clk, rst_n, ui_in[0], uo_out[7:0] and uio_out[0]. Capture reset at a rising edge, enabled increment, disabled hold and 254→255→0. Explain that wrap is high at count=255 while enabled, before overflow; it becomes low when enable is low. Keep the complete FST as evidence. No waveform viewer was installed in the review environment. |

After adding a capture, update its status in the lecturer notes, `build_slides.py` and this checklist, rebuild and render again.

## Source verification and teaching limits

- [Official templates](https://tinytapeout.com/hdl/templates/) and current template files were read, including `info.yaml`, test README/Makefile, workflows and dev-container configuration. SKY currently pins `ttsky26d`, IHP `ttihp26b`, GF `ttgf26c`. IHP26b is closed; a template pin does not prove open booking space. Current SKY/IHP template comments describe approximately 167 × 108 µm per 1x1 tile, and GF approximately 340 × 160 µm. The old roughly 1,000-gate estimate applies to historical TT04–TT10, not every current process.
- Current [SKY action](https://raw.githubusercontent.com/TinyTapeout/tt-gds-action/ttsky26d/action.yml) uses LibreLane 3.0.14; [IHP action](https://raw.githubusercontent.com/TinyTapeout/tt-gds-action/ttihp26b/action.yml) uses 3.0.5. The historical Making ASICs page/video mentions OpenLane; current template files take precedence for commands and versions.
- [Testing](https://tinytapeout.com/hdl/testing/) is checked against the current repository. Install its pinned requirements; use Python + make + Icarus. `make -B` must be followed by `python -m cocotb_tools.check_results results.xml`. Current waves are `tb.fst`, despite an older guide's VCD example. A development container requests 10 GB; this deck does not promise that every standard Codespace has been validated.
- [GPIO limits](https://tinytapeout.com/specs/gpio/) distinguish SKY130 input 66 MHz from output 33 MHz, and both from internal timing. A 50 MHz design target and positive timing margin are not a fabricated-chip maximum-frequency measurement.
- The [latest ETR board guide](https://tinytapeout.com/guides/get-started-demoboard-etr/) identifies RP2350B; older boards use RP2040. This counter supplies binary pins, not a seven-segment decoder. Use a slow controller clock or single-step and synchronise/debounce physical enable switches.
- [Teaching starting prices](https://tinytapeout.com/teaching/) and [shuttle schedule](https://tinytapeout.com/chips/) were checked for the staff appendix. Prices, availability, shipping and deadlines must be refreshed before procurement. Historical reported IHP loan restrictions are marked as requiring the exact current shuttle agreement; current 2027 terms were not verified.
- Video links remain lecturer preparation references; the slides do not claim that all videos have been watched.

Full per-slide URLs are in PowerPoint notes and [slide-sources.json](slide-sources.json). The deck's public example has passed automated checks and has not been manufactured or submitted.
