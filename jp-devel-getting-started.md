# はじめよう

* ここではソースコードをコンパイルしてとりあえず論理検証を行うまでの手順を説明します．

## 1. 環境構築

* [ここ](en-devel-environment) 
（[日本語版](https://translate.google.com/translate?hl=jp&sl=en&tl=ja&u=https://github.com/rsd-devel/rsd/wiki/en-devel-environment)）を参照して，必要なツールをインストールしてください


## 2. 環境変数の設定

* [ここ](en-devel-environment-variables)（[日本語版](https://translate.google.com/translate?hl=jp&sl=en&tl=ja&u=https://github.com/rsd-devel/rsd/wiki/en-devel-environment-variables)） を参照して，環境変数を設定してください


## 3. シミュレーション

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
* 備考
    * くわしくは[機能シミュレーション](jp-test-simulation)を参照してください
    * 自分で作ったプログラムを RSD 上で実行するための方法は [こちら](https://translate.google.com/translate?hl=jp&sl=en&tl=ja&u=https://github.com/rsd-devel/rsd/wiki/en-test-how-to-compile-and-run-your-program) を参照してください．
* シミュレーション結果の可視化
    * シミュレーションが成功した場合，"kanata.log" が Processor/Src 内に生成されます
    * [Konata](https://github.com/shioyadan/Konata/releases) を使用することで，ログの可視化ができます

## 4. 合成

* [合成の手順](jp-synth-howto) を参照してください

## 5. コードをいじる前に 
下記に目を通しておいてください
* [コーディング規約](jp-devel-coding-convention)
* [リポジトリの更新方法](jp-devel-repository-convention)



