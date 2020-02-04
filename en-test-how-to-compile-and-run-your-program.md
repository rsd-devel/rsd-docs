This page describes how to compile and run your program on RSD on Verilator.

## 0. Go to $RSD_ROOT/Processor/Src.
* Make sure RSD is correctly compiled by ```make -f Makefile.verilator.mk```.
    * Tested environment
        * Verilator 4.026 2020-01-11 rev v4.026-2-g0c6c83e
        * GCC 6.5.0 (x86-64)
        * GCC 8.1.0 (RISC-V)
## 1. Open Verification/TestCode/Makefile.inc and update the version number of gcc to the version you are using.
* example (I'm using 8.1.0):
    ``` 
    LIBGCC = \
      -L$(RSD_GCC_NATIVE)/../lib/gcc/riscv32-unknown-elf/8.1.0 \
      -lgcc \
      -lgcov \
      -L$(RSD_GCC_NATIVE)/../riscv32-unknown-elf/lib \
      -lm
    ```
* This step is required for now but we will fix it soon.
## 2. Copy Verification/TestCode/C/HelloWorld to Verification/TestCode/C/YourTest.
* Note that the YourTest directory must be in Verification/TestCode/C.
## 3. Overwrite Verification/TestCode/C/YourTest/code.c with your test code.
* Note that RSD does not support printf at this time.
* See Verification/TestCode/C/HelloWorld/code.c to learn how RSD currently outputs characters.
## 4. Modify Verification/TestCode/C/YourTest/serial.ref.txt so that this file has the expected output of your test code.
## 5. If you add any source code file except for code.c, add them in the SRCS variable in Verification/TestCode/C/YourTest/Makefile.
## 6. Go to Verification/TestCode/C/YourTest and make your test code by the following command.
```
cd Verification/TestCode/C/YourTest
make
```
* This command will compile YourTest and generate code.hex in Verification/TestCode/C/YourTest.
## 8. Go back to $RSD_ROOT/Processor/Src, open Makefile.verilator.mk, and modify the TEST_CODE variable as below.
```
TEST_CODE = Verification/TestCode/C/YourTest
```
## 9. Run simulation with your test code by the following command.
```
make -f Makefile.verilator.mk run
```