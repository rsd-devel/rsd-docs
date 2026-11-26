# FPGA board

The supported board is Zedboard. See [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/Vivado.inc.mk) for build settings.

## Digilent Zedboard

This Zynq board is the primary target for the RISC-V version of RSD.

### FPGA part

- Technology: Xilinx Zynq-7000
- Part: XC7Z020
- Package: CLG484
- Speed: -1

### Software

#### Vivado and Vitis

For the PS Linux SD image, Vivado 2019.2 generates the bitstream and Vitis 2019.2 builds the first-stage bootloader (FSBL). Once the board boots, you can run RSD programs from the development host over SSH. See [SD setup, program execution and FPGA updates](zynq/synth-for-linux.md).

#### USB-UART driver

The driver exposes the board's USB-to-UART bridge as a serial port on the host. Serial communication transfers data between the host and FPGA. The existing procedure expects Vivado installation to install this driver as well.

#### Tera Term

Tera Term is a serial-terminal application.
