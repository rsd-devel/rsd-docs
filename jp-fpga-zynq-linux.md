# ZYNQ の PS 向けの Linux  

* ZYNQ とは
    * おおまかに，ZYNQ は ARM ハードプロセッサを中心に構成される非リコンフィギャラブルな PS (Processing System) 部と，FPGA を中心に構成されるリコンフィギャラブルな PL (Programmagle Logic) 部で構成されています． 
    * このページでは，ZYNQ についての基本的な知識は省略しています．  
    * ZYNQ についての基本的な情報は[公式ドキュメント](https://japan.xilinx.com/support/documentation/user_guides/j_ug585-Zynq-7000-TRM.pdf)を参照してください．  
* RSD の ZYNQ への実装に際し，開発における利便性やシステムコール命令のサポートのために PS 部で Linux を動作させます．
    * このページではその Linux について説明します．  
        * **RSD 上で動作する Linux についてではないことに注意してください．**  
    * ここに書いてある内容は Xilinx Zynq-7000 向けです．  
    * **また，このページの記述は [zynq向けのシステムアーキテクチャ](jp-fpga-zynq-arch) のシステムアーキテクチャを前提としたものとなっているので，先にそちらを読むことをお勧めします．**  

## 概要 
PS 部で Linux を動作させるためには，主に以下の要素が必要になります．  
  * RSD を含めたシステムの bitstream ファイル (.bit)
  * 電源が起動して最初に PS 部が読み込む standalone プログラム (fsbl.elf)
  * PC における BIOS の役割を果たす U-Boot (u-boot.elf)
  * Linux カーネル
  * Device-tree (devicetree.btb)
  * U-Boot と bitstream，fsbl をパックしたバイナリファイル (boot.bin)

各要素の役割についての詳細は [Xilinx の公式ドキュメント](https://japan.xilinx.com/support/documentation/user_guides/j_ug585-Zynq-7000-TRM.pdf) を読んでください．  

## 準備
 [Vivado の初期設定](jp-devel-vivado)を元に初期設定を行っておく．  
また，必ず Linux 上で作業してください．  


## ターゲットボードの設定

"$(RSD\_ROOT)/Processor/Src/MakefileのTARGET\_BOARD" に対象のボード名を設定  
(07.04.2017現在の対応ボード)

* Zedboard


## ビルド

Getting started か Built from scratch のどちらか1つだけで十分です

### Getting started  

* [この](jp-fpga-zynq-build-linux-simple) の手順通りに作業する

### Build from scratch  

* [この](jp-fpga-zynq-build-linux-detail) 手順通りに作業する

## 実機上で RSD へのプログラムのロードと動作確認方法

- ssh ログイン後のホームディレクトリに実行したい code.hex を scp などを使ってコピーする
- ホームディレクトリの loader がプログラムローダーなので，以下のコマンドで実行する (詳細はソースコード loader.c を参照)  
    ```
    # loader の第 2 引数 は読み込ませるバイナリのサイズ．メモリマップの仕様により，入力すべき値が変化するので注意．
    ./loader code.hex 163840
    ```
- 正しく動作していれば，code.hex の出力が表示される
- また，約1秒ごとに実行命令数と最後にコミットされた PC が表示される

## Linux のメモリ領域について
ARM と RSD は同じ外部メモリを共有しているため，RSD が Linux が動作する物理アドレス空間を不正に書き換えないようにする必要があります．  
この方法には大まかに  
* Linux が全メモリ領域を管理し，RSD は Linux が確保した CMA 領域のみにアクセスする
* Linux と RSD でメモリを分割し，排他管理する
の 2 種類がありますが，今回は後者を選択しました．

Zedboardでは以下のようにメモリ空間を分割しています．

|アドレス|内容|
|-------|----|
|0x00000000~0x10000000|Linux用領域|
|0x10000000~0x1FFFFFFF|RSD用領域|

ZC706では以下のようにメモリ空間を分割しています．

|アドレス|内容|
|-------|----|
|0x00000000~0x30000000|Linux用領域|
|0x30000000~0x3FFFFFFF|RSD用領域|

このため，Linux から RSD 用のメモリ空間には UIO (Userspace I/O) ドライバでインストールされた /dev/uio* デバイスファイルをopen，mmap することでアクセスします．  
**/dev/uio0 が RSD 用のメモリ空間です．**

また，この仕様のため RSD のメモリ空間は 0x0 以外の物理アドレスから開始することになりますが，依然として RSD は　[メモリ・マップ](jp-arch-mem-map) で述べたように 0x0 から開始するメモリ空間を扱います．  

このギャップを解消するため，[Dramコントローラ_zynq編](jp-fpga-zynq-mem-controller) の axi4Memory モジュールが RSD からのメモリアクセス要求のアドレスに オフセット (例: Zedboardでは0x10000000) を加算して PS に要求を発行します．




## Linux 上での RSD との通信方法
[Zynq 向けのシステムアーキテクチャ](jp-fpga-zynq-arch) にある通り，RSD との通信はメモリマップドレジスタを介して行います．
これらは RSD 用のメモリ空間と同様に UIO (Userspace I/O) ドライバでインストールされた /dev/uio* デバイスファイルをopen，mmap することでアクセスします．  
**/dev/uio1 が Axi4LitePlToPsControlRegister，/dev/uio2 が Axi4LitePsToPlControlRegister です．**

## Linux 上での PL 部のリコンフィギュレーション方法

- ホスト PC にて「 make arm-linux 」で新しい boot.bit を $(RSD\_ARM\_LINUX)/boot に作成
- 作成した boot.bit を scp 等で PS の Linux にコピー
- PS の Linux 上で「 cat boot.bit > /dev/xdevcfg 」を実行する

**注意  
PS との境界の PL も再構成されるため，動作が不安定になる場合があります．  
そのため，万が一不安定になったら PS の Linux を一度シャットダウンし，SD カードの boot.bin を更新して再起動し直すことをお勧めします．**