# ZedBoard の PS Linux 経由で RSD を動かす

Zynq の ARM（PS）側で Linux を起動し，FPGA（PL）側の RSD にプログラムをロードします．初回は以下の手順で SD カードを作ります．ボードがすでに起動している場合は，[プログラムの実行](#ボードの起動とプログラムの実行) または [RTL の更新](#rtl-を変更したときの-fpga-更新) から始めてください．

## SD イメージを作る

* リポジトリのルートで順に実行します．
    * `./RunContainer.sh` の行は Dev Container 内で動作します．
    * 手順 3 のパスはホストのインストール先に合わせてください．
        * [開発環境](jp-devel-environment)・[環境変数](jp-devel-environment-variables)
* 手順
    1. ソースを取得する（初回）
        ```bash
        ./RunContainer.sh make platform/zynq/fetch
        ```
    2. Linux・U-Boot・rootfs をビルドする
        * 既定は `eth0` の DHCP で，ホスト名は `rsd-zedboard` です．
        * 固定 IP や既存の SSH 鍵を使う場合は，この段階で[初期設定](#初期設定)を指定します．
        ```bash
        ./RunContainer.sh make platform/zynq/build
        ```
    3. ホストでビットストリームと `boot.bin` を生成する
        ```bash
        make platform/zynq/boot/build RSD_VIVADO_ROOT=/path/to/Vivado/2019.2 RSD_VITIS_ROOT=/path/to/Vitis/2019.2
        ```
    4. SD イメージを生成する
        ```bash
        ./RunContainer.sh make platform/zynq/image/build
        ```

* 完成したイメージは `Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard.img` です．
    * 既定では接続用の SSH 秘密鍵 `rsd-zedboard_ed25519` も同じディレクトリにあります．

## SD カードに書き込む

* Linux ホストで `lsblk -o NAME,SIZE,MODEL,MOUNTPOINTS` を実行し，モデルと容量でカードを特定します．
* マウント中のパーティションをアンマウントし，次の `/dev/sdX` を**カード全体**のデバイス名に置き換えてください．
    ```bash
    make platform/zynq/image/write RSD_SD_DEVICE=/dev/sdX
    ```

出力例（リポジトリが `/work/rsd-open`，カードが `/dev/sdX` の場合）

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

* 表示されたモデルと容量を確認し，自分の端末に表示された `sudo dd` を手動で実行します．
* `dd` が正常終了したらカードを挿し直し，`lsblk` でデバイス名を確認します．名前が変わっていたら，表示された `cmp` のデバイス名を直してから実行してください．`SD image verified.` と表示されたら[ボードの起動](#ボードの起動とプログラムの実行)に進みます．


## 初期設定

### 固定 IP と DNS

固定 IP を使う場合は，Dev Container から参照できる任意の場所に設定用ディレクトリを用意します．以下では例として，リポジトリ内の `Work/ZedBoard/settings/` に置いたものとします．このディレクトリ内のファイルは，同じ相対パスでボードのルートファイルシステムに組み込まれます．

設定用ディレクトリの下に `etc/network/interfaces` を作成し，利用するネットワークに合わせてアドレスを指定します．

```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.1.50
    netmask 255.255.255.0
    gateway 192.168.1.1
```

DNS は同じディレクトリの下の `etc/resolv.conf` に指定します．

```text
nameserver 192.168.1.1
```

手順 2 では，選んだ設定用ディレクトリをコンテナ内の絶対パスで `RSD_ROOTFS_OVERLAY` に指定します．この例では `RSD_ROOTFS_OVERLAY=/workspaces/rsd-open/Work/ZedBoard/settings` をコマンドに追加します．

PC との直結だけなら gateway と DNS は省略できます．設定の更新は再ビルドで反映されますが，overlay を外したりファイルを削除した場合は Buildroot に古い内容が残るため，`platform/zynq/clean` 後の再ビルドが必要です．**clean は生成した SSH 鍵も削除するので，必要な鍵は先に保存してください．**

### SSH の鍵

既定の秘密鍵はパスフレーズなしで生成され，再ビルド時も再利用されます．秘密鍵は接続元で保管してください．ボード側には公開鍵を組み込み，SSH は鍵認証のみを受け付けます．既存の鍵を使う場合は，手順 2 に `RSD_SSH_PUBLIC_KEY=/absolute/path/to/key.pub` を追加します．パスはコンテナ内から参照できるものを指定してください．

## ボードの起動とプログラムの実行

ZedBoard を SD 起動に設定して電源を入れます．USB-UART は 115200 baud です（Linux ホストの例: `minicom -D /dev/ttyACM0 -b 115200`．ポート名は実機に合わせます）．DHCP で取得した IP はシリアルコンソールで `ip -4 addr show eth0` として確認できます．

開発ホストでボードの接続先を設定すると，ビルドしたテストを名前で指定して実行できます．SSH の秘密鍵は SD イメージと同じディレクトリのものを使います．独自の公開鍵を組み込んだ場合は，対応する秘密鍵のパスを `RSD_ZYNQ_SSH_KEY` に指定してください．

```bash
export RSD_ZYNQ_HOST=root@192.168.1.50  # ボードのアドレスに置き換える
./RunContainer.sh make test/C/build
make test/C/HelloWorld/zynq/run
```

`zynq/run` は HEX を `/root/rsd/program.hex` に転送し，`rsd-loader` を起動します．開発ホストの端末に `Hello,World!` が表示されたら Ctrl-C でローダーを終了します．別のプログラムを試す例は [ZedBoard での CoreMark 実行](jp-test-coremark#zedboard-で-coremark-を実行する) を参照してください．

| 操作 | ホストで実行するコマンド |
| --- | --- |
| HEX のパスを表示 | `make -s test/C/HelloWorld/hex-path` |
| 転送だけ行う | `make test/C/HelloWorld/zynq/deploy` |
| 前回転送したプログラムを再実行 | `make platform/zynq/program/run` |
| 任意の HEX を転送だけする | `make platform/zynq/program/deploy RSD_ZYNQ_HEX=path/to/code.hex` |
| 任意の HEX を転送して実行 | `make platform/zynq/program/run RSD_ZYNQ_HEX=path/to/code.hex` |

実機実行にはビルド済みの HEX を使います．`RSD_ZYNQ_HEX` の相対パスは `make` を実行したディレクトリが基準です．[プログラムのビルド方法](jp-test-how-to-compile-and-run-your-program) も参照してください．

## RTL を変更したときの FPGA 更新

PS Linux の設定やデバイスツリーをそのまま使える場合は，SSH 経由で起動ファイルだけを更新できます．次のコマンドを順に実行します．再起動は都合のよいタイミングで行ってください．

```bash
make platform/zynq/boot/build RSD_VIVADO_ROOT=/path/to/Vivado/2019.2 RSD_VITIS_ROOT=/path/to/Vitis/2019.2
make platform/zynq/boot/deploy
make platform/zynq/reboot
```

`boot/deploy` は転送した `boot.bin` の SHA-256 を照合し，SD の第 1 パーティションの起動ファイルを置き換えます．再起動すると新しいビットストリームが有効になります．`reboot` は再起動要求を送ると終了します．SSH が復帰したら，ホストで `make platform/zynq/program/run` を実行すると，SD に保存した HEX で動作を確認できます．

Linux・デバイスツリー・初期設定を変更した場合は，対象を再ビルドして SD イメージを再生成し，上記の手順でカードに書き込みます．U-Boot を変更した場合は `bootbin/build` もやり直します．Buildroot の中間ファイルは元のビルド環境で再利用します．カーネルやブートローダーのソース・パッチを変更した場合は clean 後に再ビルドしてください．

実機では，更新した `boot.bin` の読み戻し，再起動後の SSH 接続，HelloWorld の UART 出力を確認しています．

- [Zynq 上のシステム構成](jp-fpga-zynq-arch)
- [PS Linux の構成](jp-fpga-zynq-linux)
- [クロック周波数の変更](jp-fpga-zynq-clock)
