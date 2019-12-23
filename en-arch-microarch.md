# Microarchitecture

## Overall

Please refer to the following link.

* [An Open Source FPGA-Optimized Out-of-Order RISC-V Soft Processor](http://sv.rsg.ci.i.u-tokyo.ac.jp/pdfs/Mashimo-FPT'19.pdf)
* [面積効率を指向するプロセッサ「雷上動」の設計と実装](https://repository.dl.itc.u-tokyo.ac.jp/?action=repository_action_common_download&item_id=5849&item_no=1&attribute_id=14&file_no=1)


## About the zero register

The zero register is implemented as follows.

* An instruction that writes to the zero register is cleared the register write flag
    * Determine whether it is zero register when writing to opInfo.writeReg of Decoder.sv
* Register file is initialized by reset circuit so that all zeros are written
    * This process is written in RegisterFile.sv
* In RMT (Register Map Table), the zero register is assigned to physical register's entry 0 when initialized and this entry is not released

Reading the zero register is actually performed from the physical register, but value 0 is always read due to the above conditions

## Handling exceptions

### Related signals

* Mainly related units
    * Privileged/CSR\_Unit.sv
    * Privileged/CSR\_UnitIF.sv
    * Pipeline/MemoryBackEnd/MemoryTagAccessStage.sv
        * This module judges whether an exception occurred

* csrUnitIF.triggerInterrupt
    * Interrupt: triggered by external factors, such as timers, independent of instruction execution

* csrUnitIF.triggerExcpt
    * Exception: triggered as the instruction executes
    * Exception is further divided into fault and trap
        * fault: address biolation, etc.
        * trap: system call, etc.
    * Determine the type of exception with csrUnitIF.excptCause.
        * If csrUnitIF.excptCause is EXEC\_STATE\_TRAP\_ECALL, trigger trap
        * If csrUnitIF.excptCause is EXEC\_STATE\_FAULT\_LOAD\_MISALIGNED, trigger fault, and so on.

### Flow when a fault occurs

* Address check is performed in Pipeline/MemoryBackEnd/MemoryTagAccessStage.sv
    * Fault is registered in ExecState at this time

    ```
    // If the execution is completed correctly, check whether the fault occurred
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
* ExecState is written to the ActiveList in write back stage
* Wait until the faulting instruction is at the top of the ActiveList
    * Faults are not subject to runtime recovery
* Detecting faulted instruction in the commit stage
* Send a recovery request to the RecoveryManager
    * In recovery, the instruction caused the fault is flushed as well
* Send a trigger request of fault to the CSR\_Unit from the RecoveryManager
* Update the csr and PC according to the fault that generated CSR\_Unit
    ```
    @ CSR_Unit.sv
    csrNext.mepc = port.excptCauseAddr; // Write the PC where the exception occurred
    csrNext.mtval = port.excptCauseDataAddr;// PC for ECALL / EBREAK?
    csrNext.mcause.isInterrupt = FALSE;
    csrNext.mcause.code.trapCode = ToTrapCodeFromExecState(port.excptCause);
    ```