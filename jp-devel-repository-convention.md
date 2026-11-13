# リポジトリの更新規約

テスト手順は本体の構成に合わせています．テスト群の範囲と外部ソースの準備は [テスト・プログラム](jp-test-program)，既知の ACT4 の制約は [マイクロアーキテクチャ](jp-arch-microarch) を参照してください．

## 基本

* git リポジトリで作業をする際は，[github-flow](https://gist.github.com/Gab-km/3705015) に従ってください
    * git-flow ではないので注意

* 要するに
    1. master から説明的なブランチを作成
    2. その上で作業
    3. master に対し pull request 
    4. マージ

* 注意
    * master 上で直接作業をしない
    * マージ後は基本的にブランチは削除

* git の操作に関しては，（なれてない人は）GUI クライアントの使用を強く推奨
    * git のブランチの視覚的なイメージがないと，何が行われているのかが理解できない


## コミット・メッセージについて

* コミット・メッセージは [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) に従って書いてください
* 一部の古いコミットは，この規約にしたがっていません


## master へマージする時のチェックリスト
### 概要

* 以下では RSD/master にプルリクエストを送ってマージするまでにチェックすべき項目について記します.
* 別途, 下記を参照してください.
    * [機能シミュレーション](jp-test-simulation)
    * [合成後・タイミング付きシミュレーション](jp-synth-simulation)
    * [Coremark について](jp-test-coremark)


### マージ時のチェックリスト

* modelsimでのコンパイルが通る
    * 対応するコマンド: `Processor/Src` で `make SIM=modelsim`（ModelSim/QuestaSim を別途設定）

* 簡単な機能シミュレーションテストが正しく実行される
    * 対応するコマンド: シミュレータをビルドした後に `make test/level-1/run`（ModelSim/QuestaSim は `SIM=modelsim` も指定）．これらは基本テストの HEX もビルドする
    * テストプログラムのビルド方法や内容は [テスト・プログラム](jp-test-program) 参照

* Coremark の機能シミュレーションテストが正しく実行される
    * 対応するコマンド: `make test/External/Coremark/run`（ModelSim/QuestaSim では `SIM=modelsim` を指定）
    * 初回は `make test/External/Coremark/fetch` で公開ソースを取得する

* Coremark の post-synthesis シミュレーションが正しく実行される
    * 実行方法は [合成後・タイミング付きシミュレーション](jp-synth-simulation) 参照
    * 機能テスト用 CoreMark をビルドした後，たとえば `make synth/vivado/post-synthesis/test TEST_CODE=Verification/TestCode/Coremark/Coremark` で実行する．TestDriver が合成後テストの作業ディレクトリで UART 出力を検証する


### 追加のテスト範囲

`test/all/run` は基本テストと CoreMark・Dhrystone を実行します．ACT4・Zephyr は `test/ex/run`，RTL 単体テストは `test/unit/run`，テスト基盤は `test/tools/run` で個別に実行します．変更対象に応じた検証を行い，実行したツール・構成・対象を記録してください．FP の有無や拡張選択も検証記録に含めます．

### プルリクエスト

前節のチェックリストをクリアしたのち, github のプルリクエストを介して master にマージするようにしましょう.
