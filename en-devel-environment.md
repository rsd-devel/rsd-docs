# Development Environment

Development environment required for RSD depends on what you want to do.  
This page considers the following three purposes.
* Software simulation
* Boot on Xilinx Zynq FPGA boards
* Synthesis for ASIC (experimental)

## Operating System

Cygwin on Windows or Linux can be used, depending on your purpose.

|    |  OS  |  Tested version  |
| ---- | ---- | ---- |
| Software simulation | Windows<br>Linux | Cygwin on Windows 10<br>Debian 8<br>Ubuntu 18.04 | 
| Boot on Xilinx Zynq FPGA boards | Linux | Debian 8<br>Ubuntu 18.04 | 
| Synthesis for ASIC | Linux | Debian 8<br>Ubuntu 18.04 | 

## Necessary Dependencies

The followings are required for all the three purposes on both Windows and Linux.

|    |  Tested version  |
| ---- | ---- |
| Git |  |
| GNU Make | 4.0 |
| Python 3 | 3.4.2 |
| GCC (x86-64) | 6.5.0 |
| GCC (RISC-V) | 8.1.0 |

### For Software Simulation

One of the following is also required to simulate RSD on software simulators.

|    |  Tested version  |
| ---- | ---- |
| Mentor QuestaSim | 2019.4.2 |
| Mentor ModelSim | 4.026 2020-01-11 rev v4.026-2-g0c6c83e |
| Xilinx Vitis | 2019.2 |

### For Boot on Xilinx Zynq FPGA Boards

The followings are also required to boot RSD on Xilinx Zynq FPGA boards.

|    |  Tested version  |
| ---- | ---- |
| Synopsys Synplify | 2017-03 |
| Xilinx Vitis (including Vivado) | 2019.2 |

### For Synthesis for ASIC (experimental)

The following is also required to synthesize RSD for ASIC.

|    |  Tested version  |
| ---- | ---- |
| Synopsys Design Compiler |  |

