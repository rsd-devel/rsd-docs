# 開発ツール 導入

このページは Ubuntu 18.04・Synplify M-2017.03-SP1 を使った導入記録です．現在のシミュレーション環境は [はじめよう](jp-devel-getting-started) と [環境構築](jp-devel-environment) を参照してください．以下のインストーラ操作や回避策は，記載した旧ツールを対象としています．

このページでは、RSDの開発に使用するツールのインストール手順などの情報について記載しています。
この情報はUbuntu 18.04上でテストされたものであり、異なる環境やツールではそれに応じた変更が必要な場合があります。

## Synplify

### インストール

1. Synplify と SynopsysInstaller をダウンロード  

    例 (M-2017.03-SP1): 
    * SynopsysInstaller\_v3.4.run
    * fpga\_vM-2017.03-SP1\_common.spf
    * fpga\_vM-2017.03-SP1\_linux.spf

2. SynopsysInstallerのインストール

    ```
    # 実行権限を付加して実行
    chmod 755 SynopsysInstaller_v3.4.run 
    ./SynopsysInstaller_v3.4.run 
    ```
    
    インストール場所を聞かれるので適当に応える  
    この時に ~/ を含むパスを使用すると ~ と言う名前の  
    ディレクトリが作成されてしまうので、絶対パスで指定する  
    例: /opt/cad/synopsys/installer_v3.4  

3. Synplify のインストール

    1. SynopsysInstallerの起動
        ```
        # GUI 環境でやること
        /opt/cad/synopsys/installer_v3.4/setup.sh
        ```

    2. Site ID Number は 000 のまま
    3. 次の画面に進むとインストールパッケージ（fpga_vM-2017.03-SP1_common.spfなど）が置いてあるディレクトリを聞かれるので、そこを指定
    4. M-2017.03-SP1 を指定して、インストール先を適宜指定

### *重要*

* ubuntu の場合，以下のようなエラーがでて起動しない場合がある
    ```
    $ /opt/cad/synopsys/M-2017.03-SP1/bin/synplify_premier
    /opt/cad/synopsys/M-2017.03-SP1/bin/synplify_premier: 137: [: unexpected operator
    /opt/cad/synopsys/M-2017.03-SP1/bin/synplify_premier: 151: [: !=: argument expected
    /opt/cad/synopsys/M-2017.03-SP1/bin/synplify_premier: 320: /opt/cad/synopsys/M-2017.03-SP1/bin/config/execute: Syntax error: "(" unexpected (expecting ";;")
    ```

* この場合，Synplify の インストール先の bin/ と bin/config 以下で以下のコマンドを実行
    * 必ず bin/ をバックアップしてから実行する
    * bin/synplify_premier などが並んでいるディレクトリ
    * 各ファイルの先頭を /bin/sh から /bin/bash にする
        ```
        find . -type f -exec sed -i -e "1 s/\/bin\/sh/\/bin\/bash/g" {} \;
        ```

* 参考: [起動エラーの関連情報](https://electronics.stackexchange.com/questions/327527/lattice-icecube2-error-synplify-pro-321)
* 起動時に & を末尾に付けて GUI を起動すると、起動後のエラーもコマンドラインに出てくるので色々わかる

### その後の処理
* **ライセンスの認証に失敗する場合:**
    * ```FNP_IP_ENV``` 環境変数に1をセットしておくと認証できるようになる．（理由は以下の通り）
        * 使用しているOSのバージョンが一定より新しい場合、ライセンスの認証時にNATのIPアドレスではなく，ホストマシンのIPアドレスが送られるために認証に失敗してしまう
        * しかし、この環境変数を設定しておくと自称してるアドレスではなくサーバーから見えるアドレスを使って認証するため、認証に成功する

この認証動作の説明は当時の記録であり，他の版について再検証したものではありません．

### 簡単な使い方
適当な verilog ファイルを論理合成してその結果を GUI で確認するまでの手順
* Synplify Premier を起動
    ```
    /opt/cad/synopsys/M-2017.03-SP1/bin/synplify_premier &
    ```

* ライセンス選択画面がでるので、synplifypremier をダブルクリック
* メニューの File->New->Project File からプロジェクトファイルを作成
* 生成されたプロジェクトファイルを右クリック->Add Source File から verilog のファイルを追加
* ```rev_1``` を右クリック->Implementation Options を開く
    * Technology で Xilinx Zynq を選択して閉じる
    * Verilog タブから，必要に応じてトップレベルモジュールを指定
* 左の方にある Run ボタンを押す
* 合成成功後、```rev_1``` を右クリック->RTL View で論理合成の結果が、Technology View でターゲット FPGA 上での合成結果が視覚化できる
