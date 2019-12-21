# FPGAボード

## Digilent Zedboard 

ZYNQ搭載ボード．
RISC-V版RSDプロジェクトの第一ターゲットボード．

#### FPGAの型番 

* Technology: Xilinx Zynq-7000
* Part: XC7Z020
* Package:CLG484
* Speed: -1


### ソフトウェア 

#### Xilinx SDK 
FPGA に回路データを書き込んだり，PS上のARMプロセッサにプログラムを書き込むために使用します。
Vivado をインストールする際にチェックを入れておくとインストールされる．

#### USB-UART ドライバ 
FPGA ボード上に搭載されている USB-UART 変換チップのドライバです。
これをインストールしてから PC と FPGA ボードを USB ケーブルで接続すると、
PC はシリアルポートとして認識するようになります。
シリアル通信の送受信によって、PC と FPGA の間の通信が行えるようになります。
Vivado をインストールすると自動でインストールされるはずです．

#### TeraTerm 
シリアル通信を行うためのターミナルソフトです。

## Xilinx ZC706 Evaluation Board 

ZYNQ搭載ボード．
RISC-V版RSDプロジェクトの第二ターゲットボード．

#### FPGAの型番 

* Technology: Xilinx Zynq-7000
* Part: XC7Z045 
* Package: FFG900
* Speed: -2


### ソフトウェア 

#### Xilinx SDK 
FPGA に回路データを書き込んだり，PS上のARMプロセッサにプログラムを書き込むために使用します。
Vivado をインストールする際にチェックを入れておくとインストールされる．

#### USB-UART ドライバ 
FPGA ボード上に搭載されている USB-UART 変換チップのドライバです。
これをインストールしてから PC と FPGA ボードを USB ケーブルで接続すると、
PC はシリアルポートとして認識するようになります。
シリアル通信の送受信によって、PC と FPGA の間の通信が行えるようになります。

**TODO**  
ドライバは自動的にはインストールされない場合があるので，ここにドライバのインストール方法を書く必要があるのですが，執筆者がボードを持っていないため，知らべてインストールしてその方法をここに書いてもらえると助かります．

#### TeraTerm 
シリアル通信を行うためのターミナルソフトです。

## Digilent Atlys 

メインのターゲット FPGA ボード。 ARM 版雷上動はこの FPGA ボード上でのみ動作する。  
一方 RISC-V 版は Vivado を前提としているため未検証．

情報処理学会 第1回プロセッサ設計コンテストで使われたFPGAボードで、
Spartan-6の真ん中くらいのクラスの製品が使われている。
現在の雷上動だと、2-fetch/5-issueのものがギリギリ収まる。

#### FPGAの型番 

* Technology: Xilinx Spartan 6
* Part: LX45
* Package:CSG324
* Speed: -3


### ソフトウェア 

ボード上の FPGA への回路データを書き込みや FPGA との通信のために、
PC に以下のソフトウェアおよびドライバをインストールする必要があります。

詳しくは[情報処理学会 第1回プロセッサ設計コンテスト](http://www.arch.cs.titech.ac.jp/contest/)のドキュメントを参照してください。


#### Digilent Adept 
FPGA に回路データを書き込むために使用します。


#### USB-UART ドライバ 
FPGA ボード上に搭載されている USB-UART 変換チップのドライバです。
これをインストールしてから PC と FPGA ボードを USB ケーブルで接続すると、
PC はシリアルポートとして認識するようになります。
シリアル通信の送受信によって、PC と FPGA の間の通信が行えるようになります。


#### TeraTerm 
シリアル通信を行うためのターミナルソフトです。


## 東京エレクトロンデバイス TB-6V-LX760-LSI 

東大の某研究室に昔からある、1台300万円するという噂のFPGAボード。
現在(2014/03/28)、移植作業を試みているもののプロセッサが動作するところまでは至っていない。

Virtex-6の中で最もデカい製品が使われており、4-fetch/8-issueとかの雷上動でもラクラク入ります。
これがあれば FPGA の資源不足に困ることは無いはずです。


#### FPGAの型番 

* Technology: Xilinx Virtex 6
* Part: XC6VLX760
* Package:FF1760
* Speed: -2


#### 注意点 

* ボード上のLEDやスイッチは、正論理/負論理が混在しているので、逐一ハードウェアマニュアルを見て確認すること。


### Digilent Atlys との違い 
ボードに乗っているハードウェアが全然違うために相違点は非常に多いです。
雷上動と関係する内容のみ列挙します。

* FPGA と DRAM が高性能です。
* FPGA への書き込みソフトには、Digilent Adept ではなく Xilinx ISE に付属する iMPACT を用います。
* FPGA 上で動いているプロセッサとの通信方法が確立しておらず、実験できる状態にありません。
    * TB-6V-LX760-LSI には USB-UART は搭載されていません。
    * [東京エレクトロンデバイスのサポートページ](jp/https://www.teldevice.co.jp/ppg/cgi-bin/HotLine/swTop.cgi/sepideh-v6/index.htm)で USB ポート経由で通信を行うサンプルが公開されていますが、
使用するドライバ（東京エレクトロンデバイス独自のもの）が Windows XP 32bit にしか対応していないため、そう簡単に使うことはできません。
