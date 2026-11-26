# 基本的な合成手順

以下には Vivado/Vitis 2019.2 の GUI 操作が含まれます．現在のボード用 Makefile は Zedboard を対象としており，このページの実機操作は今回再検証していません．現在のビルド設定は [Vivado.inc.mk](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Src/Makefiles/Vivado.inc.mk) を参照してください．

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
    # Vivado と Synplify を切り替えると，Make が IP を再登録する
    # 合成
    make synth/vivado/build
    ```
* 下記のファイルが生成されていれば成功
    ```
    Processor/Project/Vivado/TargetBoards/Zedboard/rsd/rsd.runs/impl_1/design_1_wrapper.bit
    ```
* 同じビルドで `Processor/Project/Vivado/TargetBoards/Zedboard/rsd/design_1_wrapper.xsa` も生成される

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
        * `Processor/Project/Synplify/ver2017-03.prj` と同じ合成ソースとインクルードパスを登録する．パッケージ，インターフェース，モジュールの読み込み順を保つ
    2. Implementation Options を設定
        * [FPGAの型番情報](../board.md)を指定
        * トップモジュールにMain\_Zynq\_Wrapperを指定。モジュール・パラメータも適宜指定
        * Implementation Results タブでImplementation Nameに"$(TARGET\_BOARD)"と設定
        * Implementation Results タブでResult Base Nameに"rsd"と設定
    3. ボード用の実装では Tcl コンソールで `set_option -hdl_define -set "RSD_SYNTHESIS_ZEDBOARD RSD_SYNTHESIS_SYNPLIFY"` を実行する．CPU 設定は `Processor/Config/MicroArch.toml` から生成した合成設定を使う
    4. [Project Files]内の"$(TARGET\_BOARD)"を選択して[Run]でコンパイル/合成


#### Synplify で合成したネットリストから Vivado で Bitstream を生成 

1. "$(RSD_ROOT)/Processor/Project/Synplify/$(TARGET\_BOARD)/"に RSD のネットリスト (rsd.vm) ができていることを確認する．
2. $(RSD\_ROOT)/Processor/Src へ移動し，下記コマンドで Vivado プロジェクトを生成し開く
    ```bash
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
4. GUI でビルドした場合はビットストリームを含む XSA をエクスポートする．3.1 のビルドでは `design_1_wrapper.xsa` を生成済み
    * プロジェクトファイルを開く
    * [メニューバー]->[File]->[Export]->[Export Hardware] をクリック
    * [Include bitstream] にチェックを入れて [OK]
5. Vitis を起動
    * Vivado の [メニューバー]->[Tools]->[Launch Vitis]
6. ソフトウェアのプロジェクトを作成
    * ベアメタルで動かすソフトウェアの雛形を生成させる
    * [メニューバー]->[File]->[New]->[Application Project]をクリック
    * [Project name] を適当に設定して [Next] をクリック
    * エクスポートした `design_1_wrapper.xsa` からプラットフォームを作り，`ps7_cortexa9_0` の standalone ドメインを選択
    * [Available Templates] で [Hello World] を選択して [Finish] をクリック
7. ソフトウェア書き換え
    * 完成したプロジェクトの "src" 内にある "helloworld.c" の中身を "$(RSD\_ROOT)/Processor/Project/Vivado/TargetBoards/Zedboard/project\_src/run_simple.c" の中身に書きかえる
    * run_simple.c では programinit() 関数内に設定したプログラムを RSD に送信して実行し，結果を UART ポートに出力する
8. ビルド
    * 作成したプロジェクト上で右クリック->[Build Project]をクリック
9. FPGA に回路を焼く
    * Vitis 上で[メニューバー]->[Xilinx]->[Program FPGA]をクリック
    * ビットストリームが選択されていない場合，$(RSD\_ROOT)/Processor/Project/Vivado/TargetBoards/Zedboard/rsd/rsd.runs/impl_1/design_1_wrapper.bit を選択
10. 作成したプロジェクト上で右クリック→[Run As]→[1 Launch on Hardware (System Debugger)] を選択する．UART に `-- Initialization started`，続いてプログラムの出力が表示されることを確認する

同梱の `run_simple.c` は，`programinit()` の文字列から固定長 64 KiB（16進数 131,072 桁）のイメージを読み取ります．ゲストを変更するときは所定の長さのイメージを用意するか，HEX ファイルから長さを読み取る [PS Linux のローダー](synth-for-linux.md) を使います．
