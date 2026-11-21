# Synthesis procedure

Verify the RTL first, then select a synthesis flow for the target. CAD tools require separate installation; see [Development environment](../development/environment.md) and [Environment variables](../development/environment-variables.md).

## Zynq FPGA

The current [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefiles/Vivado.inc.mk) identifies Zedboard as its supported board.

| Boot method | Instructions |
| --- | --- |
| Start RSD using a loader on ARM Linux | [Linux-based Zynq setup](../fpga/zynq/synth-for-linux.md) |
| Start RSD using a bare-metal ARM program | [Bare-metal setup](../fpga/zynq/synth-for-baremetal.md) |

Existing hardware instructions include Vivado/Vitis 2019.2 and older OS settings. The source board scripts still reference Xilinx 2019.2 sources. This documentation update does not validate newer tool releases or older boards.

From the source root or `Processor/Src`, `make synth/vivado/build` runs board synthesis, implementation and bitstream generation. `make synth/synplify/build` requires a separately prepared Synplify board netlist. The post-synthesis `*/post-synthesis/build` and `*/post-synthesis/test` targets generate their verification netlists automatically.


## Post-synthesis verification

See [Post-synthesis and timing simulation](post-synthesis-simulation.md). The functional tests use Vivado or Synplify synthesis with XSim. A separate VCS flow checks a routed Vivado netlist with SDF delays.

## ASIC synthesis (experimental)

[Processor/Project/DesignCompiler](https://github.com/rsd-devel/rsd/tree/master/Processor/Project/DesignCompiler) contains a Makefile and `compile.tcl`. This experimental flow requires `RSD_DC_SHELL_BIN`, a license, and suitable cell-library configuration. Inspect the script's assumptions before using it; the simulation Dev Container alone is insufficient.
