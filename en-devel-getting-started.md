# Getting started

This page builds the RSD simulator, runs the basic tests, and visualizes a pipeline trace. Commands use the RSD source checkout, not the separate Wiki repository. See the [source README](https://github.com/rsd-devel/rsd/blob/master/README.md) for the corresponding quick start.

## 1. Prepare the development environment

Install Docker and the Dev Container CLI using the host setup in [Development environment](en-devel-environment). From the RSD repository root, open a container shell:

```bash
./RunContainer.sh
```

The first launch builds the environment. Later launches reuse it and rebuild when its configuration changes. Run `./RunContainer.sh --help` on the host for command execution and rebuild options. VS Code users can also use Reopen in Container with the Dev Containers extension.

The container configures the tool paths and environment variables. For manual installation, follow [Development environment](en-devel-environment) and [Environment variables](en-devel-environment-variables).

## 2. Build and test with Verilator

Inside the container, from the repository root:

```bash
cd Processor/Src
make -j"$(nproc)"
make test/level-1/run
```

`test/level-1/run` builds the assembly and C test HEX files as needed. Success prints `Test Successful (test/level-1/run)`. Build the simulator before running program tests; the test target does not build it.

See the [test program reference](en-test-program) for CoreMark, Dhrystone, Zephyr, ACT4, and FP configurations.

## 3. Visualize the pipeline

After `test/level-1/run`, run from the same `Processor/Src` directory:

```bash
make sim/kanata TEST_CODE=Verification/TestCode/C/Fibonacci
```

Open `Processor/Src/Kanata.log` with [Konata](https://github.com/shioyadan/Konata/releases). The make target is spelled `sim/kanata`, and the log filename starts with an uppercase `K`.

See [Functional simulation](en-test-simulation), [Verilator waveforms](en-test-verilator), and [Compiling and running your program](en-test-how-to-compile-and-run-your-program).

## 4. Other simulators

ModelSim/QuestaSim and Vivado XSim need separate installations and [environment settings](en-devel-environment-variables). From `Processor/Src`:

| Simulator | Build | Run the basic tests |
| --- | --- | --- |
| ModelSim/QuestaSim | `make SIM=modelsim` | `make SIM=modelsim test/level-1/run` |
| Vivado XSim | `make SIM=xsim` | `make SIM=xsim test/level-1/run` |

## 5. Synthesis and development

- [Run RSD on a Xilinx Zynq board](en-fpga-zynq-synth-for-linux)
- [Post-synthesis and timing simulation](en-fpga-post-synth-simulation)
- [Synthesis overview, including experimental ASIC support](en-synth-howto)
- [Coding convention](en-devel-coding-convention)
- [Repository update rules](en-devel-repository-convention)

See [Build entry points and Makefile structure](en-devel-build) for the target hierarchy, configuration generation and shared-file responsibilities.
