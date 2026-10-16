# Shift-register tests

`test.py` checks reset, serial shifting, hold, old bits leaving the eight-bit
register, reset priority, unused inputs and bidirectional-pin directions.
`tb.v` connects the test to `tt_um_student_shift_register`.

The same port-level Python test is used for RTL and functional GLS. Keep the
`GL_TEST` power-pin conditionals in `tb.v` and both branches of the Makefile.

For the browser route, use the `test` workflow for RTL and `gds → gl_test` for
GLS, matching the same commit. See [guide pages 13–14](../docs/shift-register-quickstart/quickstart-root-layout.pdf)
for the GLS job, logs, XML and waveform downloads.

With Icarus, Python test packages and GNU Make already installed, the RTL command
from the repository root is:

```sh
cd test
make -B
python -m cocotb_tools.check_results results.xml
```

Local GLS additionally requires the generated `gate_level_netlist.v` and matching
SKY130 cell models under `PDK_ROOT`. The cloud GLS job supplies these and selects
the Makefile's gate-level branch with `GATES=yes`; the browser guide avoids a
local PDK installation.
