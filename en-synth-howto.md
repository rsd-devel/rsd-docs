# Synthesis procedure

Verify the RTL first, then select a synthesis flow for the target. CAD tools require separate installation; see [Development environment](en-devel-environment) and [Environment variables](en-devel-environment-variables).

## Zynq FPGA

The current [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefiles/Vivado.inc.mk) identifies Zedboard as its supported board.

| Boot method | Instructions |
| --- | --- |
| Start RSD using a loader on ARM Linux | [Linux-based Zynq setup](en-fpga-zynq-synth-for-linux) |
| Start RSD using a bare-metal ARM program | [Bare-metal setup (Japanese)](jp-fpga-zynq-synth-for-baremetal) |

Existing hardware instructions include Vivado/Vitis 2019.2 and older OS settings. The source board scripts still reference Xilinx 2019.2 sources. This Wiki update does not validate newer tool releases or older boards.

From the source root or `Processor/Src`, `make synth/vivado/build` runs board synthesis, implementation and bitstream generation. `make synth/synplify/build` requires a separately prepared Synplify board netlist. The post-synthesis `*/post-synthesis/build` and `*/post-synthesis/test` targets generate their verification netlists automatically.


## Post-synthesis verification

See [Post-synthesis and timing simulation](en-fpga-post-synth-simulation). The functional tests use Vivado or Synplify synthesis with XSim. A separate VCS flow checks a routed Vivado netlist with SDF delays.

## ASIC synthesis (experimental)

[Processor/Project/DesignCompiler](https://github.com/rsd-devel/rsd/tree/master/Processor/Project/DesignCompiler) contains a Makefile and `compile.tcl`. This experimental flow requires `RSD_DC_SHELL_BIN`, a license, and suitable cell-library configuration. Inspect the script's assumptions before using it; the simulation Dev Container alone is insufficient.
