# TestDriver の実行上限と結果検証

`RunTest.py` は各テストの `cfg.xml` を読みます．例:

```xml
<Config>
  <MaxTestInstructions>10000</MaxTestInstructions>
  <MaxNoCommitCycles>500</MaxNoCommitCycles>
  <RegisterValues>
    <R10>0</R10>
  </RegisterValues>
</Config>
```

- `MaxTestInstructions`: 起動コードを含むコミット済み RISC-V 命令数の上限です．最後のマイクロ命令のコミットで 1 命令と数え，投機実行やリプレイは消費しません．
- `MaxNoCommitCycles`: リセット解除後から，マイクロ命令が一つもコミットされない連続サイクル数の上限です．既定値は 500 で，超過すると失敗します．キャッシュフラッシュには大きい値が必要です．
- `EnablePC_Goal`: 既定値は `1` で，命令数上限までに終了 PC へ到達する必要があります．境界上の到達も成功です．命令数上限まで動かす継続型テストは `0` にします．
- `MaxTestCycles`: 追加のサイクル上限です．省略または 0 は無効です．命令数上限と併用して先にサイクル上限へ達すると失敗します．サイクル数だけの設定も受け付け，`EnablePC_Goal=0` の場合はサイクル上限が正常な終了条件です．

`EnableUART_Interrupts` は既定で `0` です．UART の DC1（`0x11`）/ DC3（`0x13`）でテストベンチの PLIC source 1 を assert/deassert する RTL テストだけ `1` にします．このとき制御 byte はテストベンチが消費し，他の byte は記録します．無効時はすべてを記録します．合成後シミュレーションではこのモードを拒否します．

正常終了後にレジスタとシリアルの期待値を検査します．実行だけ，またはシリアルだけの検査では `RegisterValues` を空にできます．`.txt` という拡張子でも `serial.out.txt`・`serial.ref.txt` は NUL を含む UART の生 byte です．比較は NUL を保持し，CRLF・CR を LF に揃えます．

上限の検査は 1 サイクルに 1 回なので，同時コミットにより命令数は上限を少し超える場合があります．ログには終了理由，コミット命令数・マイクロ命令数，経過サイクル，最大無コミット期間，IPC を記録します．IPC はリセット解除からのサイクル数で計算する参考値で，合否条件ではありません．

## テストの上限値

リポジトリ内の命令数上限は，実測の約 2 倍を 10,000 命令単位へ切り上げています．通常の無コミット上限は 500，`DCacheFlush` は 10,000，`ICacheFlush`・`Fence` は 5,000 です．キャッシュフラッシュ待ちの実測がそれぞれ 2,338・1,170 サイクルだったためです．FP 無効時の除算リプレイに 529 サイクル待つ例があったため，`IntDivZynq` は 1,100 としています．

テストベンチ変更後はシミュレータを再ビルドします．終了理由を報告しないモデルは拒否されます．`make sim/run`・`make sim/kanata`・`make sim/dump` は `cfg.xml` ではなく make 変数を使います．`MAX_TEST_INSTRUCTIONS`・`MAX_NO_COMMIT_CYCLES`・必要に応じて `MAX_TEST_CYCLES` を渡してください．

## XSim

最初に `make SIM=xsim sim/build` を実行します．TestDriver は `TestMain` snapshot を再利用し，実行時引数でプログラムを選びます．XSim は起動時に snapshot 内のファイルを書き換えるため，`make -j` の場合もファイルロックで XSim のプロセスを直列化します．テスト実行中に再ビルドや手動の `sim/run`・`sim/gui` を開始しないでください．

## ドライバのテスト

本体ルートから実行します．

```sh
make -C Processor/Tools/TestDriver test
```

設定生成と RunContainer ランチャも検査する場合は，Python 3.11 以上を用意して `Processor/Src` で実行します．

```sh
make -j2 test/tools/run
```

個別には `test/tools/Config/run`・`test/tools/TestDriver/run`・`test/tools/DevContainer/run` を指定します．ランチャ検査はスタブを使い，イメージのビルドやコンテナ起動は行いません．

CLI 検査はシミュレータのスタブを使用します．モデルの検査は `Processor/Src` で `make` と `make test/level-1/build` により Verilator モデル・Fibonacci HEX をビルド済みの場合に実行し，なければ skip と報告します．
