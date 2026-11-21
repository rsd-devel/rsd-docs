# Functional simulation with Verilator

RSD uses Verilator 5.054 and the shared SystemVerilog testbench `Verification/TestMain.sv`. See [Getting started](../development/getting-started.md). For manual setup, `RSD_VERILATOR_BIN` can select the executable; otherwise make uses `verilator` on `PATH`.

## Build and run

From `Processor/Src`:

```bash
make -j"$(nproc)"
make test/level-1/run
make sim/run TEST_CODE=Verification/TestCode/C/Fibonacci
```

`test/level-1/run` builds basic programs and checks expected results. `sim/run` executes an already built program. See [Functional simulation](simulation.md) for individual tests and settings.

## Pipeline and waveform output

After building basic tests:

```bash
make sim/kanata TEST_CODE=Verification/TestCode/C/Fibonacci
make sim/dump TEST_CODE=Verification/TestCode/C/Fibonacci
```

Outputs appear in `Processor/Src`:

| Output | Purpose |
| --- | --- |
| `Kanata.log` | Pipeline trace for Konata |
| `RSD.log` | Trace before conversion to Kanata format |
| `Register.csv` | Register values at commit |
| `simx.vcd` | Waveform from `sim/dump`, viewable with GTKWave or another VCD viewer |

The Makefile enables `--trace`; `sim/dump` passes `+WAVE_LOG_FILE=simx.vcd`. Limits for `sim/run`, `sim/kanata` and `sim/dump` are `MAX_TEST_INSTRUCTIONS`, `MAX_NO_COMMIT_CYCLES` and `MAX_TEST_CYCLES`; editing `cfg.xml` does not change their limits.

## Implementation

[VerilatorCore.inc.mk](https://github.com/rsd-devel/rsd/blob/develop/Processor/Src/Makefiles/VerilatorCore.inc.mk) and the shared [Verilator options](https://github.com/rsd-devel/rsd/blob/develop/Processor/Src/Makefiles/Verilator.inc.mk) select `TestMain` and generate the execution loop with `--main`/`--timing`. The model is `Processor/Project/Verilator/obj_dir/VTestMain`. Direct execution accepts plusargs such as `+TEST_CODE=...`; normally use make or TestDriver.

Clean and rebuild the simulator and programs after configuration changes such as enabling or disabling FP:

```bash
make clean test/level-1/clean
make -j"$(nproc)"
make test/level-1/run
```
