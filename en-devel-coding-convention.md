# Coding conventions

## File naming 

* Use Pascal Case (a combination of uppercase and lowercase letters, and capitalize the first letter).
* If there are all uppercase abbreviations, insert an underscore between the words
* Use .sv extension.


### Example

```
IntAdder.sv
```

## General Naming Rules

* ModuleName
  * Use Pascal Case.
  * If there are all uppercase abbreviations, insert an underscore between the words
* TypeName
  * When using typedef, use Pascal Case for the newly defined type name.
* InterfaceNameIF
  * Interface is basically the same as the ModuleName, with a suffix IF on the rule
* RoutineName
  * Use Pascal Case for function and task.
* localVariable
  * Use Lower Camel Case (the first letter of the entire word is lowercase, but subsequent first letters are uppercase).
* CONSTANT_VALUE
  * Named constants are all uppercase.
* PREFIX_ENUMERATED_TYPE
  * Enumeration values are capitalized as well as CONSTANT_VALUE. And prefix the constant with the type abbreviation of the entire enumeration. The type that represents the entire enumeration type follows TypeName.

### Example

```
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
        AC_AND = 4'h0,  // AND         Rd := Rn AND shifter_operand
        AC_EOR = 4'h1,  // XOR         Rd := Rn XOR shifter_operand
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
            dataInB,
        );
            
        modport Port( 
        input 
            dataOut,
        output
            code,
            dataInA,
            dataInB,
        );
    endinterface : IntALU_IF
    
    // ALU
    module IntALU( IntALU_IF.Self self );
    ...
    endmodule : IntAdder
```

## Other rules

### General rules

* Do not use assign (see below).
* Use logic.
  * Do not use wire and reg.
* Use always_comb or always_ff.
  * Do not use always
* Do not use raw values.
  * Always define constants with meaningful names before using them.

### function and modport

* When defining arguments, first declare a named type with typedef and use that type (except for 1-bit logic)
* For the function and modport arguments, write output in principle, and then write input in the order


### Selector (case statements)

* Use unique case.
* Be sure to write default case.
  * In default case, assign `x (undefined value) to variables.
  * Otherwise it will generate extra circuitry.

## Module

### Overall purpose

* Eliminate mistakes by writing always_comb as close to the program as possible (sequentially)
* Use always_comb to generate a combinational circuit that produces the same result when the same input is given
    * Easily imagine what kind of circuit it will be
    * Consider a detailed circuit for the first time when a large circuit is created

### Rules

* Basically each module defines only one always_ff and one always_comb
    * Always define FF in always_ff and do not write logic in it
    * Since the logic is completed in a single always_comb, the changes that occur in the cycle in that module can be written almost as if they were sequential programs

* Use only non-blocking assignment (<=) in always_ff and blocking assignment (=) in always_comb
    * To eliminate parallel operation from always_comb and enable sequential read.

* Do not use assign, always use always_comb
    * Using assign causes signal changes to occur in different rows
        * No sequential change from upper to lower
    * For example, in the following code, the change in the lower line will propagate to the upper line
``` 
    assign a = b & 1;
    ...
    assign b = c & d;
```

* If there is a signal exchange with an external module in always_comb, make sure that changes that occur in the lower do not propagate to the upper
    * For example, the following code is not good
```
    module Module (ext);
        always_comb begin
            hoge = ext.out; // Changes that occurred in ext.in below appear in ext.out
            ...
            ext.in = 0;
        end
    end
```

* Good example

```
    module Module (ext);
        always_comb begin
            ext.in = 0;
            hoge = ext.out; // Changes that occurred in ext.in above appear in ext.out
        end
    end
```

### Typical example
```
    module ModuleName (...);
        
        // Definition of signal lines related to FF
        ...
        
        // Definition of FF
        always_ff (...) begin
        end
        
        // Definition of signal
        ...
        
        // Logic definition
        always_comb begin
            // Basically, write the signal to flow from upper to lower
            // by input / output to external module
        end
    endmodule
```

## Encoding etc.

* Use UTF-8.
* Use LF line feed code.
* Tabs are 4 spaces
    * Do not use hard tabs.
