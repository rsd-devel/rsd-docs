# Troubleshooting

## Environment and builds

If a compiler or tool cannot be found, check the [development environment](en-devel-environment) and [environment variables](en-devel-environment-variables). The Dev Container sets these automatically. For a manual installation, copy `SetEnv.sh` to `MySetEnv.sh`, edit it, then source it.

Rebuild the simulator after changing RTL or testbench code. When changing FP or other configuration, [clean and rebuild](en-test-verilator) both the simulator and programs with matching settings. If TestDriver cannot read the termination reason, check for a stale simulator model.

## Execution limits and mismatches

Inspect the termination reason, no-commit interval and `serial.out.txt`. The `test/.../run` targets read limits from `cfg.xml`; `sim/run`, `sim/kanata` and `sim/dump` use make variables and do not compare expected results. See [Functional simulation](en-test-simulation).

Fetch missing external test inputs and dependencies with the corresponding `test/External/<suite>/fetch` and `test/External/<suite>/setup` targets. Check ACT4 selection and FP configuration in [Test programs](en-test-program). For failures, inspect each case's `result.log` and UART output.

## Synthesis and simulator differences

Verilator uses two-state simulation. Use ModelSim/QuestaSim's four-state simulation to investigate unknown values. Check RAM input/output timing, initialization, clocks and resets against the implementation.

For Synplify, check that sources are read as SystemVerilog and that types and interfaces appear in dependency order. See [Post-synthesis simulation](en-fpga-post-synth-simulation) for functional and timing checks. If placement and routing cannot finish, inspect resource use and timing constraints.
