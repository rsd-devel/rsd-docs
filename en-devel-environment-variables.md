# Environment variables

The Dev Container supplies the variables below through [devcontainer.json](https://github.com/rsd-devel/rsd/blob/master/.devcontainer/devcontainer.json). Manual installations should set them to match the host. `RSD_ROOT` is the RSD source checkout, not this Wiki checkout.

## Simulation and test builds

| Variable | Meaning | Container value |
| --- | --- | --- |
| `RSD_ROOT` | Source root inferred and exported by make; no manual setting needed | Current checkout |
| `RSD_GCC_PATH` | Directory containing the RISC-V GCC binaries | `/usr/bin` |
| `RSD_GCC_PREFIX` | Compiler filename prefix, including the final hyphen | `riscv64-unknown-elf-` |
| `RSD_VERILATOR_BIN` | Verilator executable | `/usr/local/bin/verilator` |

The compiler prefix may contain `riscv64` even when building RSD's RV32 programs. The [test compiler configuration](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Makefile.inc) explicitly selects the instruction set and `-mabi=ilp32`; it also requires picolibc support.

For example, on a manually configured host with the same tool locations, run from the RSD root:

```bash
export RSD_GCC_PATH=/usr/bin
export RSD_GCC_PREFIX=riscv64-unknown-elf-
export RSD_VERILATOR_BIN=/usr/local/bin/verilator
```

If `RSD_VERILATOR_BIN` is unset, the Verilator Makefile searches for `verilator` on `PATH`. The current flow uses the pinned Verilator 5 release described in [Development environment](en-devel-environment).

Fetch external sources with the suite's `test/External/<suite>/fetch` target and install dependencies with `test/External/<suite>/setup` where provided.

## Other simulators and synthesis tools

| Variable | Used for | Setting |
| --- | --- | --- |
| `RSD_QUESTASIM_PATH` | ModelSim/QuestaSim RTL simulation and unit tests | Directory containing `vlog`, `vsim`, etc. |
| `RSD_VIVADO_BIN` | Vivado/XSim simulation and FPGA builds | Vivado `bin` directory |
| `RSD_ARM_LINUX` | Building Linux and boot files for the Zynq PS | Work directory for downloads and builds; an external directory is convenient |
| `RSD_DC_SHELL_BIN` | Experimental Design Compiler synthesis | Path to `dc_shell` |

For Synplify post-synthesis tests, put `synplify_premier_dp` on `PATH` or pass `SYNPLIFY=/path/to/executable` to make. For VCS timing tests, put `vcs` on `PATH` or pass `VCS=/path/to/vcs`. These are make variables; the tools and licenses need separate setup.

[SetEnv.sh](https://github.com/rsd-devel/rsd/blob/master/Processor/Tools/SetEnv/SetEnv.sh) is the manual Bash setup template. Copy it to `Processor/Tools/SetEnv/MySetEnv.sh`, edit the paths, and run `source Processor/Tools/SetEnv/MySetEnv.sh` from the repository root. Make does not source this file automatically.
