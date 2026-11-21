# 基本的な合成手順

以下には Vivado/Vitis 2019.2 の GUI 操作が含まれます．現在のボード用 Makefile は Zedboard を対象としており，このページの実機操作は今回再検証していません．現在のビルド設定は [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefiles/Vivado.inc.mk) を参照してください．

* ZYNQ 上の ARM でベアメタルの RSD 起動用プログラムを起動し，そこから RSD を起動する方法を説明する


## 1. 準備

* [ここ](../../development/getting-started.md)を元に初期設定を行っておく
* Linux の場合の追加の準備
    * minicom のインストール（シリアルで接続可能なターミナル）
        ```bash
        sudo apt install minicom
        # dialout へユーザーを登録する必要がある
        # 追加後はログインし直すこと
        sudo usermod -aG dialout "$USER"
        ```
    * ケーブルのドライバを下記からインストールしておく
        ```
        <Vivado installation dir>/data/xicom/cable_drivers/lin64/install_script/install_drivers/install_digilent.sh
        ```
* 備考：
    * Vitis (Vivado) のバージョンを環境開発のページで指定されているものに正確にあわせることが重要！
    * 以下では 2019.2 を前提として説明する


## 2. ターゲットボードの設定

* "$(RSD\_ROOT)/Processor/Src/Makefiles/Vivado.inc.mk の TARGET\_BOARD" に対象のボード名を設定する  
* 現在の Makefile の既定値は `TARGET_BOARD=Zedboard`（大文字・小文字を区別）です


## 3. 回路の合成

Vivado のみで合成を行う方法と，Synplify を使って論理合成を行う方法の２つがある

1. Vivado のみを使う場合
    1. Vivado でソースコードから回路を合成して Bitstream ファイル(.bit)を作成する
    2. Bitstream ファイルを FPGA ボードに焼いて動作確認する
2. Synplify と Vivadoを使う場合
    1. Synplify でソースコードから回路を合成してネットリスト(.vm)を作成する
    2. ネットリストを含んだシステムを Vivado で合成して Bitstream ファイル(.bit)を作成する
    3. Bitstream ファイルを FPGA ボードに焼いて動作確認する


### 3.1. Vivado のみを使う場合の合成方法

* 以下のコマンドを実行
    ```bash
    # どちらの合成フローでも，Vivado のインストール先を指定する
    export RSD_VIVADO_ROOT=/path/to/Xilinx/Vivado/2019.2
    # Synplify で合成を行ったあとは必ず一度 clean しておく
    make synth/vivado/clean
    # 合成
    make synth/vivado/build
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
        * [FPGAの型番情報](../board.md)を指定
        * トップモジュールにMain\_Zynq\_Wrapperを指定。モジュール・パラメータも適宜指定
        * Implementation Results タブでImplementation Nameに"$(TARGET\_BOARD)"と設定
        * Implementation Results タブでResult Base Nameに"rsd"と設定
    3. 画面下部のTCLコンソールで"set\_option -hdl\_define -set 適切な定義"を入力して適切なhdl\_defineを設定  
        * `Processor/Src/Config/SynthesisMacros.sv` の現在の定義に合わせる．Zedboard 用には `RSD_SYNTHESIS_ZEDBOARD` を使う
    4. [Project Files]内の"$(TARGET\_BOARD)"を選択して[Run]でコンパイル/合成


#### Synplify で合成したネットリストから Vivado で Bitstream を生成 

1. "$(RSD_ROOT)/Processor/Project/Synplify/$(TARGET\_BOARD)/"に RSD のネットリスト (rsd.vm) ができていることを確認する．
2. $(RSD\_ROOT)/Processor/Src へ移動し，下記コマンドで Vivado プロジェクトを生成し開く
    ```bash
    # Vivado のみで合成をしていた場合は必ず vivado-clean を一度実行する
    make synth/synplify/clean
    make synth/synplify/open
    ```
3. 左部[Flow Navigator]→[Program and Debug]→[Generate Bitstream]をクリックしてbitstreamファイル(*.bit)を作成


#### 注意

* RSDのトップモジュールのIOポートを変更した場合，VivadoのBlock Design内でも修正が必要
* TODO: IOポートを変更した際のVivado上の作業手順を書く  


## 4. Bitstream ファイルを FPGA に焼いて動作確認 

### ZedBoard（2023/02/28）

1. ZedBoard の "PROG" ポートと "UART" ポート(どちらも microUSB ポート)と PC を microUSB-USB ケーブル2本で接続して電源を入れる  
    * ドライバは「1.準備」に説明されている方法に従ってあらかじめインストールしておくこと
2. インストールされた UART ポートに対応する COM ポートからの入力を表示できるソフトを起動して設定しておく
    * minicom の場合
    ```bash
    # Baud rate は 115200
    minicom -D /dev/ttyACM0 -b 115200
    ```
3. Vivado を起動
    ```
    <Vivado installation dir>/bin/vivado
    ```
4. ビットストリームをエクスポート
    * プロジェクトファイルを開く
    * [メニューバー]->[File]->[Export]->[Export Hardware] をクリック
    * [Include bitstream] にチェックを入れて [OK]
5. Vitis を起動
    * Vivado の [メニューバー]->[Tools]->[Launch Vitis]
6. ソフトウェアのプロジェクトを作成
    * ベアメタルで動かすソフトウェアの雛形を生成させる
    * [メニューバー]->[File]->[New]->[Application Project]をクリック
    * [Project name] を適当に設定して [Next] をクリック
    * デバイスのテンプレートで zed を選択
    * [Available Templates] で [Hello World] を選択して [Finish] をクリック
7. ソフトウェア書き換え
    * 完成したプロジェクトの "src" 内にある "helloworld.c" の中身を "$(RSD\_ROOT)/Processor/Project/Vivado/TargetBoards/Zedboard/project\_src/run_simple.c" の中身に書きかえる
    * run_simple.c では programinit() 関数内に設定したプログラムを RSD に送信して実行し，結果を UART ポートに出力する
8. ビルド
    * 作成したプロジェクト上で右クリック->[Build Project]をクリック
9. 作成したプロジェクト上で右クリック->[Run As]->[1 Launch on Hardware (System Debugger)]をクリック
    * "-- Initialization started" と出るのを待つ
10. FPGA に回路を焼く
    * Vitis 上で[メニューバー]->[Xilinx]->[Program FPGA]をクリック
    * ビットストリームが選択されていない場合，$(RSD\_ROOT)/Processor/Project/Vivado/TargetBoards/Zedboard/rsd/rsd.runs/impl_1/design_1_wrapper.bit を選択
11. UARTからプログラムの出力が表示されるはず

* 備考
    * ２回目以降は 8-10 だけを実行すれば良い
    * うまく行かない場合，programinit 関数内の文字列の末尾に元の文字列の倍程度の長さの文字列を追加するとなぜか動くようになることがある
