# Vivado の初期設定

現在の合成後テストの入口は [合成後・タイミング付きシミュレーション](../synthesis/post-synthesis-simulation.md) です．XSim を使う機能検証と VCS を使うタイミング検証を使用します．

## インストール 

* 既存のボード構築手順は Vivado/Vitis 2019.2 を前提にしています．本体のボードスクリプトにも 2019.2 系の指定が残っています．
* 別のバージョンでの互換性は今回確認していません


## 環境変数の設定  

* [環境変数](environment-variables.md) を参照し，`RSD_VIVADO_ROOT` などを設定します．`Processor/Tools/SetEnv` の例は実際のインストール先に合わせてください
