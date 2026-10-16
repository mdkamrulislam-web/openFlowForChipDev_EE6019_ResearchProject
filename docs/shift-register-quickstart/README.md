# Your Verilog to Tiny Tapeout

A new, short practical lesson for someone who already has a Verilog circuit.
The worked example is an eight-bit serial-in, parallel-out shift register.
This lesson was written from scratch on 11 October 2026 and revised on
16 October to add a dedicated GLS walkthrough and connected workflow diagram.

## Start here

Open **[START-HERE.html](START-HERE.html)** in your browser. It works offline and
includes a clock experiment, prediction answers, copy-code buttons, a downloadable
starter and checkpoints that stay in your browser. Internet access is needed for
the GitHub project and its cloud builds.

- [Revised PDF guide — 15 pages](quickstart-revised.pdf)
- [Revised editable Word guide](quickstart-revised.docx)
- [Revised PowerPoint lesson — 24 slides](lesson-revised.pptx)
- [Revised slide PDF](lesson-revised.pdf)
- [Seven-file shift-register starter](shift-register-starter.zip)

**GLS is on guide pages 13–14 and slides 19–22.** It covers the generated
netlist, shared Python test, power-pin fixture, `gl_test` job, passing summary,
`gatelevel_test_results` artifact, waveform and failure diagnosis. Its screenshot
and retained log excerpt are from the earlier successful counter example; the
shift register's GLS has not been run.

The connected chart starts with a commit/push, branches to RTL/docs/GDS, then
branches from GDS to precheck/GLS/viewer. All required checks use the same commit.

The Pages screenshot now shows all three red callout numbers. The missing **2**
was added as an editable SVG annotation, with a PNG rendering for the guide and
slides; the original official screenshot remains in `images/pages.png`.

The PDF/Word guide gives the full core and wrapper. Longer test and configuration
files are supplied in the starter rather than spread over more teaching pages.
The slides contain the essential actions, diagrams and code excerpts; presenter
notes connect each slide to its guide page.

## The route

1. Describe the existing circuit.
2. Create a project from the official SKY Verilog template.
3. Enable Actions and configure Pages.
4. Map the pins and wrap the existing module.
5. Match three module names and two source lists.
6. Describe the project and adapt its test.
7. Upload all seven files.
8. Check RTL, documentation and the complete GDS workflow for one commit.
9. View the layout and save the evidence.

The example uses `ui_in[0]` for serial data, `ui_in[1]` for shift enable,
`uo_out[7:0]` for the stored bits and `~rst_n` for the core's active-high,
synchronous reset. All bidirectional pins remain inputs.

## What was checked

The actual starter passed Icarus Verilog/cocotb RTL simulation: **one test,
zero failures**. The same test caught a deliberately reversed shift direction.
The two source lists and three top-module names were checked too. See
[verification evidence](verification/README.md).

The interactive guide was exercised on desktop and mobile widths: all 15 pages,
navigation, persistent checkpoints, clock/hold/reset, predictions, code copying
and a seven-file download with matching bytes. Word and PowerPoint were rendered
and checked for pagination, clipped text and readable diagrams.

The shift register's physical build, timing, precheck and gate-level workflows
have **not** been run. The guide explains how the learner runs and checks these.
Screenshots of GitHub Actions show the official template's interface, not a
successful shift-register build. No chip has been submitted or ordered.

## Sources and maintenance

[sources.json](sources.json) records the genuine screenshot sources and official
documentation, including the GLS action checked on 16 October 2026. The baseline template commit is
`68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a`; it uses cocotb 2.1.0.
The starter contains only seven adaptation files. Keep the template's build
infrastructure, process settings, requirements and licence.

New lesson text lives in `author_lesson.py`, producing `lesson.json`. Rebuild:

```text
python docs/shift-register-quickstart/number_pages_screenshot.py
python docs/shift-register-quickstart/author_lesson.py
python docs/shift-register-quickstart/build_interactive.py
python docs/shift-register-quickstart/build_exports.py --suffix=-revised --export-pdf --qa
```

The exports use python-docx, python-pptx, Pillow and native Word/PowerPoint for
PDF export. The interactive check uses Playwright and Edge. These are maintainer
tools; the student browser route requires none of them.

The initial `quickstart.*` and `lesson.*` files remain as earlier editions.
The `*-revised.*` files are the current review copies, allowing earlier documents
that are open in Word or PowerPoint to remain undisturbed.

Learner and supervisor review of this new lesson remains pending.
