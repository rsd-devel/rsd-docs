# トラブルシューティング

## 環境とビルド

コンパイラやツールが見つからない場合は，[開発環境](../development/environment.md) と [環境変数](../development/environment-variables.md) を確認します．Dev Container 内の設定は自動で行われます．手動環境では `SetEnv.sh` を `MySetEnv.sh` にコピーし，編集してから読み込みます．

RTL・テストベンチの更新後はシミュレータを再ビルドします．FP などの構成変更時は [クリーンからのビルド](verilator.md) を行い，テストプログラムも同じ構成で再ビルドします．TestDriver が終了理由を取得できない場合は，古いモデルを使っていないか確認してください．

## 実行上限と結果の不一致

ログの終了理由，無コミット期間，`serial.out.txt` を確認します．`test/.../run` は `cfg.xml`，`sim/run`・`sim/kanata`・`sim/dump` は make 変数から上限を読みます．後者は期待値を比較しません．[機能シミュレーション](simulation.md) を参照してください．

外部テストのソースは `test/External/<suite>/fetch` で取得します．Zephyr と ACT4 は，その後に `test/External/Zephyr/setup` または `test/External/riscv-arch-test/setup` で依存関係を導入します．ACT4 の選択範囲と FP 設定は [テスト・プログラム](program.md) で確認します．ACT4 が失敗した場合は，該当ケースの `result.log` と UART 出力を調べてください．

## 合成・シミュレータ間の差

Verilator は 2 値シミュレーションのため，不定値の問題を調べる際は ModelSim/QuestaSim の 4 値シミュレーションも使います．RAM の入出力タイミング，初期化，クロック・リセット条件が実装と一致しているか確認してください．

Synplify では SystemVerilog として読み込んでいることと，型・インターフェースの依存順を確認します．合成後の機能検証と遅延付き検証は [合成後シミュレーション](../synthesis/post-synthesis-simulation.md) を参照してください．配置配線が完了しない場合は，資源使用量とタイミング制約を確認します．
