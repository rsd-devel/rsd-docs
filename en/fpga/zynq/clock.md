# Clock configuration

The GUI steps below were recorded with Vivado 2016.4. See [design_1.tcl](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Project/Vivado/TargetBoards/Zedboard/scripts/synthesis/design_1.tcl) for current project generation. `POST_IMPLEMENTATION_CLOCK_NS` in [VCS timing verification](../../synthesis/post-synthesis-simulation.md) is a separate setting.

## Zedboard

In the v1.2.0 Zedboard design, `processing_system7_0/FCLK_CLK0` drives the RSD core and its AXI interfaces at 50 MHz. The project-generation Tcl requests this frequency through `CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ`. To change the requested clock frequency in the Vivado project (2016.4 interface):

1. Select Flow Navigator → IP Integrator → Open Block Design.
2. Double-click the Zynq block (`processing_system7_0`) in the diagram.
3. Expand Page Navigator → Clock Configuration → PL Fabric Clocks.
4. Change Requested Frequency (MHz) for the desired clock and select OK.
