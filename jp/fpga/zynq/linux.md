# Zynq の PS 向け Linux

Zynq の ARM（PS）側で Linux を動かし，FPGA（PL）側の RSD を制御します．RSD 自体で動作する Linux ではありません．[システム構成](arch.md) と [構築・SD 書き込み・実行手順](synth-for-linux.md) を参照してください．

## 起動構成

Vivado/Vitis 2019.2 が RSD の bitstream と FSBL を生成します．Buildroot 2025.02.19 が ARM ツールチェーン，U-Boot，Linux，rootfs を構築します．生成物は `Processor/Project/Vivado/ARM_Linux/Build/images/` にあります．

- `boot.bin`: FSBL・bitstream・U-Boot をまとめた起動ファイル．
- `uImage`・`rsd-zed.dtb`・`extlinux.conf`: カーネル・デバイスツリー・起動設定．
- `rootfs.ext4`: OpenSSH と `rsd-loader` を含む rootfs．
- `rsd-zedboard.img`: SD カード全体に書くパーティション付きイメージ．
- `rsd-zedboard_ed25519`・`.pub`: 既定で生成する SSH 接続用鍵．秘密鍵はイメージに含めません．

ネットワークは既定で DHCP です．固定 IP・DNS などの初期設定には `RSD_ROOTFS_OVERLAY` を使います．SSH は root の公開鍵認証で，パスワード認証は無効です．詳細は構築手順を参照してください．

## プログラムのロード

開発ホストで `make test/C/HelloWorld/zynq/run` を実行すると，ビルド済みの HEX を転送し，ボード側で `rsd-loader /root/rsd/program.hex` を起動します．ローダーは HEX を検査して RSD のメモリにロードし，Ctrl-C で終了するまで UART 出力を表示します．接続先の指定やプログラムの切り替えは[実行手順](synth-for-linux.md)を参照してください．

## メモリと制御

ARM と RSD が外部 DDR を共有するため，ZedBoard の 512 MiB を固定分割します．

| 物理アドレス（両端を含む） | 用途 |
| --- | --- |
| `0x00000000–0x0FFFFFFF` | PS Linux |
| `0x10000000–0x1FFFFFFF` | RSD |

ローダーは `/sys/class/uio/uio*/name` から `rsd-ram`・`rsd-pl2ps`・`rsd-ps2pl` を探し，対応する `/dev/uio*` を mmap します．UIO の番号には依存しません．RSD の内部アドレスは [DRAM コントローラ](mem-controller.md) が ARM 側物理アドレスに変換するため，[RSD のメモリマップ](../../architecture/memory-map.md) とは区別してください．

PS とのインターフェースが変わらない RTL 更新は，`boot.bin` を再生成・転送してボードを再起動します．PS のメモリ割当や UIO のマッピングも変わる場合は，デバイスツリーと SD イメージも更新してください．
