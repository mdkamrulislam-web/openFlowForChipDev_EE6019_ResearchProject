"""Maintainer check: run the supplied test with Icarus, then reverse shift direction.

Requires Icarus (iverilog/vvp on PATH), cocotb==2.1.0 and PyYAML.
Does not change the starter. Build products stay in a temporary directory.
"""

from __future__ import annotations

import hashlib
import argparse
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

import cocotb
from cocotb_tools.runner import get_runner
import yaml


HERE = Path(__file__).resolve().parent
STARTER = HERE.parent / "starter"
TEMPLATE_COMMIT = "68c3fd3f3ec640e5edcb6a5f74f360ebc016bb2a"


def results(path: Path) -> dict:
    root = ET.parse(path).getroot()
    cases = list(root.iter("testcase"))
    failed = sum(bool(list(case.iter("failure")) + list(case.iter("error"))) for case in cases)
    return {"tests": len(cases), "failures": failed, "passed": len(cases) - failed}


def simulate(sources: list[Path], build: Path, name: str) -> dict:
    run_dir = build / name
    run_dir.mkdir()
    runner = get_runner("icarus")
    runner.build(
        sources=sources,
        hdl_toplevel="tb",
        build_dir=run_dir,
        always=True,
        build_args=["-Wall"],
        log_file=HERE / f"{name}-compile.log",
    )
    test_exception = None
    try:
        runner.test(
            hdl_toplevel="tb",
            test_module="test",
            test_dir=run_dir,
            extra_env={"PYTHONDONTWRITEBYTECODE": "1"},
            results_xml=HERE / f"{name}-results.xml",
            waves=True,
            log_file=HERE / f"{name}-simulation.log",
        )
    except (RuntimeError, SystemExit) as exc:
        test_exception = str(exc)
    outcome = results(HERE / f"{name}-results.xml")
    outcome["runner_exception"] = test_exception
    if name == "rtl":
        shutil.copy2(run_dir / "tb.fst", HERE / "rtl-waveform.fst")
    return outcome


def main() -> int:
    global STARTER, HERE
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-dir', type=Path, default=STARTER)
    parser.add_argument('--output-dir', type=Path, default=HERE)
    parser.add_argument('--checked-on', default='2026-10-11')
    args = parser.parse_args()
    STARTER = args.project_dir.resolve()
    HERE = args.output_dir.resolve()
    HERE.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(STARTER / 'test'))
    metadata = yaml.safe_load((STARTER / "info.yaml").read_text(encoding="utf-8"))
    project = metadata["project"]
    assert metadata["yaml_version"] == 6
    assert len(metadata["pinout"]) == 24
    assert project["clock_hz"] == 50_000_000
    assert project["source_files"] == ["project.v", "shift_register.v"]
    assert project["top_module"] == "tt_um_student_shift_register"
    wrapper = (STARTER / "src/project.v").read_text()
    fixture = (STARTER / "test/tb.v").read_text()
    makefile = (STARTER / "test/Makefile").read_text()
    top = re.escape(project["top_module"])
    assert re.search(rf"\bmodule\s+{top}\s*\(", wrapper)
    assert re.search(rf"\b{top}\s+user_project\s*\(", fixture)
    declared_sources = re.search(r"^PROJECT_SOURCES\s*=\s*(.+)$", makefile, re.MULTILINE).group(1).split()
    assert declared_sources == project["source_files"]
    assert all((STARTER / "src" / name).is_file() for name in declared_sources)

    sources = [STARTER / "src" / name for name in project["source_files"]]
    sources.append(STARTER / "test/tb.v")
    with tempfile.TemporaryDirectory(prefix="tt-shift-rtl-") as temporary:
        build = Path(temporary)
        original = simulate(sources, build, "rtl")
        core = (STARTER / "src/shift_register.v").read_text()
        wrong_direction = core.replace("{q[6:0], serial_in}", "{serial_in, q[7:1]}")
        assert wrong_direction != core
        mutant = build / "wrong_shift_direction.v"
        mutant.write_text(wrong_direction, encoding="utf-8")
        mutated = simulate([sources[0], mutant, sources[2]], build, "mutation")

    report = {
        "checked_on": args.checked_on,
        "scope": "Local RTL simulation of the seven shift-register project files",
        "template_repository": "https://github.com/TinyTapeout/ttsky-verilog-template",
        "template_commit": TEMPLATE_COMMIT,
        "template_action_tag": "ttsky26d",
        "template_cocotb_version": "2.1.0",
        "host": platform.platform(),
        "host_python": platform.python_version(),
        "embedded_python": re.search(r"Using Python (\S+) interpreter", (HERE / "rtl-simulation.log").read_text()).group(1),
        "cocotb": cocotb.__version__,
        "iverilog": subprocess.run(["iverilog", "-V"], text=True, capture_output=True).stdout.splitlines()[0],
        "local_runner": "cocotb_tools.runner Python API; template make/Actions not executed locally",
        "rtl": original,
        "mutation": {"change": "Reverse shift direction in a temporary core copy", **mutated},
        "timing": {"simulation_cycle_ns": 20, "declared_clock_hz": 50_000_000, "template_clock_period_ns": 20},
        "checks": [
            "reset clears to zero",
            "input 10110010 yields B2 after eight enabled rising edges",
            "shift enable low holds the stored value",
            "ninth input bit drops the oldest bit: B2 then 1 gives 65",
            "unused input changes do not change the function",
            "reset wins over shifting and works with enable low",
            "repeated ones fill and repeated zeros empty the register",
            "uio_oe and uio_out remain zero on every sampled cycle",
            "top-module name and source lists agree across the three configuration points",
        ],
        "not_run": ["GitHub Actions", "synthesis", "place and route", "timing sign-off", "GDS generation", "Tiny Tapeout precheck", "gate-level simulation", "submission"],
        "starter_sha256": {
            name: hashlib.sha256((STARTER / name).read_bytes()).hexdigest()
            for name in sorted(['info.yaml', 'src/project.v', 'src/shift_register.v',
                                'test/Makefile', 'test/tb.v', 'test/test.py', 'docs/info.md'])
        },
    }
    (HERE / "verification-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    success = original["tests"] == 1 and original["failures"] == 0 and mutated["failures"] == 1
    print(json.dumps({"rtl": original, "mutation": mutated, "success": success}, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
