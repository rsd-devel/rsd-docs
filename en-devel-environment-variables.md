# Environment Variables

This page describes the environment variables that must be set to use RSD.  
The required environment variables depend on what you want to do.  
This page considers the following four purposes.
* Software simulation
* Boot on Xilinx Zynq FPGA boards
* Post-synthesis Simulation For FPGA
* Synthesis for ASIC (experimental)

Note that you must setup the [development environment](https://github.com/rsd-devel/rsd/wiki/en-devel-environment) first.

All the environment variables of RSD are written in SetEnv.* file in [Processor/Tools/SetEnv](https://github.com/rsd-devel/rsd/tree/master/Processor/Tools/SetEnv).
* SetEnv.bat : for Windows
* SetEnv.sh  : for Linux  

Please copy the SetEnv.* to MySetEnv.* to create your own SetEnv file.   
(MySetEnv.* is gitignored.)

## Necessary Environment Variables

The followings are necessary for all the four purposes.

| Variable Name | Detail |
| ---- | ---- |
| RSD_ROOT | Specify the root directory where you checked out RSD. |
| RSD_GCC_PATH | Specify the directory that contains a RISC-V GCC binary. |
| RSD_GCC_PREFIX | Specify the prefix of the RISC-V GCC binary.<br>Example: riscv32-unknown-elf- |
| RSD_GCC_VERSION | Specify the version number of the RISC-V gcc cross compiler.<br>Example: 8.1.0 |

### For Software Simulation

Some environment variables below are also required to simulate RSD on software simulators, depending on the simulator you use.

* Mentor QuestaSim, Mentor ModelSim

    | Variable Name | Detail |
    | ---- | ---- |
    | RSD_QUESTASIM_PATH | Specify the ```bin``` directory of Modelsim or QuestaSim. |

* Verilator

    No additional variable is required.  
    Make sure the ```verilator``` command is functioning.

* Xilinx Vitis (Vivado)

    | Variable Name | Detail |
    | ---- | ---- |
    | RSD_VIVADO_BIN | Specify the ```bin``` directory of Vivado.<br>Example: /Xilinx_tool_install_path/Vivado/2019.2/bin |   

### For Boot on Xilinx Zynq FPGA Boards / Post-synthesis Simulation For FPGA

The followings are also required to boot RSD on Xilinx Zynq FPGA boards or run post-synthesis simulation for FPGA.  

| Variable Name | Detail |
| ---- | ---- |
| RSD_VIVADO_BIN | Specify the ```bin``` directory of Vivado.<br>Example: /Xilinx_tool_install_path/Vivado/2019.2/bin |
| RSD_ARM_LINUX | Specify a directory where you want to download and build [Zynq PS Linux](https://github.com/rsd-devel/rsd/wiki/en-fpga-zynq-build-linux-simple).<br>A directory outside $(RSD_ROOT) is recommended. |

### For Synthesis for ASIC (experimental)

The following is also required to synthesize RSD for ASIC.

| Variable Name | Detail |
| ---- | ---- |
| RSD_DC_SHELL_BIN | Specify the ```dc_shell``` binary of Design Compiler. |

