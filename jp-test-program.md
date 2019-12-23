# テスト・プログラム

雷上動プロセッサ上で実行可能なテスト・プログラムについて記述します。

テスト・プログラムのビルドの際は，RISCV用のクロスコンパイラを環境変数に設定することが必要になります．Processor/Tools/SetEnv を参照してください．
また，テスト後は[リポジトリの更新方法](jp-devel-repository-convention)も参照してください.

## 一覧
テスト・プログラムのディレクトリは，Src/Verification/TestCode です。
テスト・プログラムはアセンブリ言語，C 言語，その他のベンチマークの3種類に大別されます．
ビルド・コマンドは RSD/Processor/Src 下で実行できます．

|ディレクトリ名|ビルドコマンド|説明|
|-------------|-------------|----|
|Asm|test-build-asm|アセンブリ言語で記述するテストプログラム|
|C|test-build-C|C言語で記述するテストプログラム|
|Coremark|test-build-Coremark|Coremark （詳しくは[coremarkについて](jp-test-coremark)を参照）|
|Zephyr [*](#事前準備)|test-build-Zephyr|Zephyr 上で動かすプログラム|
|Dhrystone [*](#事前準備)|test-build-Zephyr|Zephyr 上で動く Dhrystone （2018年に開催されたコンテスト用）|
|riscv-compliance [*](#事前準備)|test-build-riscv-compliance|riscv-compliance のテストスイート（現時点ではRV32Iのみ）|

補足1：ライセンス上の問題のため，一部のプログラムは RSD リポジトリには置いてありません．これらはビルドの際に RSD-env から自動的にコピーされるようになっています．

補足2：Dhrystone は C 言語版と Zephyr 版の 2 種類があります．C 言語版は C ディレクトリ以下にあります．


## 事前準備

一部のテスト・プログラム（[一覧](#一覧)で*印のついたもの）については，データのダウンロードや git リポジトリからのクローンが必要であるため，事前に次のことを行っておく必要があります．

1. Zephyr SDK のインストール
    * RSD-env/Tools/OS/Zephyr へ移動し，以下のコマンドを実行してください．
```
    sudo make install_deps  # apt で必要なものを入れる
    make install            # zephyr 自体や SDK を入れる
    make build              # zephyr のアプリ（ELFファイル）をビルドする
    make run_qemu_philosophers   # philosophers を QEMU で動かしてみる
```

2. Zephyr 上で動くアプリケーションの hex ファイルなどの生成
    * RSD-env/Tools/Testbench/Zephyr に移動して `make` を実行
        * 1 の make build でも ELF ファイルはできるのだが，RSD の入力として使える hex ファイルは作られないので，ここで make する必要がある．
        * RSD リポジトリでの make test-env-build-XXXX みたいなのはここでビルドしたものをコピーしてくるだけになっているので注意．


3. riscv-compliance のクローン／ビルド
    * RSD-env/Tools/Testbench/riscv-compliance で make を実行してください．

## ビルド手順

個々のテスト・プログラムをビルドする手順の概要を説明します。

### 一括ビルド

RSD/Processor/Src へ移動し，以下のコマンドを実行すれば全てのプログラムを一括してビルドできます．（ただし，Zephyr 関連のプログラムと riscv-compliance は RSD-env からコピーしてくるだけでビルドはしません）．

    make test-build

Zephyr 関連のプログラムと riscv-compliance を再ビルドしたい場合は，以下のコマンドを実行してください．

    make test-env-build                       # Zephyr 関連のプログラムの再ビルド
    make test-env-build-riscv-coompliance     # riscv-compliance の再ビルド


### 個別ビルド

RSD/Processor/Src 上で，[一覧](#一覧)内にあるビルドコマンドを実行すれば，対象を特定の種類に絞ってビルドできます．

### ビルド時の動作（仕様が昔と異なるため要修正？）

* RISCVクロスコンパイラを呼び出し，アセンブリプログラムを出力(C言語のみ)

* RISCVアセンブラ／リンカを呼び出し，objectファイルを作成
    * 雷上動専用のスタートアップルーチン(rsd-crt.s)とリンカスクリプト(rsd-ld.script)を使用する

* Tools/TestDriver/ObjectFileConverter.py を呼び出し，objectファイルをbinファイルに変換
* Tools/TestDriver/BinToHex.py を呼び出し，binファイルをhexファイルに変換
    * hexファイルの形式にすれば，SystemVerilogのコード上で雷上動のメインメモリにロードできる

## プログラムの追加
テスト・プログラムを追加する手順を説明します。

* 実行したいコードを TestCode/Asm または TestCode/C にフォルダを作成して code.hex と cfg.xml を追加
* TestCode/Asm または TestCode/C の Makefile を編集してビルド用の設定
* RSD/Processor/Src の Makefile を編集してテスト用の設定

Makefile の編集は、基本的に他のテスト・プログラムを参考にして書けば大丈夫です。