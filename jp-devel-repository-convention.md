# リポジトリの更新規約

現在，一部テスト関係のコードが機能していないため，make test 系が失敗する可能性があります（2020/01/18）．近日中にテスト用ベンチマークを統合して修正する予定です．

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
    * [QuestaSim で合成結果をシミュレーション](jp-synth-simulation)
    * [Coremark について](jp-test-coremark)


### マージ時のチェックリスト

* modelsimでのコンパイルが通る
    * 対応するコマンド: `make` または `make rtl`

* 簡単な機能シミュレーションテストが正しく実行される
    * 対応するコマンド: `make test-build` の後に `make test-1`
    * テストプログラムのビルド方法や内容は [テスト・プログラム](jp/開発手順/テストとデバッグ/テスト・プログラム) 参照

* Coremark の機能シミュレーションテストが正しく実行される
    * 対応するコマンド: `make test-Coremark`
    * RSD レポジトリには Coremark のテストコードは含まれていないので, RSD_ENV を設定して RSD-env レポジトリからコピーする必要あり(Src/Verification/TestCode/C/Makefile.inc 参照)

* Coremark の post-synthesis シミュレーションが正しく実行される
    * 実行方法は [QuestaSim で合成結果をシミュレーション](jp-synth-simulation) 参照
    * 実行結果の確認は Src/Verification/TestCode/C/Coremark/serial.out.txt が 同フォルダserial.ref.txt と一致しているかで行う


### プルリクエスト

前節のチェックリストをクリアしたのち, github のプルリクエストを介して master にマージするようにしましょう.

