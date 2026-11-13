# 制約ファイル

制約ファイルは，HDL だけでは表せないピン配置，クロック周期，配置条件などを合成・配置配線ツールへ伝えます．Vivado は XDC，Synplify は SDC/FDC 形式の制約を使用します．

## Zedboard の制約

ピン制約は [zedboard.xdc](https://github.com/rsd-devel/rsd/blob/master/Processor/Project/Vivado/TargetBoards/Zedboard/project_src/zedboard.xdc)，プロジェクト生成とクロック設定は [Vivado スクリプト](https://github.com/rsd-devel/rsd/tree/master/Processor/Project/Vivado/TargetBoards/Zedboard/scripts/synthesis) を参照してください．

## タイミングの確認

クロック周期は要求するタイミング条件です．設定するだけで動作周波数が保証されるわけではなく，合成・配置配線後のレポートで制約を満たすか確認します．厳しすぎる制約や過大な資源使用量は配置配線の収束を妨げます．

クロック，入出力遅延，対象外パスなどの前提を記録して結果を比較してください．[VCS によるタイミング検証](jp-synth-simulation) の `POST_IMPLEMENTATION_CLOCK_NS` と [ボードのクロック設定](jp-fpga-zynq-clock) は別の設定です．
