# How to compile and run your program on RSD on Verilator.

## 0. Build RSD using Verilator.
1. See [this wiki page](https://github.com/rsd-devel/rsd/wiki/en-devel-environment) and setup the required development environment.
2. Go to $RSD_ROOT/Processor/Src.
3. Make sure RSD is correctly compiled by ```make -f Makefile.verilator.mk```.

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
## 8. Go to $RSD_ROOT/Processor/Src, open Makefile.verilator.mk, and modify the TEST_CODE variable as below.
```
TEST_CODE = Verification/TestCode/C/YourTest
```
## 9. Run simulation with your test code by the following command.
```
make -f Makefile.verilator.mk run
```