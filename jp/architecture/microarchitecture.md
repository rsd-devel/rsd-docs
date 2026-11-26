# マイクロアーキテクチャ

RSD は 32 bit RISC-V のアウト・オブ・オーダ実行スーパースカラプロセッサです．以下は既定構成です．設計の背景は [FPT 2019 論文](https://www.rsg.ci.i.u-tokyo.ac.jp/members/shioya/pdfs/Mashimo-FPT%2719.pdf) と [雷上動の設計・実装に関する論文](https://repository.dl.itc.u-tokyo.ac.jp/?action=repository_action_common_download&item_id=5849&item_no=1&attribute_id=14&file_no=1) を参照してください．

## 構成と設定箇所

数値パラメータと CPU マクロの設定元は [MicroArch.toml](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Config/MicroArch.toml) です．生成される `Config/MicroArchConf.sv` が数値定義，`Makefiles/MicroArch.inc.mk` がシミュレーション用の既定マクロ，`Config/MicroArchMacros.svh` が合成用マクロを供給します．派生パラメータは `Config/MicroArchConf.template.sv`，ツール・ボード固有の設定は `Config/SynthesisMacros.sv` にあります．

| 項目 | 既定値 |
| --- | --- |
| フェッチ幅 / コミット幅 | 各 2 命令 |
| 発行幅 | 整数 2，複雑整数 1，メモリ 2，FP 1 の計 6 |
| ActiveList（ROB） | 64 エントリ |
| 物理レジスタ | 整数・FP 各 64 |
| IssueQueue / ReplayQueue | 16 / 20 エントリ |
| LoadQueue / StoreQueue | 各 16 エントリ |
| I-cache / D-cache | 各 4 KiB，2 way，8 byte ライン |
| D-cache MSHR | 2 エントリ |

発行幅には構成上の制約があります．整数幅の変更，ロード・ストアの統合，乗除算とメモリパイプの統合，FP の有無は [ディレクティブ](../development/directive.md) を参照してください．構成変更時はシミュレータとテストプログラムを同じ設定で再ビルドします．

## ISA と検証範囲

整数 I/M/A，CSR，FENCE.I の処理が実装され，FP は `RSD_MARCH_FP_PIPE` で切り替えます．既定では FP，`RSD_ENABLE_ZBA`，`RSD_ENABLE_ZICOND`，`RSD_ENABLE_ZICFILP` が有効です．命令のデコードは [Decoder.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Decoder/Decoder.sv) を参照してください．命令アラインメントは 32 bit（IALIGN=32）です．

ACT4 は既定構成で整数・特権命令 90 ケースと F の 281 ケースを対象とします．F は FP 有効時に既定で含まれます．I/M/A，Zba，Zicond，CSR，FENCE.I，例外，M/S/U モードからの割り込み・委譲・PLIC 経由の外部割り込みを検証します．FP は全 5 丸めモードと例外フラグを検査し，基本 CSR テストが FS/SD・FP アクセス制御・dirty tracking を補います．S モードは Bare のみで，ページングと完全な S モード適合性は対象外です．

実行方法と範囲は [テスト・プログラム](../testing/program.md) と[ACT4 の説明](../testing/program.md#riscv-arch-testact4) を参照してください．この文書更新ではシミュレーションを再実行していません．

## ゼロレジスタ

整数の x0 への書き込みは Decoder の `opInfo.writeReg` を落として抑止します．[RegisterFile.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/RegisterFile/RegisterFile.sv) はリセット時に物理レジスタをゼロで初期化します．FP の f0 は通常の書き込み可能なレジスタです．

[RMT.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/RenameLogic/RMT.sv) の初期割り当ては，整数論理レジスタ番号に `SCALAR_FREE_LIST_ENTRY_NUM` を加えた物理レジスタ番号です．既定では `64 - 32 = 32` なので，x0 は物理レジスタ 32 番を読みます．書き込み先の再割り当てが行われないため，このレジスタはゼロを保持します．ソース内の古い「0 番」というコメントではなく，RMT の初期化式に従ってください．

## 例外と割り込み

デコード，整数実行，メモリ実行などで検出された例外は `execState` と関連する PC・アドレスで伝えられます．ロード・ストアに加え LR/SC・AMO のアドレス検査もあるため，旧来のロード・ストアだけのコード断片では全経路を説明できません．実装は [MemoryTagAccessStage.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Pipeline/MemoryBackEnd/MemoryTagAccessStage.sv) などを参照してください．

フォールトの基本的な流れは次のとおりです．

1. 実行結果とともに例外状態を ActiveList へ記録する．
2. コミット時に先頭の例外命令を検出する．
3. RecoveryManager が例外命令を含む後続命令を取り消し，CSR ユニットへ `triggerExcpt` を送る．
4. CSR ユニットが特権状態・委譲設定に応じて CSR を更新し，例外ハンドラへの遷移先を返す．

[CSR_Unit.sv](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Privileged/CSR_Unit.sv) は不正命令の `mtval` を 0 とします．命令ビット列を保持する方式ではありません．IALIGN=32 のため，`mepc` の読み取りと MRET が参照するアドレスの下位 2 bit はマスクされます．

割り込みは `triggerInterrupt` を使います．タイマー・ソフトウェア割り込みの CLINT，外部割り込みの PLIC と，アドレス配置は [メモリ・マップ](memory-map.md) を参照してください．
