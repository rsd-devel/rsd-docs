# Constraint files

Constraints describe pin assignments, clock periods and placement requirements that HDL alone does not express. Vivado uses XDC; Synplify uses SDC/FDC constraints.

## Zedboard constraints

See [zedboard.xdc](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Project/Vivado/TargetBoards/Zedboard/project_src/zedboard.xdc) for pin constraints and the [Vivado scripts](https://github.com/rsd-devel/rsd/tree/v1.2.0/Processor/Project/Vivado/TargetBoards/Zedboard/scripts/synthesis) for project generation and clock configuration.

## Timing checks

The clock period is a timing requirement. Setting it does not guarantee an operating frequency: inspect synthesis and implementation reports to confirm that timing is met. Overly tight constraints or excessive resource use can prevent placement and routing from converging.

Record clock, I/O delay and excluded-path assumptions when comparing results. `POST_IMPLEMENTATION_CLOCK_NS` in [VCS timing verification](post-synthesis-simulation.md) is separate from the [board clock configuration](../fpga/zynq/clock.md).
