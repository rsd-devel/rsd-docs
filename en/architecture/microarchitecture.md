# Microarchitecture

RSD is a 32-bit RISC-V out-of-order superscalar processor. This page describes the default configuration. For design background, see the [FPT 2019 paper](https://www.rsg.ci.i.u-tokyo.ac.jp/members/shioya/pdfs/Mashimo-FPT%2719.pdf) and the [earlier RSD design thesis (Japanese)](https://repository.dl.itc.u-tokyo.ac.jp/?action=repository_action_common_download&item_id=5849&item_no=1&attribute_id=14&file_no=1).

## Configuration

Numeric parameters and CPU macro defaults come from `Processor/Config/MicroArch.toml`. Generated `Config/MicroArchConf.sv` supplies numeric definitions, `Makefiles/MicroArch.inc.mk` supplies simulation defaults, and `Config/MicroArchMacros.svh` supplies synthesis macros. Derived parameters are in `Config/MicroArchConf.template.sv`; tool/board settings are in `Config/SynthesisMacros.sv`.

| Parameter | Default |
| --- | --- |
| Fetch / commit width | 2 instructions each |
| Issue width | 2 integer, 1 complex integer, 2 memory, 1 FP: 6 total |
| ActiveList (ROB) | 64 entries |
| Physical registers | 64 integer and 64 FP |
| IssueQueue / ReplayQueue | 16 / 20 entries |
| LoadQueue / StoreQueue | 16 entries each |
| I-cache / D-cache | 4 KiB each, 2 ways, 8-byte lines |
| D-cache MSHRs | 2 entries |

The parameters have configuration constraints. See [Compiler directives](../development/directive.md) for integer issue width, unified load/store or multiply/divide/memory pipelines, and optional FP. Rebuild both the simulator and test programs with the same configuration after a change.

## ISA implementation and verification

The RTL implements integer I/M/A, CSR and FENCE.I operations. `RSD_MARCH_FP_PIPE` controls the FP pipeline. FP, `RSD_ENABLE_ZBA`, `RSD_ENABLE_ZICOND`, and `RSD_ENABLE_ZICFILP` are enabled by default. See [Decoder.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Decoder/Decoder.sv) for instruction decoding. Instruction alignment is 32 bits (IALIGN=32).

ACT4 selects 90 integer/privileged cases and 281 F cases in the default configuration. F is included when FP is enabled. Coverage includes I/M/A, Zba, Zicond, CSR, FENCE.I, exceptions, and interrupts from M/S/U mode, including delegation and external interrupts through the PLIC. FP tests check all five rounding modes and exception flags; basic CSR tests separately cover FS/SD, FP access control and dirty tracking. S mode is Bare-only; paging and full S-mode compliance are outside this subset.

See the [test program reference](../testing/program.md#riscv-arch-test-act4) for commands and coverage. Simulations were not rerun for this documentation update.

## Zero register

The decoder suppresses writes to integer x0 through `opInfo.writeReg`. [RegisterFile.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/RegisterFile/RegisterFile.sv) initializes the physical registers to zero during reset. FP register f0 remains writable.

The initial integer mapping in [RMT.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/RenameLogic/RMT.sv) is the logical register number plus `SCALAR_FREE_LIST_ENTRY_NUM`. With the default configuration this offset is `64 - 32 = 32`, so x0 reads physical register 32. No destination remapping is performed for x0, preserving that register's zero value. The initialization expression supersedes the older source comment that names physical register 0.

## Exceptions and interrupts

Exceptions detected during decoding, integer execution, or memory execution travel with `execState` and the relevant PC/address. Address checks include LR/SC and AMO paths as well as normal loads/stores; see [MemoryTagAccessStage.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Pipeline/MemoryBackEnd/MemoryTagAccessStage.sv).

A fault follows this general sequence:

1. The execution result records its exception state in the ActiveList.
2. Commit detects the faulting instruction at the head.
3. RecoveryManager flushes that instruction and younger instructions, then signals `triggerExcpt` to the CSR unit.
4. The CSR unit updates the appropriate CSRs according to privilege and delegation state and returns the handler address.

[CSR_Unit.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Privileged/CSR_Unit.sv) reports `mtval = 0` for illegal instructions; the pipeline does not retain their encodings for trap values. With IALIGN=32, reads of `mepc` and MRET's implicit read mask the low two bits.

Interrupts use `triggerInterrupt`. Timer/software interrupts use CLINT, and external interrupts use PLIC. See [Memory map](memory-map.md) for their addresses and the generated memory-map configuration.
