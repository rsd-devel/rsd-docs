# QEMU でのシミュレーション

## 概要
QEMUによって,ELFファイルの正しい実行結果を得ることを目的としたシミュレーションです.  
`make dump` コマンドに倣って各命令の逐次実行時の論理レジスタのdumpを得ることができます.

## QEMUの導入
QEMUの実行はLinux上で行うことを前提としています.
2017/5/27現在で動作を確認しているのは Ubuntu 16.04 LTS です.

QEMUのバイナリは RSD-env のレポジトリの RSD-env/Tools/Emulator/QEMU/riscv-qemu.tar.gz にあります.  
/opt/ 以下に解凍してください.  
解凍後は /opt/riscv-qemu/bin というファイル階層になります.

また, QEMUでのシミュレーションには, RISCV用のGDB(riscv32-unknown-elf-gdb)が必要となります.  
普通は RISCV用のクロスコンパイラ と同じパスにあります.  


GDBを利用するにあたって, コンパイル時に -g オプションがついている必要があることに注意してください.


## QEMUシミュレーションの実行

QEMUシミュレーションで用いるMakefile, テストベンチなどは, 
機能シミュレーションやpost-synthesisシミュレーションなどに用いるものとは分離しています.

場所は RSD/Processor/Tools/QEMU_SimDriver です.

Makefile 中のQEMU Dumpの項目にある各変数の内容は以下の通りです.
シミュレーションのために変更するのは, Makefile 内の TEST\_CODE と MAX\_TEST\_CYCLES で, 他は基本的には変えなくていいです.

| QEMU\_SIM\_ELF | 実行するELFファイル(code.elf)へのパス |
| QEMU | QEMU(qemu-riscv32)へのパス |
| GDB  | RISCV用のGDB(riscv32-unknown-elf-gdb)へのパス |
| GDB\_COMMAND\_FILE | GDBの自動実行に必要なコマンドファイルへのパス |
| GDB\_COMMAND\_FILE\_GENERATOR | GDBの自動実行に必要なコマンドファイルを作成するスクリプトへのパス |
| QEMU\_LOG\_CONVERTER | GDBのログをCSV形式に変更するためのスクリプトへのパス |

上の変数を設定し終えたら  
`make qemu-dump`  
のコマンドを実行すると, Makefile と同じ階層にQEMU_register.csv というファイルが生成されます.

