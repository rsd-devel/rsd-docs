# メモリ・マップ


## 概要

* メモリ・マップに関する情報は基本的に Memory/MemoryMapTypes.sv にて定義されている
    * アドレスのマッピングの他に，PC の初期値や IO のアドレスなども含む
* 32ビットの論理アドレスから，物理アドレスへの変換が行われる
    * 各キャッシュや LSQ ではこの物理アドレスに基づいて処理が行われる
    * 論理から物理アドレスへのマッピングは，現在は固定ルールで行われる
    * 物理アドレスは，メモリと IO で別れている（１ビットのフラグで識別）
* アドレス変換時に論理アドレスの範囲がチェックされ，無効な場合は例外が発生する
* 物理メモリの実際の容量は Src/BasicType.sv の MEMORY\_ADDR\_BIT\_SIZE によって決められる.

## アドレス・マッピング

物理アドレスは下記のように，isIO によって IO 空間とメモリ空間に分かれる

    typedef struct packed {
        logic isIO; // True if address is IO
        PhyRawAddrPath addr;
    } PhyAddrPath;

|論理アドレス                  |物理アドレス（メモリ） |内容   |
|-----------------------------|---------------------|-------|
|0x0000\_1000 ~ 0x0000\_ffff  |0x0\_1000 ~ 0x0\_ffff    |ROM    |
|0x8000\_0000 ~ 0x8003\_ffff  |0x1\_0000 ~ 0x4\_ffff    |RAM    |

|論理アドレス                  |物理アドレス（IO）     |内容   |
|-----------------------------|---------------------|-------|
|0x4000\_0000 ~ 0x4000\_000f  |0x0\_0000 ~ 0x0\_000f    |Timer  |
|0x4000\_2000 ~ 0x4000\_2000  |0x0\_2000 ~ 0x0\_2000    |UART   |


## ソフトウェア側

* Verification/TestCode/rsd-crt.s
    * スタートアップルーチン
    * main 関数に入る前にこれが実行される
    * スタックの初期値はここでレジスタに代入している
    * ローダ（Verification/TestCode/rsd-loader.c ）がここで呼ばれ，ROM にあるデータを RAM に展開する

* Verification/TestCode/rsd-ld.script
    * リンカースクリプト
    * リンク時のコードやデータのアドレス配置が定義されている

* セクションとアドレスの関係
    * 0x0000\_1000 - 0x0001\_7fff: text（コード）
    * 0x8000\_0000 - 0x8000\_7fff: data, bss（静的データ）
    * 0x8001\_8000 - 0x8002\_0000: stack 

スタートアップルーチン

	stack_top = 0x80020000
	...
	li  x29,0
	li  x30,0
	li  x31,0
	li  sp,0x80020000

リンカースクリプト

    OUTPUT_FORMAT("elf32-littleriscv");
    OUTPUT_ARCH("riscv")

    /* エントリポイント．_start は rsd-crt.s で定義 */
    ENTRY(_start);


    MEMORY {
        ROM(rxai) :     ORIGIN = 0x00001000, LENGTH = 32k
        RAM(wa) :       ORIGIN = 0x80000000, LENGTH = 32k
    }

    SECTIONS
    {
        .text : { *(.text) }     > ROM
        .rodata : { *(.rodata) } > ROM
        __rodata_end = .;
        .data : { 
        __data_start = .;
        *(.data)
        *(.sdata)
        __data_end = .;
        } > RAM  AT> ROM 
        . = ALIGN(4);
        .bss : { 
        __bss_start = .;
        *(.bss)
        *(.sbss)
        __bss_end = . ;
        } > RAM AT> ROM
        
        .comment : { *(.comment) } > ROM
    }

* symbol = .; しておくと，そのアドレスに，変数が置かれるので，C言語の方でextern int symbol; とやって &symbol を見ればそのアドレスが分かる
* "> RAM" はプログラム実行中に参照する時はRAMにあるように見える，という意味
* "AT > ROM" はELFを展開するローダはROM領域に置くようにしろということ（rsd-loaderはさらに実行時にROM領域内の静的データをRAM領域に展開する別のローダ）
  * このローダが変数を置くアドレス（LMA; Load Memory Address）は objdump でも確認できるが，readelfだと Virtual Address として表示される
  * ややこしいことに，readelf でいう Physical Address が objdump のいう Virtual Memory Address (VMA) になる


