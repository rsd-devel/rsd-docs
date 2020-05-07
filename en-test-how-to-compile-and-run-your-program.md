# How to compile and run your program on RSD on Verilator.

## 0. Build RSD using Verilator.
1. See [Development Environment](https://github.com/rsd-devel/rsd/wiki/en-devel-environment) and setup the development environment for ```Software simulation```.
2. See [Environment Variables](https://github.com/rsd-devel/rsd/wiki/en-devel-environment-variables) and setup the environment variables for ```Software simulation```.
3. Go to $RSD_ROOT/Processor/Src.
4. Make sure RSD is correctly compiled by ```make -f Makefile.verilator.mk```.

## 1. Copy Verification/TestCode/C/HelloWorld to Verification/TestCode/C/YourTest.
* Note that the YourTest directory must be in Verification/TestCode/C.
## 2. Overwrite Verification/TestCode/C/YourTest/code.c with your test code.
* Note that RSD does not support printf at this time.
* See Verification/TestCode/C/HelloWorld/code.c to learn how RSD currently outputs characters.
## 3. Modify Verification/TestCode/C/YourTest/serial.ref.txt so that this file has the expected output of your test code.
## 4. If you add any source code file except for code.c, add them in the SRCS variable in Verification/TestCode/C/YourTest/Makefile.
## 5. Go to Verification/TestCode/C/YourTest and make your test code by the following command.
```
cd Verification/TestCode/C/YourTest
make
```
* This command will compile YourTest and generate code.hex in Verification/TestCode/C/YourTest.
## 6. Go to $RSD_ROOT/Processor/Src, open Makefile.verilator.mk, and modify the TEST_CODE variable as below.
```
TEST_CODE = Verification/TestCode/C/YourTest
```
## 7. Run simulation with your test code by the following command.
```
make -f Makefile.verilator.mk run
```