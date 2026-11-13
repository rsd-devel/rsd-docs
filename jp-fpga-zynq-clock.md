# クロック

以下の GUI 操作は Vivado 2016.4 の記録です．現行のプロジェクト生成処理は [design_1.tcl](https://github.com/rsd-devel/rsd/blob/master/Processor/Project/Vivado/TargetBoards/Zedboard/scripts/synthesis/design_1.tcl) を参照してください．[VCS のタイミング検証](jp-synth-simulation) の `POST_IMPLEMENTATION_CLOCK_NS` は別の設定です．

## Digilent Zedboard 

Zedboardに限らず，ZYNQボードではPL部のクロックはPS部から供給されます．
クロック動作周波数の変更は，Vivadoプロジェクト上で以下の手順で行えます(2016.4現在)．

* 左部[Flow Navigator]->[IP Integrator]->[Open Block Disign]をクリック
* 開いた[Diagram]内のZYNQブロック(processing\_system 7_0)をダブルクリック
* 左部[Page Navigator]->[Clock Configuration]->[PL Fabric Clocks]の+ボタンをクリックして展開
* 変更したいクロックの[Requested Frequency(MHz)]の数値を変更して[OK]
