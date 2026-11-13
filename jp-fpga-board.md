# FPGAボード

対応ボードは Zedboard です．ビルド設定は [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefiles/Vivado.inc.mk) を参照してください．

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
