# Vivado の初期設定

## インストール 

* 08.27.2022 現在，必ず Vivado 2019.2 (Vitis に入っているもの) を使ってください！ 
* それ以外では動作確認をしていないので，高確率で動きません
* また，インストール時は必ずXilinx SDKも一緒に入れること
    * インストーラーの途中でインストールする内容を設定する画面が出てくるが，SDKはデフォルトではチェックが外れていてそのままではインストールされないので注意


## 環境変数の設定  

* Processor/Tools/SetEnv 内を参考に，環境変数内のを元に初期設定を行っておく


## ModelSim 用のシミュレーションライブラリのコンパイルと設定  

* Vivado で合成したものを ModelSim を使って Post-synthesis simulation する場合，Xilinx のプリミティブモジュールライブラリを ModelSim 用にコンパイルして設定しておく必要がある(※ここでは Vivado 2016.4 と ModelSim 10.4c を前提にしている)．
* 手順
    * Vivadoを起動する．
    * メニューバーの[Tools]->[Compile Simulation Libraries...]をクリック
    * [Simulator]に "ModelSim" を設定
    * [Language]に"verilog"を設定
    * [Library]，[Family]に "All" と設定
    * [Compiled library location]にライブラリの出力先を設定
    * [Simulator executable path]に "${modelsim install path}/bin" を設定
    * [Miscellaneous option]は空欄で可
    * その他チェックボックスもチェック無しで可
    * [Compile]でコンパイル
    * [Compiled library location]で指定した出力先に出来た modelsim.ini のパスを環境変数 RSD\_MODELSIM\_INI に設定  
* 例: RSD\_MODELSIM\_INI = /PATH/TO/MODELSIM.INI/modelsim.ini

