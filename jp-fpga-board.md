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

#### Vivado / Vitis

PS Linux 用の SD イメージを作るときは，Vivado 2019.2 でビットストリームを，Vitis 2019.2 で初段ブートローダー（FSBL）を生成します．起動後は開発ホストから SSH 経由で RSD のプログラムを実行できます．[SD の作成・実行・更新手順](jp-fpga-zynq-synth-for-linux) を参照してください．

#### USB-UART ドライバ 
FPGA ボード上に搭載されている USB-UART 変換チップのドライバです。
これをインストールしてから PC と FPGA ボードを USB ケーブルで接続すると、
PC はシリアルポートとして認識するようになります。
シリアル通信の送受信によって、PC と FPGA の間の通信が行えるようになります。
Vivado をインストールすると自動でインストールされるはずです．

#### TeraTerm 
シリアル通信を行うためのターミナルソフトです。
