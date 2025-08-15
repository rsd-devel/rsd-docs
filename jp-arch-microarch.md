# マイクロアーキテクチャ

## 全体

下記を参照してください．

* [An Open Source FPGA-Optimized Out-of-Order RISC-V Soft Processor](https://www.rsg.ci.i.u-tokyo.ac.jp/members/shioya/pdfs/Mashimo-FPT'19.pdf)
* [面積効率を指向するプロセッサ「雷上動」の設計と実装](https://repository.dl.itc.u-tokyo.ac.jp/?action=repository_action_common_download&item_id=5849&item_no=1&attribute_id=14&file_no=1)


## ゼロレジスタについて

以下のようにしてゼロレジスタは実装されています.

* ゼロレジスタへ書き込む命令は，レジスタ書き込みフラグを落とす
    * Decoder.svのopInfo.writeRegへの書き込みの際にゼロレジスタかどうかを判定
* レジスタファイルはリセット回路による初期化で, すべてにゼロが書き込まれるようにする
    * RegisterFile.sv内で記述
* RMTは初期化によって, 物理レジスタの0番エントリにゼロレジスタが割り当てられ, 解放されることがない
* ゼロレジスタの読み込みは実際に物理レジスタから行われるが, 上の条件により常に０が読みだされる

## 例外の処理

### 直接関係する信号

* 関連するユニット
    * Privileged/CSR\_Unit.sv
    * Privileged/CSR\_UnitIF.sv
    * Pipeline/MemoryBackEnd/MemoryTagAccessStage.sv
        * 例外判定を行っている

* csrUnitIF.triggerInterrupt
    * 割り込み: タイマーなどの，命令の実行とは独立に外部要因によってよりトリガされる

* csrUnitIF.triggerExcpt
    * 例外: 命令の実行に伴ってトリガされる
    * 例外はさらに，fault と trap に別れる
        * fault: アドレス違反等
        * trap: システムコール呼び出し等
    * csrUnitIF.excptCause のコードによって上記を判別する
        * EXEC\_STATE\_TRAP\_ECALL ならトラップ，
        * EXEC\_STATE\_FAULT\_LOAD\_MISALIGNED ならフォールトなど

### フォールト発生時のフロー

* @Pipeline/MemoryBackEnd/MemoryTagAccessStage.sv でアドレスチェックが行われ，ExecState にフォールトが登録される
    ```
    // 実行が正しく終了してる場合，フォールト判定を行う
    if (nextStage[i].execState == EXEC_STATE_SUCCESS) begin
        if (isLoad[i]) begin
            if (pipeReg[i].memMapType == MMT_ILLEGAL)
                nextStage[i].execState = EXEC_STATE_FAULT_LOAD_VIOLATION;
            else if (IsMisalignedAddress(pipeReg[i].addrOut, iqData[i].memOpInfo.memAccessMode.size))
                nextStage[i].execState = EXEC_STATE_FAULT_LOAD_MISALIGNED;
        end
        else if (isStore[i]) begin
            if (pipeReg[i].memMapType == MMT_ILLEGAL)
                nextStage[i].execState = EXEC_STATE_FAULT_STORE_VIOLATION;
            else if (IsMisalignedAddress(pipeReg[i].addrOut, iqData[i].memOpInfo.memAccessMode.size))
                nextStage[i].execState = EXEC_STATE_FAULT_STORE_MISALIGNED;
        end
    end
    ```
* ライトバックステージで ActiveList に execState が書き込まれる
* フォールトを起こした命令が ActiveList の先頭に来るまで待つ
    * フォールトは実行時リカバリの対象とはならないようにしている
* コミットステージでフォールトを起こした命令を検出
* RecoveryManager にリカバリ要求をだす
    * リカバリの一種として，フォールトを起こした命令が自分ごと取り消される
* RecoveryManager から CSR\_Unit に対してフォールトのトリガを要求
* CSR\_Unit が発生したフォールトの種類などに応じて csr や PC を書き換える
    ```
    @ CSR_Unit.sv
    csrNext.mepc = port.excptCauseAddr; // 例外の発生元 PC を書き込む
    csrNext.mtval = port.excptCauseDataAddr;// ECALL/EBREAK の場合は PC?
    csrNext.mcause.isInterrupt = FALSE;
    csrNext.mcause.code.trapCode = ToTrapCodeFromExecState(port.excptCause);
    ```