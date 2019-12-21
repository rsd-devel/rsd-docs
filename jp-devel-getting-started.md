# はじめよう

* ここではソースコードをコンパイルしてとりあえず論理検証を行うまでの手順を説明します．

## 環境構築

* Windows の場合
    * cygwin をインストールしてください
        * make を同時に入れるようにしておいてください
    * python と git は cygwin のものを使っても良いですが，windows 版を入れておいた方がいいかもしれません
* Windows/Linux 共通
    * python, make, git を導入しておいてください

### 機能シミュレーションに必要なツール

下記のいずれかが必要です
* MentorGraphics QuestaSim or ModelSim
* Verilator
* Vivado

### FPGA で合成するために必要なツール

PC 上で機能シミュレーションを行うのみであれば，下記は必要ありません．

* Synopsys Synplify
    * SystemVerilog のコンパイル（論理合成）に使用
* Xilinx Vivado
    * Synplify の出力したネットリストを元に，FPGA 用 bitstream を出力

### 推奨ツールの導入

* パイプライン・ビューア Konata
    * [Konata](https://github.com/shioyadan/Konata) からビルド済みバイナリのアーカイブをダウンロードして展開する
* エディタ
    * [Visual Studio Code](https://code.visualstudio.com/) を推奨
    * 導入後は SystemVerilog 拡張を導入してください
    * リンタ [svls-vscode](https://github.com/dalance/svls-vscode) のインストールを推奨します



## 環境変数の設定
* "Processor/Tools/SetEnv" 内のファイルを参照して，環境変数を設定してください
* Windows では "SetEnv.bat" を，Linux では "SetEnv.sh" を参照してください
* シミュレーションのためには最低でも RSD_ROOT を設定する必要があります
* Windows ではさらに，RSD_CYGWIN_PATH を設定する必要があります
* Modelsim/QuestaSim の使用時は RSD_QUESTASIM_PATH を設定してください

## シミュレーション

* Processor/Src にて，make を行ってください
    * Modelsim/QuestaSim の場合
        ```
        make
        make run        # run simulation
        make kanata     # run simulation & outputs a konata log file
        ```
    * Verilator の場合は，```make -f Makefile.verilator``` のように，Makefile.verilator を指定してください
    * Vivado の場合は，```make -f Makefile.vivado``` のように，Makefile.vivado を指定してください
* 上記のサブコマンドは "konata" ではなく  "kanata" です
* くわしくは下記を参照してください
    * [機能シミュレーション](jp-devel-test-simulation) を参照


## シミュレーション結果の可視化

* シミュレーションが成功した場合，"kanata.log" が Processor/Src 内に生成されます
* [Konata](https://github.com/shioyadan/Konata/releases) を使用することで，ログの可視化ができます

## 合成

* [合成の手順](jp-synth-howto) を参照してください

## コードをいじる前に 
下記に目を通しておいてください
* [コーディング規約](jp-devel-coding-convention)
* [リポジトリの更新方法](jp-devel-repository-convention)



