# Running RSD through PS Linux on ZedBoard

Linux runs on the Zynq ARM Processing System (PS) and loads programs into RSD in the FPGA Programmable Logic (PL). For first-time setup, build the SD image below. If the board is already running, go directly to [running a program](#boot-the-board-and-run-a-program) or [updating the FPGA](#update-the-fpga-after-an-rtl-change).

Build the FPGA image and guest HEX files from the same RSD checkout so the software uses the UART registers implemented in the FPGA. See [Getting started](../../development/getting-started.md) for the v1.2.0 checkout instructions.

## Build the SD image

* Run the commands in order from the repository root.
    * Commands starting with `./RunContainer.sh` run inside the Dev Container.
    * In step 3, use the Vivado and Vitis installation paths on your host. See [Development environment](../../development/environment.md) and [Environment variables](../../development/environment-variables.md).
* Build steps
    1. Fetch the sources before the first build.

       ```bash
       ./RunContainer.sh make platform/zynq/fetch
       ```

    2. Build Linux, U-Boot, and the root filesystem.
       * By default, the board uses DHCP on `eth0` and has the hostname `rsd-zedboard`.
       * For a static IP or an existing SSH key, specify the [initial settings](#initial-settings) at this step. You can [keep the MAC address used on first boot](#fixed-mac-address) once the board is running.

       ```bash
       ./RunContainer.sh make platform/zynq/build
       ```

    3. Generate the FPGA bitstream and `boot.bin` on the host.

       ```bash
       make platform/zynq/boot/build RSD_VIVADO_ROOT=/path/to/Vivado/2019.2 RSD_VITIS_ROOT=/path/to/Vitis/2019.2
       ```

    4. Generate the SD image.

       ```bash
       ./RunContainer.sh make platform/zynq/image/build
       ```

* The finished image is `Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard.img`.
    * By default, the same directory also contains the SSH private key `rsd-zedboard_ed25519` for connecting to the board.

## Write the SD card

* On the Linux host, run `lsblk -o NAME,SIZE,MODEL,MOUNTPOINTS` and identify the card by its model and capacity.
* Unmount any mounted partitions on the card. Replace `/dev/sdX` below with the device path for the **whole card**.

    ```bash
    make platform/zynq/image/write RSD_SD_DEVICE=/dev/sdX
    ```

Example output for a checkout at `/work/rsd-open` and a card at `/dev/sdX`

```text
==================== 1. Write the SD card ====================
NAME  SIZE MODEL      TRAN
sdX  29.1G USB Reader usb
Check the device above, then run this command to overwrite /dev/sdX.
sudo dd if=/work/rsd-open/Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard.img of=/dev/sdX bs=4M status=progress conv=fsync

==================== 2. Verify the SD card ===================
After dd succeeds, reinsert the card. Check its path with lsblk and update it in the command below if it changed.
sudo cmp -n 303038464 -- /work/rsd-open/Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard.img /dev/sdX && echo "SD image verified."
==============================================================
```

* Confirm the model and capacity, then manually run the `sudo dd` command printed in your terminal.
* After `dd` succeeds, reinsert the card and check its device path with `lsblk`. Update the path in the printed `cmp` command if it changed. Run the command and wait for `SD image verified.` before [booting the board](#boot-the-board-and-run-a-program).

## Initial settings

### Static IP and DNS

For a static IP, create a settings directory anywhere the Dev Container can access. This example uses `Work/ZedBoard/settings/` in the repository. Files in this directory are installed at the same relative paths under the root of the board filesystem.

Create `etc/network/interfaces` under the settings directory and adjust the addresses for your network.

```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.1.50
    netmask 255.255.255.0
    gateway 192.168.1.1
```

Create `etc/resolv.conf` under the same directory with your DNS settings.

```text
nameserver 192.168.1.1
```

In step 2, set `RSD_ROOTFS_OVERLAY` to the absolute path of your settings directory inside the container. From the RSD repository root, build with this example overlay.

```bash
./RunContainer.sh sh -c 'make platform/zynq/build RSD_ROOTFS_OVERLAY="$PWD/Work/ZedBoard/settings"'
```

For a direct PC connection only, gateway and DNS can be omitted. Rebuilding applies updated files, but Buildroot retains old files when an overlay or files within it are removed. In that case, run `platform/zynq/clean` and rebuild. **clean also deletes generated SSH keys; save any keys you need first.**

### Fixed MAC address

U-Boot may choose a new MAC address at each boot. To keep the address already in use, boot the board once with no MAC address configured. Run this command on the board and copy the address it prints.

```bash
cat /sys/class/net/eth0/address
```

On the board, edit `/etc/network/interfaces`. Add this line under the existing `iface eth0 inet dhcp` or `iface eth0 inet static` line, replacing `<MAC>` with the address you copied.

```text
    hwaddress ether <MAC>
```

After rebooting, run the same `cat` command to confirm the address stayed the same. To keep this setting when rebuilding the SD image, copy the board's `/etc/network/interfaces` to `etc/network/interfaces` in its [settings directory](#static-ip-and-dns). Use each board's own address when preparing images for multiple boards.

### SSH keys

The default private key is generated without a passphrase and reused on subsequent builds. Keep it on the client. The board image includes the public key and accepts only key-based SSH authentication. To use an existing key, append `RSD_SSH_PUBLIC_KEY=/absolute/path/to/key.pub` to step 2, using a path visible inside the container.

## Boot the board and run a program

Set ZedBoard for SD boot and power it on. USB-UART runs at 115200 baud (Linux host example: `minicom -D /dev/ttyACM0 -b 115200`; adjust the port). To find a DHCP address, run `ip -4 addr show eth0` on the serial console.

On the development host, set the board address and run a built test by name. For a custom client key, set `RSD_ZYNQ_SSH_KEY` to the private key matching the installed public key. The default is the key beside the SD image.

```bash
export RSD_ZYNQ_HOST=root@192.168.1.50  # replace with your board address
./RunContainer.sh make test/C/build
make test/C/HelloWorld/zynq/run
```

`zynq/run` uploads the HEX to `/root/rsd/program.hex` and starts `rsd-loader`. When `Hello,World!` appears in the host terminal, press Ctrl-C to stop the loader. To try another program, see [Running CoreMark on ZedBoard](../../testing/coremark.md#run-coremark-on-zedboard).

| Operation | Command on the host |
| --- | --- |
| Print the HEX path | `make -s test/C/HelloWorld/hex-path` |
| Upload without running | `make test/C/HelloWorld/zynq/deploy` |
| Run the last uploaded program again | `make platform/zynq/program/run` |
| Upload another HEX without running it | `make platform/zynq/program/deploy RSD_ZYNQ_HEX=path/to/code.hex` |
| Upload and run another HEX | `make platform/zynq/program/run RSD_ZYNQ_HEX=path/to/code.hex` |

Use the same `hex-path`, `zynq/deploy` and `zynq/run` suffixes for any individual level-1 or level-2 program or Zephyr sample. For example, after `test/C/build`, run `make test/C/Fibonacci/zynq/run`. Fibonacci returns its result in a register and produces no UART output. Board targets use a built HEX and display UART output for manual inspection. For FP and LandingPad, select a matching build configuration and bitstream. A relative `RSD_ZYNQ_HEX` path starts in the directory where you invoke `make`. See [Building programs](../../testing/build-and-run.md) for the build steps.

## Update the FPGA after an RTL change

When the PS Linux configuration and device tree are still compatible, update just the boot file over SSH. Run these commands separately so you can choose when to reboot.

```bash
make platform/zynq/boot/build RSD_VIVADO_ROOT=/path/to/Vivado/2019.2 RSD_VITIS_ROOT=/path/to/Vitis/2019.2
make platform/zynq/boot/deploy
make platform/zynq/reboot
```

Deployment verifies the uploaded `boot.bin` against its SHA-256 and replaces it on the first SD partition. The new bitstream takes effect on reboot. `reboot` returns once it has requested the restart. When SSH is available again, run `make platform/zynq/program/run` on the host to test the HEX saved on the SD card.

For changes to Linux, the device tree or initial settings, rebuild the affected components, regenerate the full SD image and follow the card-writing instructions above. After changing U-Boot, run `make platform/zynq/bootbin/build RSD_VIVADO_ROOT=/path/to/Vivado/2019.2` on the host to repackage `boot.bin`. Buildroot intermediates require the original build environment. Clean and rebuild after modifying kernel or bootloader sources or patches.

After updating the ZedBoard boot partition, we verified the new `boot.bin` by reading it back. Following a power cycle, Linux was reachable over SSH, and the complete HelloWorld and CoreMark outputs matched their references.

- [Zynq system architecture](arch.md)
- [PS Linux configuration](linux.md)
- [Changing the clock frequency](clock.md)
