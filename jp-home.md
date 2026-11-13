# RSD Wiki Home (日本語)

ビルド・テストの詳細はこの Wiki で管理します．本体ソースへのリンクは master の最新版を参照します．実機・CAD ツールの操作は，各ページに記載した環境を前提とします．

ここは RSD の開発に関わる情報を集めた Wiki です．

## ページを編集するときの注意（必ず読んでね！）

* 各ページは最初に「#ページのタイトル」の形で先頭にタイトルを必ず書くようにしてください
* 日本語ページは「jp-」以下に作成してください
    * 適宜「-」で区切って，グルーピングしてください


## はじめての人へ

まずは [こちら](jp-devel-getting-started) のページを見て，そこから始めてみてください．


## ページ一覧

### 開発
* [はじめてみよう](jp-devel-getting-started)
* [ビルドの入口と Makefile の構成](jp-devel-build)
* [ディレクティブ一覧](jp-devel-directive)
* [コーディング規約](jp-devel-coding-convention)
* [リポジトリ更新規約](jp-devel-repository-convention)
* [環境構築](jp-devel-environment)
* [環境変数（英語）](jp-devel-environment-variables)
* [旧ツールの導入記録](jp-devel-tools)

### テスト・デバッグ
* [テスト・プログラム](jp-test-program)
* [TestDriver の実行上限と結果検証](jp-test-driver)
* [トラブルシューティング](jp-test-trouble-shooting)
* [機能シミュレーション](jp-test-simulation)
* [単体テスト](jp-test-unit-test)
* [CoreMark・Dhrystone の検証と計測](jp-test-coremark)
* [Verilator による機能シミュレーション](jp-test-verilator)
* [自分のプログラムをコンパイルして実行する方法](jp-test-how-to-compile-and-run-your-program)

### アーキテクチャ
* [メモリ・マップ](jp-arch-mem-map)
* [バイナリ](jp-arch-binary)
* [マイクロアーキテクチャ](jp-arch-microarch)

### 合成
* [合成方法](jp-synth-howto)
* [制約とは](jp-synth-constrain)
* [合成結果を使ったシミュレーション](jp-synth-simulation)
* [Synplify による合成結果の確認](jp-synth-synplify)

### FPGA ZYNQ 向けの情報
* [クロック・ジェネレータ](jp-fpga-zynq-clock)   
* [メモリ・コントローラ](jp-fpga-zynq-mem-controller)
* [システム・アーキテクチャ](jp-fpga-zynq-arch)
* [PS 部の Linux](jp-fpga-zynq-linux)                
* [ZYNQ において Linux を介して起動する場合の合成方法](jp-fpga-zynq-synth-for-linux)
* [ZYNQ において直接起動する場合の合成方法](jp-fpga-zynq-synth-for-baremetal)
