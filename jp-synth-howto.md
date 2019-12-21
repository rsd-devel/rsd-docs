# 基本的な合成手順 (Vivado編) 
QuestaSimでのシミュレーションが終わったコードを、SynplifyとVivadoを使って合成し、FPGAに焼く手順について説明する。

## 準備
 [開発環境/ツール/Vivado](jp/開発環境/ツール/Vivado)を元に初期設定を行っておく

## 大まかな流れ

* 作成した.svソースコード群をSynplifyで合成してネットリスト(.vm)を作成する
* ネットリストを含んだシステムをVivadoで合成してBitstreamファイル(.bit)を作成する
* BitstreamファイルをFPGAボードに焼いて動作確認する

## ターゲットボードの設定

$(RSD\_ROOT)/Processor/Src/MakefileのTARGET\_BOARDに対象のボード名を設定  
(06.24.2017現在の対応ボード)

* Zedboard
* ZC706 (暫定)


## Synplifyでの合成  

Getting started か Built from scratch のどちらか1つだけで十分です

### Getting started  

* Synplifyで$(RSD\_ROOT)/Processor/Project/Synplify/proj\_1.prjを開く

* [Project Files]内の"$(TARGET\_BOARD)"を選択して[Run]でコンパイル/合成

### Build from scratch  

* プロジェクトを作成し、ソースファイルを追加
    * .svファイルを追加(Src/Verification/以下は除く)

* Implementation Options を設定
    * [FPGAの型番情報](jp-fpga-board.md)を指定
    * トップモジュールにMainを指定。モジュール・パラメータも適宜指定
    * Implementation Results タブでImplementation Nameに"$(TARGET\_BOARD)"と設定
    * Implementation Results タブでResult Base Nameに"rsd"と設定

* 画面下部のTCLコンソールで"set\_option -hdl\_define -set 適切な定義"を入力して適切なhdl\_defineを設定  
(06.12.2017現在の対応リスト)  
    * RSD\_SYNTHESIS\_ZEDBOARD ($(TARGET\_BOARD)=Zedboard)

* [Project Files]内の"$(TARGET\_BOARD)"を選択して[Run]でコンパイル/合成



## VivadoでBitstreamを生成 

* "$(RSD_ROOT)/Processor/Project/Synplify/$(TARGET\_BOARD)/"に、RSDのネットリスト (rsd.vm) ができていることを確認する．

* Cygwin上で$(RSD\_ROOT)/Processor/Srcにcdして"make vivado"でVivadoプロジェクトを開く

* 左部[Flow Navigator]→[Program and Debug]→[Generate Bitstream]をクリックしてbitstreamファイル(*.bit)を作成

### 注意

RSDのトップモジュールのIOポートを変更した場合，VivadoのBlock Design内でも修正が必要  
色々複雑なのでとりあえず今はBasecampで聞いてください...  
TODO: IOポートを変更した際のVivado上の作業手順を書く  

## BitstreamファイルをFPGAに焼いて動作確認 

### Zedboard  

* Zedboardの"PROG"ポートと"UART"ポート(どちらもmicroUSBポート)とPCをmicroUSB-USBケーブル2本で接続して電源を入れる  
※ドライバはVivadoをインストールしていれば自動で入るはず

* インストールされたUARTポートに対応するCOMポートからの入力を表示できるソフトを起動して設定しておく
    * Baud rateは115200
    * 筆者はTera Termを使用．使い方はG先生が教えてくれる．

* Vivadoのプロジェクトを開き，[メニューバー]->[File]->[Export]->[Export Hardware]をクリック

* [Include bitstream]にチェックを入れて[OK]

* Vivado上で[メニューバー]->[File]->[Launch SDK]をクリックしてSDKを起動

* Xilinx SDK上で[メニューバー]->[Xilinx Tools]->[Program FPGA]をクリック

* [Program]をクリックしてbitstreamファイルをFPGAに焼く

* [メニューバー]->[File]->[New]->[Application Project]をクリック

* [Project name]を適当に設定して[Next]をクリック

* [Available Templates]で[Hello World]を選択して[Finish]をクリック

* 完成したプロジェクトの"src"内にある"helloworld.c"を削除し，代わりに"$(RSD\_ROOT)/Processor/Project/Vivado/Zedboard/project\_src/$(適当なプログラム).c"をコピー  
※プロジェクトは"(設定した名前)"と"(設定した名前)\_bsp"の2つが出来るが，"(設定した名前)"の方  
(06.12.2017現在の対応プログラム)
    * run_simple  
        * ソースコードのprograminit()関数内に設定したプログラムをRSDに送信して実行し，結果をUARTポートに出力する

* 作成したプロジェクト上で右クリック->[Run As]->[1 Launch on Hardware (System Debugger)]をクリック

* UARTからプログラムの出力が表示されるはず

### ZC706  

* ZC706のPCIeプラケットにある"USB-to-JTAG"ポート(microUSBポート)と"USB-to-UART"ポート(miniUSBポート)とPCをminiUSB-USBケーブルとmicroUSB-USBケーブルで接続して電源を入れる  
**TODO**  
※ドライバは自動で入らない可能性があるので，調べてインストールしてここと[開発環境/fpgaボード](jp/開発環境/fpgaボード)を編集してください．

* インストールされたUARTポートに対応するCOMポートからの入力を表示できるソフトを起動して設定しておく
    * Baud rateは115200
    * 筆者はTera Termを使用．使い方はG先生が教えてくれる．

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