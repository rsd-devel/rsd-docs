# RSDのバイナリ

このドキュメントでは，RSDのバイナリに関する様々な情報について説明します．

## バイナリフォーマット

RSDはバイナリに一般的なelfファイルではなくhex形式のメモリイメージを使用します．
これは，elfファイルを直接メモリに展開するプログラムローダーが存在しないためです．

hex形式メモリイメージは，1行あたり16Bのhex値を持ち，1行目から順にLMA(Load Memory Address) 0x0以降にロードされるフォーマットで作成されます．
1行あたりのデータ量が16Bである理由は，このメモリイメージがシミュレーション時に直接ロードされる[メインメモリ](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Memory/Memory.sv)のデータアレイの幅が16Bで，それに合わせるためです．

## コンパイルフロー

RSDのバイナリ生成は以下のフローでソースコードをhex形式のメモリイメージにすることを意味します．
1. gccとldを用いてソースコードからelfファイル(code.elf)を生成
2. objcopyを用いてelfファイルからバイナリのメモリイメージ(code.bin)を生成
3. [Pythonスクリプト](https://github.com/rsd-devel/rsd/blob/master/Processor/Tools/TestDriver/BinaryToHex.py)を用いてcode.binからhex形式のメモリイメージ(code.hex)を生成  

詳細は[Makefile(Asmプログラム用)](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Asm/Makefile)および[Makefile(Cプログラム用)](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/C/BuildC.inc.mk)を参照してください．

## バイナリの構成

バイナリの構成は[リンカースクリプト](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/rsd-ld.script)に定義されています．

バイナリは.textや.dataなど複数のセクションから構成され，それぞれがVMA(Virtual Memory Address)空間の特定の領域にマップされます．
RSDのVMA空間にはROM領域とRAM領域があり，バイナリの.textセクションなどの読み出し専用セクションはROM領域に，.dataなどの読み書きセクションはRAM領域に割り当てられます．
具体的なVMA空間のアドレスと領域，割り当てられるセクションの関係は以下の通りです．

|Virtual Address              |内容   |割り当てられるセクション    |
|-----------------------------|-------|-----------------------|
|0x0000\_1000 ~ 0x0000\_FFFF  |ROM    | .text, .rodata, .srodata |
|0x8000\_0000 ~ 0x8003\_FFFF  |RAM    | .data, .bss             |

## バイナリのロード

バイナリのすべてのセクションは，まず始めにRSD外のプログラムローダーによってROM領域にロードされます．
つまり，VMA空間ではRAM領域に割り当てられた.dataセクションなどもすべてROM領域にロードされます．
ここで各セクションがROM領域にロードされる際のアドレスをLMA(Load Memory Address)と呼びます．
RSD外部のプログラムローダーの実装は，RSDの動作環境ごとに以下の通りです．
|動作環境|プログラムローダー|
|-------|-----------------|
|QuestaSim|[SystemVerilog test bench code](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestMain.sv) initializes the ROM using $readmemh|
|Verilator|[C++ test bench code](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/SysDeps/Verilator/TestMain.cpp) directly initializes the ROM|
|Vivado(Functional)|[SystemVerilog test bench code](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestMain.sv) initializes the ROM using $readmemh|
|Vivado(Post-synthesis)|Vivado synthesizes the ROM with a code.hex using $readmemh|
|Xilinx Zynq FPGA|[C++ loader](https://github.com/rsd-devel/rsd/blob/master/Processor/Project/Vivado/ARM_Linux/ProgramLoader/loader.c) on ARM host processor loads a code.hex|

この仕様によりRAM領域に割り当てられたセクションはVMA≠LMAとなるため，バイナリがロードされた後にROM領域からRAM領域へのコピーが必要になります．
具体的には，RSDはmain関数に入る前のスタートアップルーチンで.dataセクションをROM領域からRAM領域にコピーし，.bssセクションが割り当てられたRAM領域を初期化します．
このコピー操作の実装は[このファイル](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/rsd-loader.c)にあります．
一方，ROM領域に割り当てられるセクション(.textなど)はVMA=LMAとなるように設定されるため，コピーなどは不要です．

まとめると，RSDの起動時のバイナリ(code.hex)のロードは以下のフローで行われます．
1. RSD外部のプログラムローダーがcode.hexをLMAで設定されたROM領域に展開しRSDをリセット
2. RSDがcode.hex内のスタートアップルーチンで.dataセクションをLMAで設定されたROM領域からVMAで設定されたRAM領域にコピー
3. RSDが同スタートアップルーチンで.bssセクションのVMAで設定されたRAM領域を初期化
3. RSDがmain関数へジャンプしてプログラム実行スタート
