# QuestaSim で合成結果をシミュレーション (Vivado編)

Vivadoで合成した結果をもとに、QuestaSimでシミュレーションを行うことができます。
機能シミュレーションよりも実際の振る舞いに近いシミュレーションを行うことができるので、
機能シミュレーションと実機の動作が食い違う場合のデバッグに利用できます。

## 準備
 [Vivado の初期設定](jp-devel-vivado)を元に初期設定を行っておく

## 大まかな流れ

* 作成した.svソースコード群をSynplifyで合成してネットリスト(.vm)を作成する
* ネットリストをVivadoで合成してPost-synthesisシミュレーションモデル(.v)を作成する
* シミュレーションモデルをQuestaSimでシミュレーションする

これをバグが直るまで繰り返す

## 合成後モデルの種類 

Vivadoの合成では、以下の2つのステップを順に行います。

* Synthesis
* Implementation (Place and Route)

どのステップまで終了したかに応じて、以下の2種類のモデルが存在します。

* Post Synthesis Simulation Model
* Post Timing Simulation Model

Post Timing Simulation Model は回路遅延を反映したモデルになっています。  
これを使用すれば、タイミング付き検証を行うことができますが，まだやったことはありません。  
(TODO: Post Timing Simulation Modelを使ったシミュレーション方法の追記)


## Synplifyを用いたネットリストの作成 

Getting started か Built from scratch のどちらか1つだけで十分です

### Getting started  

* "$(RSD\_ROOT)/Processor/Project/Synplify/"内にシミュレーションに使いたいプログラムのcode.hexを置く．

* Synplifyで"$(RSD\_ROOT)/Processor/Project/Synplify/proj\_1.prj"を開く

* [Project Files]内の"$(TARGET\_BOARD)\_post\_synthesis"を選択して[Run]でコンパイル/合成

### Build from scratch  

* "$(RSD\_ROOT)/Processor/Project/Synplify/"内にシミュレーションに使いたいプログラムのcode.hexを置く．

* プロジェクトを作成し、ソースファイルを追加
    * .svファイルを追加(Src/Verification/以下は除く)
    * 先ほど設置した code.hex を追加

* [Add Implementation]をクリックして Implementation Options を設定
    * [FPGAの型番情報](jp-fpga-board)を指定
    * トップモジュールにMainを指定。モジュール・パラメータも適宜指定
    * Implementation Results タブでImplementation Nameに"$(TARGET\_BOARD)\_post\_synthesis"と設定
    * Implementation Results タブでResult Base Nameに"rsd"と設定

* 画面下部のTCLコンソールで"set\_option -hdl\_define -set RSD\_POST\_SYNTHESIS"を入力する

* [Project Files]内の"$(TARGET\_BOARD)\_post\_synthesis"を選択して[Run]でコンパイル/合成

## Vivadoを用いた Post-Synthesis シミュレーションモデルの作成

* "$(RSD\_ROOT)/Processor/Project/Synplify/$(TARGET\_BOARD)\_post\_synthesis/"内に、RSDのネットリスト (rsd.vm) ができていることを確認する．

* Cygwin上で"$(RSD\_ROOT)/Processor/Src"にcdして"make post-synthesis"でPost-synthesisシミュレーションモデルの作成

* Post-synthesisシミュレーションモデル "$(RSD\_ROOT)/Processor/Project/Vivado/$(TARGET_BOARD)/Main\_post\_synthesis.v"が作成されていることを確認する

## QuestaSim でのシミュレーション 
Vivado が生成した Verilog ファイルの中には、合成済のトップモジュールが定義されています。
この Verilog ファイルは、FPGA の各資源（LUTなど）に相当するモジュールをインスタンシエートしてそれらを接続するという形で記述されており、
算術演算子や論理演算子は一切使われていません。

この合成済のトップモジュールをインスタンシエートするテストベンチを書けば、通常通りQuestaSimでシミュレーションを行うことができます。
FPGA の資源というレベルで動作をシミュレーションするため、
機能シミュレーションよりも実際の振る舞いに近いシミュレーションを行うことができます。


## Makefileのコマンド 

$(RSD\_ROOT)/Processor/Src/Makefileには、合成結果をシミュレーションするためのコマンドが存在します。

|コマンド名|動作|備考|h
|post-synthesis|Post Synthesis Simulation Model を使ってテストをコンパイルします|あらかじめ上記の手順でPost Synthesis Simulation Modelを作成しておく必要があります|
|post-synthesis-run|Post Synthesis Simulation Model を使ってテストを実行します|あらかじめPost Synthesis Simulation Modelをコンパイルしておく必要があります|
|post-synthesis-kanata|Post Synthesis Simulation Model を使ってテストを実行し、Kanata形式のログを出力します|あらかじめPost Synthesis Simulation Modelをコンパイルしておく必要があります|
