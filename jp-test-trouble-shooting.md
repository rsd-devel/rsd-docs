# トラブルシューティング



## QuestaSimの機能シミュレーション結果がおかしい 

### モジュール間で信号の受け渡しがうまくできない 

モジュールの入力ポートに多次元配列を使う場合，input ではなく ref と宣言しないと信号の値を渡せないことがある．
Synplify では ref は受け付けないため，コンパイラディレクティブを使って処理系ごとにコードが変わるようにする必要がある．


*合成時のみコンパイルするファイル 

     `define REF input


モジュールを宣言するファイル 

     `ifndef REF
       `define REF ref
     `endif
     module Hoge (
       input   logic clk, rst,
       `REF    logic [BIT_WIDTH-1:0] multidimensionalArray [ INDEX_WIDTH_1 ][ INDEX_WIDTH_2 ],
     ...


### 「** Error (suppressible): (vsim-*) Iteration limit **** reached at time **** ns.」 と出て怒られる 

for文の中でmodportインスタンス内のlogicへ代入するものが条件によって変わる場合，QuestaSimでエラーが出ることがある(出ないこともある)．  
だめな例: 

     module Sample(SampleIF.Samplemodport port);
         ...
         for (int i = 0; i < SAMPLE_NUM; i++) begin
             if (sampleflag) begin
                 port.sampleData[i] = SampleA;
             end
             else begin
                 port.sampleData[i] = SampleB;
             end
         end
         ...
     endmodule
     
いい例: 

     module Sample(SampleIF.Samplemodport port);
         ...
         logic [SAMPLE_DATA_WIDTH-1:0] portSampleData [0:SAMPLE_NUM-1];
         for (int i = 0; i < SAMPLE_NUM; i++) begin
             if (sampleflag) begin
                 portSampleData[i] = SampleA;
             end
             else begin
                 portSampleData[i] = SampleB;
             end
         end
         ...
         for (int i = 0; i < SAMPLE_NUM; i++) begin
             port.sampleData[i] = portSampleData[i];
         end
         ...
     endmodule



## QuestaSim の Post-***シミュレーション結果がおかしい 

機能シミュレーションは通るけど，論理合成して Post-Translate / Post-Map / Post-Place-and-Route シミュレーションをやると結果がおかしい場合．


### 波形比較 
QuestaSimには，2つのシミュレーション結果の波形を比較する機能があります．
これで（正しい）機能シミュレーションの結果と（バグってる）Post-~シミュレーションの結果を比較しましょう．

具体的なQuestaSimの操作方法は，まだ執筆中．とりあえず「QuestaSim 波形比較」とかでググれ．


### バグの原因例 

合成すると結果がおかしくなる，というバグの原因としてはこれまで以下のようなものありました．参考までに．

* FPGA のプリミティブの仕様を正しく把握しておらず，機能シミュレーションではその辺をいい加減にごまかしていたので通っていたが，合成した後のシミュレーションではうまくいかなかったというケース
    * Block RAM の入出力タイミングを間違えた，クロックモジュールにキャリブレーションが必要なのを無視してた，など

* 不定値 'x' が悪さをしていたケース
    * 機能シミュレーション時は'x'だった値が，Post-~シミュレーションでは'0'or'1'になることで，シミュレーションの挙動が変わった

* タイミング・フォールト
    * Post-Map / Post-Place-and-Route シミュレーションでは遅延を計算に入れるので，タイミング・フォールトが起こることがある．
ただし，こういうケースは論理合成or配置配線の時点でエラーとなり，エラーが起きた場所も教えてもらえるので，わざわざPost-~シミュレーションで扱うことは無いと思う．

## Synplify の論理合成が通らない

Synplify の Run ボタンを押すと

* Compile
* Map
* Place and Route

が実行されますが，ここでは前2つについて書きます．
Place and Route が通らない場合は「ISEの配置配線が通らない」などを見てください．


### Compile 時のエラーと警告 

#### undefined variable reference ... というCompile時エラー 

* たぶんコンパイラの不具合で詳細は不明だが、以下の対処で解決したケースあり
    * += や |= などの自己代入演算子の使用をやめる
    * Synplify プロジェクトで読み込む Verilog ファイルの順番を入れ替える
        * あるモジュールで使うモジュール/インターフェースの定義が、必ずそれ以前に読み込まれているようにする


#### 意味がわからないCompile時エラー 

* SystemVerilog ファイルが Verilog として認識されていないか疑う
    * ファイル名を右クリック -> File Options から設定可能
    * Implementation Options -> Verilog の SystemVerilog にチェックを付けておくと、デフォルトで SystemVerilog だと思ってくれる


### Map 時のエラーと警告 


#### Tristate driver ... というMap時警告 

* 現状のInterfaceの実装では、この警告が大量に出る
    * モジュールA,B,Cをつなぐインターフェースがあった時、AとBのみ接続しCには接続しない配線があると、この警告が出る


## ISEの配置配線が通らない

### Synplifyの論理合成でのエラーや警告 

### 配置配線が終わらない or XX signals are unrouted 

資源消費が多すぎたり，タイミング制約が厳しすぎる場合は，配置配線が不可能になる．
このような場合はなかなか配置配線が終わらず，最終的に配置配線できなかったとしてエラーになる．

あくまで目安だが，使用 LUT 数が全体の2/3を超えてくると，配置配線を自動で行うのがかなり厳しくなる．

自動で配線できなかった信号だけ手動で配線することもできるが，いまのところ雷上動の開発で試したことはない．


