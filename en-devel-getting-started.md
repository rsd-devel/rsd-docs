# Getting started

* This section describes the procedure from compiling the source code to perform functional simulation.


## Environment

* For Windows
    * Install cygwin
        * Make sure to install "make" at the same time
    * You can use cygwin's python and git, but it may be better to install Windows version
* For Windows and Linux
    * Install python, make, git


### Tools required for functional simulation

One of the following is required
* Mentor QuestaSim or ModelSim
* Verilator
* Vivado


### Tools required for synthesis for FPGA

The following is not required if you only perform functional simulation.

* Synopsys Synplify
    * Used for compiling (logic synthesis) of SystemVerilog
* Xilinx Vivado
    * Output bitstream for FPGA based on netlist output by Synplify


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

## simulation

* Move to "Processor/Src" and make as follows
    * For Modelsim / QuestaSim
        ```
        make
        make run        # run simulation
        make kanata     # run simulation & outputs a konata log file
        ```
    * For Verilator, specify Makefile.verilator, like ```make -f Makefile.verilator```
    * For Vivado, specify Makefile.vivado, like ```make -f Makefile.vivado```
* The above sub-command is "kanata", not "konata"
* See below for details
    * See [Functional simulation](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-test-simulation)


## Visualization of simulation results

* If the simulation is successful, "kanata.log" is generated in Processor/Src
* Use [Konata](https://github.com/shioyadan/Konata/releases) to visualize logs

## Synthesis

* See "[How to Synthesis](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-synth-howto)"

## Before editing the code
* [Coding convention](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-devel-coding-convention)
* [Repository update rules](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-devel-repository-convention)
