# Linux on the Zynq PS

This describes Linux running on Zynq's ARM Processing System (PS), not Linux on RSD. RSD occupies the Programmable Logic (PL). These are existing Zynq-7000 procedures; board boot was not revalidated for this Wiki update. Start with [System architecture](en-fpga-zynq-arch) and the [board build instructions](en-fpga-zynq-synth-for-linux). See the [Zynq reference manual](https://japan.xilinx.com/support/documentation/user_guides/j_ug585-Zynq-7000-TRM.pdf) for background.

## Boot components

The PS Linux environment needs the RSD system bitstream, first-stage bootloader (`fsbl.elf`), U-Boot (`u-boot.elf`), Linux kernel, device tree (`devicetree.dtb`), and a `boot.bin` packaging FSBL, bitstream and U-Boot.

## Setup and build

Work on Linux, configure Vivado and the [environment variables](en-devel-environment-variables), and select `TARGET_BOARD=Zedboard` in `Processor/Src/Makefiles/Vivado.inc.mk`. Follow [Run RSD via Linux](en-fpga-zynq-synth-for-linux) to build and prepare the SD card.

## Loading a program

Copy `code.hex` into the ARM user's home directory, for example with scp. After logging in by SSH, run the loader there:

```bash
./loader code.hex 163840
```

The second argument is the image size; adjust it for the actual image and memory map, following `loader.c`. Program output should appear, followed by periodic instruction-count and last-committed-PC information, approximately once per second.

## Memory partitioning

ARM and RSD share external memory. To avoid RSD overwriting Linux, either Linux can allocate a CMA region for RSD, or the two can use fixed disjoint regions. This setup uses a fixed partition on Zedboard:

| Physical addresses (inclusive) | Use |
| --- | --- |
| `0x00000000–0x0FFFFFFF` | Linux |
| `0x10000000–0x1FFFFFFF` | RSD |

Linux opens and maps UIO devices for access; `/dev/uio0` exposes RSD memory. The [DRAM controller](en-fpga-zynq-mem-controller) adds the board offset (here `0x10000000`) to internal memory requests. RSD's own [memory map](en-arch-mem-map) remains distinct from ARM physical addresses.

## Communication

Control uses memory-mapped registers through UIO: `/dev/uio1` is `Axi4LitePlToPsControlRegister`, and `/dev/uio2` is `Axi4LitePsToPlControlRegister`. See [System architecture](en-fpga-zynq-arch).

## Reconfiguring the PL under Linux

1. On the host, run `make platform/zynq/build` from `Processor/Src` to create a new `boot.bit` under `$(RSD_ARM_LINUX)/boot`.
2. Copy it to the PS Linux system.
3. On that system, run `cat boot.bit > /dev/xdevcfg` using the documented kernel's device interface.

Reconfiguration also replaces the PL boundary connected to the PS and may destabilize the system. If that occurs, shut down PS Linux, update `boot.bin` on the SD card and reboot.
