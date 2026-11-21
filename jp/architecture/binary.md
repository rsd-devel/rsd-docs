# RSD のバイナリ

RSD のテストベンチには ELF を直接ロードせず，ビルドで生成した `code.hex` を渡します．メモリのアドレス範囲は [メモリ・マップ](memory-map.md) を参照してください．

## HEX の形式

[BinaryToHex.py](https://github.com/rsd-devel/rsd/blob/master/Processor/Tools/TestDriver/BinaryToHex.py) は，通常 1 行あたり 16 byte を表す 32 桁の hex 値を出力します．これはメインメモリの 1 エントリの幅に対応します．各行ではアドレスの大きい byte が左側に並びます．

ファイルは内部メモリの先頭から連続して展開されます．基本テストのイメージは，先頭の `0x1000` byte のパディングと，その後の ROM 用データを含みます．ROM・RAM の両方を含むイメージでは，ファイルの先頭 64 KiB が ROM 側，続く領域が論理アドレス `0x80000000` 以降の RAM 側に対応します．

アドレス・サイズは生成された `rsd-memory-map.mk`・`.h`・`.ld` を共有します．ROM のパディングは `RSD_ROM_PHYSICAL_BASE`，ROM イメージのサイズは `RSD_ROM_PHYSICAL_END + 1` です．`END` は有効な最終アドレスなので，objcopy の `--pad-to` には論理アドレスの `RSD_ROM_END + 1` を渡します．上記の数値は既定マップの場合です．

## 基本 C テストのビルド

[BuildC.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/C/BuildC.inc.mk) と [Makefile.inc](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Makefile.inc) が次の処理を行います．

1. GCC でソース・スタートアップ・ローダをコンパイルし，GCC のリンクドライバと `rsd-ld.script` で `code.elf` を生成する．
2. objcopy で必要なセクションを取り出し，先頭のパディングを加えて `code.bin` を生成する．
3. `BinaryToHex.py` で `code.hex` に変換する．

コンパイラのファイル名は `riscv64-unknown-elf-*` でも，ビルドフラグが RV32 と `ilp32` ABI を選択します．FP 有効時の ISA 指定は `rv32imaf_zicsr_zifencei`，無効時は `rv32ima_zicsr_zifencei` です．基本 C テストは soft-float ABI と互換の RV32IM ランタイムライブラリを使用します．FP 命令の実装・検証上の制約は [マイクロアーキテクチャ](microarchitecture.md) を参照してください．

## VMA と LMA

VMA は実行時に参照するアドレス，LMA はセクションの初期値をロードするアドレスです．基本 C テストのリンカスクリプトでは，`.text`・`.rodata`・`.srodata` を ROM に配置し，`.data`・`.sdata` は RAM の VMA と ROM の LMA を持たせます．

`rsd-crt.s` は `main` の前に [rsd-loader.c](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/rsd-loader.c) の `_load` を呼び，初期値を ROM から RAM にコピーし，BSS をゼロで初期化します．`main` から戻ると `0x1004` の終了ループに入ります．テストベンチは PC の下位 16 bit で終了を判定します．ACT4 は RAM 内の別アドレスとの誤一致を避けるため PC による終了判定を無効にし，命令数上限と実行結果で検証します．これは基本テスト用の起動処理で，他のスイートが同じリンカスクリプト・ローダを使うとは限りません．

リンカは `.data` の ROM/RAM 開始位置と `.bss` を 4 byte に揃え，`__data_load_start = LOADADDR(.data)` を定義します．ローダはこの LMA を使い，byte 単位のコピー・ゼロ初期化で端数も処理します．

## ROM と RAM を含むイメージ

ACT4 の [Makefile](https://github.com/rsd-devel/rsd/blob/develop/Processor/Src/Verification/TestCode/riscv-arch-test/Makefile) は，ELF から ROM と RAM の内容を別々に取り出し，パディング・ROM・RAM の順に結合して HEX を生成します．テスト本体は RAM 上で実行され，RAM の初期値もテストベンチがロードします．基本 C テストのように，すべての初期値を ROM に置いてからコピーする方式ではありません．

Zephyr などにも専用のビルド・起動処理があります．配置の詳細は各スイートの Makefile とリンカスクリプトを参照してください．

## 環境ごとのロード

| 環境 | ロード方法 |
| --- | --- |
| Verilator 5，ModelSim/QuestaSim，Vivado の RTL シミュレーション | 共通の [TestMain.sv](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestMain.sv) が `InitializeMemory` を呼び，HEX を内部メモリへ展開 |
| 現在の合成後テスト | 対象プログラムの HEX を内部メモリの初期値としてネットリストに組み込む．HEX 変更時は再合成が必要 |
| Zynq 上の ARM Linux から起動 | ARM 上の [loader.c](https://github.com/rsd-devel/rsd/blob/master/Processor/Project/Vivado/ARM_Linux/ProgramLoader/loader.c) がプログラムを転送 |

シミュレーション向けに用意されたイメージを実機へ持ち込む場合は，ボード側のローダとメモリ構成にも合わせてください．
