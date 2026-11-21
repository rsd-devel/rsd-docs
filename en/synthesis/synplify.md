# Inspecting Synplify synthesis results

This page describes resource and critical-path inspection after synthesis. First follow [Synthesis](overview.md). GUI labels and available report paths depend on the installed version and project.

## Critical paths

For a schematic view, select HDL Analyst → Technology → Hierarchical Critical Path in the main window. This shows the critical-path block diagram. The number of alternative paths available in this view has not been verified.

For a detailed report:

1. Open Project Status in the main window.
2. Select Detailed report in Timing Summary.
3. Expand Detailed Report for Clocks.
4. Expand the relevant clock, such as Clock: Main_Zynq_Wrapper|clk.
5. Select Worst Path Information.

The table below Instance / Net lists delay contributions. The older workflow described up to four worst paths; the number available in other versions has not been verified.

## Resource use

Read Project Status → Area Summary for whole-design use. For omitted resources, inspect the Report tab. Open Hierarchical Area report within Area Summary and expand module hierarchy for per-module use.

The board project's detailed HTML report is `Processor/Project/Synplify/Zedboard/rpt_Main_Zynq_Wrapper_areasrr.htm`.
