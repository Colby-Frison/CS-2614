# Assembly Program Documentation

## Overview
This program takes a two-digit odd number as input, calculates the sum of all odd numbers from that number down to 1, and then displays the result in octal format.

## Program Flow

### 1. Input Processing
The program uses two input loops to get a two-digit number:
- First loop (`LOOPA`) gets the tens digit
- Second loop (`LOOPB`) gets the ones digit

Each digit is processed as follows:
```assembly
LOOPA, SKI                  / loop for first input
BUN LOOPA                   / back to loop if no input
    CLA                     / Clear AC
    INP                     / get input (10s place)
    ADD CON_TO_DEC          / convert to decimal
```

The tens digit is multiplied by 10 using repeated addition:
```assembly
    / x10 by adding to itself 9 times
    ADD NUM
    ADD NUM
    ADD NUM
    ...
```

### 2. Odd Number Summation
The program calculates the sum of all odd numbers from the input number down to 1:
```assembly
SUMLOOP, LDA SUM            / start loop load sum
    ADD NUM                 / add current odd num to sum
    STA SUM                 / store new sum

    LDA NUM                 / load num
    ADD DECREMENT           / decrease by 2
    STA NUM                 / sta decremented num
    LDA NUM                 / reload num to check negative

    SNA                     / if num is < 0 skip call back to loop
    BUN SUMLOOP
```

### 3. Decimal to Octal Conversion
The sum is converted to octal using a division by 8 subroutine. The conversion process involves:

1. **Division Subroutine (DIVIDE_BY_8)**
```assembly
DIVIDE_BY_8, DEC 0          / Return address stored here
    STA VALTEMP             / Store the number to divide (dividend)
    CLA                     / Clear AC (Quotient = 0)
    STA QUOTTEMP            / Initialize quotient to 0

DIV_LOOP, LDA VALTEMP       / Load current value
    ADD NEG8                / Subtract 8
    STA VALTEMP             / Store updated value
    SPA                     / Skip if positive or zero
    BUN DIV_DONE            / If negative, division is done

    LDA QUOTTEMP            / Load quotient
    INC                     / Increment quotient
    STA QUOTTEMP            / Store updated quotient
    BUN DIV_LOOP            / Loop again

DIV_DONE, LDA VALTEMP       / Load the negative result
    ADD POS8                / Add 8 back to get remainder
    STA REMTEMP             / Store the remainder
    BUN DIVIDE_BY_8 I       / Return to caller
```

2. **Conversion Process**
   - The subroutine is called four times to get all octal digits
   - Each call:
     - Divides the current value by 8
     - Stores the remainder as an octal digit
     - Uses the quotient for the next division
   - The process starts with the least significant digit (LSB) and works up to the most significant digit (MSB)

3. **Implementation Details**
```assembly
/ First digit (LSB)
LDA DECIMAL             / Load current value
BSA DIVIDE_BY_8         / Call division subroutine
LDA REMTEMP             / Get remainder
STA OCTALRES0           / Store as least significant digit
LDA QUOTTEMP            / Get quotient
STA DECIMAL             / Update for next division

/ Second digit
LDA DECIMAL
BSA DIVIDE_BY_8
LDA REMTEMP
STA OCTALRES1
LDA QUOTTEMP
STA DECIMAL

/ Third digit
LDA DECIMAL
BSA DIVIDE_BY_8
LDA REMTEMP
STA OCTALRES2
LDA QUOTTEMP
STA DECIMAL

/ Fourth digit (MSB)
LDA DECIMAL             / The remaining value is the most significant digit
STA OCTALRES3           / Store it
```

4. **Key Variables Used**
   - `DECIMAL`: Stores the current value being converted
   - `OCTALRES0` to `OCTALRES3`: Store the four octal digits
   - `VALTEMP`: Temporary storage for division
   - `QUOTTEMP`: Stores the quotient during division
   - `REMTEMP`: Stores the remainder (octal digit)
   - `NEG8`: Constant -8 for subtraction
   - `POS8`: Constant 8 for remainder calculation

5. **Output Process**
   - The digits are stored in memory locations `OCTALRES0` to `OCTALRES3`
   - Output starts with the most significant digit (MSB)
   - Each digit is converted to ASCII by adding 48
   - Output is synchronized using SKO to ensure proper display

This conversion process ensures that the decimal sum is properly converted to a four-digit octal number, with each digit stored separately for output.

### 4. Output
The octal digits are output from most significant to least significant:
```assembly
OUTPUT_DONE, LDA OCTALRES3  / Start with most significant digit
    ADD CON_TO_ASCII        / Convert to ASCII
    OUT3, SKO
        BUN OUT3
    OUT                     / Output
```

## Key Components

### Variable Initialization
All variables and constants are initialized at the end of the program using the `DEC` pseudo-instruction:
```assembly
//=============== Variables ===================

/ variable for taking in input
NUM,  DEC 0

/ variables to handle odd sum
SUM, DEC 0
DECREMENT, DEC -2

/ variables for ASCII conversion
CON_TO_DEC, DEC -48         / convert ASCII to decimal
CON_TO_ASCII, DEC 48        / convert decimal to ASCII

/ Variables for octal conversion
NEG8, DEC -8                / subtraction constant
POS8, DEC 8
DECIMAL, DEC 0
REMAINDER, DEC 0
OCTALRES0, DEC 0            / Stores the final octal number
OCTALRES1, DEC 0            / Stores the second digit of octal number
OCTALRES2, DEC 0            / Stores the third digit of octal number
OCTALRES3, DEC 0            / Stores the fourth digit of octal number
REMTEMP, DEC 0              / Temporary storage for remainder
QUOTTEMP, DEC 0             / Temporary storage for quotient in subroutine
VALTEMP, DEC 0              / Temporary storage for intermediate value in subroutine
    END
```

Key points about variable initialization:
1. All variables are initialized to appropriate starting values
2. Constants are declared with their fixed values
3. Memory locations are reserved for all needed variables
4. Variables are grouped by their purpose (input, sum calculation, conversion)
5. Each variable has a descriptive comment explaining its use
6. The `END` directive marks the end of the program

### Registers Used
- AC (Accumulator): Main working register
- AR (Address Register): Used for memory addressing
- IC (Instruction Counter): Tracks program execution

### Memory Locations
- `NUM`: Stores the input number
- `SUM`: Stores the running sum of odd numbers
- `DECIMAL`: Working register for octal conversion
- `OCTALRES0-3`: Store the four octal digits
- `REMTEMP`: Temporary storage for division remainder
- `QUOTTEMP`: Temporary storage for division quotient
- `VALTEMP`: Temporary value storage

### Constants
- `CON_TO_DEC`: -48 (converts ASCII to decimal)
- `CON_TO_ASCII`: 48 (converts decimal to ASCII)
- `DECREMENT`: -2 (for odd number decrement)
- `NEG8`: -8 (for octal conversion)
- `POS8`: 8 (for remainder calculation)

## Debugging Tips
1. Watch the AC register during:
   - Input processing (should show ASCII values then decimal)
   - Sum calculation (should increment by odd numbers)
   - Octal conversion (should show remainders and quotients)
2. Monitor memory locations:
   - `NUM` should decrease by 2 each odd number iteration
   - `SUM` should accumulate the running total
   - `OCTALRES0-3` should fill with octal digits
3. Check the IC register to ensure proper program flow
4. Verify AR register during memory operations 