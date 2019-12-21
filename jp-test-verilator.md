# Verilatorで機能シミュレーション
まだ殴り書き状態だけど，これから整理します．

## 最初に

SetEnv 中の velirator のパスを適宜設定


## ビルドと実行

* Processor/Src を vscode で開いて，F1 キー から >runtask とか打って，タスクの実行を選択
    * vscode の上でビルドすると，エディタ内でエラーの箇所を出してくれるようにしておいた

* run, make, clean, dump ってのが出てくるので，それぞれ選ぶ
    * あるいは，以下のコマンドを直にうつ
    make -f Makefile.verilator.mk run 


## メモ
* Makefile.verilator.mk の -CFLAGS "-O0 -g" \ の -O0 を -O2 にすると数倍速くなるけど，コンパイルがかなり遅くなる

* VS Code について以下の拡張が結構いいので，入れてみるとよい．
    SystemVerilog - Language Support
    eirikpre.systemverilog
    Eirik Prestegårdshus8,226リポジトリ


## 波形の見方

Makefile.verilator.mk 内で，
* 以下の行の -D RSD_VERILATOR_TRACE を有効に
	CXXFLAGS="-D RSD_FUNCTIONAL_SIMULATION_VERILATOR -D RSD_FUNCTIONAL_SIMULATION -D RSD_VERILATOR_TRACE -Wno-attributes" \

* VERILATOR_OPTION に --trace のオプションをつける


* make したあと，make dump
    * simx.vcd と言うファイルが生成される

* gtkwave と言うソフトで開く
    * https://sourceforge.net/projects/gtkwave/files/

* 構造体がまとめてしか表示されないので，場合によっては，個別の信号を定義して代入しておく
* 波形のリストに出てこない場合，以下のようなプラグマをつけると見れる
    logic s /*verilator public*/;

