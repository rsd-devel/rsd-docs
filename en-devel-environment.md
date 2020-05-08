# Development Environment

This page describes the development environment required for RSD.  
The environment depends on what you want to do.  
This page considers the following four purposes.
* Functional simulation
* Boot on Xilinx Zynq FPGA boards
* Post-Synthesis Simulation For FPGA
* Synthesis for ASIC (experimental)

Please read this page carefully and setup required OS, tools, and packages.  
The version of each software that we tested is also listed, but RSD could work with other versions.  

## Operating System

Cygwin on Windows or Linux can be used, depending on your purpose.  
Only x86-64 machines are tested.

|    |  OS  |  Tested version  |
| ---- | ---- | ---- |
| Functional simulation | Windows<br>Linux | Cygwin on Windows 10<br>Debian 8<br>Ubuntu 18.04 | 
| Boot on Xilinx Zynq FPGA boards | Linux | Debian 8<br>Ubuntu 18.04 | 
| Post-Synthesis Simulation For FPGA | Linux | Debian 8<br>Ubuntu 18.04 | 
| Synthesis for ASIC | Linux | Debian 8<br>Ubuntu 18.04 | 

## Necessary Dependencies

The followings are required for all the four purposes on both Windows and Linux.

|    |  Tested version  |
| ---- | ---- |
| Git |  |
| Python 3 | 3.4.2 |
| RISC-V GCC cross compiler | 8.1.0 |

### For Functional Simulation

One of the followings is also required to simulate RSD on software simulators.

|    |  Tested version  |
| ---- | ---- |
| Mentor QuestaSim | 2019.4.2 |
| Verilator | 4.026<br>3.922 |
| Xilinx Vitis (including Vivado) | 2019.2.1 |

### For Boot on Xilinx Zynq FPGA Boards / Post-synthesis Simulation For FPGA

The followings are also required to boot RSD on Xilinx Zynq FPGA boards or run post-synthesis simulation for FPGA.  

|    |  Tested version  |
| ---- | ---- |
| Xilinx Vitis (including Vivado) | 2019.2.1 |

In addition, run the following commands to install necessary packages via apt-get.
```
alias gmake=make  # If you use Ubuntu    
sudo apt-get install u-boot-tools ntp device-tree-compiler flex openssl   
```

* **(Optional)**  
    RSD can be synthesized using Synopsys Synplify.  
    **In our evaluation, Synplify+Vivado provided better operating frequency than Vivado-only**.  
    We therefore recommend to use Synplify if you have its license.  
    The following is required for running the Synplify+Vivado design on Xilinx Zynq FPGA boards.

    |    |  Tested version  |
    | ---- | ---- |
    | Synopsys Synplify | M-2017.03-SP1 |

    In addition, the following is required for post-synthesis simulation for the Synplify+Vivado design. 
    |    |  Tested version  |
    | ---- | ---- |
    | Mentor QuestaSim | 2019.4.2 |


### For Synthesis for ASIC (experimental)

The following is also required to synthesize RSD for ASIC.

|    |  Tested version  |
| ---- | ---- |
| Synopsys Design Compiler | O-2018.06-SP4 |

## Recommended Tools

* Pipeline viewer [Konata](https://github.com/shioyadan/Konata)
    * Download and extract the pre-built binary archive.
* [Visual Studio Code](https://code.visualstudio.com/)
    * Please install SystemVerilog extension after introduction.
    * We strongly recommend to use [svls-vscode](https://github.com/dalance/svls-vscode).

## Related documents

You must also setup some environment variables after setting up the development environment.  
Please see [this wiki page](https://github.com/rsd-devel/rsd/wiki/en-devel-environment-variables) for the details.
