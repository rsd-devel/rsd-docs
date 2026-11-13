# 合成手順

RTL の機能検証を済ませてから，対象に応じた合成フローを選びます．CAD ツールは [開発環境](jp-devel-environment) と [環境変数](jp-devel-environment-variables) を参照して別途準備してください．

## Zynq FPGA

現在の [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefiles/Vivado.inc.mk) が対応ボードとして案内するのは Zedboard です．

| 起動方法 | 手順 |
| --- | --- |
| ARM Linux 上のローダから RSD を起動 | [Linux 経由の構築方法](jp-fpga-zynq-synth-for-linux) |
| ARM 上のベアメタルプログラムから RSD を起動 | [ベアメタル起動](jp-fpga-zynq-synth-for-baremetal) |

既存の実機手順には Vivado/Vitis 2019.2 と旧 OS の設定例が含まれます．本体のボードスクリプトも Xilinx 2019.2 系のソースを参照しています．ツールの新版や旧ボードでの動作を今回確認したものではありません．

本体ルートまたは `Processor/Src` から `make synth/vivado/build` を実行すると，ボード合成から配置配線・bitstream 生成まで行います．`make synth/synplify/build` は別途準備した Synplify ネットリストを使います．合成後検証の `*/post-synthesis/build`・`*/post-synthesis/test` は検証用ネットリストを自動生成します．


## 合成後の検証

[合成後・タイミング付きシミュレーション](jp-synth-simulation) を参照してください．Vivado / Synplify の機能検証は XSim，配置配線後の遅延付き検証には VCS を使うターゲットがあります．

## ASIC（実験的）

[Processor/Project/DesignCompiler](https://github.com/rsd-devel/rsd/tree/master/Processor/Project/DesignCompiler) に Makefile と `compile.tcl` があります．`RSD_DC_SHELL_BIN`，ライセンス，対象のセルライブラリなどを設定し，スクリプトの前提を確認して使う実験的なフローです．Dev Container のシミュレーション環境だけでは実行できません．
