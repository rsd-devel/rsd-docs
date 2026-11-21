# リポジトリの更新規約

テスト手順は本体の構成に合わせています．テスト群の範囲と外部ソースの準備は [テスト・プログラム](../testing/program.md)，既知の ACT4 の制約は [マイクロアーキテクチャ](../architecture/microarchitecture.md) を参照してください．

## 基本

1. `develop` から変更内容を表す名前のブランチを作成します．
2. ブランチで作業し，`develop` に対してプルリクエストを作成します．
3. レビューとテストの後にマージし，使い終わったブランチは削除します．

リリース時は，統合済みの `develop` を検証してから `master` にマージします．

* git の操作に関しては，（なれてない人は）GUI クライアントの使用を強く推奨
    * git のブランチの視覚的なイメージがないと，何が行われているのかが理解できない


## コミット・メッセージについて

* コミット・メッセージは [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) に従って書いてください
* 一部の古いコミットは，この規約にしたがっていません


## マージ前のチェックリスト
### 概要

* 以下では RSD の develop にプルリクエストを送ってマージするまでにチェックすべき項目について記します.
* 別途, 下記を参照してください.
    * [機能シミュレーション](../testing/simulation.md)
    * [合成後・タイミング付きシミュレーション](../synthesis/post-synthesis-simulation.md)
    * [Coremark について](../testing/coremark.md)


### マージ時のチェックリスト

* modelsimでのコンパイルが通る
    * 対応するコマンド: `Processor/Src` で `make SIM=modelsim`（ModelSim/QuestaSim を別途設定）

* 簡単な機能シミュレーションテストが正しく実行される
    * 対応するコマンド: シミュレータをビルドした後に `make test/level-1/run`（ModelSim/QuestaSim は `SIM=modelsim` も指定）．これらは基本テストの HEX もビルドする
    * テストプログラムのビルド方法や内容は [テスト・プログラム](../testing/program.md) 参照

* Coremark の機能シミュレーションテストが正しく実行される
    * 対応するコマンド: `make test/External/Coremark/run`（ModelSim/QuestaSim では `SIM=modelsim` を指定）
    * 初回は `make test/External/Coremark/fetch` で公開ソースを取得する

* Coremark の post-synthesis シミュレーションが正しく実行される
    * 実行方法は [合成後・タイミング付きシミュレーション](../synthesis/post-synthesis-simulation.md) 参照
    * 機能テスト用 CoreMark をビルドした後，たとえば `make synth/vivado/post-synthesis/test TEST_CODE=Verification/TestCode/Coremark/Coremark` で実行する．TestDriver が合成後テストの作業ディレクトリで UART 出力を検証する


### 追加のテスト範囲

`test/all/run` は基本テストと CoreMark・Dhrystone を実行します．ACT4・Zephyr は `test/ex/run`，RTL 単体テストは `test/unit/run`，テスト基盤は `test/tools/run` で個別に実行します．変更対象に応じた検証を行い，実行したツール・構成・対象を記録してください．FP の有無や拡張選択も検証記録に含めます．

### プルリクエスト

前節のチェックリストをクリアしたのち, github のプルリクエストを介して develop にマージするようにしましょう.
