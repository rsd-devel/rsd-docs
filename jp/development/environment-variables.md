# 環境変数

Dev Container は [devcontainer.json](https://github.com/rsd-devel/rsd/blob/develop/.devcontainer/devcontainer.json) に従って設定します．手動導入ではホストの配置に合わせます．`RSD_ROOT` は RSD 本体ソースのルートです．

## シミュレーションとテストのビルド

| 変数 | 意味 | コンテナ内の値 |
| --- | --- | --- |
| `RSD_ROOT` | make がソース位置から決定・export．手動設定不要 | 現在のチェックアウト |
| `RSD_GCC_PATH` | RISC-V GCC の実行ファイルのディレクトリ | `/usr/bin` |
| `RSD_GCC_PREFIX` | 末尾のハイフンを含むコンパイラ名の接頭辞 | `riscv64-unknown-elf-` |
| `RSD_VERILATOR_BIN` | Verilator 実行ファイル | `/usr/local/bin/verilator` |

接頭辞に `riscv64` が含まれていても，テストの [コンパイラ設定](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Makefile.inc) が RV32 の命令セットと `-mabi=ilp32` を指定します．picolibc も必要です．同じ配置の手動環境なら，本体ルートで次のように設定します．

```bash
export RSD_GCC_PATH=/usr/bin
export RSD_GCC_PREFIX=riscv64-unknown-elf-
export RSD_VERILATOR_BIN=/usr/local/bin/verilator
```

`RSD_VERILATOR_BIN` 未設定時は `PATH` 上の `verilator` を使用します．使用する固定版は [開発環境](environment.md) を参照してください．外部ソースは `test/External/<suite>/fetch`，依存関係は用意されている `test/External/<suite>/setup` で準備します．

## その他のシミュレータ・合成ツール

| 変数 | 用途 | 設定値 |
| --- | --- | --- |
| `RSD_QUESTASIM_PATH` | ModelSim/QuestaSim の RTL・単体テスト | `vlog`・`vsim` などのディレクトリ |
| `RSD_VIVADO_ROOT` | Vivado/XSim，FPGA ビルド | Vivado のバージョンを含むインストールディレクトリ（例: `/opt/Xilinx/Vivado/2019.2`） |
| `RSD_VITIS_ROOT` | ZedBoard の FSBL 生成 | Vitis のバージョンを含むインストールディレクトリ（例: `/opt/Xilinx/Vitis/2019.2`） |
| `RSD_DC_SHELL_BIN` | 実験的 Design Compiler 合成 | `dc_shell` のパス |

Synplify は `synplify_premier_dp` を `PATH` に置くか，make に `SYNPLIFY=/path/to/executable` を渡します．VCS は `vcs` を `PATH` に置くか `VCS=/path/to/vcs` を渡します．ツールとライセンスの設定は別途必要です．

[SetEnv.sh](https://github.com/rsd-devel/rsd/blob/master/Processor/Tools/SetEnv/SetEnv.sh) は Bash 用の手動設定テンプレートです．`Processor/Tools/SetEnv/MySetEnv.sh` にコピーして編集し，本体ルートから `source Processor/Tools/SetEnv/MySetEnv.sh` を実行します．make はこのファイルを自動では読み込みません．
