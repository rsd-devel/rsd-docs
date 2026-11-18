# Running RSD through PS Linux on ZedBoard

Buildroot Linux runs on the Zynq ARM Processing System (PS) and loads programs into RSD in the Programmable Logic (PL). This is not Linux running on RSD itself. The hardware flow retains Vivado/Vitis 2019.2; Buildroot 2025.02.19 builds Linux, U-Boot and the rootfs. The old Debian rootfs download and manual extraction are no longer needed.

Run these commands from the repository root. Build Linux in the Dev Container, and run Vivado/Vitis and SD writes on the Linux host. See [Development environment](en-devel-environment) and [Environment variables](en-devel-environment-variables).

## 1. Build Linux

```bash
./RunContainer.sh make platform/zynq/fetch
./RunContainer.sh make platform/zynq/build
```

After fetching public sources, this builds the ARM toolchain, Linux, U-Boot, OpenSSH and `rsd-loader`. The first build takes time. Outputs are under `Processor/Project/Vivado/ARM_Linux/Build/images/`. Buildroot intermediates are not relocatable; keep using the same build environment.

### Initial network settings

The default is DHCP on `eth0`, with hostname `rsd-zedboard`. For a static IP, create e.g. `Work/ZedBoard/settings/etc/network/interfaces` with the following contents. Adjust the addresses for your network.

```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.1.50
    netmask 255.255.255.0
    gateway 192.168.1.1
```

Specify DNS separately in `Work/ZedBoard/settings/etc/resolv.conf`:

```text
nameserver 192.168.1.1
```

Replace the `platform/zynq/build` command above with:

```bash
./RunContainer.sh make platform/zynq/build \
    RSD_ROOTFS_OVERLAY=/workspaces/rsd-open/Work/ZedBoard/settings
```

`RSD_ROOTFS_OVERLAY` must be an absolute directory path visible inside the build environment. Its contents are copied over the rootfs. For a direct PC connection only, gateway and DNS can be omitted. Rebuilding applies updated files, but Buildroot retains old files when an overlay or files within it are removed. In that case, run `platform/zynq/clean` and rebuild. **clean also deletes generated SSH keys; save any keys you need first.**

### SSH keys

Without an explicit public key, the first build generates `Build/images/rsd-zedboard_ed25519` and `.pub`, and later builds reuse them. Keep the private key, which has no passphrase, on the client. Only the public key is installed in the image. To use an existing public key, pass `RSD_SSH_PUBLIC_KEY=/absolute/path/to/key.pub` to `platform/zynq/build`. That path must also be accessible inside the container. SSH password authentication is disabled.

## 2. Generate hardware and the SD image

Use Vivado/Vitis 2019.2 on the host. Replace these paths with your installation paths. The default target board is Zedboard.

```bash
make platform/zynq/boot/build \
    RSD_VIVADO_ROOT=/path/to/Vivado/2019.2 \
    RSD_VITIS_ROOT=/path/to/Vitis/2019.2
./RunContainer.sh make platform/zynq/image/build
```

`boot/build` generates the bitstream, XSA and FSBL, then packages FSBL, bitstream and U-Boot into `boot.bin`. This order is preserved with `-j`. The separate `hardware/build` and `bootbin/build` targets remain available. `image/build` creates **`Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard.img`**, including the boot FAT and rootfs partitions. image/build does not rebuild Linux or the rootfs itself.

## 3. Write the SD card

On the Linux host, identify the SD card device and unmount any mounted partitions on it.

```bash
lsblk -o NAME,SIZE,MODEL,MOUNTPOINTS
# Replace /dev/sdX with the actual whole SD card device.
make platform/zynq/image/write RSD_SD_DEVICE=/dev/sdX
```

**Existing data on the selected disk will be overwritten.** Do not specify a partition such as `/dev/sdX1`. Check the displayed model and capacity, then type the displayed device path to confirm. This target uses the existing image without rebuilding or unmounting anything. It rejects insufficient capacity, read-only devices, mounted filesystems and active swap on the device. Only the write uses `sudo dd`, with progress reporting and a final data sync. Do not run this inside the Dev Container.

## 4. Boot and run an RSD program

Set ZedBoard for SD boot and power it on. USB-UART runs at 115200 baud (Linux host example: `minicom -D /dev/ttyACM0 -b 115200`; adjust the port). To find a DHCP address, run `ip -4 addr show eth0` on the serial console.

```bash
ssh -i Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard_ed25519 root@<board-ip>
```

For example, build and transfer HelloWorld. If you installed your own public key, use its corresponding private key with `-i`.

```bash
./RunContainer.sh make test/C/build
scp -i Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard_ed25519 \
    Processor/Src/Verification/TestCode/C/HelloWorld/code.hex root@<board-ip>:/root/hello.hex
```

On the board, run the following. The loader is already installed; no manual size argument or compilation on the board is required.

```bash
rsd-loader /root/hello.hex
```

The loader displays program UART output. Use Ctrl-C to exit. See also [Building programs](en-test-how-to-compile-and-run-your-program).

## Updates and validation scope

After RTL changes, run `boot/build` and `image/build` in that order, then rewrite the SD card and reboot. Linux or initial-setting changes require `platform/zynq/build` first. U-Boot changes also require rebuilding `bootbin/build`. Kernel/bootloader source or patch changes require clean and rebuild.

As of 2026-11-17, bitstream/XSA/FSBL/SD-image generation and PS Linux boot with static IP/routes/DNS and SSH/SFTP in QEMU have been checked. The SD write target's confirmation and rejection paths were tested using mocked commands. Actual SD writes, board boot through FSBL/U-Boot, and RSD execution on hardware have not been validated.

- [Zynq system architecture](en-fpga-zynq-arch)
- [PS Linux configuration](en-fpga-zynq-linux)
- [Changing the clock frequency](en-fpga-zynq-clock)
