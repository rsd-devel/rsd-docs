# 基本的な合成手順 (Vivado編) 
QuestaSimでのシミュレーションが終わったコードを、SynplifyとVivadoを使って合成し、FPGAに焼く手順について説明する。

## 準備
 [jp devel vivado](jp-devel-vivado)を元に初期設定を行っておく

## 大まかな流れ

1. 作成した.svソースコード群をSynplifyで合成してネットリスト(.vm)を作成する
1. ネットリストを含んだシステムをVivadoで合成してBitstreamファイル(.bit)を作成する
1. BitstreamファイルをFPGAボードに焼いて動作確認する

## ターゲットボードの設定

$(RSD\_ROOT)/Processor/Src/MakefileのTARGET\_BOARDに対象のボード名を設定  
(06.24.2017現在の対応ボード)

* Zedboard
* ZC706 (暫定)


## Synplifyでの合成  

Getting started か Built from scratch のどちらか1つだけで十分です

* Getting started の手順は Synplify M-2017.03 でのみ動作確認しています．お手元のバージョンのSynplifyで正しくビルドできない場合は，Build from scratch の手順を試してみてください．

### Getting started  

1. Synplifyで$(RSD\_ROOT)/Processor/Project/Synplify/ver2017-03.prjを開く

1. [Project Files]内の"$(TARGET\_BOARD)"を選択して[Run]でコンパイル/合成

### Build from scratch  

1. プロジェクトを作成し、ソースファイルを追加
    * .svファイルを追加(Src/Verification/以下は除く)

1. Implementation Options を設定
    * [FPGAの型番情報](jp-fpga-board)を指定
    * トップモジュールにMain\_Zynq\_Wrapperを指定。モジュール・パラメータも適宜指定
    * Implementation Results タブでImplementation Nameに"$(TARGET\_BOARD)"と設定
    * Implementation Results タブでResult Base Nameに"rsd"と設定

1. 画面下部のTCLコンソールで"set\_option -hdl\_define -set 適切な定義"を入力して適切なhdl\_defineを設定  
(06.12.2017現在の対応リスト)  
    * RSD\_SYNTHESIS\_ZEDBOARD ($(TARGET\_BOARD)=Zedboard)

1. [Project Files]内の"$(TARGET\_BOARD)"を選択して[Run]でコンパイル/合成



## VivadoでBitstreamを生成 

1. "$(RSD_ROOT)/Processor/Project/Synplify/$(TARGET\_BOARD)/"に、RSDのネットリスト (rsd.vm) ができていることを確認する．

1. $(RSD\_ROOT)/Processor/Src　へ移動し，"make vivado"でVivadoプロジェクトを開く

1. 左部[Flow Navigator]→[Program and Debug]→[Generate Bitstream]をクリックしてbitstreamファイル(*.bit)を作成

### 注意

RSDのトップモジュールのIOポートを変更した場合，VivadoのBlock Design内でも修正が必要
TODO: IOポートを変更した際のVivado上の作業手順を書く  

## BitstreamファイルをFPGAに焼いて動作確認 

### Zedboard  

1. Zedboardの"PROG"ポートと"UART"ポート(どちらもmicroUSBポート)とPCをmicroUSB-USBケーブル2本で接続して電源を入れる  
※ドライバはVivadoをインストールしていれば自動で入るはず

1. インストールされたUARTポートに対応するCOMポートからの入力を表示できるソフトを起動して設定しておく
    * Tera Term や minicom など
    * Baud rateは115200

1. Vivadoのプロジェクトを開き，[メニューバー]->[File]->[Export]->[Export Hardware]をクリック

1. [Include bitstream]にチェックを入れて[OK]

1. Vivado上で[メニューバー]->[File]->[Launch SDK]をクリックしてSDKを起動

1. Xilinx SDK上で[メニューバー]->[Xilinx Tools]->[Program FPGA]をクリック

1. [Program]をクリックしてbitstreamファイルをFPGAに焼く

1. [メニューバー]->[File]->[New]->[Application Project]をクリック

1. [Project name]を適当に設定して[Next]をクリック

1. [Available Templates]で[Hello World]を選択して[Finish]をクリック

1. 完成したプロジェクトの"src"内にある"helloworld.c"を削除し，代わりに"$(RSD\_ROOT)/Processor/Project/Vivado/Zedboard/project\_src/$(適当なプログラム).c"をコピー  
※プロジェクトは"(設定した名前)"と"(設定した名前)\_bsp"の2つが出来るが，"(設定した名前)"の方  
(06.12.2017現在の対応プログラム)
    * run_simple  
        * ソースコードのprograminit()関数内に設定したプログラムをRSDに送信して実行し，結果をUARTポートに出力する

1. 作成したプロジェクト上で右クリック->[Run As]->[1 Launch on Hardware (System Debugger)]をクリック

1. UARTからプログラムの出力が表示されるはず

### ZC706  

* ZC706のPCIeプラケットにある"USB-to-JTAG"ポート(microUSBポート)と"USB-to-UART"ポート(miniUSBポート)とPCをminiUSB-USBケーブルとmicroUSB-USBケーブルで接続して電源を入れる  
**TODO**  
※ドライバは自動で入らない可能性があるので，調べてインストールしてここと[FPGAの型番情報](jp-fpga-board)を編集してください．

* インストールされたUARTポートに対応するCOMポートからの入力を表示できるソフトを起動して設定しておく
    * Tera Term や minicom など
    * Baud rateは115200

* Vivadoのプロジェクトを開き，[メニューバー]->[File]->[Export]->[Export Hardware]をクリック

* [Include bitstream]にチェックを入れて[OK]

* Vivado上で[メニューバー]->[File]->[Launch SDK]をクリックしてSDKを起動

* Xilinx SDK上で[メニューバー]->[Xilinx Tools]->[Program FPGA]をクリック

* [Program]をクリックしてbitstreamファイルをFPGAに焼く

* [メニューバー]->[File]->[New]->[Application Project]をクリック

* [Project name]を適当に設定して[Next]をクリック

* [Available Templates]で[Hello World]を選択して[Finish]をクリック

* 完成したプロジェクトの"src"内にある"helloworld.c"を削除し，代わりに"$(RSD\_ROOT)/Processor/Project/Vivado/ZC706/project\_src/$(適当なプログラム).c"をコピー  
※プロジェクトは"(設定した名前)"と"(設定した名前)\_bsp"の2つが出来るが，"(設定した名前)"の方  
(06.12.2017現在の対応プログラム)
    * run_simple  
        * ソースコードのprograminit()関数内に設定したプログラムをRSDに送信して実行し，結果をUARTポートに出力する

* 作成したプロジェクト上で右クリック->[Run As]->[1 Launch on Hardware (System Debugger)]をクリック

* UARTからプログラムの出力が表示されるはず