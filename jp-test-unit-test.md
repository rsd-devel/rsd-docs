# 単体テスト

## 単体テスト 

各モジュールの入出力を、 SystemVerilog Assertion を使って検証します。


### テストの実行方法 

Src/Verification/UnitTest に、各単体テストのディレクトリが存在します。

各テストにはMakefileが存在し、以下のようにコマンドを実行できます。

|コマンド名|動作|備考|h
|make rtl / make rtl-run|ISEの合成結果を使わず、Modelsimのみでテスト対象のモジュールをコンパイル/実行します||
|make translate / make translate-run|Post Translate Simulation Model を使ってテストをコンパイル/実行します|あらかじめ [Post Translate Simulation Modelを作成](jp-synth-howto.md) しておく必要があります|
|make map / make map-run|Post Map Simulation Model を使ってテストをコンパイル/実行します|あらかじめ [Post Map Simulation Modelを作成](jp-synth-howto.md) しておく必要があります|
|make par / make par-run|Post Place-and-Route Simulation Model を使ってテストをコンパイル/実行します。回路遅延を反映したテストを行うことができます|あらかじめ [Post Place-and-Route Simulation Modelを作成](jp-synth-howto.md) しておく必要があります|


### 注意点 

* Assertionは、プロセッサのパラメータがある特定の値であることを前提に記述してます。
パラメータが変わったら、Assertionも書き直す必要があります。
