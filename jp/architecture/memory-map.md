# メモリ・マップ

以下は RSD の既定構成です．32 bit の論理アドレスを固定のルールで内部物理アドレスへ変換します．メモリマップの設定元は [MemoryMap.toml](https://github.com/rsd-devel/rsd/blob/master/Processor/Config/MemoryMap.toml) です．

## 設定と生成

`Processor/Config/MemoryMap.toml` の設定を [ConfigGenerator.py](https://github.com/rsd-devel/rsd/blob/master/Processor/Tools/ConfigGenerator/ConfigGenerator.py) が読み，次の共通定義を生成します．

- RTL: `Processor/Src/Config/MemoryMapTypes.sv`（テンプレートは同じディレクトリの `MemoryMapTypes.template.sv`）
- C・アセンブリ: `Processor/Src/Verification/TestCode/rsd-memory-map.h`
- リンカスクリプト: 同ディレクトリの `rsd-memory-map.ld`
- Makefile: 同ディレクトリの `rsd-memory-map.mk`

`Makefiles/GenerateConfig.inc.mk` により，RTL・単体テスト・個別プログラムのビルド時にも必要に応じて再生成します．生成物は Git に含め，編集は TOML またはテンプレートに対して行います．ツールを直接起動する場合は，本体ルートで先に次を実行してください．Python 3.11 以上の標準 tomllib を使用します．

```bash
python3 Processor/Tools/ConfigGenerator/ConfigGenerator.py --rsd-root .
```

このコマンドはメモリマップとマイクロアーキテクチャを生成します．一方だけを生成する場合は `--only memory-map` または `--only microarch` を指定します．

`insn_reset_vector` は `INSN_RESET_VECTOR` / `RSD_RESET_VECTOR`，`pc_goal` は `PC_GOAL` / `RSD_PC_GOAL` を生成します．既定値はそれぞれ `0x1000`，`0x80001004` です．終了判定は LED に出る PC の下位 16 bit を比較するため，基本テストの終了ループ `0x1004` も一致します．

PC 圧縮は既定で無効です．`memory_map.pc.width = 19` は無効時には使われず，現在のマップを圧縮するには少なくとも 20 bit が必要です．不適合な設定はジェネレータが拒否します．

領域の `size` は byte 数で，すべての `END` 定数は末尾の有効アドレスを含みます．`translation: low_bits` は論理アドレスの下位 bit を `physical_base` に加算し，`relative` は `logical_address - logical_base` を加算します．生成するソフトウェア側の `RSD_*_PHYSICAL_BASE` は変換後の先頭アドレスであり，SV の加算基準 `PHY_ADDR_*_BASE` と常に同じではありません．

## アドレスと属性

内部の `PhyAddrPath` は 24 bit で，内訳は次のとおりです．この幅は実装された RAM 容量そのものを表す値ではありません．

```systemverilog
// PhyRawAddrPath は既定構成で 22 bit
typedef struct packed {
    logic isUncachable;
    logic isIO;
    PhyRawAddrPath addr;
} PhyAddrPath;
```

以下の内部アドレス欄はフラグを除いた `addr` フィールドです．範囲の両端を含みます．

| 論理アドレス | 内部アドレス `addr` | `isUncachable` | `isIO` | 用途 |
| --- | --- | --- | --- | --- |
| `0x00001000–0x0000FFFF` | `0x001000–0x00FFFF` | 0 | 0 | ROM（60 KiB） |
| `0x80000000–0x8003FFFF` | `0x010000–0x04FFFF` | 0 | 0 | キャッシュ可能 RAM（256 KiB） |
| `0x80040000–0x8004FFFF` | `0x050000–0x05FFFF` | 1 | 0 | キャッシュ不可 RAM（64 KiB） |
| `0x40002000` | `0x002000` | 1 | 1 | UART 出力 |
| `0x40010000–0x40017FFF` | `0x000000–0x007FFF` | 1 | 1 | CLINT |
| `0xC0000000–0xC0201FFF` | `0x010000–0x211FFF` | 1 | 1 | PLIC |

24 bit の packed 値として見る場合，`isUncachable` は bit 23，`isIO` は bit 22 です．たとえば UART は `0xC02000`，キャッシュ不可 RAM の先頭は `0x850000` となります．同じ `addr` の値でも属性によって異なる領域を表します．

領域判定と変換は生成される `GetMemoryMapType` と `ToPhyAddrFromLogical` を参照してください．未定義の論理アドレスは `MMT_ILLEGAL` となり，パイプラインでアクセス例外として処理されます．

内部メモリ容量は最大の変換後メモリアドレスに穴を含めて合わせます．既定の `MEMORY_MAP_BYTE_SIZE` は `0x60000`（384 KiB）で，IO 領域は容量に含めません．キャッシュ不可 RAM は別の記憶領域であり，通常 RAM の別名ではありません．

## MMIO のアクセス順序

RSD は `type = "io"` の全領域を強順序として扱います．同じハートが発行した通常のロード・ストアは，異なるデバイスに対してもプログラム順に届きます．RSD はコミット済みのストアを順番に送り出します．ロード先が MMIO だと判明すると，その命令を直列化して再フェッチし，先行ストアがストアキューから出るのを待ってからデバイスを読みます．キャッシュ不可 RAM の属性は `type = "memory"` で，通常のメモリと同じ順序規則に従います．MMIO に対する `LR.W` はロードアクセスフォールト，`SC.W` と AMO はストア／AMO アクセスフォールトになります．

UART では，1 文字ごとに `RSD_SERIAL_STATUS` の bit 0 が 0 になるのを待ち，`RSD_SERIAL_OUTPUT` に書き込みます．STATUS を読んでも FIFO のデータは残ります．次の STATUS 読み出しは直前の書き込みの後に行われるため，1 文字ごとの `fence` は不要です．割り込みハンドラからも出力する場合は，双方が同じ空き枠を使わないよう，空き確認から書き込みまでをまとめて排他します．

テストベンチは `PC_GOAL` の命令がリタイアすると停止します．共通の起動コードは終了時に一度 `fence iorw, iorw` を実行し，最後の UART 書き込みが FIFO に届いてから終了します．この時点で FIFO 内に未読の文字が残る場合があります．

## 割り込みコントローラ

| レジスタ | 論理アドレス |
| --- | --- |
| CLINT `MSIP` | `0x40010000` |
| CLINT `mtimecmp` low / high | `0x40014000` / `0x40014004` |
| CLINT `mtime` low / high | `0x40017FF8` / `0x40017FFC` |
| PLIC source priority base | `0xC0000000` |
| PLIC pending base | `0xC0001000` |
| PLIC enable base | `0xC0002000` |
| PLIC priority threshold base | `0xC0200000` |
| PLIC claim/complete base | `0xC0200004` |

PLIC の各欄はレジスタ群の基準アドレスです．領域内のすべてのアドレスが個別の有効なレジスタになるわけではありません．実装は [IO_Unit.sv](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/IO/IO_Unit.sv) と [PLIC_Unit.sv](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/IO/PLIC_Unit.sv) にあります．

## ソフトウェアの配置

ハードウェアが受け付けるアドレス範囲と，各プログラムのリンカスクリプトが使用する範囲は区別してください．

基本 C テストの [rsd-ld.script](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/rsd-ld.script) は生成されたベースアドレスを使い，ROM/RAM の各容量を `MIN(領域サイズ, 32 KiB)` に制限します．既定では ROM は `0x00001000`，RAM は `0x80000000` から各 32 KiB です．[rsd-crt.s](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/rsd-crt.s) はスタックポインタを `RSD_RAM_BASE + 0x20000`（既定で `0x80020000`）に設定し，`rsd-loader.c` によるデータコピーと BSS 初期化を行ってから `main` を呼びます．

Zephyr は独自の board/SoC 定義を使用し，ACT4 は [link.ld](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/riscv-arch-test/link.ld) でテスト本体を `RSD_RAM_BASE + 0x10000`（既定で `0x80010000`）以降の RAM に配置します．すべてのプログラムの `.text` が ROM 上で動くとは限りません．HEX の配置と起動処理は [バイナリ](binary.md) を参照してください．

起動コード・UART 関数・リンカ・ACT4・Zephyr は共通定数を利用します．ただし，各リンカのセクション配置やプログラム容量制限，アセンブリの直接指定アドレス・期待値，ACT4 の Sail 用デバイス設定まで自動的に移動するわけではありません．マップ変更時はそれらも確認してください．
