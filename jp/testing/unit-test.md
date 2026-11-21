# 単体テスト

RTL のモジュールごとにテストベンチを実行します．既定では Dev Container 内の Verilator を使用します．ModelSim/QuestaSim を使う場合は別途インストールし，`RSD_QUESTASIM_PATH` を設定して `SIM=modelsim` を指定します．

## 実行

`Processor/Src` で実行します．

```bash
make -j4 test/unit/run
make test/unit/Divider/run
make SIM=modelsim test/unit/run
```

`test/unit/run` はFP 有効時は以下の 16 テストを実行します．共有の生成 RTL を準備してから，各テストベンチをビルド・実行します．コア全体のシミュレータを先にビルドする必要はありません．

- `InitializedBlockRAM`
- `BlockDualPortRAM`
- `DistributedDualPortRAM`
- `DistributedMultiPortRAM`
- `MultiBankRAM`
- `MultiWidthQueuePointer`
- `MultiWidthFreeList`
- `Divider`
- `MulDivUnit`
- `Memory`
- `ICache`
- `DCache`
- `DecodeStage`
- `SerialOutput`
- `InterruptController`
- `FPDivSqrtUnit`（FP 有効時のみ）

個別指定は `test/unit/<名前>/run` です．定義は本体の [Makefile](https://github.com/rsd-devel/rsd/blob/master/Processor/Src/Makefile)，テストベンチは [Verification/UnitTest](https://github.com/rsd-devel/rsd/tree/master/Processor/Src/Verification/UnitTest) にあります．

## 他のテストとの関係

`test/all/run` はプログラムテストの集約で，単体テストを含みません．設定生成・TestDriver・RunContainer ランチャを検証する `test/tools/run` も別のターゲットです．[テスト・プログラム](program.md) を参照してください．

合成したコアの検証は [合成後シミュレーション](../synthesis/post-synthesis-simulation.md) を参照してください．

プロセッサのパラメータを変更した場合は，各テストの入力・期待値・assertion の前提も確認してください．
