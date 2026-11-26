# Post-synthesis and timing simulation for FPGA

The current test targets synthesize a program into a Zedboard core's internal memory and verify its UART output. They are separate from the RTL program suites and board boot-image generation. This page follows the Makefiles in RSD; the documentation update itself does not rerun CAD tools or validate hardware.

## Preparation

Install the required CAD tools and licenses separately from the Dev Container. Set `RSD_VIVADO_ROOT` to the versioned Vivado installation directory (e.g. `/opt/Xilinx/Vivado/2019.2`). For Synplify, put `synplify_premier_dp` on `PATH` or pass `SYNPLIFY=/path/to/executable`. For VCS, put `vcs` on `PATH` or pass `VCS=/path/to/vcs`.

Prepare the RISC-V compiler and [environment variables](../development/environment-variables.md). From `Processor/Src`, build the program HEX before synthesis:

```bash
make test/level-1/build
```

This command builds test programs and does not require building the Verilator simulator. The targets below default to `Verification/TestCode/C/HelloWorld`. A selected program needs `code.hex`, `cfg.xml`, and a nonempty `serial.ref.txt`.

## Functional post-synthesis tests

Choose the command for the synthesis tool:

```bash
make synth/vivado/post-synthesis/test
make synth/synplify/post-synthesis/test
```

Both flows use XSim for simulation and TestDriver to check results. The Synplify target runs batch synthesis itself; the board flow's manual `ver2017-03.prj` procedure is a separate workflow.

To select another prepared UART-checked program, pass `TEST_CODE`:

```bash
make synth/vivado/post-synthesis/test \
    TEST_CODE=Verification/TestCode/C/HelloWorld
```

Working directories are `Processor/Project/PostSynthesis/vivado/<program>` and `Processor/Project/PostSynthesis/synplify/<program>`. The inputs are copied there. Execution limits come from the copied `cfg.xml`; see the [TestDriver documentation](../testing/driver.md).

Use the public targets `make synth/vivado/post-synthesis/test` and `make synth/synplify/post-synthesis/test` from either the source root or `Processor/Src`.

## Routed timing simulation with VCS

```bash
make sim/vcs/post-implementation/test
```

Vivado performs synthesis, placement/routing, and netlist/SDF export. VCS simulates the routed netlist with delays, followed by TestDriver verification. Outputs are under `Processor/Project/PostSynthesis/vivado-timing/<program>`.

The defaults are `POST_IMPLEMENTATION_CLOCK_NS=32`, `VCS_CORNER=slow`, and `VCS_DELAY=max`. The supported corner values are `slow`/`fast`, and delay values are `min`/`max`. A previously generated netlist can be reused with:

```bash
make sim/vcs/post-implementation/run
```

Use the same `TEST_CODE` and clock setting as the build. The target checks that the current HEX matches the synthesized copy. When the HEX or RTL changes, run `sim/vcs/post-implementation/test` to rebuild. Changing only `cfg.xml` or the expected serial output does not replace the program embedded in the netlist.

## Other project-based targets

`Makefiles/Vivado.mk` also retains project-based `synth/vivado/post-synthesis/timing/test`, `synth/vivado/post-implementation/test`, and `synth/vivado/post-implementation/timing/test` targets, with GUI and Kanata variants. Their paths and options differ from the batch tests above; inspect [Makefiles/Vivado.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/Vivado.mk) when using them. [Makefiles/Synplify.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/Synplify.mk) and [Makefiles/VCS.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/VCS.mk) define the other flows.

## Adding RTL sources

Update [CoreSources.inc.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/CoreSources.inc.mk):

| File type | List |
| --- | --- |
| Package/type definitions | `TYPES`, in dependency order |
| Core modules and interfaces | `CORE_MODULES` |
| Board wrapper and other system modules | `MODULES` |
| Simulation-only testbench modules | `TEST_MODULES` |
| Header files for IP packaging | `HEADERS` |

Vivado uses these lists to build its verification netlist. Synplify reads the source list in `Processor/Project/Synplify/ver2017-03.prj` for both the board and the post-synthesis test. Add new synthesis sources to that project as well, with packages first, then interfaces and modules.

CPU settings come from `Processor/Config/MicroArch.toml`, including `overrides.synthesis`. Netlist testbenches use `RSD_SYNTHESIS_SRC_CFG` to match synthesis. A command-line `RSD_SRC_CFG` override alone does not change synthesis settings.
