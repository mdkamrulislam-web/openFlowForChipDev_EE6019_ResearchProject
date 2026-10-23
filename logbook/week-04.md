# Week 4 log: TinyQV in simulation (23 October 2026)

*Copied from Kamrul's session notes of 23 October. The meeting that followed is in [week-04-meeting.md](week-04-meeting.md). Before the meeting, little project time was spent this week (EE6041 assignment week).*

## 1. The goal for today, in one sentence

Before changing anything, check that the TinyQV chip design works by running its existing tests on the computer.

## 2. Words used in this log

| Word | Simple meaning |
|---|---|
| **TinyQV** | A very small RISC-V processor (CPU) made for Tiny Tapeout chips. My project will add to it. |
| **NPU** | A small extra block attached to TinyQV that does neural-network maths (multiply and add). Someone else built it in 2025. I want to compare my idea against it. |
| **Simulation** | Running the chip design as a program on the computer, to see if it behaves correctly, without making a real chip. |
| **Test** | A small program that gives inputs to the design and checks the outputs are right. PASS = correct. |
| **Waveform** (`.fst` file) | A recording of every signal in the chip over time, like an oscilloscope screen. |
| **Surfer** | A program for viewing waveforms. |
| **QSPI** | The 4-wire connection TinyQV uses to talk to its external memory chips (flash for code, RAM for data). It is slow. |
| **Submodule** | A folder inside the project that is really another project. It must be downloaded separately. |
| **Dev container** | A ready-made computer setup with all the chip tools already installed. |
| **MNIST** | A famous dataset of hand-written digits 0–9. Used to test small AI models. |

## 3. What I ran and what happened

All three test runs **passed**.

| # | What was tested | Command (run in the `test` folder) | Result | Time it took |
|---|---|---|---|---|
| 1 | The CPU itself (11 different checks) | `make core` | ✅ **11 out of 11 passed** | about 7.5 min |
| 2 | A real "hello" program running on the CPU, loaded from (simulated) flash memory | `PROG=hello make -B -f test_prog.mk` | ✅ **Passed**. The program printed: `Cycles 13032, time 1629, instret 3144` | about 13 min |
| 3 | The NPU running a small AI model that reads hand-written digits | `make peri_num_4` | ✅ **2 out of 2 passed**. The NPU gave exactly the same answers as the software version of the model. The model is right **92%** of the time (9,223 out of 10,000 digits). | about 6 min |

**Important:** the NPU test sends data to the NPU through a test tool, not through the CPU. So its timing is **not** a measure of how fast TinyQV is. Do not quote it as a speed result.

## 4. Mistakes and problems, and how I fixed them

Prof. Popovici asked me to record every problem and fix. Here they are, in the order they happened.

### Problem 1: The chip tools were missing
- **What I saw:** the simulator program `iverilog` was "not found".
- **Why:** the Codespace started with a plain, empty computer setup (Alpine Linux), not the Tiny Tapeout setup that has all the tools.
- **Fix:** I installed the tools myself:
  ```
  sudo apk add iverilog python3 py3-pip make g++
  python3 -m venv ~/venv
  . ~/venv/bin/activate
  pip install -r test/requirements.txt
  ```
- **Lesson:** when opening a Codespace, check it uses the Tiny Tapeout dev container. If it doesn't, choose "Rebuild container" (this is slower but gives the correct setup).

### Problem 2: The CPU files were missing
- **What I saw:** the CPU folder `src/tinyQV` was empty.
- **Why:** the CPU is a submodule (a project inside the project). It is not downloaded automatically.
- **Fix:** `git submodule update --init --recursive`
- **Lesson:** always run this command after downloading the project.

### Problem 3: The test tool could not start
- **What I saw:** `Unable to open lib libcocotb.so` and `results.xml was not written by the simulation!`
- **Why:** the test tool (cocotb) could not find one of its own files. This happens on Alpine Linux because it looks for files differently from Ubuntu (which the official setup uses).
- **Fix:** tell the computer where the files are, before running tests:
  ```
  export LD_LIBRARY_PATH=$(cocotb-config --lib-dir)
  ```
- **Lesson:** this problem would not happen inside the official dev container.

### Problem 4: An error message after the CPU tests (not a real problem)
- **What I saw:** `mv: cannot stat 'sim_build/gl/tb*.fst'` at the very end.
- **Why:** the script also looks for a second kind of recording ("gate-level") that we did not make. It ignores this on purpose.
- **Fix:** nothing needed.
- **Lesson:** read the PASS/FAIL table, not just the last line.

### Problem 5: A warning in the hello test (not a real problem)
- **What I saw:** `Not enough words in the file for the requested range`.
- **Why:** the simulated memory chip is bigger than the hello program, so part of the memory is empty. That is normal.
- **Fix:** nothing needed.

### Problem 6: The tests were very slow
- **What I saw:** the hello test took about 13 minutes.
- **Why:** the simulator uses only 1 of the 4 processor cores, and the test reads the printed text one bit at a time, at real serial-port speed.
- **Fix:** while hello was running, I ran the NPU test at the same time in a **separate copy** of the project. (It cannot share the same folder, because each test deletes the other's files.)
- **Lesson:** start long tests early, and run them side by side in separate folders.

**Also seen:** many lines starting with `sorry:` or `warning:` while the design was being prepared. They come from other people's add-on blocks (not TinyQV or the NPU) and are normal for this simulator. They do not affect the results.

## 5. What I found out about the NPU (for the research question)

- The AI model is small: 144 inputs (a 12×12 picture) → 18 → 10 outputs (one for each digit).
- For **one picture**, the CPU has to talk to the NPU **810 times**.
  - 698 of these send data, but each one carries only **4 weights** (4-bit numbers).
  - The rest set up settings and read results.
- On TinyQV, reading 32 bits from memory takes about **20 clock cycles**, because memory is reached over the slow QSPI wires.

**My idea (not yet proven):** on TinyQV, **moving data around probably costs more time than the maths itself**. One 32-bit register can hold **8** four-bit weights, but the NPU takes only 4 at a time and the CPU has to repack them first. A special new CPU instruction might use all 8 directly.

**Research question:** *when memory is the slowest part, is a new CPU instruction better than a separate NPU block?*

**Next step to test this:** write the same model in plain C on TinyQV and count the clock cycles. That number is my "baseline" to beat.

*Update after the meeting:* Prof. Popovici steered the research away from extending TinyQV (see [week-04-meeting.md](week-04-meeting.md)). The point about data movement still applies, now to the link between an FPGA and the accelerator chip.

## 6. Where the files are

`hello-rtl.fst` and `npu.log` were downloaded to Kamrul's laptop. The other files stayed in the Codespace.

| File | What it is |
|---|---|
| `test/hello-rtl.fst` | Waveform of the hello program. **Best one to show** (it has the clock, the QSPI memory wires and the program counter). |
| `test/basic-rtl.fst` | Waveform of the CPU tests. |
| `test/npu.test-rtl.fst` | Waveform of the NPU test. |
| `test/npu.log` | Full text output of the NPU test, including small pictures of the digits and the NPU's answers. |
| Screenshots | _Write the file names here after taking them._ |

These files are **not saved in git**. Download any you want to keep (right-click → Download) before deleting the Codespace.

## 7. How to look at a waveform with Surfer (step by step)

Surfer is now installed in VS Code in this Codespace.

1. In the VS Code file list on the left, open the `test` folder.
2. Click **`hello-rtl.fst`**. It should open in Surfer.
   (If it does not: right-click it → **Open With…** → **Surfer**.)
3. On the left of Surfer is a list of **scopes** (parts of the design), like folders. Click **`tb_qspi`**.
4. Below it you will see the signals in that part. Click a signal name to add it to the screen. Add:
   - `clk`: the clock (the heartbeat of the chip)
   - `qspi_clk_out`: the memory clock
   - `qspi_flash_select`: goes low when the CPU reads code from flash
   - `qspi_data_in` and `qspi_data_out`: the 4 data wires to and from memory
5. To add the **program counter** (the address of the instruction the CPU is running):
   open `tb_qspi` → `user_project` → `i_tinyqv` → `cpu`, then click **`pc`**.
6. Moving around:
   - **Zoom** in or out: hold **Ctrl** and scroll the mouse wheel. Or use the zoom buttons at the top.
   - **Move left/right:** scroll the mouse wheel.
   - **See everything:** press the "zoom to fit" button at the top.
   - **Read a value at one moment:** click on the waveform; a line (cursor) appears and the values show next to the signal names.
7. To see numbers in hex: right-click a signal like `pc` → **Format** → **Hexadecimal**.
8. Zoom in near the start, where the CPU fetches its first instructions from flash. You should see `qspi_flash_select` go low, `qspi_clk_out` toggling, data on the QSPI wires, and `pc` counting up. **Take the screenshot there.**

**What to say about the picture:** "This is the CPU starting up. It reads its instructions from flash memory over 4 wires, a few bits at a time. That is why memory access is slow on TinyQV."
