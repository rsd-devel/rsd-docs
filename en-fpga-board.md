# FPGA board

The supported board is Zedboard. See [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefiles/Vivado.inc.mk) for build settings.

## Digilent Zedboard

This Zynq board is the primary target for the RISC-V version of RSD.

### FPGA part

- Technology: Xilinx Zynq-7000
- Part: XC7Z020
- Package: CLG484
- Speed: -1

### Software

#### Xilinx SDK

The SDK programs the FPGA and the ARM processor in the PS. In the documented tool versions, select it when installing Vivado.

#### USB-UART driver

The driver exposes the board's USB-to-UART bridge as a serial port on the host. Serial communication transfers data between the host and FPGA. The existing procedure expects Vivado installation to install this driver as well.

#### Tera Term

Tera Term is a serial-terminal application.
