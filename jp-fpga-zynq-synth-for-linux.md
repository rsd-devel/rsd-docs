# ZedBoard の PS Linux 経由で RSD を動かす

Zynq の ARM（PS）側で Buildroot の Linux を動かし，PL 側の RSD へプログラムをロードします．RSD 自体で Linux を起動する手順ではありません．Vivado/Vitis 2019.2 を維持し，Linux・U-Boot・rootfs は Buildroot 2025.02.19 で生成します．従来の Debian rootfs のダウンロードや手動展開は不要です．

以下はリポジトリのルートから実行します．Linux のビルドには Dev Container を使い，Vivado/Vitis と SD 書き込みは Linux ホストで実行します．[開発環境](jp-devel-environment) と [環境変数](jp-devel-environment-variables) も参照してください．

## 1. Linux の生成

```bash
./RunContainer.sh make platform/zynq/fetch
./RunContainer.sh make platform/zynq/build
```

公開ソースの取得後，ARM ツールチェーン，Linux，U-Boot，OpenSSH，`rsd-loader` をビルドします．初回は時間がかかります．成果物は `Processor/Project/Vivado/ARM_Linux/Build/images/` に生成されます．Buildroot の中間ファイルは移動できないため，同じビルド環境を継続して使用してください．

### 初期ネットワーク設定

既定は `eth0` の DHCP，ホスト名は `rsd-zedboard` です．固定 IP を使う場合は，例えば `Work/ZedBoard/settings/etc/network/interfaces` を次の内容で用意します．アドレスは利用するネットワークに合わせてください．

```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.1.50
    netmask 255.255.255.0
    gateway 192.168.1.1
```

DNS は別ファイル `Work/ZedBoard/settings/etc/resolv.conf` に指定します．

```text
nameserver 192.168.1.1
```

上の `platform/zynq/build` に代えて，次のようにビルドします．

```bash
./RunContainer.sh make platform/zynq/build \
    RSD_ROOTFS_OVERLAY=/workspaces/rsd-open/Work/ZedBoard/settings
```

`RSD_ROOTFS_OVERLAY` はビルド環境から見える絶対ディレクトリパスです．中身が rootfs に重ねてコピーされます．PC との直結だけなら gateway と DNS は省略できます．設定の更新は再ビルドで反映されますが，overlay を外したりファイルを削除した場合は Buildroot に古い内容が残るため，`platform/zynq/clean` 後の再ビルドが必要です．**clean は生成した SSH 鍵も削除するので，必要な鍵は先に保存してください．**

### SSH の鍵

公開鍵を指定しない場合，初回ビルドで `Build/images/rsd-zedboard_ed25519` と `.pub` を生成し，以後のビルドでは再利用します．秘密鍵はパスフレーズなしで接続元に保管し，イメージには公開鍵だけを組み込みます．既存の公開鍵を使う場合は `platform/zynq/build` に `RSD_SSH_PUBLIC_KEY=/absolute/path/to/key.pub` を指定してください．このパスもコンテナ内から参照できる必要があります．SSH のパスワード認証は無効です．

## 2. ハードウェアと SD イメージの生成

ホスト側で Vivado/Vitis 2019.2 を使います．以下のパスはインストール先に置き換えてください．既定の対象ボードは Zedboard です．

```bash
make platform/zynq/hardware/build \
    RSD_VIVADO_BIN=/path/to/Vivado/2019.2/bin \
    RSD_XSCT=/path/to/Vitis/2019.2/bin/xsct
make platform/zynq/bootbin/build \
    RSD_VIVADO_BIN=/path/to/Vivado/2019.2/bin
./RunContainer.sh make platform/zynq/image/build
```

`hardware/build` は bitstream・XSA・FSBL を生成し，`bootbin/build` は FSBL・bitstream・U-Boot を `boot.bin` にまとめます．`image/build` は起動用 FAT と rootfs を含む **`Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard.img`** を作ります．image/build 自体は Linux/rootfs を再ビルドしません．

## 3. SD カードへの書き込み

Linux ホストで SD カードのデバイスを確認し，そのパーティションがマウントされていればアンマウントします．

```bash
lsblk -o NAME,SIZE,MODEL,MOUNTPOINTS
# /dev/sdX を実際の SD カード全体のデバイスに置き換える
make platform/zynq/image/write RSD_SD_DEVICE=/dev/sdX
```

**指定したディスクの既存データは上書きされます．** `/dev/sdX1` のようなパーティションは指定しません．モデルと容量を確認し，表示されたデバイスパスを入力すると書き込みます．このターゲットは既存イメージを使い，自動ビルドやアンマウントは行いません．容量不足，読み取り専用，マウント中・swap 使用中のデバイスは拒否します．書き込み部分だけ `sudo dd` を使い，進捗を表示して書き込みを同期します．Dev Container 内では実行しません．

## 4. 起動と RSD プログラムの実行

ZedBoard を SD 起動に設定して電源を入れます．USB-UART は 115200 baud です（Linux ホストの例: `minicom -D /dev/ttyACM0 -b 115200`．ポート名は実機に合わせます）．DHCP で取得した IP はシリアルコンソールで `ip -4 addr show eth0` として確認できます．

```bash
ssh -i Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard_ed25519 root@<board-ip>
```

HelloWorld をビルドして転送する例です．独自の公開鍵を組み込んだ場合は，対応する秘密鍵を `-i` に指定します．

```bash
./RunContainer.sh make test/C/build
scp -i Processor/Project/Vivado/ARM_Linux/Build/images/rsd-zedboard_ed25519 \
    Processor/Src/Verification/TestCode/C/HelloWorld/code.hex root@<board-ip>:/root/hello.hex
```

ボード側で実行します．ローダーはイメージに導入済みで，サイズの手動指定やボード上でのコンパイルは不要です．

```bash
rsd-loader /root/hello.hex
```

プログラムの UART 出力を表示します．ローダーを終了するには Ctrl-C を使います．[プログラムのビルド方法](jp-test-how-to-compile-and-run-your-program) も参照してください．

## 更新と検証範囲

RTL を変更したら `hardware/build` → `bootbin/build` → `image/build` の順で再生成し，SD を書き直して再起動します．Linux や初期設定の変更は先に `platform/zynq/build` が必要です．U-Boot を変更した場合は `bootbin/build` もやり直します．カーネル・ブートローダーのソースやパッチを変更した場合は clean 後に再ビルドしてください．

2026-11-17 時点で bitstream/XSA/FSBL/SD イメージの生成，QEMU での PS Linux 起動・固定 IP/経路/DNS・SSH/SFTP を確認しています．SD 書き込みターゲットの確認・拒否処理は模擬コマンドで検証しました．実 SD への書き込み，FSBL/U-Boot 経由の実機起動，実機での RSD 実行は未検証です．

- [Zynq 上のシステム構成](jp-fpga-zynq-arch)
- [PS Linux の構成](jp-fpga-zynq-linux)
- [クロック周波数の変更](jp-fpga-zynq-clock)
