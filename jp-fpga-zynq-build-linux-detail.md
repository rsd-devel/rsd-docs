# Zynq 向け Debian の構築

## Ver.

* 1.0.0: Zynq向けDebianの構築

## 手順

### 1 Vivadoのインストール

### 2 ソースコードのダウンロード
    git clone https://github.com/Xilinx/linux-xlnx.git      
    git clone https://github.com/Xilinx/u-boot-xlnx.git     
    git clone https://github.com/Xilinx/device-tree-xlnx.git        
    # apt-getでdtcをインストールする場合はいらない？
    git clone https://git.kernel.org/pub/scm/utils/dtc/dtc.git      
    git clone https://github.com/Xilinx/arm-trusted-firmware.git        
    # UltraScale+のみ
    http://www.wiki.xilinx.com/file/view/arm_ramdisk.image.gz/419243558/arm_ramdisk.image.gz        

### 3 必要なパッケージのインストール      
    sudo apt-get install qemu-user-static debootstrap binfmt-support u-boot-tools ntp git       

### 4   xilinx compilerの設定       
    export CROSS_COMPILE=arm-linux-gnueabihf-       
    source /opt/Xilinx/Vivado/2016.4/settings64.sh      

### 5   FSBLの作成      
    hsi     
    set hwdsgn [open_hw_design $my.hdf]     set hwdsgn [open_hw_design /home/mashimo/Documents/RSD/RSD/Processor/Project/Vivado/Zedboard/rsd/rsd.sdk/design_1_wrapper.hdf]
    generate_app -hw $hwdsgn -os standalone -proc ps7_cortexa9_0 -app zynq_fsbl -compile -sw fsbl -dir $fsbl_dir        generate_app -hw $hwdsgn -os standalone -proc ps7_cortexa9_0 -app zynq_fsbl -compile -sw fsbl -dir /home/mashimo/Documents/RSD/RSD/Processor/Project/Vivado/Zedboard/rsd/rsd.sdk/zynq_fsbl
    exit        
    cp $fsbl_dir/executable.elf $boot_dir/fsbl.elf      

### 6   DTCのビルド     
    cd $dtc_dir     
    make        
    export PATH=$dtc_dir:$PATH      

### 7   u-bootの作成        
    cd $u-boot_dir      
    subl $u-boot_dir/arch/arm/dts/zynq-zed.dts      
    " memory {
        device_type = ""memory"";
        reg = <0x0 0x10000000>;
    };

     chosen {
      bootargs = ""mem=256M uio_pdrv_genirq.of_id=generic-uio"";
      stdout-path = ""serial0:115200n8"";
     };"        " memory {
      device_type = ""memory"";
      reg = <0x0 0x20000000>;
     };

     chosen {
      bootargs = """";
      stdout-path = ""serial0:115200n8"";
     };"
    subl $u-boot_dir/include/configs/zynq-common.h      
    " ""sdboot=if mmcinfo; then "" \
    ""run uenvboot; "" \
    ""echo Copying Linux from SD to RAM... && "" \
    ""load mmc 0 ${kernel_load_address} ${kernel_image} && "" \
    ""load mmc 0 ${devicetree_load_address} ${devicetree_image} && "" \
    ""load mmc 0 ${ramdisk_load_address} ${ramdisk_image} && "" \
    ""bootm ${kernel_load_address} ${ramdisk_load_address} ${devicetree_load_address}; "" \
    ""fi\0"" \"       " ""sdboot=if mmcinfo; then "" \
    ""run uenvboot; "" \
    ""echo Copying Linux from SD to RAM... && "" \
    ""load mmc 0 ${kernel_load_address} ${kernel_image} && "" \
    ""load mmc 0 ${devicetree_load_address} ${devicetree_image} && "" \
    ""bootm ${kernel_load_address} - ${devicetree_load_address}; "" \
    ""fi\0"" \"
            
    make zynq_zed_config -j8        
    make -j8        
    export PATH=$u-boot_dir/tools:$PATH     
    cp $u-boot_dir/u-boot $boot_dir/u-boot.elf      

### 8   initrdの修正        
    cd $ramdisk_dir     
    gunzip $ramdisk.image.gz        
    chmod u+rwx $ramdisk.image      
    mkdir tmp_mnt/      
    sudo mount -o loop $ramdisk.image tmp_mnt/      
    cd tmp_mnt/     
    インストールしたいファイルの追加        
    sudo umount tmp_mnt/        
    gzip $ramdisk.image     
    mkimage -A arm -T ramdisk -C gzip -d $ramdisk.image.gz $uramdisk.image.gz       
    file $uramdisk.image.gz     
    file $ramdisk.image.gz      
    cp $ramdisk_dir/$uramdisk.image.gz $boot_dir/uramdisk.image.gz      


### 9   devicetreeの作成 (マニュアルには書いてあるが不要)       
    cd $devicetree_dir      
    hsm     
    open_hw_design $my.hdf      open_hw_design /home/mashimo/Documents/RSD/RSD/Processor/Project/Vivado/Zedboard/rsd/rsd.sdk/design_1_wrapper.hdf
    set_repo_path $device-tree-xlnx_dir     
    create_sw_design device-tree -os device_tree -proc ps7_cortexa9_0       
    generate_target -dir $my_dts        
    exit        
    cd $my_dts      
    dtc -I dts -O dtb -o devicetree.dtb system.dts      make ARCH=arm dtbs
    cp $devicetree_dir/devicetree.dtb $boot_dir/devicetree.dtb      make ARCH=arm system.dtb

### 10  kernelの作成        
    cd $kernel_dir      
    subl $kernel_dir/arch/arm/boot/dts/zynq-zed.dts     
    " memory {
      device_type = ""memory"";
      reg = <0x0 0x10000000>;
     };

     chosen {
      bootargs = ""mem=256M root=/dev/mmcblk0p2 rw earlyprintk rootfstype=ext4 rootwait devtmpfs.mount=1 uio_pdrv_genirq.of_id=generic-uio"";
      stdout-path = ""serial0:115200n8"";
     };"        " memory {
      device_type = ""memory"";
      reg = <0x0 0x20000000>;
     };

     chosen {
      bootargs = """";
      stdout-path = ""serial0:115200n8"";
     };"
        #include "zynq-zed-base.dtsi"       #include "zynq-7000.dtsi"
        cp zynq-7000.dtsi zynq-zed-base.dtsi        
        subl zynq-zed-base.dtsi     
        "  watchdog0: watchdog@f8005000 {
       clocks = <&clkc 45>;
       compatible = ""cdns,wdt-r1p2"";
       interrupt-parent = <&intc>;
       interrupts = <0 9 1>;
       reg = <0xf8005000 0x1000>;
       timeout-sec = <10>;
      };

      ram-uio@10000000 {
                compatible = ""generic-uio"";
                reg = <0x10000000 0x10000000>;
            };

      pl2ps-uio@43c00000 {
                compatible = ""generic-uio"";
                reg = <0x43c00000 0x1000>;
                interrupt-parent = <0x3>;
                interrupts = <0x0 0x1d 0x4>;
            };

      ps2pl-uio@43c10000 {
                compatible = ""generic-uio"";
                reg = <0x43c10000 0x1000>;
                interrupt-parent = <0x3>;
                interrupts = <0x0 0x1d 0x4>;
            };"     "  watchdog0: watchdog@f8005000 {
       clocks = <&clkc 45>;
       compatible = ""cdns,wdt-r1p2"";
       interrupt-parent = <&intc>;
       interrupts = <0 9 1>;
       reg = <0xf8005000 0x1000>;
       timeout-sec = <10>;
      };"
    make ARCH=arm xilinx_zynq_defconfig -j8     
    make ARCH=arm menuconfig -j8        
    Decice Drivers->Userspace I/O drivers->Userspace platforme dirver with genreic irq and dynamic memory       
    Decice Drivers->Generic Driver Options->DMA Contiguous Memory Allocator,Size in Mega Bytes      
    make ARCH=arm UIMAGE_LOADADDR=0x8000 uImage -j8     
    make zynq-zed.dtb       
    cp $kernel_dir/arch/arm/boot/uImage $boot_dir/uImage.bin        
    cp $kernel_dir/arch/arm/boot/dts/zynq-zed.dtb $boot_dir/devicetree.dtb      

### 11  .bitのコピー        
    cp $vivado_rsd_dir/rsd.runs/impl_1/design_1_wrapper.bit $boot_dir       

### 12  cd $boot_dir        
    boot.bifをダウンロード      
    bootgen -w -image boot.bif -o i boot.bin        

### 13  Debianの作成        
    targetdir=Debian        
    distro=wheezy       
    mkdir $targetdir        
    sudo debootstrap --arch=armhf --foreign $distro $targetdir      
    sudo cp /usr/bin/qemu-arm-static $targetdir/usr/bin/        
    sudo cp /etc/resolv.conf $targetdir/etc     
    sudo chroot $targetdir      
    distro=wheezy       
    export LANG=C       
    /debootstrap/debootstrap --second-stage     
    cat <<EOT > /etc/apt/sources.list       
    deb http://ftp.uk.debian.org/debian $distro main contrib non-free       
    deb-src http://ftp.uk.debian.org/debian $distro main contrib non-free       
    deb http://ftp.uk.debian.org/debian $distro-updates main contrib non-free       
    deb-src http://ftp.uk.debian.org/debian $distro-updates main contrib non-free       
    deb http://security.debian.org/debian-security $distro/updates main contrib non-free        
    deb-src http://security.debian.org/debian-security $distro/updates main contrib non-free        
    EOT     
    cat <<EOT > /etc/apt/apt.conf.d/71-no-recommends        
    APT::Install-Recommends "0";        
    APT::Install-Suggests "0";      
    EOT     
    apt-get update      
    apt-get install locales dialog      
    dpkg-reconfigure locales        
    apt-get install openssh-server ntpdate      
    passwd      
    echo <<EOT >> /etc/network/interfaces       
    "auto lo
    iface lo inet loopback
    auto eth0
    iface eth0 inet static
    address 172.17.68.11
    netmask 255.255.255.0
    gateway 172.17.68.254
    dns-nameservers 172.17.68.254"      "ここは任意に設定
    sshアクセスするためここでIPを固定することを推奨"
    EOT     
    echo debian-armhf > /etc/hostname       
    echo T0:2345:respawn:/sbin/getty -L ttyS0 115200 vt100 >> /etc/inittab      
    vi /etc/resolv.conf     
    "nameserver 8.8.8.8
    nameserver 8.8.4.4"     現在あるものはすべて削除
    exit        
    sudo rm $targetdir/usr/bin/qemu-arm-static      

### 14  SDカードの準備      

    lsblk       SDカードディレクトリの確認
    sudo fdisk /dev/sdb     sdbは先ほどのSDカードディレクトリ
    d       すべてのパーティションの削除
    n; p; 1; Enter; +1024M;     第一パーティションの設定
    n; p; 2; Enter; Enter;      第二パーティションの設定
    t; 1; b;        第一パーティションをFAT32(Win95)に設定
    a; 1;       ブート可能フラグの設定
    w       SDに反映
    出来ない場合は再度sudo fdisk /dev/sdbしてw      http://marsee101.blog19.fc2.com/blog-entry-2818.html
    sudo mkfs.msdos -n BOOT /dev/sdb1       http://marsee101.blog19.fc2.com/blog-entry-2929.html
    sudo mkfs.ext4 -L ROOTFS /dev/sdb2      
    sudo cp -R $targetdir/* $sd_dir/ROOTFS      
    sudo cp $boot_dir/devicetree.dtb $sd_dir/BOOT       
    sudo cp $boot_dir/uImage $sd_dir/BOOT       
    sudo cp $boot_dir/boot.bin $sd_dir/BOOT     

### 15  ZedboardにSDを入れて起動        
    シリアル出力に起動ログが出る        
    sshアクセスしてrootでログインして作業       
