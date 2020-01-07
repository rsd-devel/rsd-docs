# Basic synthesis procedure (require both Vivado and Synplify)
This section describes the procedure for the synthesis using Vivado and Synplify

## Preparation
Prepare a synthesis environment based on [this page](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-devel-vivado).

## General flow of synthesis

1. Synthesize the created .sv source files with Synplify and create a netlist (.vm)
1. Create a Bitstream file (.bit) by synthesizing the system including the netlist with Vivado
1. Upload the Bitstream file to FPGA board and program a board

## Target board settings

Set target board name to TARGET_BOARD of $(RSD_ROOT)/Processor/Src/Makefiles/Vivado.inc.mk
(Compatible boards as of 06.24.2017)

* Zedboard
* ZC706 (provisional)


## Synthesizing with Synplify

Do either Getting started or Build from scratch.

* The procedure of Getting started has been confirmed only on Synplify M-2017.03. If your Synplify fails to synthesis, try Build from scratch.

### Getting started

1. Open $ (RSD_ROOT) /Processor/Project/Synplify/ver2017-03.prj with Synplify

1. Select "$(TARGET_BOARD)" in [Project Files] and compile/synthesize with [Run]

### Build from scratch

1. Create a project and add source files
    * Add .sv file (except Src/Verification/)

1. Set Implementation Options
    * Specify [FPGA model number information](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-fpga-board).
    * Specify Main_Zynq_Wrapper as the top module. Specifying module parameters as appropriate
    * Set "$(TARGET_BOARD)" to Implementation Name in Implementation Results tab
    * Set "rsd" as the Result Base Name in the Implementation Results tab

1. In the TCL console at the bottom of the screen, enter "set_option -hdl_define -set appropriate definition" to set the appropriate hdl_define
(Support list as of 06.12.2017)
    * RSD_SYNTHESIS_ZEDBOARD ($(TARGET_BOARD)=Zedboard)

1. Select "$ (TARGET_BOARD)" in [Project Files] and compile / synthesize with [Run]



## Generate Bitstream with Vivado

1. Check that the RSD netlist (rsd.vm) has been created in "$(RSD_ROOT)/Processor/Project/Synplify/$(TARGET_BOARD)/".

1. Go to $(RSD_ROOT)/Processor/Src and open the Vivado project with "make vivado"

1. Click [Flow Navigator] → [Program and Debug] → [Generate Bitstream] to create a bitstream file (*.bit)

### Note

If the IO port of the top module of RSD is changed, Block Design of Vivado needs to be modified

## Upload Bitstream file to FPGA and program a board

### Zedboard

1. Connect Zedboard's "PROG" port and "UART" port (both are microUSB ports) to a PC with two microUSB-USB cables and turn on the power.
* The driver should automatically enter if you have installed Vivado

1. Start and set up the software that can display the input from the COM port corresponding to the installed UART port.
    * Tera Term, minicom, etc.
    * Baud rate 115200

1. Open the Vivado project and click [Menu Bar]-> [File]-> [Export]-> [Export Hardware]

1. Check [Include bitstream] and click [OK]

1. Launch SDK by clicking [Menu Bar]-> [File]-> [Launch SDK] on Vivado

1. Click [Menu Bar]-> [Xilinx Tools]-> [Program FPGA] on Xilinx SDK

1. Click [Program] to program FPGA

1. Click [Menu Bar]-> [File]-> [New]-> [Application Project]

1. Set [Project name] as appropriate and click [Next]

1. Select [Hello World] in [Available Templates] and click [Finish].

1. Delete "helloworld.c" in "src" of the completed project and replace it with "$(RSD_ROOT)/Processor/Project/Vivado/Zedboard/project_src/$(program_name).c"
* Choice $(project_name) project from generated two projects ($(project_name) and $(project_name)_bsp) 
(Supported programs as of 06.12.2017)
    * run_simple
        * Sends the program set in the programinit() function of the source code to the RSD, executes it, and outputs the result to the UART port

1. Right-click on the created project-> [Run As]-> [1 Launch on Hardware (System Debugger)]

1. Program output from UART should be displayed

### ZC706

* Connect the "USB-to-JTAG" port (microUSB port), "USB-to-UART" port (miniUSB port) and PC on the ZC706 PCIe placket with the miniUSB-USB cable and microUSB-USB cable to turn on the power. Put
* Since there is a possibility that the driver does not automatically enter, please check and install it based on [this page](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-fpga-board).

* Start and configure software that can display input from the COM port corresponding to the installed UART port
    * Tera Term, minicom, etc.
    * Baud rate 115200

* Open the Vivado project and click [Menu Bar]-> [File]-> [Export]-> [Export Hardware]

* Check [Include bitstream] and [OK]

* Launch SDK by clicking [Menu Bar]-> [File]-> [Launch SDK] on Vivado

* Click [Menu Bar]-> [Xilinx Tools]-> [Program FPGA] on Xilinx SDK

* Click [Program] to program FPGA

* Click [Menu Bar]-> [File]-> [New]-> [Application Project]

* Set [Project name] as appropriate and click [Next]

* Select [Hello World] in [Available Templates] and click [Finish]

* Delete "helloworld.c" in "src" of completed project, and replace it with "$(RSD_ROOT)/Processor/Project/Vivado/ZC706/project_src/$(program_name).c"
* Choice $(project_name) project from generated two projects ($(project_name) and $(project_name)_bsp) 
(Supported programs as of 06.12.2017)
    * run_simple
        * Sends the program set in the programinit() function of the source code to the RSD, executes it, and outputs the result to the UART port

* Right click on the created project-> [Run As]-> [1 Launch on Hardware (System Debugger)]

* Program output from UART should be displayed