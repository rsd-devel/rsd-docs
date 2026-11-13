# 機能シミュレーション

RSD の RTL をシミュレーションし，終了条件・論理レジスタ・UART 出力を検証します．以下は `Processor/Src` で実行します．環境構築は [はじめよう](jp-devel-getting-started) を参照してください．

## シミュレータのビルド

| シミュレータ | ビルド | 基本テスト |
| --- | --- | --- |
| Verilator | `make -j4` | `make test/level-1/run` |
| ModelSim/QuestaSim | `make SIM=modelsim` | `make SIM=modelsim test/level-1/run` |
| Vivado XSim | `make SIM=xsim` | `make SIM=xsim test/level-1/run` |

いずれも `Verification/TestMain.sv` を使用します．RTL やテストベンチを変更した後はシミュレータを再ビルドします．`test/level-1/run` などの登録済みプログラムテストは必要な HEX をビルドしますが，シミュレータ自体はビルドしません．テストの区分と外部ソースの準備は [テスト・プログラム](jp-test-program) を参照してください．

## 一つのプログラムを検証する

たとえば HelloWorld をビルド・検証する場合は，次を実行します．

```bash
make test/C/HelloWorld/run
```

任意のテストディレクトリを指定する場合は，先にそのプログラムをビルドしてから次を実行します．`RunTest.py`は指定プログラムをビルドしません．

```bash
python3 ../Tools/TestDriver/RunTest.py --simulator=verilator Verification/TestCode/C/HelloWorld
```

TestDriver は指定ディレクトリの小文字の `cfg.xml` を読み，正常に実行が終了した後，`RegisterValues` と `serial.ref.txt` の期待値を検証します．UART 出力は `serial.out.txt` に保存されます．

```xml
<Config>
  <MaxTestInstructions>10000</MaxTestInstructions>
  <MaxNoCommitCycles>500</MaxNoCommitCycles>
  <RegisterValues>
    <R10>0</R10>
  </RegisterValues>
</Config>
```

| 項目 | 意味 |
| --- | --- |
| `MaxTestInstructions` | スタートアップを含むコミット済み RISC-V 命令数の上限．投機実行・リプレイは消費しない |
| `MaxNoCommitCycles` | マイクロ命令のコミットがない連続サイクル数の上限．既定値は 500，超過は失敗 |
| `EnablePC_Goal` | 既定値は `1`．命令数上限までに終了 PC へ到達する必要がある．`0` は指定命令数まで実行する継続型テスト用 |
| `MaxTestCycles` | 追加のサイクル数上限．省略または `0` で無効．命令数上限を使うテストで先に達すると失敗 |

`RegisterValues` は UART のみを検証する場合などには空にできます．既存のサイクル数のみの設定も受け付けますが，新しいテストでは上記の命令数・無コミット期間を設定します．キャッシュフラッシュなど待ち時間の長いケースでは，無コミット期間をケースに応じて設定します．

ログには終了理由，コミット命令数・マイクロ命令数，サイクル数，最大無コミット期間，IPC が出力されます．IPC は参考値で，合否条件ではありません．境界条件などの詳細は [TestDriver reference](jp-test-driver) を参照してください．

## デバッグ用の実行

`sim/run`・`sim/kanata`・`sim/dump` は `cfg.xml` ではなく make 変数を使います．これらは期待値の比較も行わないため，結果の検証には `RunTest.py` または登録済みの `test/.../run` を使います．デバッグ時はプログラムを先にビルドしてください．

```bash
make test/level-1/build
make sim/run TEST_CODE=Verification/TestCode/C/Fibonacci
make sim/kanata TEST_CODE=Verification/TestCode/C/Fibonacci
```

`sim/kanata` が生成する `Kanata.log` を [Konata](https://github.com/shioyadan/Konata/releases) で開き，リプレイやコミット停止などを調べます．このターゲットでは `Register.csv` も出力されます．上限を変える例は次のとおりです．

```bash
make sim/kanata \
    TEST_CODE=Verification/TestCode/C/Fibonacci \
    MAX_TEST_INSTRUCTIONS=200000 MAX_NO_COMMIT_CYCLES=1000
```

Verilator の `sim/dump` は `Register.csv`，`RSD.log`，`Kanata.log`，`simx.vcd` を生成します．[Verilator の説明](jp-test-verilator) を参照してください．ModelSim/QuestaSim は `make SIM=modelsim sim/gui TEST_CODE=...`，Vivado は `make SIM=xsim sim/gui TEST_CODE=...` で GUI を起動できます．
