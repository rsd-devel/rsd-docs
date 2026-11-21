# Initial Vivado setup

See [Post-synthesis and timing simulation](../synthesis/post-synthesis-simulation.md) for the current test entry points. Functional checks use XSim; timing checks use VCS.

## Installation

Existing board procedures assume Vivado/Vitis 2019.2, and board scripts still contain 2019.2 references. Compatibility with other releases has not been checked for this update.

## Environment variables

Follow [Environment variables](environment-variables.md) to set `RSD_VIVADO_ROOT` and other required values. Adjust the examples in `Processor/Tools/SetEnv` to the actual installation paths.
