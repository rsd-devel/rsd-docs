# ZYNQ むけ Linux 構築 超簡易版

## 1.   Vitis 2019.2のインストール
* [ここ](jp-devel-getting-started)を元に初期設定を行っておく
* 特に，RSD_VIVADO_BIN/RSD_ARM_LINUX 環境変数を設定しておくこと

## 2.   必要なパッケージのインストール      
```bash
sudo ln -s /usr/bin/make /usr/bin/gmake     # Ubuntuの場合
sudo apt-get install qemu-user-static debootstrap binfmt-support u-boot-tools ntp git device-tree-compiler     
```

## 3. ターゲットボードの設定

* Processor/Src/Makefiles/Vivado.inc.mk をエディタで開き，TARGET_BOARD 変数を設定する．
* **注：以降の説明は，TARGET_BOARD に Zedboard が設定されているものとして行う．**


## 3. Vitis と Vivadoの設定        
```bash
source /<path_of_Xilinx>/Vitis/2019.2/settings64.sh
```

## 4. <!-- (Optional) --> Synplify を用いて RSD のネットリストを作成する．

1.  Synplify で Processor/Project/Synplify/ver2017-03.prj を開く．
2.  プロジェクト内で "ZedBoard" を選択し，"Run" をクリック.  
3.  合成がうまくいくと, Project/Synplify/ZedBoard/ に rsd.vm が生成される． 
<!-- 
4. Go to $(RSD_ROOT)/Processor/Src and run below command to create Vivado project.
```
make vivado-create-using-synplify-netlist
```
-->

## 5. 必要なものをすべてbuild
```bash
cd $(RSD_ROOT)/Processor/Src      
source ../Tools/SetEnv/SetEnv.sh      
make -f Makefile.vivado.mk xilinx-arm-linux      
```

## 6. Debianの解凍        
* "$(RSD_ARM_LINUX)/ROOTFS.tar.gz" を解凍 (root権限が必要)  

## 7. arm-linuxのIPアドレスの設定     
* $(RSD_ARM_LINUX)/ROOTFS/etc/network/interfacesを編集     
* 以下は192.168.1.83に設定する場合のファイル内容の例．適宜変更        

```bash
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet static
address 192.168.1.83
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 192.168.1.2
```

## 8.   SDカードの準備      
```bash
lsblk       # SDカードディレクトリの確認
sudo fdisk /dev/sdb   (sdbは例)    # sdbは先ほどのSDカードディレクトリ
d       すべてのパーティションの削除
n; p; 1; Enter; +1024M;     # 第一パーティションの設定
n; p; 2; Enter; Enter;      # 第二パーティションの設定
t; 1; b;        # 第一パーティションをFAT32(Win95)に設定
a; 1;       # ブート可能フラグの設定
w       # SDに反映
# 出来ない場合は再度sudo fdisk /dev/sdbしてw      http://marsee101.blog19.fc2.com/blog-entry-2818.html
sudo mkfs.msdos -n BOOT /dev/sdb1       # http://marsee101.blog19.fc2.com/blog-entry-2929.html
sudo mkfs.ext4 -L ROOTFS /dev/sdb2      
sudo cp -R $(RSD_ARM_LINUX)/ROOTFS/* $sd_dir/ROOTFS     
sudo cp $(RSD_ARM_LINUX)/boot/devicetree.dtb $sd_dir/BOOT     
sudo cp $(RSD_ARM_LINUX)/boot/uImage $sd_dir/BOOT     
sudo cp $(RSD_ARM_LINUX)/boot/boot.bin $sd_dir/BOOT       
```

## 9. ZedBoard に SD を入れて起動        
* シリアル出力に起動ログが出る        
* 設定したIPアドレスにsshアクセスしてrootでログインして作業       
* ユーザー名: root        
* パスワード: rsd    
            
## 10. プログラムローダーを scp で転送・コンパイル       

1. $(RSD_ROOT)/Processor/Project/Linux/ARM/ProgramLoader/loader.c を scp で ZedBoard 上の Debian に転送     
2. loader.cをコンパイル     

## 11. 実行するバイナリの転送と実行
1. 実行したいプログラムの code.hex を scp で ZedBoard 上の Debian に転送     
2. ZedBoard 上の Debian で以下を実行     
    ```bash
    ./loader <path of code.hex> <byte size of code.hex>    
    ```     
