# Compile and run your program on RSD with Verilator

Set up the [development environment](en-devel-getting-started). Run the commands below from `Processor/Src` in the RSD checkout. The shared [test compiler configuration](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Makefile.inc) selects RV32, the `ilp32` ABI, and picolibc search paths.

## 1. Build the simulator and shared startup code

```bash
make -j"$(nproc)"
make test/crt/build
```

## 2. Create a program from HelloWorld

Create a new directory under `Verification/TestCode/C` and copy only the inputs:

```bash
mkdir Verification/TestCode/C/YourTest
cp Verification/TestCode/C/HelloWorld/{Makefile,code.c,cfg.xml,serial.ref.txt} \
    Verification/TestCode/C/YourTest/
```

Edit `YourTest/code.c`. The template writes bytes to `RSD_SERIAL_OUTPUT` from generated `rsd-memory-map.h` (default `0x40002000`); `Verification/TestCode/C/lib.c` also provides serial-output helpers. The basic C template does not link a general `printf` implementation. The dedicated benchmark ports provide their own output functions.

Update `serial.ref.txt` to the exact expected UART output, including newlines, and `cfg.xml` to the expected registers and execution limits. For a program whose `main` returns zero, this configuration checks the return value in `a0`:

```xml
<Config>
  <MaxTestInstructions>10000</MaxTestInstructions>
  <MaxNoCommitCycles>500</MaxNoCommitCycles>
  <RegisterValues>
    <R10>0</R10>
  </RegisterValues>
</Config>
```

`EnablePC_Goal` defaults to `1`, requiring the program to reach the termination loop before its instruction budget expires. Set a budget appropriate to your program. See the [TestDriver documentation](en-test-driver) for continuous tests and additional limits.

Add any additional C files to `SRCS` in `YourTest/Makefile`.

## 3. Build and verify

```bash
make -C Verification/TestCode/C/YourTest
python3 ../Tools/TestDriver/RunTest.py --simulator=verilator Verification/TestCode/C/YourTest
```

The program build generates `code.elf`, `code.bin`, and `code.hex`. The `RunTest.py` command reads `cfg.xml` and compares register and serial expectations; it does not build an arbitrary `TEST_CODE` directory. Rebuild after editing the program. Keep the RTL and program configuration consistent, and clean both when changing FP configuration.

## 4. Inspect execution

```bash
make sim/run TEST_CODE=Verification/TestCode/C/YourTest
make sim/kanata TEST_CODE=Verification/TestCode/C/YourTest
make sim/dump TEST_CODE=Verification/TestCode/C/YourTest
```

Open `Kanata.log` with Konata and `simx.vcd` with a VCD viewer. These debug targets use make variables instead of `cfg.xml` and do not compare expected output. Pass, for example, `MAX_TEST_INSTRUCTIONS=200000 MAX_NO_COMMIT_CYCLES=1000` when the debug run needs different limits. There is no need to edit `TEST_CODE` in the simulator Makefile.

## 5. Add the program to a test suite

For repeated regression testing, add the directory to `Verification/TestCode/C/Makefile` and register its build dependency and execution target in `Makefiles/TestCommands.inc.mk`. See the [test program reference](en-test-program) for the existing suites.
