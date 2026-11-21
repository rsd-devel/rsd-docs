# Development tool installation notes

These notes describe Ubuntu 18.04 and Synplify M-2017.03-SP1. For the current simulation environment, see [Getting started](getting-started.md) and [Development environment](environment.md). The installer steps and workarounds below concern those older tools; other environments may need changes.

## Synplify

### Installation

1. Download Synplify and SynopsysInstaller. Example files for M-2017.03-SP1:

   - `SynopsysInstaller_v3.4.run`
   - `fpga_vM-2017.03-SP1_common.spf`
   - `fpga_vM-2017.03-SP1_linux.spf`

2. Install SynopsysInstaller:

   ```bash
   chmod 755 SynopsysInstaller_v3.4.run
   ./SynopsysInstaller_v3.4.run
   ```

   Specify an absolute installation path, such as `/opt/cad/synopsys/installer_v3.4`. This installer may treat `~/` literally and create a directory named `~`.

3. Start the installer in a graphical session:

   ```bash
   /opt/cad/synopsys/installer_v3.4/setup.sh
   ```

   Leave Site ID Number at `000`, select the directory containing the `.spf` packages, choose M-2017.03-SP1 and set the installation destination.

### Startup workaround

The documented Ubuntu installation could fail with errors such as:

```text
/opt/cad/synopsys/M-2017.03-SP1/bin/synplify_premier: 137: [: unexpected operator
/opt/cad/synopsys/M-2017.03-SP1/bin/synplify_premier: 151: [: !=: argument expected
/opt/cad/synopsys/M-2017.03-SP1/bin/config/execute: Syntax error: "(" unexpected (expecting ";;")
```

The recorded workaround changes `/bin/sh` to `/bin/bash` on the first line of scripts under the installation's `bin/` and `bin/config/`. Back up `bin/` first, then run the following from the relevant directory:

```bash
find . -type f -exec sed -i -e "1 s/\/bin\/sh/\/bin\/bash/g" {} \;
```

See the [related startup-error discussion](https://electronics.stackexchange.com/questions/327527/lattice-icecube2-error-synplify-pro-321). Starting the GUI with `&` leaves its errors visible in the terminal.

### License authentication

The recorded installation could authenticate after setting `FNP_IP_ENV=1`. The original notes attribute this to a newer OS sending the host's address instead of the NAT address; the setting uses the address observed by the server. This is a historical workaround, not a newly verified explanation for other releases.

### Basic GUI use

To synthesize a Verilog source and inspect its result:

1. Start Synplify Premier:

   ```bash
   /opt/cad/synopsys/M-2017.03-SP1/bin/synplify_premier &
   ```

2. If prompted for a license, double-click `synplifypremier`.
3. Create a project with File → New → Project File.
4. Right-click the project and select Add Source File to add Verilog files.
5. Right-click `rev_1` and open Implementation Options. Select Xilinx Zynq in Technology, and set the top-level module on the Verilog tab if needed.
6. Select Run.
7. After synthesis, right-click `rev_1`: RTL View shows the logic, while Technology View shows its mapping to FPGA resources.
