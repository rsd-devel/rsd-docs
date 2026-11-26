# コンパイラ・ディレクティブ

設定元は `Processor/Config/MicroArch.toml` です．共通値を `parameters`，モード別の差分を `overrides.simulation`・`overrides.synthesis` に記述します．

通常の make が `Config/MicroArchConf.sv`，`Config/MicroArchMacros.svh`，`Makefiles/MicroArch.inc.mk` を再生成します．これらは Git 管理される生成物です．直接編集せず TOML または `Processor/Src/Config/MicroArchConf.template.sv` を変更してください．ツール・ボード固有の設定は `Processor/Src/Config/SynthesisMacros.sv` にあります．

`RSD_SRC_CFG` はシミュレーションとソフトウェアビルドに適用され，合成用の既定値は `RSD_SYNTHESIS_SRC_CFG` と生成ヘッダに反映されます．合成後テストベンチも合成設定を使います．コマンドラインでの `RSD_SRC_CFG` 指定は合成設定を変更しません．ブール型マクロを無効化する場合は定義を省略します．`=0` で定義しても有効扱いです．

## マイクロアーキテクチャ・命令の構成

| 名前 | 意味・既定値 |
| --- | --- |
| `RSD_MARCH_INT_ISSUE_WIDTH` (`int_issue_width`) | 整数発行幅．1 または 2，既定値は 2 |
| `RSD_MARCH_FP_PIPE` (`enable_fp_pipe`) | FP パイプラインを有効にする．既定で有効 |
| `RSD_MARCH_UNIFIED_LDST_MEM_PIPE` (`enable_unified_ldst_mem_pipe`) | ロード・ストアのパイプラインを統合する．既定では未定義 |
| `RSD_MARCH_UNIFIED_MULDIV_MEM_PIPE` (`enable_unified_muldiv_mem_pipe`) | 乗除算をメモリパイプラインへ統合する．既定では未定義 |
| `RSD_ENABLE_ZBA` (`enable_zba`) | Zba 命令のデコードを有効にする．既定で有効 |
| `RSD_ENABLE_ZICOND` (`enable_zicond`) | Zicond 命令のデコードを有効にする．既定で有効 |
| `RSD_ENABLE_ZICFILP` (`enable_zicfilp`) | Zicfilp のランディングパッド保護を有効にする．既定で有効 |
| `RSD_NARROW_PC` | PC 表現の幅を縮める．`Processor/Config/MemoryMap.toml` の `memory_map.pc` から生成され，既定では無効 |

`RSD_HAS_FP` は `RSD_SRC_CFG` から求められる make 変数で，RTL のディレクティブではありません．テストの FP 選択とコンパイル対象 ISA を一致させるために使用します．FP の有無を変更した後は，シミュレータとプログラムをクリーンし，同じ構成で再ビルド・実行してください．

## ビルドの種類

| 名前 | 用途 |
| --- | --- |
| `RSD_FUNCTIONAL_SIMULATION` | シミュレーション用の処理を有効にする |
| `RSD_SYNTHESIS` | 論理合成用の処理を有効にする |
| `RSD_POST_SYNTHESIS` | 合成後テスト用ネットリストを生成する側の構成 |
| `RSD_POST_SYNTHESIS_SIMULATION` | 生成済みネットリストとテストベンチをシミュレーションする側の構成 |
| `RSD_SYNTHESIS_VIVADO` / `RSD_SYNTHESIS_SYNPLIFY` | 使用する合成ツールを選択する |
| `RSD_SYNTHESIS_ZEDBOARD` / `RSD_SYNTHESIS_ZYNQ` | Zedboard 用の設定 / Zynq 用の実装経路 |
| `RSD_SYNTHESIS_DESIGN_COMPILER` | 実験的な Design Compiler 合成 |
| `RSD_USE_EXTERNAL_MEMORY` | 外部メモリを使用する実装経路 |

これらは各 Makefile・合成スクリプトが設定します．`RSD_POST_SYNTHESIS` と `RSD_POST_SYNTHESIS_SIMULATION` は異なる段階の指定です．通常の利用では，手作業で追加せず，対応するビルドターゲットを使用します．

## デバッグ・内部制御

| 名前 | 用途 |
| --- | --- |
| `RSD_DISABLE_DEBUG_REGISTER` | デバッグ用レジスタを省略する．パイプライントレースなどに影響する |
| `RSD_DISABLE_PERFORMANCE_COUNTER` | 既定では合成時のみ定義する．`enable_performance_counter = false` にすると `Debug/PerformanceCounter.sv` のマイクロアーキテクチャ用カウンタを省略する．CSR の `mcycle` と `minstret` は利用できる |
| `RSD_STOP_FETCH_ON_PRED_MISS` | `NextPCStage.sv` の予測ミス後の待機制御．同ファイル内の定義は既定でコメントアウト |
| `RSD_ENABLE_REISSUE_ON_CACHE_MISS` | メモリアクセスの再発行に関する経路．現在は `MemoryTagAccessStage.sv` 内で定義 |

最後の 2 項目はソース内の制御で，すべてを `RSD_SRC_CFG` の任意の組み合わせとして検証しているわけではありません．
