# Tiny Tapeout counter: verified run evidence

Checked 7 October 2026. The [worked-example PR](https://github.com/mdkamrulislam-web/tt-sky130-counter/pull/1) builds the 8-bit counter in a **1 × 1 SKY130 Tiny Tapeout tile**. It is separate from this repository's earlier 150 × 150 µm counter flow. Nothing was submitted to a shuttle.

**Revision:** `61ef06bed008e76000f9ae46d65182e476d15dd6`. The submission artifact's recorded commit and the published layout match this revision.

| Check | Evidence |
|---|---|
| RTL test | [Run 37693100752](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100752): one cocotb test, zero failures/errors |
| Datasheet | [Run 37693100755](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100755): passed |
| Layout, precheck, gate-level test, viewer | [Run 37693100748](https://github.com/mdkamrulislam-web/tt-sky130-counter/actions/runs/37693100748): all four jobs passed |
| Gate-level functional test | Same port-level cocotb test: one test, zero failures/errors; unit-delay cell models, without extracted SDF timing |
| Layout viewer | [Published counter tile](https://mdkamrulislam-web.github.io/tt-sky130-counter/) |

## What fits in the tile

| Metric from the run | Value | Meaning |
|---|---|---|
| Utilisation | 4.96131% | The reported cell-area utilisation; it does not prove another design will route |
| Synthesis cells | 47 | Mapped circuit at synthesis, before physical-design additions |
| Final non-fill instances | 279 | Includes tap and other physical cells; not the logic-only count |
| Final total instances | 4,600 | Includes filler cells; not 4,600 logic gates |
| Worst setup / hold slack | 8.64285 / 0.109636 ns | Reported timing margins at the run's configured constraints |
| Reported setup / hold violations | 0 / 0 | In the completed flow reports |
| Magic DRC / LVS errors / antenna violations | 0 / 0 / 0 | Reported checks; template KLayout DRC/XOR are disabled, so this is not a claim that they ran |

The clock constraint is 20 ns (50 MHz). The workflow tag is `ttsky26d`; the run reports **LibreLane 3.0.14**. Template workflows, dev container and `src/config.json` were retained.

## Failures and warnings

- The initial blank-template `main` revision (`7998638`) failed docs and GDS metadata checks because the project title, author, description and datasheet were still placeholders. The populated example fixes those checks; it had no failed RTL, physical-design or gate-level runs.
- The successful run reports **447 `TIMESCALEMOD` lint warnings**, from generated PDK blackbox modules and the wrapper alongside `counter.v`'s timescale directive. It reports no lint errors, unmapped cells or synthesis-check errors. The warnings remain documented; no unverified cleanup was substituted for the tested revision.
- The wrapper assumes enable is synchronous to the clock. A physical button needs synchronisation and debouncing; the minimal counter test does not establish that behaviour.

Use the exact revision above when discussing results. Current `main` still contains the blank template until the PR is reviewed and merged.
