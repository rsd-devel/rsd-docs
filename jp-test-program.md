# テスト・プログラム

以下は `Processor/Src` で実行します．プログラムの検証では，先に Verilator シミュレータをビルドしてから基本テストを実行します．

```sh
make -j"$(nproc)"
make test/level-1/run
```

`test/level-1/run` は必要な ASM/C の HEX もビルドします．`test/level-1/clean` は生成物を削除します．個別ケースはソースの配置に対応し，たとえば `test/Asm/FP/run`・`test/C/HelloWorld/run`，ソース群のビルドは `test/Asm/build`・`test/C/build` です．

ビルド用ツールの検査は再ビルドが必要なときに行うため，最新の生成物はクロスコンパイラや外部テスト用ビルド環境なしでも再利用できます．ただし，ソースと中間ファイルは保持してください．HEX だけをコピーしても make の依存関係は保たれません．入力変更後はビルド用ツールが必要です．`cfg.xml`・実行上限・結果比較は [TestDriver](jp-test-driver) を参照してください．

## テスト群の選択

| ターゲット | 対象 | 準備 |
| --- | --- | --- |
| `test/all/run` | level-1（ASM/C）と level-2（CoreMark/Dhrystone） | モデルのビルド，ベンチマーク取得 |
| `test/ex/run` | ACT4 と Zephyr | モデルのビルド，各スイートの fetch/setup |
| `test/unit/run` | RAM，キューポインタ，free list，除算，メモリ，キャッシュなどの RTL 単体テスト | Dev Container の Verilator または別途設定した ModelSim/QuestaSim |
| `test/tools/run` | 設定生成，TestDriver，RunContainer ランチャ | Dev Container または Python 3.11 以上・Bash・flock のある Linux |

```sh
make -j4 test/all/run
make -j4 test/ex/run
make -j4 test/unit/run
make -j2 test/tools/run
```

`test/all/run` は通常プログラムテストのみです．拡張テストも行う場合は `test/all/run test/ex/run` を同時指定します．これらは HEX を必要に応じてビルドします．`test/all/build` は通常テスト，`test/level-1/build` は ASM/C，`test/level-2/build` は CoreMark/Dhrystone，`test/ex/build` は ACT4/Zephyr をビルドします．`test/clean` は通常・拡張の生成物を削除し，取得ソースと導入済み依存関係は保持します．

既定のコアシミュレータは Verilator です．別のシミュレータはビルドとテストの両方に `SIM=modelsim` または `SIM=xsim` を指定します．単体テストは独自のモデルをビルド・実行し，Verilator と ModelSim/QuestaSim に対応します．後者は `RSD_QUESTASIM_PATH` を設定し `make SIM=modelsim test/unit/run` とします．`UNIT_SIM` で独立選択もでき，たとえば `make SIM=xsim UNIT_SIM=verilator test/unit/run` と指定します．出力先は `UNIT_PROJECT_WORK` で上書きできます．ModelSim/QuestaSim は Verilator の2値シミュレーションでは扱えない X も検査します．個別指定は `make test/unit/Divider/run` です．

`test/tools/run` は構成生成（`test/tools/Config/run`）を含み，ランチャと runner CLI はスタブで検査します．モデルと Fibonacci HEX がある場合は実行上限のモデル検査も行い，なければ skip と報告します．モデルのビルド・ツール取得・コンテナ起動は行いません．個別ターゲットは [TestDriver](jp-test-driver) を参照してください．

合成後の検証は先に `make test/level-1/build` などで HEX をビルドします．`make synth/vivado/post-synthesis/test` は Vivado + XSim，`make synth/synplify/post-synthesis/test` は Synplify + XSim，`make sim/vcs/post-implementation/test` は Vivado の配置配線と SDF を用いた VCS 検証です．CAD ツールと `RSD_VIVADO_BIN` の設定が必要で，既定の HelloWorld 以外は `TEST_CODE` で UART 検証対象を指定できます．上記4群とは別のターゲットです．

TestDriver のログと UART 出力は各テストディレクトリに残ります．ACT4 は選択ケースの集計を `riscv-arch-test/Build/summary.log` に出力します．スコアは以下の `bench/*/run` で計測します．

## FP テストの選択

[MicroArch.toml](https://github.com/rsd-devel/rsd/blob/master/Processor/Config/MicroArch.toml) の `enable_fp_pipe = true` で基本テストの ASM/C の FP ケースが有効になります．`false` では FP を省き，コンパイル対象も rv32imaf から rv32ima へ変わります．FP 無効時の明示的な FP テストは失敗します．構成変更時は `make clean test/level-1/clean` でモデルとプログラムを消し，同じ構成の `RSD_SRC_CFG` で再ビルド・実行します．

## CFI テストの選択

同じ TOML の `enable_zicfilp = true` がランディングパッド保護と対応する level-1 テストを有効にします．`false` で CFI を無効にすると，明示的な `test/Asm/LandingPad/run` は失敗します．FP と同じくモデルと基本プログラムをクリーンして再ビルドします．TOML は合成マクロも生成します．コマンドラインの `RSD_SRC_CFG` はシミュレーションとソフトウェアだけを変更します．マクロは `=0` で定義しても有効なので，無効にする場合は定義を省きます．

## CoreMark

```sh
make test/External/Coremark/fetch
make -j"$(nproc)" test/External/Coremark/build
make test/External/Coremark/run test/External/Coremark/Coremark_for_RV32I/run
```

[Coremark/Makefile](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Coremark/Makefile) に固定された eembc/coremark のコミットを `Coremark/External/` へ取得します．ビルドはネットワークにアクセスせず，テストが HEX とシリアル期待値も必要に応じて生成します．RV32IM と RV32I は起動コードを含むオブジェクトを分離し，それぞれ対応する GCC ランタイムを選びます．どちらも FP パイプラインは不要です．

機能検証は 1 iteration で，従来の合成した 10 tick を返すため表示時間は性能値ではありません．固定の CRC と完全なシリアル出力を比較し，参照出力中のコンパイラ版だけをビルド時に埋めます．命令数上限は実測のおよそ2倍，無コミット上限は500です．`test/External/Coremark/clean` は生成物を削除し，External とテスト設定を保持します．コンパイラやビルドフラグを変更する前にクリーンしてください．

## Dhrystone

```sh
make test/External/Dhrystone/fetch
make -j"$(nproc)" test/External/Dhrystone/build
make test/External/Dhrystone/run
```

[SiFive の Dhrystone C 2.1](https://github.com/sifive/benchmark-dhrystone) を [Dhrystone/Makefile](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Dhrystone/Makefile) の固定コミットで `Dhrystone/External/` へ取得します．ビルドにネットワークは不要で，テストは HEX も必要に応じて生成します．

取得ソースにパッチを加えず100 iterations実行します．専用の malloc・time・printf が2つの固定レコード，合成したゼロ時間，最終結果の検証を提供します．6つのローカル値は元の最終レポート経由，グローバル値は直接比較し，文字列は全体を比較します．ローカル結果の出力がない場合も失敗です．RV32IM の機能テストで，タイミングスコアや FP パイプラインは不要です．戻り値0と完全な UART 参照出力の一致を要求します．命令数上限は実測のおよそ2倍，無コミット上限は500です．

GCC の libc builtin は既定で有効です．無効化する例:

```sh
make test/External/Dhrystone/run DHRYSTONE_BUILTINS=0
```

既定の `DHRYSTONE_BUILTINS=1` は共有 freestanding フラグの後に `-fbuiltin` を追加し，RV32IM bare-metal と分割コンパイルを保ちます．GCC は定数サイズの文字列・メモリ操作をインライン化でき，展開しない呼び出しはリンクされた libc を使います．GCC 14.2.0 では定数文字列の strcpy は展開され，Func_2 の strcmp は picolibc を呼びます．構造体コピーはインラインの load/store を使います．設定変更はオブジェクトの再ビルドを起こします．性能比較時は builtin 設定も記録してください．クリーンは取得ソースとテスト入力を保持します．コンパイラやフラグの変更前に実行します．

## サイクル計測

```sh
make bench/Coremark/run
make bench/Dhrystone/run
# Compare Dhrystone without GCC libc builtins:
make bench/Dhrystone/run DHRYSTONE_BUILTINS=0
# Short run for comparison:
make bench/Dhrystone/run DHRYSTONE_BENCH_ITERATIONS=100
```

`BENCHMARK=1` でビルドし，通常の結果比較を保ってカウンタ値を UART 出力へ追加します．検証成功後にのみ TestDriver が `CoreMark/MHz = iterations * 1000000 / cycles` または `DMIPS/MHz = iterations * 1000000 / (cycles * 1757)` を表示します．測定区間は既存のループ用フック内で，起動・初期化・結果検証・UART 出力を除き，CSR 読み取りのオーバーヘッドを含みます．

リセット直後からの短時間シミュレーションで，既定では CoreMark 1 iteration，Dhrystone 2000 iterationsです．後者は `DHRYSTONE_BENCH_ITERATIONS` で変更でき，自動的に再ビルドします．通常の Dhrystone テストは100 iterationsのままです．Dhrystone 計測の命令数上限は既定で2000000で，長時間実行には `MAX_TEST_INSTRUCTIONS` を指定します．CoreMark は `Coremark/Coremark/cfg.xml` の650000命令を使い，`bench/Coremark/run` は `MAX_TEST_INSTRUCTIONS` を TestDriver に渡しません．正式スコア公表に必要な最低実行時間は満たしません．合成した時刻は機能検証専用で，推定値は別に取得した実サイクル数だけから求めます．64 bit mcycle の下位32 bitを読むので，区間は `2^32` サイクル未満にしてください．

Dhrystone は mcycle と iteration 数を報告し，make は GCC と TestDriver に同じ回数を渡します．GCC builtin と8 byteの関数・ループアラインメントはスコアに大きく影響するため明示設定します．コード・データ配置も影響するので，比較ではコンパイラ版とビルド設定を記録します．

計測モードと通常テストは同じ出力先を使うため順に実行します．モード変更で自動再ビルドし，通常テストは `BENCHMARK=0` と正確な UART 比較へ戻します．`test/all/run` はベンチマークを実行しません．

## Zephyr

```sh
make test/External/Zephyr/fetch
make test/External/Zephyr/setup
make test/External/Zephyr/run
```

[Zephyr/Makefile](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Zephyr/Makefile) は公開 Zephyr 4.4.0 を `Zephyr/External/zephyr` に固定し，Python 環境と出力は `Zephyr/Build/` に保存します．HelloWorld・Philosophers・Synchronization は upstream のサンプルを変更せず，RSD の out-of-tree board/SoC，Ubuntu の RISC-V GCC，minimal libc でビルドします．west・SDK・外部モジュールは不要です．Dev Container は CMake・Ninja・gperf・device-tree compiler を含みます．fetch/setup はネットワークを使い，ビルド・テストでは取得しません．

`test/External/Zephyr/run` は3本を実行し，Philosophers や Synchronization などを途中のパスで個別選択できます．TestDriver が通常の無コミット上限と命令数上限を適用します．HelloWorld は正確な挨拶，Synchronization は `--serial-prefix` で最初の A/B/A/B の4出力を要求し，それ以降や最後の不完全行は許容します．Philosophers は [CheckOutput.py](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/Zephyr/CheckOutput.py) でフォークの状態と sleep/wakeup 後の各哲学者の eating/thinking 2周を検査します．mutex の優先度継承と UART の割り込み合いを許し，最後の不完全行を無視しますが，カーネルエラーは拒否します．

シミュレーション用 board は仮想1 MHzクロックで待ち時間を短縮し，RTL と upstream ソースは変更しません．Philosophers は upstream の `DEBUG_PRINTF=1` でカーソル制御を無効にし，`CONFIG_PRINTK_SYNC=y` で出力呼び出しを同期します．クリーンは取得ソースと Python 環境を保持します．

## riscv-arch-test（ACT4）

Ubuntu 26.04 の Dev Container で明示的に取得・依存関係の設定を行います．

```sh
make test/External/riscv-arch-test/fetch
make test/External/riscv-arch-test/setup
make test/External/riscv-arch-test/check
make -j"$(nproc)"
make -j16 test/External/riscv-arch-test/run
```

[ACT4 Makefile](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Verification/TestCode/riscv-arch-test/Makefile) が upstream コミット・Bundler・Sail 版を固定します．ソースは `riscv-arch-test/External/`，Python/Ruby環境・取得キャッシュ・checksum検証済みSailは `riscv-arch-test/Build/` にあります．Ubuntu の Python・Ruby・LLVM22 を使い，コンパイラのビルドや mise/uv の導入は不要です．fetch/setup はネットワークを使い，check は取得済みツールだけを検査します．UDB の再生成データは NFS の排他 read-only lock の制約を避けるためコンテナ内の `/tmp/rsd-arch-test-<uid>/data/` を使います．

整数・特権命令は90ケースです: I39，M8，Zaamo9，Zalrsc2，Zba3，Zicond2，Zicsr6，Zifencei1，生成された ExceptionsSm・ExceptionsZaamo・ExceptionsZalrsc 各1，InterruptsSm17．A は upstream で Zaamo（AMO）と Zalrsc（LR/SC）に分かれます．Zba・Zicond は対応マクロが有効な場合だけ含め，無効時の明示選択は拒否します．

FP 有効時は F を既定で含み，合計371ケースです．`ACT_EXTENSIONS=F` は F だけを実行します．固定されたジェネレータは全 coverpoint を保ったまま1 ELFあたり250 testcasesを目標に281ファイルへ分割し，既存RAMへ収めます．upstreamへのパッチはありません．FP無効時はFを除き，明示的なF指定も拒否します．testgen は特権ソースを `Build/Generated/` に生成します．例外テストはMモードで起動し，割り込みはM/S/Uモード，Sモードへの委譲とPLIC外部割り込みを含みます．

build はネットワークを使わず，署名ELFを作成してSailで期待値を生成し，自己検証ELFに埋めます．RSD用アダプタがリセット入口・UART・終了処理を供給し，HEXはROMとRAMを含みます．テスト本体とヘルパーはRAM，リセットコードはROMです．生成物・ログはBuild配下です．

run は各ケースを新しいシミュレータで実行し，Verilatorの並列度は `-j16` や `-j1` で選択します．失敗後も残りを実行し，ケースごとの `result.log` と名前順の `Build/summary.log` を残します．一つでも失敗すればコマンド全体が失敗します．Vivadoは逐次実行です．絞り込みの例:

```sh
make test/External/riscv-arch-test/run ACT_EXTENSIONS=I
make test/External/riscv-arch-test/run ACT_EXTENSIONS=Zicsr,ExceptionsSm
make test/External/riscv-arch-test/run ACT_EXTENSIONS=M,Zaamo,Zalrsc,Zba,Zicond
make test/External/riscv-arch-test/run ACT_EXTENSIONS=ExceptionsZaamo,ExceptionsZalrsc
make test/External/riscv-arch-test/run ACT_EXTENSIONS=InterruptsSm
make test/External/riscv-arch-test/run ACT_EXTENSIONS=Zifencei
make -j16 test/External/riscv-arch-test/run ACT_EXTENSIONS=F
make test/External/riscv-arch-test/run ACT_TESTS="I-addi-00 I-sub-00"
```

選択したケースだけをビルド・実行し，未知の指定は拒否します．LED がPCの下位16 bitしか持たないためPCによる終了判定は無効にします．各ケースは命令数上限まで動かし，`a0=0` とファイル名に対応する正確なUART成功メッセージを要求します．build が serial.ref.txt を生成し，無コミット上限で停止を検出します．成功後は終了ループで上限まで待機します．

命令数上限は整数/CSR 20000，SC/FP 50000，例外/割り込み100000，割り込みtrigger・enable-priorityの大きい検査は300000です．無コミット上限は通常500，Zifenceiとdirty cacheをflushする特権テストは2500です．失敗は `Build/Cases/<suite>/<test>/serial.out.txt` にテスト番号・命令・おおよそのPC・実測/期待値として出力します．

例外は ECALL・EBREAK・不正命令，fetch/load/store/AMO/LRSCのmisaligned・access faultを検査します．atomic は書き込み先レジスタ保持，LRSC はscratch memoryも検査します．`test/Asm/Aext/run` はcached/uncached AMO fault時のメモリ保持も別に検査します．

InterruptsSm は MEI/MSI/MTI と SEI/SSI/STI のenable mask，Direct/Vectored入口，委譲，混在優先度，遅延timerとWFI pollingを検査します．非同期trap PCは比較せず，cause・status・pending・回数を署名に含めます．priority検査では待機を挟んでから要求を消し，パイプライン排出とpending配信を待ちます．

割り込みテストは `EnableUART_Interrupts` を有効にし，共通RTLテストベンチがUART DC1/DC3でPLIC source1を制御します．他のテストは全UART byteを保持します．アダプタはM/S contextと通常のclaim/completeを使い，CSR pending bitを強制しません．要求はモジュール入力経由でCoreへ渡り，合成ラッパではボード割り込みデバイス接続までlowに固定します．この刺激はRTLシミュレーション専用で，合成後や実機では使えません．

Zifencei はRAM上の自己書換えコード，無視される非ゼロrs1/rd/funct12，rdの保持を検査し，CSRケースはmepc bit1のreadbackを検査します．参照設定は未割当アドレスでのaccess fault優先，illegal instructionとinstruction access faultのmtval=0に合わせます．

Fは全5丸めモードで数値結果と例外フラグを除算・平方根も含めて検査します．参照FPプロファイルは標準のmstatus.FSを有効化し，基本 `Asm/CSR` がFS/SD，FS Off時アクセス，dirty trackingを別に検査します．SモードはBareのみで，ページングと完全なSモード適合性は対象外です．`test/ex/run`・`test/ex/build` に含まれ，実行前にfetch/setupが必要です．`test/clean` または個別のcleanで生成物を削除し，個別cleanは導入済みツールを保持します．

## メモリマップ

[MemoryMap.toml](https://github.com/rsd-devel/rsd/blob/master/Processor/Config/MemoryMap.toml) がRTLとソフトウェアの共通アドレスを定義します．[構成ジェネレータ](https://github.com/rsd-devel/rsd/blob/master/Processor/Tools/ConfigGenerator/ConfigGenerator.py) が，本体ルートを基準に `Processor/Src/Config/MemoryMapTypes.sv` と `Processor/Src/Verification/TestCode/` 内の `rsd-memory-map.h`・`.ld`・`.mk` を生成します．make は `Processor/Src/Makefiles/GenerateConfig.inc.mk` 経由でこれらを再生成します．外部RTL利用者が生成器なしでビルドできるよう，生成物はGitに含めます．ENDは最後の有効アドレスを含み，物理0から始まるイメージサイズはPHYSICAL_END+1，objcopyのpad-toは論理END+1です．

共通の起動コード・UART関数・リンカ・ACT4・Zephyrはこれらを使いますが，リンカ固有のセクション配置・容量制限，直接アドレス指定のASMと期待値，ACT4 Sailモデル固有のデバイスアドレスは別途確認が必要です．マップ変更だけで自動移動はしません．
