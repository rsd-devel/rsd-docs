# Building and starting RSD with a bare-metal ARM program

These existing GUI instructions use Vivado/Vitis 2019.2 and Zedboard. Board operations were not revalidated for this update. See [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/Vivado.inc.mk) for the current build configuration.

A bare-metal program on the Zynq ARM processor loads and starts RSD in the PL.

## 1. Preparation

Follow [Getting started](../../development/getting-started.md). On Linux, install a serial terminal and add your user to `dialout`, then log in again:

```bash
sudo apt install minicom
sudo usermod -aG dialout "$USER"
```

Install the cable driver using:

```text
<Vivado installation dir>/data/xicom/cable_drivers/lin64/install_script/install_drivers/install_digilent.sh
```

Match the Vitis/Vivado release to the development environment. The following assumes 2019.2.

## 2. Target board

Set `TARGET_BOARD` in `Processor/Src/Makefiles/Vivado.inc.mk`. The default is `TARGET_BOARD=Zedboard`, with case significant.

## 3. Synthesis

The Vivado-only flow synthesizes RTL and generates a `.bit` file. The combined flow first generates a `.vm` netlist with Synplify, then uses Vivado to generate a `.bit` file. Program the board and check execution after either flow.

### 3.1. Vivado only

From `Processor/Src`:

```bash
export RSD_VIVADO_ROOT=/path/to/Xilinx/Vivado/2019.2
make synth/vivado/build
```

Set `RSD_VIVADO_ROOT` for either synthesis flow. Make reimports the IP when switching between Vivado and Synplify. A successful build produces the bitstream below and `rsd/design_1_wrapper.xsa` relative to the Zedboard project directory.

```text
Processor/Project/Vivado/TargetBoards/Zedboard/rsd/rsd.runs/impl_1/design_1_wrapper.bit
```

### 3.2. Synplify and Vivado

Generate the Synplify netlist with either method:

A. Existing project (documented with Synplify M-2017.03): open `Processor/Project/Synplify/ver2017-03.prj`, select `$(TARGET_BOARD)` in Project Files, then select Run to compile/synthesize. If your release cannot build it, try method B.

B. Project from scratch:

1. Create a project with the synthesis source list and include paths in `Processor/Project/Synplify/ver2017-03.prj`. Preserve the order of packages, interfaces and modules.
2. In Implementation Options, select the [FPGA part](../board.md), set `Main_Zynq_Wrapper` as the top module and configure module parameters. In Implementation Results, set Implementation Name to `$(TARGET_BOARD)` and Result Base Name to `rsd`.
3. For the board implementation, run `set_option -hdl_define -set "RSD_SYNTHESIS_ZEDBOARD RSD_SYNTHESIS_SYNPLIFY"` in the Tcl console. CPU settings come from `Processor/Config/MicroArch.toml` through the generated synthesis configuration.
4. Select `$(TARGET_BOARD)` in Project Files and select Run.

Check that `rsd.vm` exists under `Processor/Project/Synplify/$(TARGET_BOARD)/`. From `Processor/Src`, generate and open the Vivado project with the Synplify netlist.

```bash
make synth/synplify/open
```

Select Flow Navigator → Program and Debug → Generate Bitstream in Vivado. Changes to the RSD top-level I/O ports also require matching changes in Vivado's Block Design; detailed GUI instructions for that case remain undocumented.

## 4. Program the FPGA and check execution

The following Zedboard procedure was recorded on 2023-02-28:

1. Connect the board's PROG and UART micro-USB ports to the host with two cables and power it on. Install the drivers from step 1 first.
2. Open the UART serial port in a terminal. For minicom:

   ```bash
   minicom -D /dev/ttyACM0 -b 115200
   ```

3. Start Vivado:

   ```text
   <Vivado installation dir>/bin/vivado
   ```

4. Open the project. The build from step 3.1 already exported `design_1_wrapper.xsa` with the bitstream. For a GUI build, select File → Export → Export Hardware and enable Include bitstream.
5. Select Tools → Launch Vitis.
6. Create a bare-metal software project with File → New → Application Project. Create the platform from the exported `design_1_wrapper.xsa`, select the standalone domain for `ps7_cortexa9_0`, then choose Hello World under Available Templates.
7. Replace `src/helloworld.c` with `Processor/Project/Vivado/TargetBoards/Zedboard/project_src/run_simple.c`. Its `programinit()` function supplies the program sent to RSD, and UART reports the result.
8. Right-click the project and select Build Project.
9. Program the FPGA with the matching bitstream. In Vitis, use Xilinx → Program FPGA and select `design_1_wrapper.bit` from step 3.1.
10. Select Run As → 1 Launch on Hardware (System Debugger). Check the UART terminal for `-- Initialization started`, then the program output.

The bundled `run_simple.c` example reads a fixed 64 KiB program image from the hex string in `programinit()` (131,072 hexadecimal digits). For a different guest, use a complete image of the expected size or use the [PS Linux loader](synth-for-linux.md), which reads the length from the selected HEX file.
