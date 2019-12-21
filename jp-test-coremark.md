# Coremarkについて

## 概要
CoremarkはCPUコアの性能を図るためのベンチマークです. 
20171015現在, 性能や実行の正当性検証はこのベンチマークで行っています.

## ビルド
CoremarkのソースはRSDレポジトリではなくRSD-envレポジトリにあります.
このレポジトリをクローンした後に, RSD/Tools/SetEnv/SetEnv.bat からRSD_ENVを設定してください.
RSD_ENVを設定したのちに, `make test-build` コマンドによって, 
自動的に RSD-env/Tools/Testbench/Coremark が 
RSD/Processor/Src/Verification/TestCode/C/Coremark にコピーされビルドされます.

## 機能シミュレーション用のCoremark
デフォルトでRSD-env/Tools/Testbench/Coremarkに入っているソースは少し内容を変更しており,
具体的には, 時間の計測を行わず1イテレーションだけ実行するコードになっています.それはCoremarkの以下の仕様によるものです.

## Coremarkの仕様

  * Coremark/Makefile 中で設定されている ITERATIONS という定数分だけ, 性能測定ベンチマークを実行する
  * 上記の性能測定ベンチマークに入る前と入った後にそれぞれ時間を計測し, これらの関数, start\_time()とstop\_time()は, Coremark/barebones/core\_portme.c で設定している(正確にはこれらの関数はサイクル数を求め, その後 ITERATIONS同様Makefileで設定しているCLOCKS\_PER\_SECで割る)
  * 性能測定ベンチマークの実行時間が10秒以下の場合, 結果でエラーが出る
  * ITERATIONS=0のとき, 1イテレーションだけ性能測定ベンチマークを実行し, その実行時間に応じて, 10秒を少し超えた程度の実行時間になるようにイテレーションを自動的に調整する

## RSDにおける機能シミュレーション用の設定

* RSD-env/Tools/Testbench/Coremark のデフォルト
* ITERATIONS=1, CLOCKS\_PER\_SEC=1としている
* start\_time()は0を返し, stop\_time()は10を返すようにしてある

## RSDにおける実機動作用の設定

* RSD-env/Tools/Testbench/Coremark\_for\_Synthesis にあるので利用するときは, Coremarkの方に中身をコピーするか, RSDレポジトリの方のVerification/TestCode/C/Makefileを変更する
* ITERATIONS=0, CLOCKS\_PER\_SEC=80000000としている
* start\_time()とstop\_time()はbarebones\_clock()という関数を参照し, その関数中でハードウェアカウンタを読んで実行クロック数を得る. ハードウェアカウンタのアドレスは 0xffffff00 となっている.([[jp:アーキテクチャ:システム・アーキテクチャ:メモリ・マップ]]参照)
