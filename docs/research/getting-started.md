# Research: getting started with TinyQV

> **23 October 2026:** steps 1–2 were done and all tests passed (see [logbook/week-04.md](../../logbook/week-04.md)). Steps 3–5 are paused, because Prof. Popovici moved the research away from TinyQV the same day ([logbook/week-04-meeting.md](../../logbook/week-04-meeting.md)). The guide stays as a record and as a Tiny Tapeout simulation walkthrough.

*Written 18 October 2026. The plan is "A then B": first an ML instruction extension for TinyQV, then a stochastic-computing version (see [riscv-research-angles.md](riscv-research-angles.md)). These steps get TinyQV running in simulation and give you a first measured result. Commands were checked against the repositories on 18 October 2026.*

You need nothing installed on your own laptop. Everything runs in **GitHub Codespaces**, a Linux machine in the browser.

## Step 1: open TinyQV in a Codespace (about 15 minutes)

1. Fork **[TinyTapeout/ttsky25a-tinyqv](https://github.com/TinyTapeout/ttsky25a-tinyqv)** to your account. This is the full TinyQV SoC with all 2025 community peripherals, including the NPU. It is Apache-2.0.
2. In your fork: **Code → Codespaces → ⋯ → New with options**. Choose a **4-core (16 GB)** machine, because the repo's dev container asks for 10 GB of memory.
3. Wait for the dev container to build. It installs Icarus Verilog, Verilator, GTKWave and Python, and VS Code gets the Surfer waveform viewer.
4. **Stop the Codespace when you finish** (Codespaces → ⋯ → Stop). Personal accounts get a limited free allowance each month; check yours in GitHub's billing settings.

## Step 2: run the existing tests (about 30 minutes)

In the Codespace terminal:

```bash
git submodule update --init --recursive   # the CPU itself (src/tinyQV) is a submodule; without this every test fails
cd test
pip install -r requirements.txt            # cocotb 1.9.2, riscv-model, numpy …

make core                                  # the CPU's basic tests
PROG=hello make -B -f test_prog.mk         # runs hello.hex on TinyQV
PROG=prime make -B -f test_prog.mk         # a real program: finds primes
PROG=throughput make -B -f test_prog.mk    # a performance test
make peri_num_4                            # the NPU peripheral's tests (peripheral 4)
```

**What to look at:**
- **Waveforms:** each run leaves a `.fst` waveform (in `sim_build/rtl/` or renamed in `test/`). Open it with Surfer and find `clk`, the QSPI pins and the program counter. A load from memory takes many clocks.
- **Tests:** `test/test_throughput.py` shows how the existing tests measure time, which you will reuse in step 5.
- **The NPU:** the test is in `test/user_peripherals/npu/`. Read [its documentation](https://github.com/TinyTapeout/ttsky25a-tinyqv/blob/main/docs/user_peripherals/04_npu.md) alongside it: four 4-bit multipliers, a 16-bit running total, rescaling and ReLU. Its MNIST model is in `assets/`.

**Result for your log:** "TinyQV runs programs in simulation; NPU tests pass", plus a waveform screenshot.

## Step 3: install the TinyQV toolchain (about 30 minutes, mostly download)

TinyQV uses a slightly modified RISC-V GCC (RV32EC plus TinyQV's own instructions):

```bash
cd /tmp
wget https://github.com/MichaelBell/riscv-gnu-toolchain/releases/download/15.1.0-tqv-2.0/riscv32ec-15.1.0-tqv-2.0.tar.gz   # about 1 GB
tar -tzf riscv32ec-15.1.0-tqv-2.0.tar.gz | head     # look at the folder layout first
sudo mkdir -p /opt/tinyQV
# extract so that /opt/tinyQV/bin/riscv32-unknown-elf-gcc exists
# (add --strip-components=1 if the archive has one top-level folder):
sudo tar -xzf riscv32ec-15.1.0-tqv-2.0.tar.gz -C /opt/tinyQV
/opt/tinyQV/bin/riscv32-unknown-elf-gcc --version   # check
```

If you put it elsewhere, set `RISCV_TOOLCHAIN` to that folder.

## Step 4: build and run your first program (about 30 minutes)

```bash
git clone -b ttsky25a https://github.com/MichaelBell/tinyQV-sdk ~/tinyQV-sdk
mkdir -p ~/work && cp -r ~/tinyQV-sdk/example-sim-project ~/work/example
cd ~/work/example && make TINYQV_SDK=~/tinyQV-sdk     # builds example.hex
cp example.hex /workspaces/ttsky25a-tinyqv/test/      # adjust to your Codespace folder
cd /workspaces/ttsky25a-tinyqv/test && PROG=example make -B -f test_prog.mk
```

`test_example.py` in the repo already matches the SDK example. The simulation project has limited RAM and flash, which is enough for small networks.

## Step 5: the software baseline (weeks 2–3)

This is your **first research result**: how expensive is AI on TinyQV without any help?

1. Write a small fully connected layer in C with int8 (or int4) weights in your simulation project: a dot-product loop with a running total.
2. Use the same network as the NPU test (its MNIST model in `test/user_peripherals/npu/assets/`), so that every later comparison uses identical work.
3. Copy the timing approach in `test_throughput.py` to count **clock cycles** per layer.
4. Record the cycles, plus the instruction mix if you can, in your log.

This number is what both the instruction extension (A) and the stochastic version (B) must beat.

## What comes next (not yet)

- **First custom instruction:** for example, a 4-way 4-bit dot product with accumulate, in the CPU's decoder and ALU (`src/tinyQV/cpu/`). Called from C with `.insn`.
- **Energy:** post-layout power from the Tiny Tapeout flow, using the simulated switching activity.
- **Then** the stochastic-computing version, and the comparison.

## If something fails

- **`make` cannot find `iverilog`:** you are not inside the dev container. Rebuild the Codespace.
- **Errors about missing `tinyQV/cpu/*.v` files:** run `git submodule update --init --recursive` in the repo root.
- **Python errors:** re-run `pip install -r requirements.txt` inside `test/`.
- **Toolchain not found:** check `RISCV_TOOLCHAIN` and that `.../bin/riscv32-unknown-elf-gcc` exists.
- **Record every failure and its fix in the weekly log.** Prof. Popovici asked for mistakes and fixes to be recorded.
