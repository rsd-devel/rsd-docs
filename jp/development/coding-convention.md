# コーディング規約

## ファイル名

* 大文字と小文字を組み合わせて使用し，1文字目を大文字にする．
* 全て大文字の略語があった場合，単語間の切れ目にはアンダーバーをはさむ
* 拡張子は .sv

### 例

    IntAdder.sv

## 命名規則 

* ModuleName
     * 大文字と小文字を組み合わせて使用し，1文字目を大文字にする．
     * 全て大文字の略語があった場合，単語間の切れ目にはアンダーバーをはさむ
* TypeName
    * typedefの型定義では，大文字と小文字を組み合わせて使用し，1文字目を大文字にする．
* InterfaceNameIF
    * インターフェースは，基本的にモジュール名と同じでルールの上，サフィックス IF をつける
* RoutineName
    * Function，Taskには大文字と小文字を組み合わせて使用し，1文字目を大文字にする．
* localVariable
    * ローカルの配線やFFには大文字と小文字を組み合わせて使用し，1文字目を小文字にする．
* CONSTANT\_VALUE
    * 名前付き定数は全て大文字．
* PREFIX\_ENUMERATED\_TYPE
    * 列挙子については，定数と同じく大文字．ただし，先頭にデータ型を表すプレフィックスをつける．列挙型全体を表す型は TypeName に準じる



### 例 

    // Data width
    parameter DATA_WIDTH = 32;
    typedef logic [DATA_WIDTH-1:0] DataPath;
    parameter DATA_MASK = 32'hffffffff;
    parameter DATA_ZERO = 32'h00000000;
    
    // ALU result
    typedef struct  
    {
        logic    carry;
        DataPath data;
    } IntAdderResult;
    
    // ALU code
    typedef enum logic [3:0]    // enum ALU_Code
    {
        AC_AND = 4'h0,  // AND  論理積              Rd := Rn AND shifter_operand
        AC_EOR = 4'h1,  // EOR  排他的論理和        Rd := Rn EOR shifter_operand
    ...
    } IntALU_Code;
    
    // ALU interface 
    interface IntALU_IF;
        DataPath dataOut;
        IntALU_Code code;
        DataPath dataInA;   // rN
        DataPath dataInB;   // shifterOperand
        
        modport Self( 
        output
            dataOut,
        input 
            code,
            dataInA,
            dataInB
        );
            
        modport Port( 
        input 
            dataOut,
        output
            code,
            dataInA,
            dataInB
        );
    endinterface : IntALU_IF
    
    // ALU
    module IntALU( IntALU_IF.Self self );
    ...
    endmodule : IntALU


## その他ルール 

### その他

* assign は使用を禁止（後述）
* logic を使う．
    * wire/reg の使用は禁止．
* always\_comb/always\_ff を使う．
    * 素のalways は使用禁止．
* 生の値の使用禁止
    * 必ず定数として意味のある名前を定義してから使用する

### 関数や modport について

* 引数の定義では，必ず型名を typedef してから使用すること（1-bit の logic を除く）
* function や modport の引数については，原則 output を書いてから，input を書く順番に

### セレクタ（case 文） 

* unique case を使用する
* 必ずdefault の項を書く
    * `x （不定）が入るようにしておく
    * default で不定が入るようにしておかないと，かなり余計な回路が生成される


## モジュールの書き方について

### 全体の目的と気分
* always\_comb を極力プログラムに近い形で（シーケンシャルに）書くことで，ミスを無くす
* always\_comb に書いたプログラムに対し，同じ入力が与えらた場合に同じ結果を出す組み合わせ回路が生成されるつもりで書く
    * それがどんな回路になるかはある程度イメージしておくこと
    * やたらでかい回路ができてしまった場合に，はじめて詳細に検討する

### ルール
* 基本的に各モジュールは always\_ff と always\_comb を一つずつ定義する
    * always\_ff 内は極力 FF の定義に徹し，ロジックを記述しないこと
    * ロジックが単一の always\_comb 内に完結することで，そのモジュールでサイクル内に起きる変化がほぼプログラムのかのように書ける

* always\_ff の中ではノンブロッキング代入（<=），always\_comb の中ではブロッキング代入（=）のみを使用する
    * always\_comb 内から並列動作を排除し，シーケンシャルに読めるようにするため

* assign は使用せず，必ず always\_comb を使用すること
    * assign を使用すると，信号の変化が行ごとにばらばらに起きてしまう
        * 上から下にシーケンシャルに変化がおきない
    * たとえば以下のようなコードがあると，下の行でおきた変化が上の行に波及してしまう
        assign a = b & 1;
        ...
        assign b = c & d;

* always\_comb 内で外部モジュールとの信号のやり取りがある場合，下の行で起きた変化が上の行に波及しないように気をつける
    * たとえば以下のようなコードはよくない
        module Module(ext);
            always_comb begin
                hoge = ext.out; // 下の ext.in で起きた変化が ext.out に出てくる
                ...
                ext.in = 0;     
            end
        end

    * 以下のようなコードに
        module Module(ext);
            always_comb begin
                ext.in = 0;     
                hoge = ext.out; // 上の ext.in で起きた変化が ext.out に出てくる
            end
        end


### 典型的な例

    module ModuleName(...);
        
        // FF 関連の信号線の定義
        ...
        
        // FF の定義
        always_ff(...) begin
        end
        
        // 信号線の定義
        ...
        
        // ロジックの定義
        always_comb begin
            // 基本的に，上から下に信号が流れるように書く
            // 外部モジュールへの入出力により
        end
    endmodule


## エンコーディングなど

* 日本語を書く場合は UTF-8 に
* 改行コードは LF
* タブはスペース x 4 に
    * ハードタブは使用不可
