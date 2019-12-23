# List of compiler directive

This page lists the compiler directives defined in the current (2019/12/23) RSD.

## Compiler directives defined at compile time

| Name | Description |
| ---- | ---- |
| RSD\_FUNCTIONAL\_SIMULATION | Defined when compiling for functional simulation. |
| RSD\_POST\_SYNTHESIS\_SIMULATION | Defined when compiling to simulate the synthesis results. |
| RSD\_SYNTHESIS | Defined when compiling for synthesis. |
| RSD\_SYNTHESIS\_ATLYS | Defined when compiling for synthesis targeting Digilent Atlys. |
| RSD\_SYNTHESIS\_TED | Defined when compiling for synthesis targeting Tokyo Electron Device TB-6V-LX760-LSI. |
| RSD\_USE\_EXTERNAL\_MEMORY | Defined when using memory outside the FPGA as the main memory. |
| RSD\_USE\_PROGRAM\_LOADER | Defined when using the program loader. |

## Compiler directives defined by the user according to the design intent

| Name | Description |
| ---- | ---- |
| RSD\_NARROW\_PC | When defined, compress the PC width smaller than 32 bits to reduce the area. |
| RSD\_DISABLE\_DEBUG\_REGISTER | If defined, debug registers are not compiled. The circuit area becomes small, however, the output of the Konata log is not available. |
| RSD\_DISABLE\_HARDWARE\_COUNTER | If defined, hardware counters are not compiled. |
| RSD\_STOP\_FETCH\_ON\_PRED\_MISS ||
| RSD\_ENABLE\_REISSUE\_ON\_CACHE\_MISS | If defined, cache-missed load and the instructions that depend on it directly or indirectly are re-issue from the IssueQueue. If not defined, they are re-fetched and re-executed. |