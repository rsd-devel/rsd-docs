# Repository update rules

See [Test programs](../testing/program.md) for test groups and external inputs, and [Microarchitecture](../architecture/microarchitecture.md) for ACT4 coverage.

## Workflow

Create a descriptively named branch from `develop` and open a pull request against `develop`. After review and testing, merge the branch and normally delete it. For a release, validate the integrated `develop` and merge it into `master`. A graphical Git client can help unfamiliar users understand the branch structure.

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages. Some historical commits predate this convention.

## Checks before merging

Run these commands from `Processor/Src` after configuring the tools:

1. Compile with ModelSim/QuestaSim: `make SIM=modelsim`.
2. Build the selected simulator and run basic functional tests: `make test/level-1/run` for Verilator, or `make SIM=modelsim test/level-1/run` for ModelSim/QuestaSim. These targets also build the test HEX files.
3. Fetch CoreMark once with `make test/External/Coremark/fetch`, then run `make test/External/Coremark/run` (add `SIM=modelsim` for that simulator).
4. Build the functional CoreMark program and verify its synthesized implementation, for example:

```bash
make synth/vivado/post-synthesis/test TEST_CODE=Verification/TestCode/Coremark/Coremark
```

TestDriver checks UART output in the post-synthesis work directory. See [Functional simulation](../testing/simulation.md), [Post-synthesis simulation](../synthesis/post-synthesis-simulation.md) and [CoreMark](../testing/coremark.md).

## Additional coverage

`test/all/run` covers basic tests and CoreMark/Dhrystone. Run ACT4/Zephyr with `test/ex/run`, RTL units with `test/unit/run`, and test infrastructure with `test/tools/run`. Select validation appropriate to the change and record tools, configuration, targets, FP settings and extension selection. After completing the applicable checks, submit the change through a GitHub pull request to `develop`.
