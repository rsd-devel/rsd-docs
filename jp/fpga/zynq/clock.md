# クロック

以下の GUI 操作は Vivado 2016.4 の記録です．現行のプロジェクト生成処理は [design_1.tcl](https://github.com/rsd-devel/rsd/blob/v1.2.0/Processor/Project/Vivado/TargetBoards/Zedboard/scripts/synthesis/design_1.tcl) を参照してください．[VCS のタイミング検証](../../synthesis/post-synthesis-simulation.md) の `POST_IMPLEMENTATION_CLOCK_NS` は別の設定です．

## Digilent Zedboard 

v1.2.0 の Zedboard 構成では，PS の `processing_system7_0/FCLK_CLK0` が RSD コアと AXI インターフェースを 50 MHz で駆動します．プロジェクト生成 Tcl の `CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ` が要求周波数です．
クロック動作周波数の変更は，Vivadoプロジェクト上で以下の手順で行えます(2016.4現在)．

* 左部[Flow Navigator]->[IP Integrator]->[Open Block Design]をクリック
* 開いた[Diagram]内のZYNQブロック(`processing_system7_0`)をダブルクリック
* 左部[Page Navigator]->[Clock Configuration]->[PL Fabric Clocks]の+ボタンをクリックして展開
* 変更したいクロックの[Requested Frequency(MHz)]の数値を変更して[OK]
