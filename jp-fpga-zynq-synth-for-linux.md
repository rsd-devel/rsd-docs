# ZYNQ むけ Linux 経由の RSD 構築方法 簡易版

## 0. 環境構築

1. [ここ](https://translate.google.com/translate?hl=jp&sl=en&tl=ja&u=https://github.com/rsd-devel/rsd/wiki/en-devel-environment) を参照して，必要なツールをインストールしてください
    * "Boot on Xilinx Zynq FPGA boards" のパートが必須です
    * Vitis 2019.2 のインストールなどを含みます
2. [ここ](https://translate.google.com/translate?hl=jp&sl=en&tl=ja&u=https://github.com/rsd-devel/rsd/wiki/en-devel-environment-variables) を参照して，環境変数を設定してください
    * "Boot on Xilinx Zynq FPGA boards" のパートが必須です
    * 特に，RSD_VIVADO_BIN/RSD_ARM_LINUX 環境変数を設定しておくこと
3. （オプションですが推奨）Synopsys Synplifyをインストール
    * Synplify のネットリストを使用した合成と Vivado のみを使用した合成のどちらかを選択できます
    * Synplify+Vivado の方が Vivado のみの場合よりも動作周波数は大きく向上します（典型的には倍程度）


## 1. Vitis と Vivado の環境変数の設定
```bash
source /<path_of_Xilinx>/Vitis/2019.2/settings64.sh
```

## 2. ターゲットボードの設定

* Processor/Src/Makefiles/Vivado.inc.mk をエディタで開き，TARGET_BOARD 変数を設定する．
* **注：以降の説明は，TARGET_BOARD に ZedBoard が設定されているものとして行う．**


## 3. (オプション) Synplify を使用して RSD のネットリスト・ファイル (rsd.vm) を生成

VivadoのみでRSDを合成する場合は，この手順は不要です

1.  Synplify で Processor/Project/Synplify/ver2017-03.prj を開く．
2.  プロジェクト内で "ZedBoard" を選択し，"Run" をクリック.  
3.  合成がうまくいくと, Project/Synplify/ZedBoard/ に rsd.vm が生成される． 


## 4. 必要なものをすべてbuild

* $(RSD_ROOT)/Processor/Src に移動し、以下のいずれかのコマンドを実行してください。
    * Vivado のみで合成する場合
        ```bash
        Make -f Makefile.vivado.mk xilinx-arm-linux
        ```
    * Synplifyで生成したネットリストを用いて合成を行う場合
        ```bash
        make -f Makefile.synplify.mk xilinx-arm-linux
        ```
    * *一度 Vivado/Synplify で合成を行った後に合成系を切り替える場合は必ず vivado-clean を実行すること *
        ```bash
        make -f Makefile.vivado.mk vivado-clean
        make -f Makefile.synplify.mk vivado-clean
        ```
* これらのコマンドにより、$(RSD_ARM_LINUX)/boot に以下のファイルが生成されます
    * Zynq PS 用の ARM Linux カーネル (uImage) 
    * ARM Linux カーネル用デバイスツリー (devicetree.dtb)
    * RSD ビットストリームファイルを含むブートイメージ (boot.bin)
    * Zynq PS 用 Debian rootfs (ROOTFS.tar.gz) も $(RSD_ARM_LINUX) にダウンロードされます
* 備考
    * このステップはマシンやネットワークの速度によって，数分から数時間かかる場合があります
    * 一部の Xilinx ツールは GUI 環境がある場合のみ起動出来ます．うまく行かない場合は GUI から上記の Make を実行してください．
* **新しいソースファイルをVivadoプロジェクトに追加する場合は，[ここ](en-fpga-post-synth-simulation) の "Add New Files into Project" を参照してください**


## 5. Debianの解凍        
* "$(RSD_ARM_LINUX)/ROOTFS.tar.gz" を解凍
* インストール対象のシステムをいじるため，この解凍は root 権限で行う必要がある
* NFS 上などで root 権限ではうまく展開できない場合は /dev/shm 上にディレクトリを掘って使うと良い
    * /dev/shm はメモリ上の仮想ディスク

## 6. arm-linuxのIPアドレスの設定     
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

## 7. SDカードの準備      
* 高速な16GB>=のSDカードを推奨します
* root 権限が必要です

1. SD カードのデバイス名を確認
    ```bash
    lsblk       
    ```
    * 以下では ```/dev/sdd``` を SD カードのデバイスとして説明します
2. パーティションの作成
    * 
    ```bash
    # 以下は fdisk コマンド内の操作は「;」で区切っており，一つずつ実行する
    lsblk       # SDカードディレクトリの確認
    sudo fdisk /dev/sdd         # (sdd は例) sdd は先ほど確認した SD カードデバイス
    d                           # すべてのパーティションの削除（削除されるまで d を繰り返す）
    n; p; 1; Enter; +1024M;     # 第一パーティションの設定（「;」のところで実際にはエンターを押す）
    n; p; 2; Enter; Enter;      # 第二パーティションの設定
    t; 1; b;    # 第一パーティションをFAT32(Win95)に設定
    a; 1;       # ブート可能フラグの設定
    w           # SDに反映
    # 出来ない場合は再度 sudo fdisk /dev/sdd して w
    ```
3. パーティションのフォーマット
    ```bash
    # http://marsee101.blog19.fc2.com/blog-entry-2818.html
    sudo mkfs.msdos -n BOOT /dev/sdd1       
    # http://marsee101.blog19.fc2.com/blog-entry-2929.html
    sudo mkfs.ext4 -L ROOTFS /dev/sdd2      
    ```
4. 必要なファイルのコピー
    ```bash
    mkdir BOOT_MNT  # SD カードのパーティションをマウント
    mkdir ROOTFS_MNT
    sudo mount /dev/sdd1 BOOT_MNT
    sudo mount /dev/sdd2 ROOTFS_MNT
    # ROOTFS を /dev/shm に展開した場合の例
    sudo cp -R /dev/shm/ROOTFS/* ROOTFS_MNT
    sudo cp ${RSD_ARM_LINUX}/boot/devicetree.dtb BOOT_MNT
    sudo cp ${RSD_ARM_LINUX}/boot/uImage BOOT_MNT
    sudo cp ${RSD_ARM_LINUX}/boot/boot.bin BOOT_MNT
    # きちんと umount しないとコピーが反映されない可能性があるので注意！
    sudo umount BOOT_MNT
    sudo umount ROOTFS_MNT
    ```

## 8. ZedBoard に SD を入れて起動        
* 設定した IP アドレスに ssh アクセスして root でログインして作業       
    * ユーザー名: root        
    * パスワード: rsd    
* 起動出来ない場合は USB-UART の出力を確認する
    * Windows の場合は UART を USB で接続して TeraTerm でシリアルポートに接続する
    * Linux の場合は ```minicom -D /dev/ttyACM0 -b 115200```
    * Baud rate は 115200

## 9. プログラムローダーを scp で転送・コンパイル       

1. $(RSD_ROOT)/Processor/Project/Vivado/ARM_Linux/ProgramLoader/loader.c を scp 等で ZedBoard 上の Debian に転送     
2. loader.cをコンパイル     


## 10. 実行するバイナリの転送と実行
1. 実行したいプログラムの code.hex を scp で ZedBoard 上の Debian に転送     
    * 自身で書いたプログラムを走らせる場合は [ここ](https://github.com/rsd-devel/rsd/wiki/en-test-how-to-compile-and-run-your-program) を参考に
2. ZedBoard 上の Debian で以下を実行
    ```bash
    # "byte size of code.hex" はバイナリ時のサイズであり，code.bin のサイズに一致
    # 現在は 98304
    ./loader <path of code.hex> <byte size of code.hex>
    ```     

## 11. 再合成時の実行方法

1. ローカルで RSD ビットストリームファイルを含むブートイメージ（boot.bin）を再生成
    ```bash
    make -f Makefile.(synplify|vivado).mk xilinx-arm-linux
    ```
2. Zynq 側で BOOT パーティションをマウント
    ```bash
    mkdir boot
    mount /dev/mmcblk0p1 boot
    ```
3. SCP 等で boot.bin を Zynq に転送
    * boot.bin は ```${RSD_ARM_LINUX}/boot/boot.bin/boot.bin``` にある
    * 先ほどマウントした boot 内の boot.bin を上書きする
4. リブートする
    ```bash
    shutdown -r now
    ```


## 関連文章

* [Zynq 上の RSD のシステムアーキテクチャ](https://github.com/rsd-devel/rsd/wiki/jp-fpga-zynq-arch)
* [Zynq 上のクロック周波数の変更方法](https://github.com/rsd-devel/rsd/wiki/jp-fpga-zynq-clock)
* [Zynq 上の RSD のメモリインターフェース](https://github.com/rsd-devel/rsd/wiki/jp-fpga-zynq-mem-controller)
 