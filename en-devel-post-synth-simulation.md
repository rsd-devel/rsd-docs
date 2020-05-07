# Run post-synthesis (implementation) simulation

This page describes the procedure to perform post-synthesis simulation.  
This simulation may help debugging when RSD runs correctly on the functional simulation but an FPGA.  

## Setup the required development environment and environment variables.

1. See [Development Environment](https://github.com/rsd-devel/rsd/wiki/en-devel-environment) and setup the development environment for ```Post-synthesis Simulation For FPGA```.
2. See [Environment Variables](https://github.com/rsd-devel/rsd/wiki/en-devel-environment-variables) and setup the environment variables for ```Post-synthesis Simulation For FPGA```.
3. (Optional) Install Synplify.

## For using Vivado only  
### 1. Synthesize & Run Simulation
* Open Processor/Src/Makefile.vivado.mk specify the ```TEST_CODE``` and ```MAX_TEST_CYCLES``` variables   
    * ```TEST_CODE``` is the path of code.hex to be simulated with
    * ```MAX_TEST_CYCLES``` is the maximum number of cycles to be simulated 
* Go to Processor/Src and simply run below commands according to the purpose
    ```
    make -f Makefile.vivado.mk post-[synthesis|implementation][-timing]
    ```
    * For example, to run post-synthesis functional simulation,
        ```
        make -f Makefile.vivado.mk post-synthesis
        ```
    * Or to run post-implementation timing simulation,
        ```
        make -f Makefile.vivado.mk post-implementation-timing
        ```
* If simulation does not launch correctly, please remove Vivado project by below command and try again 
    ```
    make -f Makefile.vivado.mk post-synthesis-clean
    ```

## For using synplify netlist  
### 1. Generate the netlist file (rsd.vm) of RSD using Synplify.

1. Open Processor/Project/Synplify/ver2017-03.prj on Synplify.  
2. In Synplify, select "Zedboard_post_synthesis" in the opened project and click "Run".  
   * If the synthesis ran successfully, rsd.vm is generated in Project/Synplify/Zedboard_post_synthesis/. 

### 2. Synthesize using Vivado
* Run below command
```
make post-synthesis
```

### 3. Begin post-synthesis simulation on QuestaSim
* Run below command
    ```
    make post-synthesis-run
    ```
* If you want to launch GUI simulation, run below command
    ```
    make post-synthesis-run-gui
    ```
* You can dump Kanata log by executing below command
    ```
    make post-synthesis-kanata
    ```
* If simulation does not launch correctly, please remove Vivado project by below command and try again 
    ```
    make post-synthesis-clean
    ```