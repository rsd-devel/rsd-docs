
# Synplify の合成結果の確認方法

Synplify で合成後の回路の資源量とクリティカル・パスの解析方法について説明する．

## 準備

Synplify で回路合成を行っておくこと．

- やり方は[基本的な合成手順](jp-synth-howto)を参照．

## クリティカル・パス解析
### スケマティックでの解析

Synplify のメイン画面の上のタブ　HDL-Analist -> Technology -> Hierarchical Critical Path を選択． 

回路のクリティカル・パスのブロック図が表示される．
- この方法ではワーストケース・パスは1種類のみしか解析できない？（要調査）

### Detailed report による解析

手順
1. Synplifyのメイン画面にて，中央右側のペイン内のタブ Project Status を開いた状態にする．
2. Timing Summary の表内の Detailed report をクリック
3. 左側ペイン内の Detailed Report for Clocks の + マークをクリックし，展開
4. 展開されて出てきた Clock: Main_Zynq_Wrapper|clk の + マークをクリックし，展開
5. 展開されて出てきた Worst Path Information をクリック

これで，ワーストケース・パスの情報が表示される
- Instance / Net の真下にある表組みから，各モジュールにおける遅延 (Delay) を調べることが出来る．
- Detailed report では，ワーストケース・パスは4つまで見ることができる．（要検証）

## 資源量の確認

### 回路全体の資源量の確認

メイン画面の左側のペインの Project Status タブの Area Summary から確認．
- 見たい資源が記載されていない場合は，Report タブから確認する．

### モジュール毎の資源量の確認

メイン画面の左側のペインの Project Status タブの Area Summary 内にある，Hierarchical Area report をクリック．
- モジュール毎の資源量が表示される．モジュールの階層構造を適宜展開して確認する．

### より詳細に確認する方法

RSD/Processor/Project/Synplify/Zedboard/rpt_Main_Zynq_Wrapper_areasrr.htm により詳細な情報が記載されている．
