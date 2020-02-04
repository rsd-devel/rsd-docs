# Getting started

* This section describes the procedure from compiling the source code to perform functional simulation.


## Environment

* For Windows
    * Install cygwin
        * Make sure to install "make" at the same time
    * You can use cygwin's python and git, but it may be better to install Windows version
    * Note that Windows cannot be used to run RSD on a Zynq board.  
* For Windows and Linux
    * Install python, make, git, gcc (x86-64), gcc (RISC-V)
* Tested environment
    * GNU Make 4.0
    * Python 3.4.2
    * GCC 6.5.0 (x86-64)
    * GCC 8.1.0 (RISC-V)

### Tools required for functional simulation

* One of the following is required
    * Mentor QuestaSim or ModelSim
    * Verilator
    * Xilinx Vitis (including Vivado)
* Tested environment
    * Mentor QuestaSim 2019.4.2
    * Verilator 4.026 2020-01-11 rev v4.026-2-g0c6c83e
    * Xilinx Vitis 2019.2

### Tools required for synthesis for Xilinx Zynq FPGA

* The following is not required if you only perform functional simulation.
    * Synopsys Synplify
        * Used for compiling (logic synthesis) of SystemVerilog
    * Xilinx Vitis (including Vivado)
        * Output bitstream for FPGA based on netlist output by Synplify
* Tested environment
    * Synopsys Synplify 2017-03
    * Xilinx Vitis 2019.2

### Recommended tools

* Pipeline viewer Konata
    * Download and extract the pre-built binary archive from [Konata](https://github.com/shioyadan/Konata)
* Editor
    * [Visual Studio Code] (https://code.visualstudio.com/) is recommended
    * Please install SystemVerilog extension after introduction
    * It is recommended to install [svls-vscode](https://github.com/dalance/svls-vscode)

## Setting environment variables
* Refer to files in "Processor/Tools/SetEnv" and set environment variables
* See "SetEnv.bat" for Windows and "SetEnv.sh" for Linux
* At least RSD_ROOT must be set for simulation
    * On Windows, RSD_CYGWIN_PATH must also be set
* Set RSD_QUESTASIM_PATH when using Modelsim / QuestaSim

## Simulation on Verilator/Modelsim/QuestaSim/Vitis

* Move to "Processor/Src" and make as follows.
    * For Modelsim / QuestaSim
        ```
        make
        make run        # run simulation
        make kanata     # run simulation & outputs a konata log file
        ```
    * For Verilator, specify Makefile.verilator, like ```make -f Makefile.verilator```
    * For Vivado, specify Makefile.vivado, like ```make -f Makefile.vivado```
* The above sub-command is "kanata", not "konata".
* See [this wiki page](https://github.com/rsd-devel/rsd/wiki/en-test-how-to-compile-and-run-your-program) to learn how to compile and run your code on RSD on Verilator.
* See [Functional simulation](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-test-simulation) for details.

## Visualization of simulation results

* If the simulation is successful, "kanata.log" is generated in Processor/Src
* Use [Konata](https://github.com/shioyadan/Konata/releases) to visualize logs

## Synthesis for Xilinx Zynq FPGA and run on a board

* See [this RSD wiki page](https://github.com/rsd-devel/rsd/wiki/en-fpga-zynq-build-linux-simple).

## Before editing the code
* [Coding convention](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-devel-coding-convention)
* [Repository update rules](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-devel-repository-convention)
