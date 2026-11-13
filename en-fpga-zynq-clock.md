# Clock configuration

The GUI steps below were recorded with Vivado 2016.4. See [design_1.tcl](https://github.com/rsd-devel/rsd/blob/master/Processor/Project/Vivado/TargetBoards/Zedboard/scripts/synthesis/design_1.tcl) for current project generation. `POST_IMPLEMENTATION_CLOCK_NS` in [VCS timing verification](en-fpga-post-synth-simulation) is a separate setting.

## Zedboard

On Zynq boards, the PS supplies clocks to the PL. To change the requested clock frequency in the Vivado project (2016.4 interface):

1. Select **Flow Navigator → IP Integrator → Open Block Design**.
2. Double-click the Zynq block (`processing_system7_0`) in the diagram.
3. Expand **Page Navigator → Clock Configuration → PL Fabric Clocks**.
4. Change **Requested Frequency (MHz)** for the desired clock and select **OK**.
