# ZYNQ むけ Linux 経由の RSD 構築方法 簡易版

以下は Zedboard と Vivado/Vitis 2019.2 を使う既存の実機手順です．本体の Makefile に合わせて名称・参照を修正していますが，SD カード作成から実機起動までを再検証したものではありません．Dev Container はシミュレーション用で，CAD ツールやボード用 Linux の準備は別途必要です．

## 0. 環境構築

1. [ここ](jp-devel-environment) を参照して，必要なツールをインストールしてください
    * FPGA 用の CAD ツールと設定を別途準備します
    * Vitis 2019.2 のインストールなどを含みます
2. [ここ](jp-devel-environment-variables) を参照して，環境変数を設定してください
    * FPGA 用の CAD ツールと設定を別途準備します
    * 特に，RSD_VIVADO_BIN/RSD_ARM_LINUX 環境変数を設定しておくこと
3. （オプションですが推奨）Synopsys Synplifyをインストール
    * Synplify のネットリストを使用した合成と Vivado のみを使用した合成のどちらかを選択できます
    * 過去の評価では Synplify+Vivado の方が高い動作周波数を得られました．現行 RTL・ツールでの比較結果を示すものではありません


## 1. Vitis と Vivado の環境変数の設定
```bash
source /<path_of_Xilinx>/Vitis/2019.2/settings64.sh
```

## 2. ターゲットボードの設定

* Processor/Src/Makefiles/Vivado.inc.mk をエディタで開き，TARGET_BOARD 変数を設定する．
* **注：以降の説明は，TARGET_BOARD に Zedboard が設定されているものとして行う．**


## 3. (オプション) Synplify を使用して RSD のネットリスト・ファイル (rsd.vm) を生成

VivadoのみでRSDを合成する場合は，この手順は不要です

1.  Synplify で Processor/Project/Synplify/ver2017-03.prj を開く．
2.  プロジェクト内で "Zedboard" を選択し，"Run" をクリック.\
3.  合成がうまくいくと, Project/Synplify/Zedboard/ に rsd.vm が生成される．


## 4. 必要なものをすべてbuild

* $(RSD_ROOT)/Processor/Src に移動し、以下のいずれかのコマンドを実行してください。
    * Vivado のみで合成する場合
        ```bash
        make platform/zynq/build
        ```
    * Synplifyで生成したネットリストを用いて合成を行う場合
        ```bash
        make -f Makefiles/Synplify.mk xilinx-arm-linux
        ```
    * *一度 Vivado/Synplify で合成を行った後に合成系を切り替える場合は必ず vivado-clean を実行すること *
        ```bash
        make synth/vivado/clean
        make synth/synplify/clean
        ```
* これらのコマンドにより、${RSD_ARM_LINUX}/boot に以下のファイルが生成されます
    * Zynq PS 用の ARM Linux カーネル (uImage) 
    * ARM Linux カーネル用デバイスツリー (devicetree.dtb)
    * RSD ビットストリームファイルを含むブートイメージ (boot.bin)
    * Zynq PS 用 Debian rootfs (ROOTFS.tar.gz) も ${RSD_ARM_LINUX} にダウンロードされます
* 備考
    * このステップはマシンやネットワークの速度によって，数分から数時間かかる場合があります
    * 一部の Xilinx ツールは GUI 環境がある場合のみ起動出来ます．うまく行かない場合は GUI から上記の Make を実行してください．
* **新しいソースファイルをVivadoプロジェクトに追加する場合は，[合成後シミュレーション](jp-synth-simulation) の「その他のターゲットとソース追加」 を参照してください**


## 5. Debianの解凍        
* "${RSD_ARM_LINUX}/ROOTFS.tar.gz" を解凍

```text
tar -xf ROOTFS.tar.gz
```

* インストール対象のシステムをいじるため，この解凍は root 権限で行う必要がある
* NFS 上などで root 権限ではうまく展開できない場合は /dev/shm 上にディレクトリを掘って使うと良い
    * /dev/shm はメモリ上の仮想ディスク
    * 後のコピー例は `${RSD_ARM_LINUX}/ROOTFS` に展開した場合です．別の場所に展開した場合はコピー元も変更してください

## 6. arm-linuxのIPアドレスの設定     
* ${RSD_ARM_LINUX}/ROOTFS/etc/network/interfacesを編集
* 以下は192.168.1.83に設定する場合のファイル内容の例．適宜変更        

```text
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
    ```text
    # 以下は fdisk コマンド内の操作は「;」で区切っており，一つずつ実行する
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
    # 以下は ${RSD_ARM_LINUX}/ROOTFS に展開した場合の例
    sudo cp -R ${RSD_ARM_LINUX}/ROOTFS/* ROOTFS_MNT
    sudo cp ${RSD_ARM_LINUX}/boot/devicetree.dtb BOOT_MNT
    sudo cp ${RSD_ARM_LINUX}/boot/uImage BOOT_MNT
    sudo cp ${RSD_ARM_LINUX}/boot/boot.bin BOOT_MNT
    # きちんと umount しないとコピーが反映されない可能性があるので注意！
    sudo umount BOOT_MNT
    sudo umount ROOTFS_MNT
    ```

## 8. Zedboard に SD を入れて起動
* 設定した IP アドレスに ssh アクセスして root でログインして作業       
    * ユーザー名: root        
    * パスワード: rsd    
* 起動出来ない場合は USB-UART の出力を確認する
    * Windows の場合は UART を USB で接続して TeraTerm でシリアルポートに接続する
    * Linux の場合は ```minicom -D /dev/ttyACM0 -b 115200```
    * Baud rate は 115200

## 9. プログラムローダーを scp で転送・コンパイル       

1. $(RSD_ROOT)/Processor/Project/Vivado/ARM_Linux/ProgramLoader/loader.c を scp 等で Zedboard 上の Debian に転送\
2. loader.cをコンパイル     


## 10. 実行するバイナリの転送と実行
1. 実行したいプログラムの code.hex を scp で Zedboard 上の Debian に転送\
    * 自身で書いたプログラムを走らせる場合は [ここ](jp-test-how-to-compile-and-run-your-program) を参考に
2. Zedboard 上の Debian で以下を実行
    ```text
    # "byte size of code.hex" はバイナリ時のサイズであり，code.bin のサイズに一致
    ./loader code.hex <size-of-code.bin-in-bytes>
    ```     

## 11. 再合成時の実行方法

1. ローカルで RSD ビットストリームファイルを含むブートイメージ（boot.bin）を再生成
    ```bash
    make platform/zynq/build
    ```
2. Zynq 側で BOOT パーティションをマウント
    ```bash
    mkdir boot
    mount /dev/mmcblk0p1 boot
    ```
3. SCP 等で boot.bin を Zynq に転送
    * boot.bin は ```${RSD_ARM_LINUX}/boot/boot.bin``` にある
    * 先ほどマウントした boot 内の boot.bin を上書きする
4. リブートする
    ```bash
    shutdown -r now
    ```


## 関連文章

* [Zynq 上の RSD のシステムアーキテクチャ](jp-fpga-zynq-arch)
* [Zynq 上のクロック周波数の変更方法](jp-fpga-zynq-clock)
* [Zynq 上の RSD のメモリインターフェース](jp-fpga-zynq-mem-controller)
