# Getting started

* This section describes the procedure from compiling the source code to perform functional simulation.


## Environment

See [this wiki page](https://github.com/rsd-devel/rsd/wiki/en-devel-environment) and setup the required environment.

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
