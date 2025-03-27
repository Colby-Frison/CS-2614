# Midterm 2 Question Explanations

## Question 1: Register Transfer Statements [10 marks]

The question asks what's wrong with two register transfer statements:

### Part A: `zT: PC ← AR, PC ← PC+1`

**Problem**: This statement attempts to modify the Program Counter (PC) in two different ways simultaneously within the same time unit (zT). This is impossible because:
1. The first operation tries to load PC with the value from AR
2. The second operation tries to increment PC by 1
3. A register cannot have two different values assigned to it at the same exact moment (same time unit)

**Solution**: To fix this, you would need to either:
- Split these operations into different time units
- Choose one operation to perform on PC

For example:
```
zT: PC ← AR
z+1T: PC ← PC+1
```

### Part B: `xT: R1← R1', R1← R2`

**Problem**: Similar to Part A, this statement has a concurrent assignment problem:
1. The first operation tries to set R1 to R1' (complement of R1)
2. The second operation tries to set R1 to the value of R2
3. A register (R1) cannot have two different values assigned to it simultaneously

**Solution**: To fix this, you would need to:
- Perform these operations in separate time units
- Choose only one operation to perform on R1

For example:
```
xT: R1← R1'
x+1T: R1← R2
```

### Key Principle
In register transfer language (RTL):
- Operations within the same time unit (T) are meant to occur simultaneously
- A register can only be assigned one new value at a time
- If multiple operations need to modify the same register, they must be sequenced across different time units

This is similar to how in programming you can't assign two different values to a variable at the exact same time - one assignment must come after the other.

## Question 2: ROM Design for Gray Code Conversion [10 marks]

The question asks to design a combinational circuit using ROM to convert 3-bit binary inputs (0-7) to Gray code outputs.

### Part A: Truth Table [5 marks]

To create the truth table, we need to:
1. List all possible 3-bit binary inputs (000 to 111)
2. Convert each binary number to its Gray code equivalent

The conversion to Gray code follows this principle:
- Each bit in the Gray code differs from its neighbor in only one position
- To convert binary to Gray code: G[i] = B[i] XOR B[i+1]

Complete Truth Table:
```
INPUT (Binary)      OUTPUT (Gray)
X2  X1  X0         Y2  Y1  Y0
0   0   0          0   0   0
0   0   1          0   0   1
0   1   0          0   1   1
0   1   1          0   1   0
1   0   0          1   1   0
1   0   1          1   1   1
1   1   0          1   0   1
1   1   1          1   0   0
```

### Part B: ROM Size Requirements [5 marks]

To determine the ROM size, we need to calculate:
1. Number of addressable locations = 2³ = 8 (since we have 3 input bits)
2. Number of bits per location = 3 (since we need 3 output bits for the Gray code)
3. Total ROM size = 8 × 3 = 24 bits
(it is also just the height and width of the outputs, but its better to think of it in the proper way)

**Explanation of ROM Size**:
- The ROM needs enough addresses to store all possible input combinations
- With 3 input bits, we have 2³ = 8 possible combinations
- Each location needs to store a 3-bit Gray code output
- Therefore, total size = (number of locations) × (bits per location) = 8 × 3 = 24 bits

This ROM will act as a lookup table, where:
- The 3-bit input serves as the address
- Each address contains the corresponding 3-bit Gray code output
- When an input is provided, the ROM outputs the pre-stored Gray code value at that address

## Question 3: Boolean Function Implementation with 8×1 Multiplexer [20 marks]

The question asks to implement the Boolean function F(P,Q,R,S) = Σ(2,3,7,8,9,10,11,13,15) using an 8×1 multiplexer.

### Part A: Truth Table [10 marks]

First, let's understand how to complete the truth table:
1. List all possible combinations of P, Q, R, S (16 combinations total)
2. Mark output F as 1 for the specified minterms (2,3,7,8,9,10,11,13,15)

Complete Truth Table:
```
P  Q  R  S  | F
0  0  0  0  | 0  (m0)
0  0  0  1  | 0  (m1)
0  0  1  0  | 1  (m2)
0  0  1  1  | 1  (m3)
0  1  0  0  | 0  (m4)
0  1  0  1  | 0  (m5)
0  1  1  0  | 0  (m6)
0  1  1  1  | 1  (m7)
1  0  0  0  | 1  (m8)
1  0  0  1  | 1  (m9)
1  0  1  0  | 1  (m10)
1  0  1  1  | 1  (m11)
1  1  0  0  | 0  (m12)
1  1  0  1  | 1  (m13)
1  1  1  0  | 0  (m14)
1  1  1  1  | 1  (m15)
```

### Part B: 8×1 Multiplexer Implementation [10 marks]

To implement this function using an 8×1 multiplexer:

1. **MUX Configuration**:
   - The 8×1 MUX has 3 select lines and 8 data inputs
   - We need to use P, Q, R as select lines (to select between 8 inputs)
   - S will be used to determine the actual input values

2. **Implementation Strategy**:
   - Select lines: P, Q, R (in that order) determine which input is selected
   - Data inputs (0-7): Each input is connected to either S, S', 0, or 1
   - When PQR selects an input, the value of S determines the final output

3. **Connection Diagram**:
```
Input 0 (000): 0
Input 1 (001): S'
Input 2 (010): S
Input 3 (011): S
Input 4 (100): 1
Input 5 (101): 1
Input 6 (110): S
Input 7 (111): S
```

4. **How it Works**:
   - The select lines PQR choose one of the 8 inputs
   - If that input is connected to:
     * 0: Output is always 0
     * 1: Output is always 1
     * S: Output equals S
     * S': Output equals NOT S
   - This produces the correct output for all 16 input combinations

The implementation shown in the red markings correctly shows:
- P, Q, R as select lines
- S and its complement (S') connected to appropriate inputs
- Constants (0 and 1) connected where needed
- The output F representing the desired function

## Question 4: Decoder Circuit Analysis [15 marks]

The question asks to fill in the truth table for outputs X and Y of a circuit containing a 3×8 decoder and logic gates.

### Circuit Analysis

1. **Components**:
   - 3×8 decoder with inputs a, b, c (where a is MSB, c is LSB)
   - OR gate for output X (connected to D₀-D₃ and D₇)
   - NAND gate for output Y (connected to D₄-D₆)
   - Decoder outputs D₀ through D₇

2. **Decoder Operation**:
   - Input abc determines which output line is activated (becomes 1)
   - Only one output is active (1) at a time
   - All other outputs are inactive (0)
   - Output Dᵢ is active when abc = i in binary

3. **Output Functions**:
   - X is connected to D₀, D₁, D₂, D₃, and D₇ through an OR gate
   - Y is connected to D₄, D₅, and D₆ through a NAND gate

### Truth Table Solution:
```
A  B  C  | X  Y
0  0  0  | 1  1
0  0  1  | 1  1
0  1  0  | 1  1
0  1  1  | 1  1
1  0  0  | 0  1
1  0  1  | 0  1
1  1  0  | 0  1
1  1  1  | 1  1
```

### Explanation of Outputs

1. **For Output X**:
   - X is connected to D₀-D₃ and D₇ through an OR gate
   - X will be 1 when any of these decoder outputs is active
   - This occurs when abc represents 0-3 (000 to 011) or 7 (111)
   - X will be 0 only when D₄, D₅, or D₆ is active (abc = 100, 101, or 110)

2. **For Output Y**:
   - Y is connected to D₄, D₅, and D₆ through a NAND gate
   - Since the decoder only activates one output at a time, at least two inputs to the NAND gate will always be 0
   - When any input to a NAND gate is 0, the output is 1
   - Therefore, Y is always 1 for all input combinations

### Key Points:
- The decoder activates exactly one output line for each input combination
- The OR gate for X produces 1 for inputs 0-3 and 7
- The NAND gate for Y always produces 1 due to decoder behavior
- Understanding how the decoder outputs connect to the OR and NAND gates is crucial for determining the final outputs

## Question 5: 4-bit Arithmetic Circuit Analysis [15 marks]

The question presents a 4-bit arithmetic circuit with two registers A and B, and asks to determine the operation performed when select inputs S₁ = 1, S₀ = 1, Cᵢₙ = 1.

### Circuit Components

1. **Registers**:
   - Register A: bits A₀ to A₃
   - Register B: bits B₀ to B₃

2. **For each bit position**:
   - 4×1 MUX (Multiplexer)
   - FA (Full Adder)
   - NOT gates for B inputs

3. **Control Inputs**:
   - S₁, S₀: Select inputs for all MUXes
   - Cᵢₙ: Carry input for the first FA

### Circuit Operation Analysis

1. **MUX Inputs for each bit position i**:
   - Input 0: 0
   - Input 1: Aᵢ
   - Input 2: B̄ᵢ (NOT Bᵢ)
   - Input 3: 1

2. **Select Input Configuration**:
   - S₁ = 1, S₀ = 1 selects input 3 (binary 11)
   - This means all MUX outputs will be 1

3. **When S₁S₀ = 11**:
   - All MUX outputs = 1
   - Each FA receives:
     * X input = 1
     * Y input from previous FA's carry
     * First FA receives Cᵢₙ = 1

### Operation Determination

1. **Result Analysis**:
   - When S₁S₀ = 11, all MUX outputs are 1 (X inputs to FAs)
   - For each FA:
     * X input is 1 (from MUX)
     * Y input is 1 (from previous carry)
     * These 1s add to give 10 (carry of 1 to next stage)
   - This carry chain effectively cancels out, leaving only A's value
   - Therefore, the circuit performs a transfer of register A to the output

2. **Why it's a Transfer**:
   - The carry propagation is key: 1 + 1 = 0 (with carry 1)
   - This carry of 1 becomes the Y input for the next stage
   - The process repeats at each FA, preserving A's bits
   - The final result is identical to the contents of register A

### Answer: Transfer

The circuit performs a transfer operation when S₁ = 1, S₀ = 1, Cᵢₙ = 1 because:
- The carry propagation is key: 1 + 1 = 0 (with carry 1)
- This carry of 1 becomes the Y input for the next stage
- The process repeats at each FA, preserving A's bits
- The final result is identical to the contents of register A

## Common Arithmetic Operations in Digital Circuits

### Basic Operations

1. **Transfer**:
   - Simply moves data from one register to another
   - Operation: A → B
   - No mathematical modification of the data

2. **Addition**:
   - Adds two numbers together
   - Operation: A + B
   - May include carry in (Cᵢₙ) and carry out (Cₒᵤₜ)
   - Example: 0101 + 0011 = 1000

3. **Subtraction**:
   - Subtracts one number from another
   - Operation: A - B
   - Often implemented using 2's complement addition
   - Example: 1000 - 0011 = 0101

4. **Increment**:
   - Adds 1 to a number
   - Operation: A + 1
   - Special case of addition
   - Example: 0111 + 1 = 1000

5. **Decrement**:
   - Subtracts 1 from a number
   - Operation: A - 1
   - Special case of subtraction
   - Example: 1000 - 1 = 0111

### Complex Operations

6. **Multiplication**:
   - Multiplies two numbers
   - Operation: A × B
   - Usually implemented through repeated addition
   - Example: 0011 × 0010 = 0110

7. **Division**:
   - Divides one number by another
   - Operation: A ÷ B
   - Usually implemented through repeated subtraction
   - Example: 1000 ÷ 0010 = 0100

### Logical Operations (Often included with arithmetic)

8. **AND**:
   - Bitwise AND of two numbers
   - Operation: A AND B
   - Example: 1100 AND 1010 = 1000

9. **OR**:
   - Bitwise OR of two numbers
   - Operation: A OR B
   - Example: 1100 OR 1010 = 1110

10. **XOR**:
    - Bitwise XOR of two numbers
    - Operation: A XOR B
    - Example: 1100 XOR 1010 = 0110

### Special Operations

11. **Complement**:
    - One's complement: inverts all bits
    - Two's complement: one's complement + 1
    - Operation: NOT A or -(A)
    - Example: NOT 1100 = 0011

12. **Shift Operations**:
    - Logical shift: shifts bits left/right, fills with 0
    - Arithmetic shift: preserves sign bit
    - Rotate: circular shift of bits
    - Example: 1100 >> 1 = 0110 (logical right shift)

### Implementation Notes

- Most arithmetic circuits use combinations of:
  * Full adders (FA)
  * Multiplexers (MUX)
  * Logic gates
  * Registers
- Control signals determine which operation is performed
- Carry propagation is often a critical timing factor
- Many operations can be implemented using addition as the base operation

## Question 6: Register Complement using XOR [10 marks]

The question asks to determine the contents of Register B that will complement the four least significant bits of Register A using XOR operation. All registers are 8 bits wide.

### Problem Analysis

1. **Given Information**:
   - Register A contains some value (represented as XXXXXXXX)
   - Need to complement the four least significant bits only
   - Must use XOR operation
   - Register B is what we need to determine
   - Both registers are 8 bits wide

2. **XOR Properties**:
   - A XOR 0 = A (XOR with 0 keeps the original bit)
   - A XOR 1 = A' (XOR with 1 complements the bit)

### Solution Steps

1. **Desired Operation**:
   - Need to complement bits 0-3 (least significant bits)
   - Keep bits 4-7 unchanged

2. **Register B Value**:
   ```
   Register A: XXXXXXXX (where X represents any bit)
   Register B: 00001111
   Result:     XXXX(X'X'X'X') (complement of last 4 bits)
   ```

3. **Bit-by-bit Explanation**:
   - Bits 7-4: Set to 0 in B (to keep original A bits unchanged)
   - Bits 3-0: Set to 1 in B (to complement A bits)

### Answer: B = 00001111

The solution works because:
- XORing with 0 (bits 7-4): Preserves the original bits of A
- XORing with 1 (bits 3-0): Complements the bits of A
- This achieves the goal of complementing only the four least significant bits

### Verification
```
A = XXXXXXXX
B = 00001111
-----------------
R = XXXXX'X'X'X'  (where X' represents the complement of X)
```

This matches the red marking in the image showing B = 00001111 as the correct answer.

## Question 7: Register Microoperations [20 marks]

The question provides initial values for four 8-bit registers and asks to determine their values after executing three independent microoperations.

### Initial Register Values
```
AR = 11110010 = F2₁₆
BR = 11111111 = FF₁₆
CR = 10111001 = B9₁₆
DR = 11101010 = EA₁₆
```

### Microoperation 1: AR ← AR + BR

```
Step-by-step:
   AR = 1111 0010 (F2₁₆)
 + BR = 1111 1111 (FF₁₆)
 ---------------
   AR = 1111 0001 (F1₁₆) with carry out = 1
```

Result: AR = F1₁₆, BR = FF₁₆, CR = B9₁₆, DR = EA₁₆

### Microoperation 2: CR ← CR ∧ DR, BR ← BR + 1

Two parallel operations:
1. CR = CR AND DR:
```
CR = 1011 1001 (B9₁₆)
DR = 1110 1010 (EA₁₆)
-------------------
CR = 1010 1000 (A8₁₆)
```

2. BR Increment:
```
BR = 1111 1111 (FF₁₆)
 + 1
-----------------
BR = 0000 0000 (00₁₆)
```

Result: AR = F1₁₆, BR = 00₁₆, CR = A8₁₆, DR = EA₁₆

### Microoperation 3: AR ← AR - CR

```
Step-by-step:
   AR = 1111 0001 (F1₁₆)
 - CR = 1010 1000 (A8₁₆)
 ---------------
   AR = 0011 1001 (39₁₆)
```

Final Result: AR = 39₁₆, BR = FF₁₆, CR = B9₁₆, DR = EA₁₆

### Key Points:
1. Each operation is independent (results don't carry over)
2. All values are in 8-bit binary/hexadecimal
3. Operations include:
   - Addition (with possible carry)
   - Logical AND
   - Increment
   - Subtraction
4. Results match the red markings in the image for each step

### Working Method:
- Convert hex to binary when needed for operations
- Perform the operation carefully considering carries/borrows
- Convert result back to hexadecimal
- Keep track of which registers are affected by each operation
- Remember these are independent operations (don't use results from previous operations)
