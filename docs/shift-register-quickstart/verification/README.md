# Shift-register verification evidence

Checked on 11 October 2026. The supplied starter is a **seven-file overlay** for
the official SKY130 Verilog template, not a replacement for its infrastructure.
Keep the template's workflows, `test/requirements.txt`, `src/config.json` and
licence. There is no new chip flow.

## Result

**Root layout rechecked on 16 October:** the same real simulation was run against
the canonical `src/` and `test/` files at the research repository root. It passed
one test with zero failures; the deliberately reversed shift still failed.
See [root-layout evidence](root-layout/verification-report.json) and
[layout checks](../root-layout-checks.json). All seven root files match the
portable starter; the official workflow/config/requirement files are unchanged.
No physical build or GLS result is inferred from this move.

The starter's real Verilog and Python test passed in local RTL simulation:
**1 test, 1 pass, 0 failures, 740 ns simulated**. Icarus Verilog 12.0 (devel)
compiled and simulated the design, with cocotb 2.1.0 on Windows.

The same test detected a deliberate error: reversing the core's shift direction
in a temporary copy failed at 40 ns, with actual output 128 instead of 1. The
starter itself was not altered by this check.

Checks cover reset, eight serial bits, hold, a ninth bit discarding the oldest
bit, changes to unused inputs, reset priority, reset with enable low, repeated
bits and bidirectional pin direction. Configuration checks establish matching
top-module names and source lists. Both simulation and declared clock use
50 MHz (20 ns per cycle), matching the template's default `CLOCK_PERIOD`.

The core reset is synchronous. Its implementation clears on a rising edge.
The test checks its edge-driven reset result; it does not separately test
between-edge reset behaviour.

**Physical build has not run for this shift register.** These results do not
establish synthesis, timing, layout, precheck or gate-level success. The learner
must run the template's `test`, `docs` and full `gds` workflow for the same final
commit. No submission or purchase was made.

## Files

| File | What it records |
|---|---|
| `verification-report.json` | Results, tool versions, limits and SHA-256 hashes of all seven starter files |
| `rtl-results.xml` | Original cocotb JUnit test result |
| `rtl-simulation.log` | Original simulation output, including each checked case |
| `rtl-compile.log` | Original compiler output |
| `rtl-waveform.fst` | Genuine signal waveform from the passing simulation |
| `rtl-waveform.vcd` | The same waveform converted with GTKWave's `fst2vcd` tool; useful for plotting |
| `mutation-results.xml`, `mutation-simulation.log`, `mutation-compile.log` | Evidence that the deliberately wrong shift direction is caught |
| `run_rtl.py` | Repeatable maintainer check; builds and mutates in temporary directories |

The compiler reports that the two RTL modules have no explicit time unit.
They contain no delays; the test fixture explicitly uses `1ns/1ps`. This warning
does not affect the 20 ns test cycle. The host Python reports 3.13.15; the
embedded Python startup reports 3.13.8. Both are retained in the report. The
official template's cloud test uses Python 3.11.

## Reproduce locally

With Icarus (`iverilog` and `vvp`) on `PATH`, install `cocotb==2.1.0` and `PyYAML`
in a Python environment, then run from the research repository root:

```text
python docs/shift-register-quickstart/verification/run_rtl.py
```

To check the actual project root and keep its evidence separate:

```text
python docs/shift-register-quickstart/verification/run_rtl.py --project-dir . --output-dir docs/shift-register-quickstart/verification/root-layout --checked-on 2026-10-16
```

The script exits 0 only if the original test passes and the deliberately wrong
version fails. It writes evidence beside itself. It uses cocotb's Python runner;
the template Makefile and GitHub Actions were not run in this local check.

After adding the seven files to a template repository, its normal Linux/Actions
command is:

```sh
cd test
make clean
make
python -m cocotb_tools.check_results results.xml
```

This is the template's verified source command; this particular command was not
executed locally because the Windows host has no GNU Make or WSL installation.

## Primary-source baseline

The official [SKY Verilog template](https://github.com/TinyTapeout/ttsky-verilog-template)
was fetched at commit `68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a`, dated
30 September 2026. The starter core, wrapper, test and datasheet were newly
written. The Makefile preserves the template rules and changes only
`PROJECT_SOURCES` to include the additional core file. The fixture preserves
the power-port conditional required for gate-level simulation.

- [Fixed port interface](https://github.com/TinyTapeout/ttsky-verilog-template/blob/68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a/src/project.v)
- [Project schema, source list and pinout](https://github.com/TinyTapeout/ttsky-verilog-template/blob/68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a/info.yaml)
- [Simulation Makefile](https://github.com/TinyTapeout/ttsky-verilog-template/blob/68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a/test/Makefile)
- [Pinned cocotb requirement](https://github.com/TinyTapeout/ttsky-verilog-template/blob/68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a/test/requirements.txt)
- [Cloud test and result check](https://github.com/TinyTapeout/ttsky-verilog-template/blob/68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a/.github/workflows/test.yaml)
- [GDS, precheck, gate-level and viewer jobs](https://github.com/TinyTapeout/ttsky-verilog-template/blob/68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a/.github/workflows/gds.yaml)
- [Default 20 ns build target](https://github.com/TinyTapeout/ttsky-verilog-template/blob/68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a/src/config.json)
- [cocotb runner documentation](https://docs.cocotb.org/en/stable/runner.html)

Local Icarus binaries were [downloaded from the Windows packager linked by
Icarus](https://bleyer.org/icarus/) and extracted into a temporary tools directory
with [innoextract](https://constexpr.org/innoextract/). No installer ran. This
route was used only to verify the teaching example; students can use the
template's cloud workflow without installing local tools.
