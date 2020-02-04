# Development Environment

Development environment required for RSD depends on what you want to do.  
This page considers the following three purposes.
* Software simulation
* Boot on Xilinx Zynq FPGA boards
* Synthesis for ASIC  

## Operating System

Cygwin on Windows or Linux can be used, depending on your purpose.

|    |  OS  |  Tested version  |
| ---- | ---- | ---- |
| Software simulation | Windows<br>Linux | Cygwin on Windows 10<br>Debian 8<br>Ubuntu 18.04 | 
| Boot on Xilinx Zynq FPGA boards | Linux | Debian 8<br>Ubuntu 18.04 | 
| Synthesis for ASIC | Linux | Debian 8<br>Ubuntu 18.04 | 

## Necessary Dependencies

The follows are required for all the three purposes on both Windows and Linux.

|    |  Tested version  |
| ---- | ---- |
| Git |  |
| GNU Make | 4.0 |
| Python 3 | 3.4.2 |
| GCC (x86-64) | 6.5.0 |
| GCC (RISC-V) | 8.1.0 |
