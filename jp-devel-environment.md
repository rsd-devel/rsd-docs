# 開発環境

シミュレーション環境の定義は本体の [Dockerfile](https://github.com/rsd-devel/rsd/blob/master/.devcontainer/Dockerfile)，[コンテナ設定](https://github.com/rsd-devel/rsd/blob/master/.devcontainer/devcontainer.json) にあります．リンクは master の最新版を指します．

## Dev Container

本体の [README](https://github.com/rsd-devel/rsd/blob/master/README.md) は新しい Ubuntu 24.04 ホスト向けに次の導入手順を示しています．Docker が設定済みなら，そのインストールとグループ設定は省略してください．

```bash
sudo apt update
sudo apt install -y docker.io docker-buildx python3 build-essential nodejs npm
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
sudo npm install -g @devcontainers/cli@0.83.3
```

Docker グループ設定を反映するためログインし直し，RSD 本体のルートで実行します．

```bash
./RunContainer.sh
```

ホスト OS とコンテナ OS は別です．コンテナは Ubuntu 26.04 を使用し，以下を含みます．

| 要素 | 構成 |
| --- | --- |
| Verilator | 固定リリース 5.054，timing 対応でビルド |
| RISC-V コンパイラ | Ubuntu の `gcc-riscv64-unknown-elf` と binutils．Makefile が RV32・`ilp32` を指定 |
| C ライブラリ | `picolibc-riscv64-unknown-elf` |
| Python | Python 3.11 以上の標準 tomllib．外部テストの依存関係は各 setup で導入 |
| Zephyr 用ツール | CMake，Ninja，gperf，device-tree compiler |
| ACT4 用ツール | Ruby，LLVM/Clang/LLD 22．個別依存関係は setup ターゲットで導入 |

[はじめよう](jp-devel-getting-started) に従ってシミュレータをビルドし，テストします．ベンチマークや拡張テストは個別の取得・セットアップが必要です．[テスト・プログラム](jp-test-program) を参照してください．

## 手動導入

Dockerfile の OS・パッケージ・固定ツールのビルド手順を基準とします．Python 3.11 以上を用意し，[環境変数](jp-devel-environment-variables) をホストに合わせて設定します．Verilator は共通の SystemVerilog `TestMain` と `--main`・`--timing` を使用します．再現時には指定のツール版を使ってください．

## 別途導入する CAD ツール

ライセンスが必要なシミュレータ・合成ツールは Dev Container に含まれません．ツールとライセンスを別途設定してください．

| 用途 | ツール・入口 |
| --- | --- |
| RTL シミュレーション・単体テスト | ModelSim/QuestaSim，`make SIM=modelsim` / `make SIM=modelsim test/unit/run` |
| XSim による RTL シミュレーション | Vivado，`make SIM=xsim` |
| Zedboard の実装 | Vivado/Vitis，必要に応じ Synplify |
| 合成後の機能検証 | Vivado + XSim または Synplify + XSim |
| 配置配線後のタイミング検証 | Vivado + VCS，`make sim/vcs/post-implementation/test` |
| 実験的 ASIC 合成 | Design Compiler，`Processor/Project/DesignCompiler` |

既存の設定例には QuestaSim 2019.4.2，Vivado/Vitis 2019.2，Synplify M-2017.03-SP1，Design Compiler O-2018.06-SP4 が記載されています．これは新たな互換性検証ではありません．ボードスクリプトも Xilinx 2019.2 系ソースを参照しており，今回の Wiki 更新で新しい CAD 版への対応を確認してはいません．

FPGA は [Zynq ボード手順](jp-fpga-zynq-synth-for-linux) と [合成後シミュレーション](jp-synth-simulation) を参照してください．ボード構築にはコンテナ以外のホストパッケージが必要な場合があります．

## 結果の表示

[Konata](https://github.com/shioyadan/Konata/releases) で `Kanata.log` を開きます．Verilator の `sim/dump` は `simx.vcd` も生成し，GTKWave などで表示できます．[Verilator の説明](jp-test-verilator) を参照してください．
