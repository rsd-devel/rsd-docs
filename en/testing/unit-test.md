# Unit tests

The RTL units listed below have dedicated testbenches. The default simulator is Verilator in the Dev Container. For ModelSim/QuestaSim, install it separately, set `RSD_QUESTASIM_PATH`, and select `SIM=modelsim`.

## Running tests

From `Processor/Src`:

```bash
make -j4 test/unit/run
make test/unit/Divider/run
make SIM=modelsim test/unit/run
```

The default FP-enabled configuration runs 16 tests. The aggregate target generates shared RTL before building and running the individual testbenches; no prior core simulator build is required.

- `InitializedBlockRAM`
- `BlockDualPortRAM`
- `DistributedDualPortRAM`
- `DistributedMultiPortRAM`
- `MultiBankRAM`
- `MultiWidthQueuePointer`
- `MultiWidthFreeList`
- `Divider`
- `MulDivUnit`
- `Memory`
- `ICache`
- `DCache`
- `DecodeStage`
- `SerialOutput`
- `InterruptController`
- `FPDivSqrtUnit` (FP-enabled configurations only)

Select a unit with `test/unit/<name>/run`. Definitions are in the [Makefile](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefile); testbenches are in [Verification/UnitTest](https://github.com/rsd-devel/rsd/tree/v1.2.0/Processor/Src/Verification/UnitTest).

## Other test groups

`test/all/run` covers program tests and excludes units. `test/tools/run` separately checks configuration generation, TestDriver and the RunContainer launcher. See [Test programs](program.md) and [Post-synthesis simulation](../synthesis/post-synthesis-simulation.md).

After changing processor parameters, review each unit's input, expected values and assertion assumptions.
