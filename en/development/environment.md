# Development environment

The simulation environment is defined in the RSD source repository's [Dockerfile](https://github.com/rsd-devel/rsd/blob/develop/.devcontainer/Dockerfile) and [container configuration](https://github.com/rsd-devel/rsd/blob/develop/.devcontainer/devcontainer.json). Source links point to the latest files on `master`.

## Dev Container

The [source README](https://github.com/rsd-devel/rsd/blob/master/README.md) provides this host setup for a fresh Ubuntu 24.04 installation. Skip Docker installation and group setup if already configured:

```bash
sudo apt update
sudo apt install -y docker.io docker-buildx python3 build-essential nodejs npm
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
sudo npm install -g @devcontainers/cli@0.83.3
```

Log out and log back in to apply Docker group membership. From the RSD repository root, run:

```bash
./RunContainer.sh
```

The host setup above and the container's OS are separate: the container uses Ubuntu 26.04. Its configuration includes:

| Component | Configuration |
| --- | --- |
| Verilator | 5.054, built from the pinned release with timing support |
| RISC-V compiler | Ubuntu `gcc-riscv64-unknown-elf` and binutils packages; the test Makefiles select RV32 and `ilp32` |
| C library support | `picolibc-riscv64-unknown-elf` |
| Python | Python 3.11+ standard-library tomllib; suite-specific dependencies use their setup targets |
| Zephyr build tools | CMake, Ninja, gperf, device-tree compiler |
| ACT4 build tools | Ruby and LLVM/Clang/LLD 22; suite-specific dependencies are installed by its setup target |

Follow [Getting started](getting-started.md) to build the simulator and run tests. Benchmark and extended-test sources require their own fetch/setup commands; see the [test program reference](../testing/program.md).

## Manual installation

Use the Dockerfile's OS, package list, and pinned tool build steps as the reference. Use Python 3.11 or later, and set the variables in [Environment variables](environment-variables.md), adjusting paths to your host.

The current Verilator flow uses the shared SystemVerilog `TestMain` with `--main` and `--timing`. Use the pinned tool version when reproducing it.

## Separately installed CAD tools

The Dev Container does not install the licensed simulators or synthesis tools. Configure them and their licenses separately:

| Purpose | Tools / entry point |
| --- | --- |
| RTL simulation and RTL unit tests | ModelSim/QuestaSim; `make SIM=modelsim` / `make SIM=modelsim test/unit/run` |
| RTL simulation with XSim | Vivado; `make SIM=xsim` |
| Zedboard implementation | Vivado/Vitis; optionally Synplify for synthesis |
| Functional post-synthesis tests | Vivado + XSim, or Synplify + XSim |
| Routed timing tests | Vivado + VCS; `make sim/vcs/post-implementation/test` |
| Experimental ASIC synthesis | Design Compiler; `Processor/Project/DesignCompiler` |

The older setup examples use QuestaSim 2019.4.2, Vivado/Vitis 2019.2, Synplify M-2017.03-SP1, and Design Compiler O-2018.06-SP4. These are historical reference versions, not a new compatibility test. The board scripts still reference Xilinx 2019.2 sources; this documentation update does not establish support for newer CAD releases.

For FPGA setup, see [Zynq board instructions](../fpga/zynq/synth-for-linux.md) and [post-synthesis simulation](../synthesis/post-synthesis-simulation.md). Older board instructions may require additional host packages that are separate from the simulation container.

## Viewing results

[Konata](https://github.com/shioyadan/Konata/releases) opens `Kanata.log`. Verilator's `sim/dump` target also generates `simx.vcd`, which can be opened with a VCD viewer such as GTKWave. See [Verilator simulation](../testing/verilator.md).
