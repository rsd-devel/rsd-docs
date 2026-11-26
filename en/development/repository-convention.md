# Repository update rules

See [Test programs](../testing/program.md) for test groups and external inputs, and [Microarchitecture](../architecture/microarchitecture.md) for ACT4 coverage.

## Workflow

Create a descriptively named branch from `develop` and open a pull request against `develop`. After review and testing, merge the branch and normally delete it. For a release, validate the integrated `develop` and merge it into `master`. A graphical Git client can help unfamiliar users understand the branch structure.

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages. Some historical commits predate this convention.

## Documentation versions

The `master` branch of rsd-docs describes the `master` branch of RSD. Keep instructions for a feature on a documentation branch until the corresponding code reaches RSD `master`.

Use relative links for pages and images in rsd-docs. When asking readers to edit a file or run a command in a directory, give the path from the RSD source root, such as `Processor/Config/MicroArch.toml`. Link directly to source files when readers need to inspect an implementation or example.

For a release, check the English and Japanese checkout instructions, build options and test defaults against the tagged RSD source. From the rsd-docs root, run the following command with the path to your RSD clone, the new release tag and the ref used by existing source links.

```bash
python3 tools/release_links.py /path/to/rsd NEW_TAG --from-ref OLD_REF
```

The command checks every linked file and directory in the new tag before rewriting any links. Omit `--from-ref OLD_REF` to check the links without writing. Review and commit the documentation changes, then tag that commit with the same release tag as RSD.

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
