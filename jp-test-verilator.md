# Verilator による機能シミュレーション

RSD では Verilator 5.054 と，共通の SystemVerilog テストベンチ `Verification/TestMain.sv` を使用します．環境構築は [はじめよう](jp-devel-getting-started) を参照してください．手動導入では `RSD_VERILATOR_BIN` に Verilator 実行ファイルを設定できます．省略時は `PATH` 上の `verilator` を使います．

## ビルドと実行

`Processor/Src` で実行します．

```bash
make -j"$(nproc)"
make test/level-1/run
make sim/run TEST_CODE=Verification/TestCode/C/Fibonacci
```

`test/level-1/run` は基本プログラムをビルドして期待値を検証します．`sim/run` はビルド済みのプログラムを実行します．個別のテストや設定は [機能シミュレーション](jp-test-simulation) を参照してください．

## パイプラインと波形の出力

基本テストのビルド後，次を実行します．

```bash
make sim/kanata TEST_CODE=Verification/TestCode/C/Fibonacci
make sim/dump TEST_CODE=Verification/TestCode/C/Fibonacci
```

| 出力 | 用途 |
| --- | --- |
| `Kanata.log` | Konata でパイプラインを表示 |
| `RSD.log` | Kanata 形式への変換前のログ |
| `Register.csv` | コミット時のレジスタ値 |
| `simx.vcd` | `sim/dump` の波形．GTKWave などで表示 |

出力先は `Processor/Src` です．現在の Makefile は `--trace` を有効にしており，`sim/dump` が `+WAVE_LOG_FILE=simx.vcd` を渡します．

`sim/run`・`sim/kanata`・`sim/dump` の実行上限は `MAX_TEST_INSTRUCTIONS`，`MAX_NO_COMMIT_CYCLES`，`MAX_TEST_CYCLES` で指定します．`cfg.xml` を変更してもこれらのターゲットの上限は変わりません．

## 実装を調べる場合

[Makefiles/VerilatorCore.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefiles/VerilatorCore.inc.mk) と [共有オプション](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefiles/Verilator.inc.mk) は `TestMain` をトップとして `--main`・`--timing` で実行ループを生成します．生成モデルは `Processor/Project/Verilator/obj_dir/VTestMain` です．モデルを直接実行する場合の引数は `+TEST_CODE=...` のような plusarg 形式です．通常は make または TestDriver 経由で実行します．

FP などの構成を変えるときは，シミュレータとテストをクリーンしてからビルドします．

```bash
make clean test/level-1/clean
make -j"$(nproc)"
make test/level-1/run
```
