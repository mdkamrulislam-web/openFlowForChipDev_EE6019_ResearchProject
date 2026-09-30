#!/usr/bin/env python3
"""Print the sign-off metrics of a LibreLane run as a short table.

Usage: python3 scripts/summary.py designs/<design>/runs/<tag>
Exits non-zero if any sign-off check failed, so it can gate CI.
"""
import json
import sys
from pathlib import Path

# (metric key, label, must be zero?)
CHECKS = [
    ("route__drc_errors", "Routing DRC errors", True),
    ("magic__drc_error__count", "Magic DRC errors", True),
    ("klayout__drc_error__count", "KLayout DRC errors", True),
    ("design__lvs_error__count", "LVS errors", True),
    ("antenna__violating__nets", "Antenna violations", True),
    ("timing__setup_vio__count", "Setup violations", True),
    ("timing__hold_vio__count", "Hold violations", True),
    ("design__max_slew_violation__count", "Max slew violations", True),
    ("design__max_cap_violation__count", "Max cap violations", True),
    ("timing__setup__ws", "Worst setup slack (ns)", False),
    ("timing__hold__ws", "Worst hold slack (ns)", False),
    ("design__die__area", "Die area (um^2)", False),
    ("design__instance__count__stdcell", "Standard cells", False),
    ("power__total", "Total power (W)", False),
]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    run = Path(sys.argv[1])
    metrics_file = run / "final" / "metrics.json"
    if not metrics_file.exists():
        print(f"No metrics at {metrics_file}; did the harden step finish?")
        return 1
    metrics = json.loads(metrics_file.read_text())

    failed = False
    print(f"Run: {run}")
    for key, label, must_be_zero in CHECKS:
        value = metrics.get(key)
        if value is None:
            shown, status = "n/a", ""
        elif must_be_zero:
            ok = value == 0
            failed |= not ok
            shown, status = str(value), "ok" if ok else "FAIL"
        else:
            shown = f"{value:.4g}" if isinstance(value, float) else str(value)
            status = ""
        print(f"  {label:<26} {shown:>12}  {status}")
    gds = run / "final" / "gds"
    print(f"  GDS: {', '.join(str(p) for p in gds.glob('*.gds')) or 'missing'}")
    print("Sign-off: " + ("FAILED" if failed else "clean"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
