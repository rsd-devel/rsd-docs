# RSD binaries

The testbench loads generated `code.hex`, not ELF directly. See [Memory map](memory-map.md) for address ranges.

## HEX format

[BinaryToHex.py](https://github.com/rsd-devel/rsd/blob/master/Processor/Tools/TestDriver/BinaryToHex.py) normally emits 32 hex digits per line, representing one 16-byte main-memory entry. Higher-address bytes appear on the left.

The file expands contiguously from the start of internal memory. Basic images contain `0x1000` padding bytes followed by ROM data. In combined ROM/RAM images, the first 64 KiB represents ROM and subsequent bytes represent RAM starting at logical address `0x80000000`.

Addresses and sizes come from generated `rsd-memory-map.mk`, `.h` and `.ld`. ROM padding is `RSD_ROM_PHYSICAL_BASE`; ROM image size is `RSD_ROM_PHYSICAL_END + 1`. Because `END` is inclusive, objcopy receives the exclusive logical bound `RSD_ROM_END + 1` for `--pad-to`. The numbers above describe the default map.

## Building basic C tests

[BuildC.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/C/BuildC.inc.mk) and the shared [Makefile.inc](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Makefile.inc) perform these steps:

1. Compile source, startup and loader with GCC; link `code.elf` using the GCC driver and `rsd-ld.script`.
2. Extract sections with objcopy and prepend padding to produce `code.bin`.
3. Convert to `code.hex` with `BinaryToHex.py`.

Even when executable names begin with `riscv64-unknown-elf-`, flags select RV32 and the `ilp32` ABI. The ISA is `rv32imaf_zicsr_zifencei` with FP or `rv32ima_zicsr_zifencei` without it. Basic C tests use soft-float-compatible RV32IM runtime libraries. See [Microarchitecture](microarchitecture.md) for FP coverage.

## VMA and LMA

VMA is the runtime address; LMA is the address holding a section's initial contents. The basic C linker script places `.text`, `.rodata` and `.srodata` in ROM. `.data` and `.sdata` have RAM VMAs and ROM LMAs.

Before `main`, `rsd-crt.s` calls `_load` in [rsd-loader.c](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/rsd-loader.c) to copy initialized data from ROM to RAM and clear BSS. Returning from `main` enters the loop at `0x1004`. The testbench compares the low 16 PC bits to detect termination. ACT4 disables PC termination to avoid aliases with RAM addresses, instead checking the instruction budget and execution results. Other suites may use different startup and linker code.

The linker aligns the ROM/RAM starts of `.data` and the start of `.bss` to four bytes, and defines `__data_load_start = LOADADDR(.data)`. The loader uses that LMA and byte-copy/zeroing semantics, including trailing bytes.

## Combined ROM/RAM images

The ACT4 [Makefile](https://github.com/rsd-devel/rsd/blob/develop/Processor/Src/Verification/TestCode/riscv-arch-test/Makefile) extracts ROM/RAM separately, concatenates padding, ROM and RAM, then generates HEX. Test code runs in RAM, whose initial contents are loaded by the testbench; it does not copy all initial data from ROM like basic C tests.

Zephyr has its own build/startup flow. Consult each suite's Makefile and linker script for placement.

## Loading by environment

| Environment | Loading method |
| --- | --- |
| Verilator 5, ModelSim/QuestaSim, Vivado RTL simulation | Shared [TestMain.sv](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestMain.sv) calls `InitializeMemory` to expand HEX into internal memory |
| Current post-synthesis tests | HEX is embedded as memory initialization in the netlist; changing it requires resynthesis |
| ARM Linux on Zynq | ARM-side [loader.c](https://github.com/rsd-devel/rsd/blob/master/Processor/Project/Vivado/ARM_Linux/ProgramLoader/loader.c) transfers the program |

When moving a simulation image to hardware, match the board loader and memory layout.
