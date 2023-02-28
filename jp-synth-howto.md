# 基本的な合成手順

* ここでは論理シミュレーションにより検証が終わったコードを合成し，Zynq FPGA 上で動かす手順について説明する
* RSD を Zynq FPGA 用に合成する方法には以下の２つがある
    1. Zynq 上の ARM Linux を介して RSD を起動する方法
        * [こちら](jp-fpga-zynq-build-linux-simple) を参照
        * **こちらの方が色々らくなので，基本的には上記リンク先の方法を推奨する**
    2. ARM Linux を介さず直接 RSD を起動する方法
        * 本ページではこの Linux を介さない方法を説明する
        * Linux のセットアップを行いたくない場合などはこちらを使用する

## 1. 準備

* [ここ](jp-devel-getting-started)を元に初期設定を行っておく
* Linux の場合の追加の準備
    * minicom のインストール（シリアルで接続可能なターミナル）
        ```
        sudo apt install minicom
        ```
    * ケーブルのドライバを下記からインストールしておく
        ```
        <Vivado installation dir>/data/xicom/cable_drivers/lin64/install_script/install_drivers/install_digilent.sh
        ```
* 備考：
    * Vitis (Vivado) のバージョンを環境開発のページで指定されているものに正確にあわせることが重要！
    * 以下では 2019.02 を前提として説明する


## 2. ターゲットボードの設定

* "$(RSD\_ROOT)/Processor/Src/Makefiles/Vivado.inc.mk の TARGET\_BOARD" に対象のボード名を設定する  
* (09.05.2022 現在の対応ボード)
    * ZedBoard（デフォルト）
    * ZC706 (09.05.2022 現在メンテナンスされていない)

## 3. 回路の合成

Vivado のみで合成を行う方法と，Synplify を使って論理合成を行う方法の２つがある

1. Vivado のみを使う場合
    1. Vivado でソースコードから回路を合成して Bitstream ファイル(.bit)を作成する
    3. Bitstream ファイルを FPGA ボードに焼いて動作確認する
2. Synplify と Vivadoを使う場合
    1. Synplify でソースコードから回路を合成してネットリスト(.vm)を作成する
    2. ネットリストを含んだシステムを Vivado で合成して Bitstream ファイル(.bit)を作成する
    3. Bitstream ファイルを FPGA ボードに焼いて動作確認する


### 3.1. Vivado のみを使う場合の合成方法

* 以下のコマンドを実行
    ```bash
    # Vitis と Vivado の環境変数の設定
    # パスは Vitis なので注意
    source /<path_of_Xilinx>/Vitis/2019.2/settings64.sh
    # 合成
    make -f Makefile.vivado.mk vivado-synthesis
    ```
* 下記のファイルが生成されていれば成功
    ```
    $(RSD\_ROOT)/Processor/Project/Vivado/TargetBoards/Zedboard/rsd/rsd.runs/impl_1/design_1_wrapper.bit
    ```

### 3.2. Synplify と Vivadoを使う場合の合成方法

#### Synplify によるネットリストの合成

* 以下で説明する A. Getting started か B. Built from scratch のどちらか片方を行ってください
    * Getting started の手順は Synplify M-2017.03 でのみ動作確認しています
    * お手元のバージョンのSynplifyで正しくビルドできない場合は，Build from scratch の手順を試してみてください
* A. Getting started  
    1. Synplifyで$(RSD\_ROOT)/Processor/Project/Synplify/ver2017-03.prjを開く
    2. [Project Files]内の"$(TARGET\_BOARD)"を選択して[Run]でコンパイル/合成
* B. Build from scratch  
    1. プロジェクトを作成し、ソースファイルを追加
        * .svファイルを追加(Src/Verification/以下は除く)
    2. Implementation Options を設定
        * [FPGAの型番情報](jp-fpga-board)を指定
        * トップモジュールにMain\_Zynq\_Wrapperを指定。モジュール・パラメータも適宜指定
        * Implementation Results タブでImplementation Nameに"$(TARGET\_BOARD)"と設定
        * Implementation Results タブでResult Base Nameに"rsd"と設定
    3. 画面下部のTCLコンソールで"set\_option -hdl\_define -set 適切な定義"を入力して適切なhdl\_defineを設定  
        * (06.12.2017現在の対応リスト)  
            * RSD\_SYNTHESIS\_ZedBoard ($(TARGET\_BOARD)=ZedBoard)
    4. [Project Files]内の"$(TARGET\_BOARD)"を選択して[Run]でコンパイル/合成


#### Synplify で合成したネットリストから Vivado で Bitstream を生成 

1. "$(RSD_ROOT)/Processor/Project/Synplify/$(TARGET\_BOARD)/"に、RSDのネットリスト (rsd.vm) ができていることを確認する．
2. $(RSD\_ROOT)/Processor/Src　へ移動し，下記コマンドで Vivado プロジェクトを生成し開く
    ```make -f Makefile.vivado.mk vivado```
3. 左部[Flow Navigator]→[Program and Debug]→[Generate Bitstream]をクリックしてbitstreamファイル(*.bit)を作成


#### 注意

* RSDのトップモジュールのIOポートを変更した場合，VivadoのBlock Design内でも修正が必要
* TODO: IOポートを変更した際のVivado上の作業手順を書く  


## 4. Bitstream ファイルを FPGA に焼いて動作確認 

### ZedBoard  

1. ZedBoard の "PROG" ポートと "UART" ポート(どちらもmicroUSBポート)と PC を microUSB-USB ケーブル2本で接続して電源を入れる  
    * ドライバは「1.準備」に説明されている方法に従ってあらかじめインストールしておくこと
2. インストールされた UART ポートに対応する COM ポートからの入力を表示できるソフトを起動して設定しておく
    * Tera Term や minicom など
    * Baud rate は 115200
3. Vivado を起動
    * プロジェクトファイルを開く
    * [メニューバー]->[File]->[Export]->[Export Hardware]をクリック


### ZedBoard (古い方法)


1. ZedBoard の "PROG" ポートと "UART" ポート(どちらもmicroUSBポート)と PC を microUSB-USB ケーブル2本で接続して電源を入れる  
    * ※ドライバはVivadoをインストールしていれば自動で入るはず
2. インストールされた UART ポートに対応する COM ポートからの入力を表示できるソフトを起動して設定しておく
    * Tera Term や minicom など
    * Baud rate は 115200
3. Vivadoのプロジェクトを開き，[メニューバー]->[File]->[Export]->[Export Hardware]をクリック
4. [Include bitstream]にチェックを入れて[OK]
5. Vivado上で[メニューバー]->[File]->[Launch SDK]をクリックしてSDKを起動
6. Xilinx SDK上で[メニューバー]->[Xilinx Tools]->[Program FPGA]をクリック
7. [Program]をクリックしてbitstreamファイルをFPGAに焼く
8. [メニューバー]->[File]->[New]->[Application Project]をクリック
9. [Project name]を適当に設定して[Next]をクリック
10. [Available Templates]で[Hello World]を選択して[Finish]をクリック
11. 完成したプロジェクトの"src"内にある"helloworld.c"を削除し，代わりに"$(RSD\_ROOT)/Processor/Project/Vivado/ZedBoard/project\_src/$(適当なプログラム).c"をコピー  
※プロジェクトは"(設定した名前)"と"(設定した名前)\_bsp"の2つが出来るが，"(設定した名前)"の方  
(06.12.2017現在の対応プログラム)
    * run_simple  
        * ソースコードの programinit() 関数内に設定したプログラムをRSDに送信して実行し，結果をUARTポートに出力する
12. 作成したプロジェクト上で右クリック->[Run As]->[1 Launch on Hardware (System Debugger)]をクリック
13. UARTからプログラムの出力が表示されるはず

### ZC706  

* ZC706のPCIeプラケットにある "USB-to-JTAG" ポート(microUSBポート)と"USB-to-UART"ポート(miniUSBポート)とPCをminiUSB-USBケーブルとmicroUSB-USBケーブルで接続して電源を入れる  
    * **TODO**  
    * ※ドライバは自動で入らない可能性があるので，調べてインストールしてここと[FPGAの型番情報](jp-fpga-board)を編集してください．
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
    * ※プロジェクトは"(設定した名前)"と"(設定した名前)\_bsp"の2つが出来るが，"(設定した名前)"の方  
    * (06.12.2017現在の対応プログラム)
        * run_simple  
            * ソースコードの programinit() 関数内に設定したプログラムをRSDに送信して実行し，結果をUARTポートに出力する
* 作成したプロジェクト上で右クリック->[Run As]->[1 Launch on Hardware (System Debugger)]をクリック
* UARTからプログラムの出力が表示されるはず
