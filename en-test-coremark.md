# CoreMark and Dhrystone: checks and measurements

Simulation benchmarks use pinned public sources. Build the simulator, then run these commands from `Processor/Src`. See the [test program reference](en-test-program#coremark).

## Fetching and functional tests

```bash
make test/External/Coremark/fetch
make test/External/Dhrystone/fetch
make test/External/Coremark/run test/External/Coremark/Coremark_for_RV32I/run
make test/External/Dhrystone/run
```

Sources are stored in `Coremark/External` and `Dhrystone/External`. Test targets build HEX files and reference output as needed. Use `test/External/Coremark/build` or `test/External/Dhrystone/build` to build only.

| Test | Configuration and checks |
| --- | --- |
| CoreMark | RV32IM and RV32I, one iteration each; CRC and UART output |
| Dhrystone | RV32IM C port, 100 iterations; return value, final state and UART output |

Neither requires an FP pipeline. Functional tests return synthetic time, so their displayed time cannot measure performance. `test/level-2/run` aggregates these tests and is included in `test/all/run`.

## Cycle-based measurements

```bash
make bench/Coremark/run
make bench/Dhrystone/run
make bench/Dhrystone/run DHRYSTONE_BUILTINS=0
```

`bench/*/run` builds with `BENCHMARK=1`, checks results and reads the actual cycle counter. After validation, TestDriver prints:

| Metric | Formula |
| --- | --- |
| CoreMark/MHz | `iterations * 1000000 / cycles` |
| DMIPS/MHz | `iterations * 1000000 / (cycles * 1757)` |

The measured interval covers the benchmark loop, excluding startup, initialization, validation and UART output, but including CSR-read overhead. Defaults are one CoreMark iteration and 2000 Dhrystone iterations. Adjust `DHRYSTONE_BENCH_ITERATIONS` and, for longer runs, `MAX_TEST_INSTRUCTIONS`. Keep the interval below `2^32` cycles because the measurement code reads only the lower 32 bits of the 64-bit `mcycle` counter.

These short simulations from reset provide estimates, not runs meeting the minimum duration for official score publication. Record compiler version, iterations and build settings. Dhrystone defaults to `DHRYSTONE_BUILTINS=1`, allowing GCC libc optimizations and using 8-byte function/loop alignment; this affects scores.

Functional tests and benchmarks share output directories: run them sequentially. Mode changes trigger rebuilding, and `test/.../run` restores functional mode. `test/all/run` excludes `bench/*/run`.

## Cleaning

`test/External/Coremark/clean` and `test/External/Dhrystone/clean` remove outputs but preserve fetched sources. Clean after changing compiler or normal build flags.

## Run CoreMark on ZedBoard

Set `RSD_ZYNQ_HOST` on the development host as described in the [board startup instructions](en-fpga-zynq-synth-for-linux#boot-the-board-and-run-a-program). Run these commands from the repository root. Fetch the sources once.

```bash
./RunContainer.sh make test/External/Coremark/fetch
./RunContainer.sh make test/External/Coremark/build
make test/External/Coremark/zynq/run
```

`zynq/run` uploads the built RV32IM program and displays its UART output in the terminal. Press Ctrl-C to stop the loader. On hardware, CoreMark started, but characters were missing from subsequent UART output, so the CRC and score remain unverified. Hardware measurements also require checking the clock frequency, timing code and run duration.
