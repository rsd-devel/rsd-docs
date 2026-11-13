# Functional simulation

RSD's RTL simulation checks termination conditions, architectural registers and UART output. Run commands from `Processor/Src`; see [Getting started](en-devel-getting-started).

## Build the simulator

| Simulator | Build | Basic tests |
| --- | --- | --- |
| Verilator | `make -j4` | `make test/level-1/run` |
| ModelSim/QuestaSim | `make SIM=modelsim` | `make SIM=modelsim test/level-1/run` |
| Vivado XSim | `make SIM=xsim` | `make SIM=xsim test/level-1/run` |

All use `Verification/TestMain.sv`. Rebuild after RTL/testbench changes. Registered program targets such as `test/level-1/run` build required HEX files but do not build the simulator. See [Test programs](en-test-program) for groups and external setup.

## Verify one program

Build and verify HelloWorld:

```bash
make test/C/HelloWorld/run
```

For an arbitrary directory, build its program first; the `RunTest.py` command does not build the selected program:

```bash
python3 ../Tools/TestDriver/RunTest.py --simulator=verilator Verification/TestCode/C/HelloWorld
```

TestDriver reads lowercase `cfg.xml` from that directory, then checks `RegisterValues` and `serial.ref.txt` after normal termination. UART output is saved in `serial.out.txt`.

```xml
<Config>
  <MaxTestInstructions>10000</MaxTestInstructions>
  <MaxNoCommitCycles>500</MaxNoCommitCycles>
  <RegisterValues>
    <R10>0</R10>
  </RegisterValues>
</Config>
```

| Setting | Meaning |
| --- | --- |
| `MaxTestInstructions` | Limit on committed RISC-V instructions including startup; speculation/replay does not consume it |
| `MaxNoCommitCycles` | Maximum consecutive cycles without micro-operation commit; default 500; exceeding it fails |
| `EnablePC_Goal` | Default `1`: reach the termination PC before the instruction budget; `0` runs to the budget for continuous tests |
| `MaxTestCycles` | Additional cycle limit; omitted or `0` disables it; reaching it before the instruction budget fails |

`RegisterValues` can be empty for UART-only checks. Legacy cycle-only configurations remain accepted; new tests should specify instruction and no-commit limits. Increase no-commit limits for cases with long waits such as cache flushing.

Logs report termination reason, committed instructions/micro-operations, cycles, maximum no-commit interval and IPC. IPC is informational, not a pass criterion. See the [TestDriver reference](en-test-driver) for boundary conditions.

## Debugging

`sim/run`, `sim/kanata` and `sim/dump` use make variables rather than `cfg.xml` and do not compare expected results. Use `RunTest.py` or registered `test/.../run` targets for validation. Build the program first:

```bash
make test/level-1/build
make sim/run TEST_CODE=Verification/TestCode/C/Fibonacci
make sim/kanata TEST_CODE=Verification/TestCode/C/Fibonacci
```

Open `Kanata.log` with [Konata](https://github.com/shioyadan/Konata/releases) to investigate replay and stalled commits. `sim/kanata` also writes `Register.csv`. To adjust limits:

```bash
make sim/kanata \
    TEST_CODE=Verification/TestCode/C/Fibonacci \
    MAX_TEST_INSTRUCTIONS=200000 MAX_NO_COMMIT_CYCLES=1000
```

Verilator's `sim/dump` generates `Register.csv`, `RSD.log`, `Kanata.log` and `simx.vcd`; see [Verilator](en-test-verilator). Start a GUI with `make SIM=modelsim sim/gui TEST_CODE=...` or `make SIM=xsim sim/gui TEST_CODE=...`.
