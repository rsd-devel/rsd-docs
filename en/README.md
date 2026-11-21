# RSD documentation

These guides cover building, testing, and running RSD. Source links point to the `master` branch of the RSD repository. Hardware and CAD instructions use the tool versions listed on each page.

When adding a page, place the English version under `en/` and the Japanese version at the same relative path under `jp/`. Start each page with its title and add it to the index for its language.

## Getting Started

Start from [here](development/getting-started.md)

## Development

* [Getting started](development/getting-started.md)
* [Build entry points and Makefile structure](development/build.md)
* [Development environment](development/environment.md)
* [Environment variables](development/environment-variables.md)
* [Compiler directives](development/directive.md)
* [Coding convention](development/coding-convention.md)
* [Repository update rules](development/repository-convention.md)
* [Initial Vivado setup](development/vivado.md)
* [Older tool installation notes](development/tools.md)

## Tests and debugging

* [Test programs](testing/program.md)
* [TestDriver: limits and result checking](testing/driver.md)
* [Compile and run your program](testing/build-and-run.md)
* [Functional simulation](testing/simulation.md)
* [Verilator](testing/verilator.md)
* [Unit tests](testing/unit-test.md)
* [CoreMark and Dhrystone](testing/coremark.md)
* [Troubleshooting](testing/troubleshooting.md)

## Architecture

* [Microarchitecture](architecture/microarchitecture.md)
* [Memory map](architecture/memory-map.md)
* [Binaries](architecture/binary.md)

## Synthesis

* [Synthesis overview](synthesis/overview.md)
* [Constraints](synthesis/constraints.md)
* [Post-synthesis and timing simulation](synthesis/post-synthesis-simulation.md)
* [Inspecting Synplify results](synthesis/synplify.md)

## Zynq FPGA

* [FPGA board](fpga/board.md)
* [Run RSD via Linux](fpga/zynq/synth-for-linux.md)
* [Bare-metal ARM startup](fpga/zynq/synth-for-baremetal.md)
* [System architecture](fpga/zynq/arch.md)
* [Clock configuration](fpga/zynq/clock.md)
* [Memory controller](fpga/zynq/mem-controller.md)
* [Linux on the PS](fpga/zynq/linux.md)
