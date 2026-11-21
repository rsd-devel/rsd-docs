# 自作プログラムを Verilator でコンパイル・実行する

[開発環境](../development/getting-started.md) を準備し，RSD 本体の `Processor/Src` で実行します．共通の [コンパイラ設定](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Makefile.inc) は RV32，`ilp32` ABI，picolibc の検索パスを選択します．

## 1. シミュレータと共有起動コードのビルド

```bash
make -j"$(nproc)"
make test/crt/build
```

## 2. HelloWorld からプログラムを作成

`Verification/TestCode/C` にディレクトリを作り，入力ファイルだけをコピーします．

```bash
mkdir Verification/TestCode/C/YourTest
cp Verification/TestCode/C/HelloWorld/{Makefile,code.c,cfg.xml,serial.ref.txt} \
    Verification/TestCode/C/YourTest/
```

`YourTest/code.c` を編集します．テンプレートは生成ヘッダ `rsd-memory-map.h` の `RSD_SERIAL_OUTPUT`（既定値 `0x40002000`）の UART へ出力します．`Verification/TestCode/C/lib.c` にもシリアル出力用の関数があります．基本 C テンプレートは汎用の `printf` 実装をリンクしません．ベンチマークの移植版は独自の出力関数を持ちます．

`serial.ref.txt` は改行を含む正確な期待出力に更新し，`cfg.xml` に期待するレジスタ値と実行上限を設定します．`main` が 0 を返すプログラムでは，次の設定で `a0` を検査できます．

```xml
<Config>
  <MaxTestInstructions>10000</MaxTestInstructions>
  <MaxNoCommitCycles>500</MaxNoCommitCycles>
  <RegisterValues>
    <R10>0</R10>
  </RegisterValues>
</Config>
```

`EnablePC_Goal` は既定で `1` で，命令数上限までに終了ループへ到達する必要があります．プログラムに合う上限を設定してください．継続型テストや追加の制限は [TestDriver の説明](driver.md) を参照してください．追加の C ファイルは `YourTest/Makefile` の `SRCS` に登録します．

## 3. ビルドと検証

```bash
make -C Verification/TestCode/C/YourTest
python3 ../Tools/TestDriver/RunTest.py --simulator=verilator Verification/TestCode/C/YourTest
```

ビルドにより `code.elf`，`code.bin`，`code.hex` が生成されます．`RunTest.py`は `cfg.xml` のレジスタ・シリアル期待値を検査しますが，任意の `TEST_CODE` をビルドしません．プログラム編集後は再ビルドしてください．RTL とプログラムの構成を揃え，FP の有無を変更した場合は両方をクリーンします．

## 4. 実行内容の確認

```bash
make sim/run TEST_CODE=Verification/TestCode/C/YourTest
make sim/kanata TEST_CODE=Verification/TestCode/C/YourTest
make sim/dump TEST_CODE=Verification/TestCode/C/YourTest
```

`Kanata.log` を Konata，`simx.vcd` を波形ビューアで開きます．これらのデバッグ用ターゲットは `cfg.xml` ではなく make 変数を使い，期待値の比較は行いません．上限を変える場合は，たとえば `MAX_TEST_INSTRUCTIONS=200000 MAX_NO_COMMIT_CYCLES=1000` を渡します．Makefile 内の `TEST_CODE` を編集する必要はありません．

## 5. テスト群への登録

`Verification/TestCode/C/Makefile` の `SRC_DIRS` に `YourTest` を，`Makefiles/TestCommands.inc.mk` の `LEVEL1_TESTS` に `test/C/YourTest/run` を追加します．これで `make test/C/YourTest/run` が必要に応じて C テストをビルドし，シミュレータで結果を照合します．同じ登録から，ビルド済みの HEX に対する `hex-path`・`zynq/deploy`・`zynq/run` も使えるようになります．SSH 接続と手動実行の手順は [ZedBoard の実機ガイド](../fpga/zynq/synth-for-linux.md) を参照してください．
