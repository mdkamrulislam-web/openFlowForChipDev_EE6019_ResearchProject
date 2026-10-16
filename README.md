# Tiny Tapeout shift-register project

**Start in this directory.** It contains the Tiny Tapeout project described in
the short guide and slides. `src/project.v` means the file in this repository's
root `src` folder.

Open the [interactive guide](docs/shift-register-quickstart/START-HERE.html),
[PDF guide](docs/shift-register-quickstart/quickstart-root-layout.pdf) or
[PowerPoint lesson](docs/shift-register-quickstart/lesson-root-layout.pptx).
GLS is on guide pages 13–14 and slides 19–22.

## The project tree used in the lesson

```text
openFlowForChipDev_EE6019_ResearchProject/
├── .github/
│   └── workflows/
│       ├── test.yaml          # RTL simulation
│       ├── docs.yaml          # Datasheet
│       ├── gds.yaml           # Layout, precheck, GLS and viewer
│       └── fpga.yaml          # Optional FPGA workflow
├── src/
│   ├── shift_register.v       # Existing eight-bit circuit
│   ├── project.v              # Tiny Tapeout wrapper
│   └── config.json            # Template physical-build settings
├── test/
│   ├── Makefile               # Source lists; RTL and gate-level branches
│   ├── tb.v                   # Simulation fixture; GLS power pins
│   ├── test.py                # Shared cocotb tests for RTL and GLS
│   ├── requirements.txt       # Python test packages
│   └── README.md
├── docs/
│   ├── info.md                # Shift-register datasheet text
│   └── shift-register-quickstart/  # Guide, slides, downloads and evidence
├── info.yaml                  # Module name, source list, pins and metadata
├── .devcontainer/             # Optional template development environment
├── .vscode/                   # Template editor settings
├── LICENSE                    # Upstream template licence
├── logbook/                   # EE6019 project records
└── archive/
    └── legacy-flow/           # Earlier standalone counter flow, preserved
```

Other teaching and research notes remain inside `docs`. The hidden `.git`
folder stores this repository's history.

## Follow the example

The seven adaptation files are already in their documented locations:

```text
info.yaml
src/shift_register.v
src/project.v
test/Makefile
test/tb.v
test/test.py
docs/info.md
```

Read/edit those files directly here. Keep `.github`, `src/config.json` and
`test/requirements.txt` supplied by the template. The starter ZIP is a portable
copy of these seven files for uploading into your own template repository.

The wrapper maps serial data to `ui_in[0]`, shift enable to `ui_in[1]`, and the
eight stored bits to `uo_out`. The clock connects directly; `~rst_n` supplies
the core's active-high synchronous reset. Bidirectional pins stay as inputs.

In a GitHub template repository, a saved commit starts `test`, `docs` and `gds`.
Check them for the same commit. The GDS build feeds `precheck`, `gl_test` and
`viewer`. Configure **Settings → Pages → Source: GitHub Actions** to publish
the layout viewer. The short guide shows each browser step.

## Verification state

The shift-register RTL test and deliberately incorrect-shift check have passed
their expected outcomes; see [evidence](docs/shift-register-quickstart/verification/README.md).
Moving files into the root does not establish a physical build or GLS result.
Those stages remain to be run for this example. The guide's successful GLS
screenshot comes from the earlier, separately identified counter project.

Template infrastructure comes from
[`TinyTapeout/ttsky-verilog-template` at `68c3fd3`](https://github.com/TinyTapeout/ttsky-verilog-template/tree/68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a).
The upstream template licence is retained; licensing of original teaching and
research material remains to be agreed with the supervisor.

The [earlier standalone flow](archive/README.md) is preserved under `archive`.
