# 基本的な合成手順

* ここでは論理シミュレーションにより検証が終わったコードから回路を合成する方法を説明する

## ZYNQ 向け合成方法
RSD を Zynq FPGA 用に合成する方法には以下の２つがある

1. Zynq 上の ARM Linux を介して RSD を起動する方法
    * [こちら](jp-fpga-zynq-synth-for-linux) を参照
    * ZYNQ 上の ARM で Linux を起動し，その上で動くユーザーアプリケーションから RSD を起動する
    * **こちらの方が色々らくなので，基本的にはこの方法を推奨**
        * 下記の 2. の方法では Vivado と Vitis を立ち上げ GUI から色々操作をする必要があるが，こちらはターミナルからコマンドを打つだけで済む
2. ARM Linux を介さず直接 RSD を起動する方法
    * [こちら](jp-fpga-zynq-synth-for-baremetal) を参照
    * ZYNQ 上の ARM でベアメタルの RSD 起動用プログラムを起動し，そこから RSD を起動する

