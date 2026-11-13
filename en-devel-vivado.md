# Initial Vivado setup

See [Post-synthesis and timing simulation](en-fpga-post-synth-simulation) for the current test entry points. Functional checks use XSim; timing checks use VCS.

## Installation

Existing board procedures assume Vivado/Vitis 2019.2, and board scripts still contain 2019.2 references. Compatibility with other releases has not been checked for this update.

## Environment variables

Follow [Environment variables](en-devel-environment-variables) to set `RSD_VIVADO_BIN` and other required values. Adjust the examples in `Processor/Tools/SetEnv` to the actual installation paths.
