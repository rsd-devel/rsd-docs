# How to run RSD on a Xilinx Zynq board

0.  Tested environments.

    * Debian 8
    * Ubuntu 18.04

1.  Install the following software.

    * Xilinx Vitis 2019.2
    * Synopsys Synplify 2017-03 or later

2.  Install required packages using apt.
    ```
    sudo ln -s /usr/bin/make /usr/bin/gmake  # If you use Ubuntu    
    sudo apt-get install u-boot-tools ntp device-tree-compiler    
    ```

3.  Set the following environment variables in Processor/Tools/SetEnv/SetEnv.sh.

    * RSD_ROOT
    * RSD_GCC_PATH
    * SYNOPSYS_BIN
    * RSD_VIVADO
    * RSD_VIVADO_BIN
    * RSD_ARM_LINUX

4.  Setup the environment variables and Vitis.
    ```
    source /<path_of_Xilinx>/Vitis/2019.2/settings64.sh   
    source Processor/Tools/SetEnv/SetEnv.sh
    ```

5.  Generate the netlist file (rsd.vm) of RSD using Synplify.

    1.  Open Processor/Project/Synplify/ver2017-03.prj on Synplify.  
    2.  In Synplify, select "Zedboaed" in the opened project and click "Run".  
    3.  If the synthesis ran successfully, you find Project/Synplify/Zedboard/rsd.vm.  

6.  Build all the necessary files.
    ```
    cd Processor/Src/      
    make xilinx-arm-linux      
    ```
    These commands generate the following files in $(RSD_ARM_LINUX)/boot.
    * ARM Linux kernel for Zynq PS (uImage) 
    * Device tree for ARM Linux kernel (devicetree.dtb)
    * Boot image including the RSD bitstream file (boot.bin)

    A Debian rootfs for Zynq PS (ROOTFS.tar.gz) is also downloaded in $(RSD_ARM_LINUX).

7.  Extract the Debian rootfs for Zynq PS (ROOTFS.tar.gz).

    Note: root privileges are required. 

8.  Set an IP address in the Debian rootfs.
 
    Edit $(RSD_ARM_LINUX)/ROOTFS/etc/network/interfaces using a text editor.  
    Note: root privileges are required.  
    Example (set the IP address statically to 192.168.1.83):  
    ```
    auto lo
    iface lo inet loopback
    auto eth0
    iface eth0 inet static
    address 192.168.1.83
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 192.168.1.2
    ```

9.  Send all the necessary files to an SD card.  

    Note: A high-speed 16GB> SD card is recoomended.  
    Note: root privileges are required.  
    
    1.  Check the device name of the SD card in /dev/.
        ```
        lsblk       
        ```
        Note: ```/dev/sdb``` is considered in the following steps.

    2.  Create partitions in the SD card.          
        ```
        sudo fdisk /dev/sdb
        d        # Delete all the partitions in the SD card
        n; p; 1; Enter; +1024M; # Create the 1st partition
        n; p; 2; Enter; Enter;  # Create the 2nd partition
        t; 1; b; # Change the partition type of the 1st partition to FAT32(Win95)
        a; 1;    # Add a bootable flag to the 1st partition
        w        # Apply all the changes to the SD card
        ```

    3.  Format the SD card.  
        ```
        sudo mkfs.msdos -n BOOT /dev/sdb1
        sudo mkfs.ext4 -L ROOTFS /dev/sdb2      
        ```
    
    4.  Copy all files to the SD card.  
        ```
        sudo cp -R $(RSD_ARM_LINUX)/ROOTFS/* $sd_dir/ROOTFS 
        sudo cp $(RSD_ARM_LINUX)/boot/devicetree.dtb $sd_dir/BOOT     
        sudo cp $(RSD_ARM_LINUX)/boot/uImage $sd_dir/BOOT     
        sudo cp $(RSD_ARM_LINUX)/boot/boot.bin $sd_dir/BOOT       
        ```

10. Insert the SD card into Zedboard and boot.  
    
    * Login via SSH.  
        ```
        User name : root
        Password  : rsd
        ```
        
    * Please check the boot log via the USB-UART port if SSH connection is not established.

11. Send and compile the RSD program loader.  

    1.  Send Processor/Project/Linux/ARM/ProgramLoader/loader.c to Zedboard via SCP.
    
    2.  Compile loader.c on Zedboard.

12. Run your program on RSD on Zedboard.
    
    1.  Send your program code.hex via SCP.

    2.  Run your program using the program loader.
        ```
        ./loader <path of code.hex> <byte size of code.hex>
        ```
