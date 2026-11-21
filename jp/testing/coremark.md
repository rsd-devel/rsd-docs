# CoreMark・Dhrystone の検証と計測

現在のシミュレーション用ベンチマークは公開リポジトリの固定リビジョンを使用します．以下はシミュレータをビルドした後，`Processor/Src` で実行します．詳細は[テスト・プログラム](program.md#coremark) を参照してください．

## ソースの取得と機能テスト

```bash
make test/External/Coremark/fetch
make test/External/Dhrystone/fetch
make test/External/Coremark/run test/External/Coremark/Coremark_for_RV32I/run
make test/External/Dhrystone/run
```

取得先は `Coremark/External` と `Dhrystone/External` です．テストターゲットが HEX と必要な参照出力をビルドします．ビルドだけ行う場合は `test/External/Coremark/build` または `test/External/Dhrystone/build` を指定します．

| テスト | 設定と検証 |
| --- | --- |
| CoreMark | RV32IM と RV32I の各版を 1 iteration 実行．CRC と UART 出力を検証 |
| Dhrystone | RV32IM の C 版を 100 iterations 実行．戻り値，最終結果，UART 出力を検証 |

いずれも FP パイプラインは不要です．通常の機能テストは合成した時刻を返すため，その時間表示から性能を求めることはできません．`test/level-2/run` がこれらをまとめて実行し，`test/all/run` にも含まれます．

## サイクル数を使う計測

```bash
make bench/Coremark/run
make bench/Dhrystone/run
make bench/Dhrystone/run DHRYSTONE_BUILTINS=0
```

`bench/*/run` は `BENCHMARK=1` でビルドし，通常の結果検証に加えて実際のサイクルカウンタを読み取ります．検証成功後に TestDriver が次の値を表示します．

| 指標 | 計算式 |
| --- | --- |
| CoreMark/MHz | `iterations * 1000000 / cycles` |
| DMIPS/MHz | `iterations * 1000000 / (cycles * 1757)` |

計測区間はベンチマークのループで，起動・初期化・結果検証・UART 出力を除き，CSR 読み取りのオーバーヘッドを含みます．既定値は CoreMark が 1 iteration，Dhrystone が 2000 iterations です．Dhrystone は `DHRYSTONE_BENCH_ITERATIONS` で変更でき，長い実行では `MAX_TEST_INSTRUCTIONS` も調整します．計測コードは64 bitの `mcycle` カウンタの下位32 bitだけを読むため，計測区間は `2^32` サイクル未満にします．

これらはリセット直後からの短時間シミュレーションによる推定値で，正式なスコア公表に必要な最低実行時間を満たすものではありません．比較時にはコンパイラ版，iteration 数，ビルド設定を記録してください．Dhrystone は既定で `DHRYSTONE_BUILTINS=1` とし，GCC による libc 関数の最適化と 8 byte の関数・ループアラインメントを使用します．この設定もスコアに影響します．

通常テストと計測モードは生成物のディレクトリを共用します．同時に実行せず，順に実行してください．モード変更は再ビルドに反映され，`test/.../run` は通常の検証モードに戻ります．`test/all/run` に `bench/*/run` は含まれません．

## クリーン

`test/External/Coremark/clean` と `test/External/Dhrystone/clean` は生成物を削除し，取得済みソースを保持します．コンパイラや通常のビルドフラグを変える場合は先にクリーンしてください．

## ZedBoard で CoreMark を実行する

[ZedBoard の起動手順](../fpga/zynq/synth-for-linux.md#ボードの起動とプログラムの実行) に従って開発ホストで `RSD_ZYNQ_HOST` を設定し，リポジトリのルートから実行します．最初の `fetch` は初回だけ必要です．

```bash
./RunContainer.sh make test/External/Coremark/fetch
./RunContainer.sh make test/External/Coremark/build
make test/External/Coremark/zynq/run
```

`zynq/run` はビルド済みの RV32IM 版をボードに転送し，UART 出力を端末に表示します．Ctrl-C でローダーを終了します．FIFO の空きを待つ方式で出力するには，FPGA のビットストリームとゲストの HEX を両方更新してください．旧版では ARM が読み出せない間に文字が欠落することがありました．ZedBoard 実機では，RV32IM 版の 1 iteration テストで，最終 CRC `0xe714` を含む UART 出力全 429 バイトが期待値と一致しました．実機でスコアを測るには，クロック周波数，計時方法，実行時間も確認してください．
