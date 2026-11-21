# Memory map

The default configuration translates 32-bit logical addresses into internal physical addresses using fixed rules defined in [MemoryMap.toml](https://github.com/rsd-devel/rsd/blob/develop/Processor/Config/MemoryMap.toml).

## Configuration and generation

[ConfigGenerator.py](https://github.com/rsd-devel/rsd/blob/develop/Processor/Tools/ConfigGenerator/ConfigGenerator.py) reads `Processor/Config/MemoryMap.toml` and generates:

- RTL: `Processor/Src/Config/MemoryMapTypes.sv`, using `MemoryMapTypes.template.sv` in the same directory.
- C/assembly: `Processor/Src/Verification/TestCode/rsd-memory-map.h`.
- Linker symbols: `rsd-memory-map.ld` in the same test directory.
- Make variables: `rsd-memory-map.mk` in the same test directory.

`Makefiles/GenerateConfig.inc.mk` regenerates these as needed for RTL, units and standalone program builds. Keep generated files in Git; edit TOML or templates. Before invoking tools directly, run this from the source root with Python 3.11 or later (standard-library tomllib):

```bash
python3 Processor/Tools/ConfigGenerator/ConfigGenerator.py --rsd-root .
```

This generates both memory-map and microarchitecture definitions. Select one group with `--only memory-map` or `--only microarch`.

`insn_reset_vector` generates `INSN_RESET_VECTOR` / `RSD_RESET_VECTOR`; `pc_goal` generates `PC_GOAL` / `RSD_PC_GOAL`. Defaults are `0x1000` and `0x80001004`. Termination compares the low 16 LED PC bits, so the basic loop at `0x1004` also matches.

PC compression is disabled by default. `memory_map.pc.width = 19` is ignored while disabled; compressing the current map requires at least 20 bits. The generator rejects incompatible settings.

Region `size` is in bytes, and all `END` constants include the last valid address. `translation: low_bits` adds low logical-address bits to `physical_base`; `relative` adds `logical_address - logical_base`. Software `RSD_*_PHYSICAL_BASE` is the translated first address, which need not equal the SV additive base `PHY_ADDR_*_BASE`.

## Addresses and attributes

Internal `PhyAddrPath` is 24 bits; this width does not itself describe installed RAM capacity.

```systemverilog
// PhyRawAddrPath is 22 bits in the default configuration.
typedef struct packed {
    logic isUncachable;
    logic isIO;
    PhyRawAddrPath addr;
} PhyAddrPath;
```

The internal-address column below is the `addr` field without flags. Both endpoints are inclusive.

| Logical address | Internal address `addr` | `isUncachable` | `isIO` | Purpose |
| --- | --- | --- | --- | --- |
| `0x00001000–0x0000FFFF` | `0x001000–0x00FFFF` | 0 | 0 | ROM (60 KiB) |
| `0x80000000–0x8003FFFF` | `0x010000–0x04FFFF` | 0 | 0 | Cacheable RAM (256 KiB) |
| `0x80040000–0x8004FFFF` | `0x050000–0x05FFFF` | 1 | 0 | Uncacheable RAM (64 KiB) |
| `0x40002000` | `0x002000` | 1 | 1 | UART DATA (write, low byte) |
| `0x40002004` | `0x002004` | 1 | 1 | UART STATUS (read, bit 0 = TX_FULL) |
| `0x40010000–0x40017FFF` | `0x000000–0x007FFF` | 1 | 1 | CLINT |
| `0xC0000000–0xC0201FFF` | `0x010000–0x211FFF` | 1 | 1 | PLIC |

In the packed 24-bit value, `isUncachable` is bit 23 and `isIO` is bit 22. UART therefore maps to `0xC02000`, and uncacheable RAM starts at `0x850000`. Identical `addr` fields can identify different regions through their attributes.

The serial region covers `0x40002000–0x40002007`.

Generated `GetMemoryMapType` and `ToPhyAddrFromLogical` implement classification and translation. Undefined logical addresses yield `MMT_ILLEGAL` and cause access faults in the pipeline.

Backing memory covers the highest translated memory address, including holes. Default `MEMORY_MAP_BYTE_SIZE` is `0x60000` (384 KiB); IO regions do not contribute. Uncacheable RAM is separate storage, not an alias of normal RAM.

## MMIO ordering

RSD treats all regions marked `type = "io"` as strongly ordered. Ordinary loads and stores from one hart reach the devices in program order, even when they access different devices. RSD drains committed stores in order. When a load first resolves to MMIO, the core refetches it as a serialized instruction and waits for older stores to leave the store queue before reading the device. Uncacheable RAM has `type = "memory"` and follows ordinary memory ordering. An `LR.W` to MMIO raises a load access fault, and an `SC.W` or AMO raises a store/AMO access fault.

For each UART byte, poll `RSD_SERIAL_STATUS` until bit 0 clears, then write `RSD_SERIAL_OUTPUT`. Reading STATUS leaves the FIFO intact. The next poll observes the preceding write, so this sequence needs no per-byte `fence`. If an interrupt handler can also write the UART, protect the poll and write together so both writers cannot claim the same free slot.

The testbench stops when `PC_GOAL` retires. The common startup code executes one `fence iorw, iorw` on exit so the final UART store reaches the FIFO before the test stops. The receiver may still have bytes to read.

## Interrupt controllers

| Register | Logical address |
| --- | --- |
| CLINT `MSIP` | `0x40010000` |
| CLINT `mtimecmp` low / high | `0x40014000` / `0x40014004` |
| CLINT `mtime` low / high | `0x40017FF8` / `0x40017FFC` |
| PLIC source priority base | `0xC0000000` |
| PLIC pending base | `0xC0001000` |
| PLIC enable base | `0xC0002000` |
| PLIC priority threshold base | `0xC0200000` |
| PLIC claim/complete base | `0xC0200004` |

PLIC entries are register-group base addresses, not declarations that every address in each region is valid. See [IO_Unit.sv](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/IO/IO_Unit.sv) and [PLIC_Unit.sv](https://github.com/rsd-devel/rsd/blob/develop/Processor/Src/IO/PLIC_Unit.sv).

## Software placement

Hardware address ranges and program linker ranges differ. The basic C [rsd-ld.script](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/rsd-ld.script) uses generated base addresses and limits each ROM/RAM region to `MIN(region size, 32 KiB)`. Defaults remain 32 KiB ROM at `0x00001000` and 32 KiB RAM at `0x80000000`. [rsd-crt.s](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/rsd-crt.s) sets the stack to `RSD_RAM_BASE + 0x20000` (default `0x80020000`), then invokes data copying and BSS initialization in `rsd-loader.c` before `main`.

Zephyr uses its own board/SoC definitions. ACT4's [link.ld](https://github.com/rsd-devel/rsd/blob/develop/Processor/Src/Verification/TestCode/riscv-arch-test/link.ld) places test code in RAM from `RSD_RAM_BASE + 0x10000` (default `0x80010000`); not all `.text` runs in ROM. See [Binaries](binary.md) for HEX placement and startup.

Startup, UART helpers, linker scripts, ACT4 and Zephyr use shared constants. This does not automatically relocate linker section layouts and program limits, directed assembly addresses/expected values or ACT4 Sail-specific device settings. Review these when changing the map.
