# How it works

This design stores eight bits. A rising clock edge is the instant the clock
changes from 0 to 1. On that edge:

- If `rst_n` is 0, all eight bits become 0.
- Otherwise, if `ui_in[1]` is 1, each stored bit moves one position towards
  `q[7]`, and `ui_in[0]` enters `q[0]`. The old `q[7]` is discarded.
- If `ui_in[1]` is 0, the stored value stays the same.

The eight output pins show `q[7:0]` at the same time. Reset is synchronous:
changing `rst_n` alone does not clear the register; a rising clock edge is needed.

## How to test

1. Select this project and supply a clock. The declared target is 50 MHz
   (one cycle every 20 ns); a slower clock can be used for a manual demonstration.
2. Hold `rst_n=0` through a rising edge. Check `uo_out=00000000`.
3. Set `rst_n=1`, `ui_in[1]=1`. Send `1,0,1,1,0,0,1,0` on `ui_in[0]`,
   holding each bit steady before its rising edge.
4. After eight rising edges, check `uo_out=10110010` (hexadecimal `B2`).
5. Set `ui_in[1]=0` and clock again. Check that `uo_out` still shows `B2`.
6. Enable shifting and send another 1. Check `uo_out=01100101` (hexadecimal `65`).

Run the Python test in `test/test.py` to check these cases automatically.
Use `ui_in[1]` for shift enable. The separate Tiny Tapeout port `ena` is the
project-selection signal; it is not the shift-enable input.

## External hardware

A Tiny Tapeout demo board is sufficient. The `uio` pins are unused and set to
input direction. This example has no serial-output pin or parallel-load mode.
