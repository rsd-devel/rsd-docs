# Development Environment

This page describes the development environment required for RSD.  
The environment depends on what you want to do.  
This page considers the following three purposes.
* Software simulation
* Boot on Xilinx Zynq FPGA boards
* Synthesis for ASIC (experimental)

Please read this page carefully and setup required OS, tools, and packages.  
The version of each software that we tested is also listed, but RSD could work with other versions.  

## Operating System

Cygwin on Windows or Linux can be used, depending on your purpose.  
Only x86-64 machines are tested.

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
| Python 3 | 3.4.2 |
| RISC-V GCC cross compiler | 8.1.0 |

### For Software Simulation

One of the followings is also required to simulate RSD on software simulators.

|    |  Tested version  |
| ---- | ---- |
| Mentor QuestaSim | 2019.4.2 |
| Mentor ModelSim |  |
| Verilator | 4.026<br>3.922 |
| Xilinx Vitis (including Vivado) | 2019.2.1 |

### For Boot on Xilinx Zynq FPGA Boards

The followings are also required to boot RSD on Xilinx Zynq FPGA boards.  

|    |  Tested version  |
| ---- | ---- |
| Xilinx Vitis (including Vivado) | 2019.2.1 |

In addition, run the following commands to install necessary packages via apt-get.
```
alias gmake=make  # If you use Ubuntu    
sudo apt-get install u-boot-tools ntp device-tree-compiler flex openssl   
```

### For Synthesis for ASIC (experimental)

The following is also required to synthesize RSD for ASIC.

|    |  Tested version  |
| ---- | ---- |
| Synopsys Design Compiler | O-2018.06-SP4 |

## Recommended Tools

### For Boot on Xilinx Zynq FPGA Boards

RSD can be synthesized using Synopsys Synplify.  
**In our evaluation, Synplify+Vitis provided better operating frequency than Vitis-only**.  
We therefore recommend to use Synplify if you have its license.  

|    |  Tested version  |
| ---- | ---- |
| Synopsys Synplify | M-2017.03-SP1 |

### For Development

* Pipeline viewer [Konata](https://github.com/shioyadan/Konata)
    * Download and extract the pre-built binary archive.
* [Visual Studio Code](https://code.visualstudio.com/)
    * Please install SystemVerilog extension after introduction.
    * We strongly recommend to use [svls-vscode](https://github.com/dalance/svls-vscode).

## Related documents

You must also setup some environment variables after setting up the development environment.  
Please see [this wiki page](https://github.com/rsd-devel/rsd/wiki/en-devel-environment-variables) for the details.
