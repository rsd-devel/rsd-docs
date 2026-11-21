# はじめよう

RSD のシミュレータをビルドし，基本テストとパイプラインの可視化を行う手順です．コマンドは RSD 本体のチェックアウトで実行します．本体の [README](https://github.com/rsd-devel/rsd/blob/master/README.md) にも対応する手順があります．

## 1. 開発環境の準備

[環境構築](environment.md) のホスト側の手順に従って Docker と Dev Container CLI をインストールします．RSD 本体のルートで次のコマンドを実行すると，コンテナ内のシェルが開きます．

```bash
./RunContainer.sh
```

初回は開発環境をビルドします．次回以降は環境を再利用し，設定に変更があれば再ビルドします．ホスト側で `./RunContainer.sh --help` を実行すると，コマンド実行や再ビルドのオプションを確認できます．VS Code の Dev Containers 拡張から Reopen in Container を選ぶ方法もあります．

コンテナ内のツールのパスと環境変数は設定済みです．手動で環境を構築する場合は，[環境構築](environment.md) と [環境変数](environment-variables.md) を参照してください．

## 2. Verilator でビルド・テスト

コンテナ内で，RSD 本体のルートから次を実行します．

```bash
cd Processor/Src
make -j"$(nproc)"
make test/level-1/run
```

`test/level-1/run` はアセンブリ・C テストの HEX ファイルも必要に応じてビルドします．成功時には `Test Successful (test/level-1/run)` と表示されます．シミュレータ自体は先にビルドしてください．

CoreMark・Dhrystone・Zephyr・ACT4 や FP 無効構成については，[テスト・プログラム](../testing/program.md) を参照してください．

## 3. パイプラインの可視化

`test/level-1/run` の実行後，同じ `Processor/Src` で次を実行します．

```bash
make sim/kanata TEST_CODE=Verification/TestCode/C/Fibonacci
```

生成された `Processor/Src/Kanata.log` を [Konata](https://github.com/shioyadan/Konata/releases) で開きます．make のターゲット名は `sim/kanata`，ログの先頭文字は大文字の `K` です．

[機能シミュレーション](../testing/simulation.md)，[Verilator の波形出力](../testing/verilator.md)，[自作プログラムの実行](../testing/build-and-run.md) も参照してください．

## 4. 他のシミュレータ

ModelSim/QuestaSim と Vivado XSim は別途インストールし，[環境変数](environment-variables.md) を設定します．以下は `Processor/Src` で実行します．

| シミュレータ | ビルド | 基本テスト |
| --- | --- | --- |
| ModelSim/QuestaSim | `make SIM=modelsim` | `make SIM=modelsim test/level-1/run` |
| Vivado XSim | `make SIM=xsim` | `make SIM=xsim test/level-1/run` |

## 5. 合成・開発

- [Zynq ボードでの Linux 経由起動](../fpga/zynq/synth-for-linux.md)
- [合成手順](../synthesis/overview.md)
- [合成後のシミュレーション](../synthesis/post-synthesis-simulation.md)
- [コーディング規約](coding-convention.md)
- [リポジトリの更新規約](repository-convention.md)

[ビルドの入口と Makefile の構成](build.md) に，ターゲットの階層・設定生成・共通ファイルの役割をまとめています．
