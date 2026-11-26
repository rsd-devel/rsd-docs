# FPGA の合成後・タイミング付きシミュレーション

現在のテストターゲットは，プログラムを内部メモリの初期値として組み込んだ Zedboard 用コアを合成し，UART 出力を検証します．RTL のプログラムテストや実機用ブートイメージ生成とは別の手順です．以下は本体の Makefile に基づきます．今回の 文書更新で CAD ツールや実機を再検証したものではありません．

## 準備

Dev Container とは別に CAD ツールとライセンスを設定します．`RSD_VIVADO_ROOT` に Vivado のバージョンを含むインストールディレクトリ（例: `/opt/Xilinx/Vivado/2019.2`）を指定してください．Synplify は `synplify_premier_dp`，VCS は `vcs` を `PATH` に置くか，make に `SYNPLIFY=/path/to/executable` または `VCS=/path/to/vcs` を渡します．

RISC-V コンパイラと [環境変数](../development/environment-variables.md) を準備し，`Processor/Src` でプログラムを先にビルドします．

```bash
make test/level-1/build
```

このコマンドはプログラムをビルドするもので，Verilator のシミュレータモデルは不要です．以下のターゲットの既定プログラムは `Verification/TestCode/C/HelloWorld` です．別のプログラムを選ぶ場合も `code.hex`・`cfg.xml`・空でない `serial.ref.txt` が必要です．

## 合成後の機能検証

合成ツールに応じて，いずれかを実行します．

```bash
make synth/vivado/post-synthesis/test
make synth/synplify/post-synthesis/test
```

両方ともシミュレーションには XSim，結果検証には TestDriver を使用します．Synplify のターゲットもバッチ合成を実行するため，ボード用 `ver2017-03.prj` の手動合成とは手順が異なります．

対象プログラムはコマンドラインで指定できます．

```bash
make synth/vivado/post-synthesis/test \
    TEST_CODE=Verification/TestCode/C/HelloWorld
```

作業ディレクトリはそれぞれ `Processor/Project/PostSynthesis/vivado/<プログラム名>` と `Processor/Project/PostSynthesis/synplify/<プログラム名>` です．ここへ入力ファイルがコピーされ，`cfg.xml` の実行上限と UART の期待値を使います．詳細は [TestDriver reference](../testing/driver.md) を参照してください．

公開ターゲットは `make synth/vivado/post-synthesis/test` と `make synth/synplify/post-synthesis/test` です．本体ルートと `Processor/Src` のどちらからも実行できます．

## VCS による配置配線後のタイミング検証

```bash
make sim/vcs/post-implementation/test
```

Vivado が合成・配置配線・ネットリストと SDF の出力を行い，VCS が遅延付きシミュレーションを実行し，TestDriver が結果を検証します．生成先は `Processor/Project/PostSynthesis/vivado-timing/<プログラム名>` です．

既定値は `POST_IMPLEMENTATION_CLOCK_NS=32`，`VCS_CORNER=slow`，`VCS_DELAY=max` です．コーナーには `slow` / `fast`，遅延値には `min` / `max` を指定できます．既存ネットリストを再利用する場合は，ビルド時と同じ `TEST_CODE`・クロック設定で次を実行します．

```bash
make sim/vcs/post-implementation/run
```

HEX と合成時にコピーした内容が一致することが検査されます．HEX または RTL を変更した場合は `sim/vcs/post-implementation/test` で再合成してください．`cfg.xml` や参照出力だけを変更しても，ネットリスト内のプログラムは変わりません．

## その他のターゲットとソース追加

Vivado のプロジェクトを使う `synth/vivado/post-synthesis/timing/test`・`synth/vivado/post-implementation/test`・`synth/vivado/post-implementation/timing/test` と GUI・Kanata 用ターゲットも残っています．上記のバッチテストとは出力先やオプションが異なるため，[Makefiles/Vivado.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/Vivado.mk) を参照してください．他のフローは [Makefiles/Synplify.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/Synplify.mk) と [Makefiles/VCS.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/VCS.mk) にあります．

RTL の追加時は [CoreSources.inc.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/CoreSources.inc.mk) の一覧を更新します．

| 種類 | 変数 |
| --- | --- |
| パッケージ・型定義 | `TYPES`（依存順に配置） |
| コアのモジュール・インターフェース | `CORE_MODULES` |
| ボード用ラッパなど | `MODULES` |
| シミュレーション専用テストベンチ | `TEST_MODULES` |
| IP パッケージ用ヘッダ | `HEADERS` |

Vivado はこれらの一覧を使って検証用ネットリストを生成します．Synplify はボード合成と合成後テストの両方で `Processor/Project/Synplify/ver2017-03.prj` のソース一覧を読みます．合成対象のソースを追加するときは，このプロジェクトにもパッケージ，インターフェース，モジュールの順で登録します．

CPU 構成は `Processor/Config/MicroArch.toml` の `overrides.synthesis` を含む合成設定から生成します．合成後テストベンチも `RSD_SYNTHESIS_SRC_CFG` を使います．`RSD_SRC_CFG` のコマンドライン指定だけでは合成設定を変更できません．
