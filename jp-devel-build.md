# ビルドの入口と Makefile の構成

本体ルートの `Makefile` は `Processor/Src/Makefile` へのシンボリックリンクです．`Processor/Src` 以外から実行すると，同ディレクトリへターゲット・変数・並列ジョブを引き継いで処理を転送します．両方のディレクトリで通常の make とターゲット補完が使えます．`TEST_CODE` などの相対パスは `Processor/Src` を基準に解決します．

```sh
make -j8                             # Same as sim/build; Verilator by default
make test/C/HelloWorld/run           # Build the program, run and check results
make test/level-1/run
make SIM=modelsim sim/build          # ModelSim/QuestaSim
make SIM=xsim sim/build              # XSim
make SIM=xsim test/level-1/run
make test/unit/run                      # Verilator RTL unit tests
make SIM=modelsim test/unit/run          # ModelSim/QuestaSim RTL unit tests
make synth/vivado/build              # Board synthesis through bitstream generation
make synth/vivado/post-synthesis/test # Vivado + XSim functional test
make synth/synplify/post-synthesis/test # Synplify + XSim functional test
make sim/vcs/post-implementation/test # Vivado implementation + VCS timing test
```

RTL のバックエンド `VerilatorCore.inc.mk`・`ModelSimCore.inc.mk`・`XSimCore.inc.mk` は共通 Makefile が読み込み，`SIM` で選択します．単体テストは `Makefiles/UnitTest.inc.mk` を共有します．VCS は配置配線後のタイミング検証用で，`SIM=vcs` の RTL バックエンドはありません．準備とテスト方法は [テスト・プログラム](jp-test-program) を参照してください．

## 公開ターゲット

公開ターゲットは `sim/`・`synth/`・`test/`・`bench/`・`platform/` に分かれます．テストは `test/level-1/build`，`test/level-1/run`，`test/External/Coremark/build` のように末尾が操作名です．`External` は Coremark・Dhrystone・Zephyr・riscv-arch-test をまとめる名前であり，ソースの保存場所は変わりません．シミュレータの `test/.../run` は結果を自動照合し，`bench/Coremark/run`・`bench/Dhrystone/run` はスコアを計測します．HelloWorld と CoreMark の `test/.../zynq/run` はビルド済みの HEX を実機で実行し，UART 出力を端末に表示します．

通常の Bash 補完は `/` ごとに階層を表示し，専用補完スクリプトは不要です．`make`・`make all` は `sim/build`，`make clean` は `sim/clean` の短縮形です．`test/level-1/run`・`test/level-2/run`・`test/ex/run`・`test/all/run` は従来と同じテスト群を実行します．`test/all/run` は level-1 と level-2 だけを含みます．

`EDA.inc.mk` が EDA・プラットフォーム操作を個別のツール用 submake へ転送し，コマンドライン変数と並列ジョブ数を保持します．バックエンドの `Vivado.mk`・`Synplify.mk`・`VCS.mk` は `Processor/Src` から `make -f Makefiles/<tool>.mk` で直接呼ぶこともできます．読み込み専用のファイルは `.inc.mk` という名前です．

`synth/vivado/build`・`synth/synplify/build` はボードの実装と bitstream 生成を含みます．後者は別途用意した Synplify のボード用ネットリストが必要です．合成後の `build`・`test` は検証用ネットリストを自動生成します．`sim/vcs/post-implementation/run` は配置配線済みネットリストを再利用し，`test` はその生成も行います．ARM Linux の操作は `platform/zynq/` にあります．Linux/rootfs は Dev Container 内の Buildroot，ハードウェアはホストの Vivado/Vitis で生成します．SD 書き込みもホストで行います．[ZedBoard の構築手順](jp-fpga-zynq-synth-for-linux) を参照してください．

## 共有ファイル

- `CoreSources.inc.mk`: ソース・構成の一覧です．sv-tests が make を評価せず `TYPES` と `CORE_MODULES` を直接解析するため，パス・変数名・リテラルのファイル一覧・継続行・順序を保ちます．
- `GenerateConfig.inc.mk`: `Processor/Config/MemoryMap.toml` と `Processor/Config/MicroArch.toml` を入力に，RTL とソフトウェア用の定義を生成する規則です．生成される `MicroArch.inc.mk` が CPU マクロの既定値，`Config/MicroArchMacros.svh` が合成マクロを供給します．RTL 定義・テンプレート・合成設定は `Src/Config/`，編集する TOML は `Processor/Config/` にあります．`overrides.simulation`・`overrides.synthesis` が共通値を上書きし，合成後テストベンチは `RSD_SYNTHESIS_SRC_CFG` で合成側と一致させます．
- `Build.inc.mk`: シミュレーション・合成で共有する RTL 生成と依存関係です．
- 共通 `Makefile`: シミュレータ選択，手動実行の引数，TestDriver 呼び出し，単体テストの集約です．単体テストは `SIM` に従い，`UNIT_SIM` で独立指定もできます．
- `TestCommands.inc.mk`: プログラムのビルド，テスト群，ツール検査です．
- `UnitTest.inc.mk`: 単体テストのシミュレータ選択・ビルド・実行です．
- `Verilator.inc.mk`・`ModelSim.inc.mk`: コアと単体テストで共有するツール設定です．
- `PostSynthesis.inc.mk`: Vivado/Synplify の XSim 機能検証です．各バックエンドがネットリストと定義を渡します．
- `Vivado.inc.mk`: ボード実装と PS Linux ビルドの共通規則です．

ツール固有の設定と出力先は各バックエンドにあり，プログラムと単体テストは個別の Makefile を持ちます．通常の生成物は `Processor/Project` 配下，構成の生成定義はソースの横に保存して外部利用のため Git に含めます．Verilator の単体テストは `Verilator/UnitTest/<unit>`，ModelSim は `ModelSim/<unit>` に出力します．

## 環境の初期化

Dev Container は環境を設定済みです．手動導入では [SetEnv.sh](https://github.com/rsd-devel/rsd/blob/master/Processor/Tools/SetEnv/SetEnv.sh) をコピー・編集し，`MySetEnv.sh` を読み込みます．`RSD_ROOT` は Makefile の位置から求めて export し，手動設定は不要です．プログラムには `RSD_GCC_PATH`・`RSD_GCC_PREFIX`，ModelSim/QuestaSim には `RSD_QUESTASIM_PATH`，Vivado/XSim には `RSD_VIVADO_ROOT` が必要です．Verilator・Synplify・VCS は PATH 上のコマンドを使用できます．

RTL/EDA と外部テストの入口は最初に `Environment.inc.mk` を読みます．通常のプログラムは共通の `TestCode/Makefile.inc`（`BuildC.inc.mk` も使用）で初期化するため，個別 Makefile に追加設定は不要です．構成生成規則は初期化済みの環境を使います．make の問い合わせモードでは環境検査を省略するので，未設定でも補完が動作します．
