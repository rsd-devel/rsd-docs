# RSD ドキュメント

RSD v1.2.0 向けのシミュレータ、テスト、ZedBoard 用 Linux イメージの手順をまとめています。実機や CAD ツールの手順は、各ページに記載したバージョンを前提としています。

ページを追加するときは、日本語版を `jp/` に、英語版を `en/` の同じ相対パスに置いてください。各ページの先頭にタイトルを書き、それぞれの言語の目次に追加してください。

## はじめての人へ

[はじめてみよう](development/getting-started.md)の手順に沿って，シミュレータをビルドし，基本テストを実行してください．


## ページ一覧

### 開発
* [はじめてみよう](development/getting-started.md)
* [ビルドの入口と Makefile の構成](development/build.md)
* [ディレクティブ一覧](development/directive.md)
* [コーディング規約](development/coding-convention.md)
* [リポジトリ更新規約](development/repository-convention.md)
* [環境構築](development/environment.md)
* [環境変数](development/environment-variables.md)
* [Vivado の初期設定](development/vivado.md)
* [旧ツールの導入記録](development/tools.md)

### テスト・デバッグ
* [テスト・プログラム](testing/program.md)
* [TestDriver の実行上限と結果検証](testing/driver.md)
* [トラブルシューティング](testing/troubleshooting.md)
* [機能シミュレーション](testing/simulation.md)
* [単体テスト](testing/unit-test.md)
* [CoreMark・Dhrystone の検証と計測](testing/coremark.md)
* [Verilator による機能シミュレーション](testing/verilator.md)
* [自分のプログラムをコンパイルして実行する方法](testing/build-and-run.md)

### アーキテクチャ
* [メモリ・マップ](architecture/memory-map.md)
* [バイナリ](architecture/binary.md)
* [マイクロアーキテクチャ](architecture/microarchitecture.md)

### 合成
* [合成方法](synthesis/overview.md)
* [制約とは](synthesis/constraints.md)
* [合成結果を使ったシミュレーション](synthesis/post-synthesis-simulation.md)
* [Synplify による合成結果の確認](synthesis/synplify.md)

### FPGA ZYNQ 向けの情報
* [FPGA ボード](fpga/board.md)
* [クロック・ジェネレータ](fpga/zynq/clock.md)
* [メモリ・コントローラ](fpga/zynq/mem-controller.md)
* [システム・アーキテクチャ](fpga/zynq/arch.md)
* [PS 部の Linux](fpga/zynq/linux.md)
* [ZYNQ において Linux を介して起動する場合の合成方法](fpga/zynq/synth-for-linux.md)
* [ZYNQ において直接起動する場合の合成方法](fpga/zynq/synth-for-baremetal.md)
