# Assembly Project Design Document

## Introduction
The task for this project is to **take a 2-digits odd decimal number as user input, and write an assembly program to calculate the sum of odd positive numbers up to that odd decimal number, and then display the sum in octal**. On a higher level this can be done by counting up from 1 and adding the count to sum, it will then increment by 2 until the counter is equal to the input.

Doing this in assembly introduces a lot of difficulties however, to better explain each topic I will break it into a few sections:

1. The use of the assembly instructions in the problem-solving approaches
2. How to take in and convert input character into decimal number
3. Loop conditions for calculating the sum
4. How to convert the result into octal number and display it

## 1. Problem-Solving Approach Using Assembly Instructions

To complete the project I will need to keep two main categories of instructions in mind:

### Instructions for memory and data management:
- LDA and STA
   - These instructions will be used to load and store data, this is needed in almost every single main operation as data is constantly being moved and altered whether it be in loops, conversion, or inputs and outputs
- ADD, CIL, and CIR
   - ADD will be the primary way arithmetic is done simply adding to the AC or adding a negative number to subtract. This instruction will be used in every single major operation from adding numbers to the sum to handling input and output. CIL and CIR can also theoretically be used for multiplication/division, but without having done testing I cant be 100% sure
- BUN and BSA
   - BUN, which is an unconditional jump, is the core instruction for looping. Because of this it is necessary to be very familiar with this as without it the loop needed to complete a lot of the major operations will not be possible. BSA is for subroutines, I'm sure there are a lot of positive applications of it, but at the moment the main operation I think is important is BUN

### Instructions for processing data:  
- CLA and CLE
   - These instructions are quite simply, just clearing the AC or E register. These operations are good to use when starting an operation, or a lot of arithmetic is done that is independent from another.
- INC and ISZ
   - INC seems like it would be extremely useful for looping, but in our case we are counting odd numbers only meaning we are counting by 2, so either INC could be used twice, or just add 2 using a declared variable. ISZ on the will be very useful for loops as it can track loops, which will help keep track of loops which can be useful in conversion for the output
- SPA, SNA, and SZA
   - All of these are also instructions that are useful in handling loops as it can skip an operation that breaks the loop, meaning it can act as a sort of if statement to make loops conditionally end
- INP and OUT
   - These are simple instructions for taking the input and outputting AC

   
## 2. Input Processing and ASCII Conversion

### Getting the Input
The program needs to:
1. Get the first digit from input
   - Using INP to read character
   - Convert to decimal (explained later)
   - Multiply by 10 to put the number in the tens place
   - Store in num
3. Get the second digit
   - INP to get char
   - convert to decimal
   - add to num
4. Store full number in memory for use later

### Converting from ASCII to Numbers
When we get input characters, they're in ASCII. For example, if someone types "5", we actually get the ASCII value 53 (which is "5" in ASCII). To convert this to the actual number 5:
1. Take the ASCII character value
2. Subtract 48 (ASCII value for "0")
   - Add -48 since there is no subtraction instruction
3. For the first digit, multiply by 10 (2 ways)
   - Using CIL
      1. Use CIL for multiplication
      3. Shift left 3 times for times 8
      3. Then add to its self 2 more times to have a total of times 10
   - Using addition
      1. Simply add to itself 9 times to have a total of times 10
         - Although its simpler it uses more lines and could be seen as worse
4. for the second digit, its just adding converting and adding to sum

For example:
If input is "25":
- First digit "2": (50 - 48) × 10 = 20
- Second digit "5": (53 - 48) = 5
- Final number: 20 + 5 = 25

## 3. Loop Implementation and Conditions

### How to Do Loops in Assembly
Since assembly doesn't have while or for loops, we have to make our own using:
1. A counter variable in memory
   -  Store using STA, update with ADD
2. A way to change the counter (add or increment)
   - Using ADD or INC instructions
3. A way to check if it should continue looping
   - Using skip instructions (SPA, SNA, SZA)
4. A way to jump back to the start of the loop
   - Using BUN instruction

This will be the basic outline of loops which will be used for calculating the sum of odd number and for converting, spiting numbers, and handling inputs.

Since the sum of odd numbers is the key operation, I'll go a little more in depth on that operation.

### Loop Conditions for Sum Calculation
This is the basic outline of how calculating the sum of odd numbers will occur using a countdown approach:

Initial setup:
- Counter starts at input number (n)
  * Initialize using LDA to load input
- Sum starts at 0
  * Initialize using CLA

Each loop iteration:
1. Add current counter to sum
2. Subtract 2 from counter (to get next odd number down)
3. Check if counter is less than 1
   * There are many ways to control when to skip the BUN instruction, but a good one is ISZ to check if we've reached zero or gone negative
4. If counter >= 1, go back to step 1
   * Use BUN to return to loop start
5. If counter < 1, break

Example: If input is 7
- First iteration: sum = 0 + 7 = 7, counter = 5
- Second iteration: sum = 7 + 5 = 12, counter = 3
- Third iteration: sum = 12 + 3 = 15, counter = 1
- Fourth iteration: sum = 15 + 1 = 16, counter = -1
- Counter < 1, so stop. Result is 16

The task can be completed in a variety of ways, but counting down comes with a few advantages:
1. Simpler loop control
2. No need for complex comparison logic
3. Natural termination when we hit 1 or go below it
4. Produces the same result as counting up but with cleaner code

## 4. Converting to Octal and Display

To convert our decimal sum to octal:
1. Take the number we want to convert
   * Load using LDA
2. Keep dividing by 8 and saving the remainders
   * counting the number of times 8 is subtracted, remainder is when it cant be subtracted without going past 0
3. The remainders in reverse order give us the octal number
   * Store each digit temporarily

Example converting 16 to octal:
- 16 ÷ 8 = 2 remainder 0
- 2 ÷ 8 = 0 remainder 2
- Reading remainders bottom-up: 20 (octal)

Since we can't do division in assembly, we'll:
1. Repeatedly subtract 8
   * Add -8 using ADD instruction
2. Count how many times we can subtract
   * done by incrementing counter with INC
3. The remainder is what we couldn't subtract
   * Check using SNA for negative
4. Convert each digit to ASCII before output
   * Add 48 to get ASCII value
   * Use OUT to display

### Outputting Multi-Digit Numbers
When we need to display a number that's more than one digit, we need to:
1. Split the number into its digits
   - For a two-digit number:
      - Keep subtracting 10 until we can't anymore
      - Count how many times we subtracted (this is the tens digit)
      - What's left is the ones digit
2. Then use the above steps to convert the decimal to octal and then the octal to ASCII

This approach can then be extended for larger numbers by subtracting 100 for hundreds digit, etc.

## 5. Program Organization

The program will be organized in this order:
1. Set up memory for variables
   * Using ORG and DEC directives
2. Get and process input
3. Do the sum calculation loop
4. Convert to octal
5. Show the result
   * End with HLT instruction

## Memory Organization
We'll need to set up our memory with:
1. Variables (using DEC):
   - Input digits (2 locations)
   - Sum and counter
   - Temporary storage
2. Constants:
   - ASCII conversion (-48)
   - Loop increment (2)
   - Octal base (8)
3. Working space for calculations

## Testing Plan
I'll test the program systematically with different types of inputs:

### 1. Basic Functionality Tests
- Input: 13
  * Sum should be 1 + 3 + 5 + 7 + 9 + 11 + 13 = 49
  * Octal result should be 61
  * Tests basic odd number summing
  * Easy to verify manually

- Input: 15
  * Sum should be 1 + 3 + 5 + 7 + 9 + 11 + 13 + 15 = 64
  * Octal result should be 100
  * Tests handling of three-digit octal output

### 2. Edge Cases
- Input: 99 (largest possible input)
  * Tests handling of large numbers
  * Verifies no overflow in sum calculation
  * Checks multi-digit octal conversion

- Input: 11
  * Tests handling of repeated digits
  * Verifies ASCII to decimal conversion works correctly

### 3. Input Validation Tests
- Single digit inputs
  * Program should wait for second digit

- Even number inputs
  * Should handle appropriately based on requirements

- Non-numeric inputs
  * Test with letters or special characters
  * Verify program handles invalid input gracefully

### 4. Step-by-Step Verification
For each test case, I'll verify:
1. Input Processing
   * Correct ASCII to decimal conversion
   * Proper handling of both digits

2. Sum Calculation
   * Counter increments correctly
   * Sum accumulates properly
   * Loop terminates at right point

3. Octal Conversion
   * Correct remainders generated
   * Proper order of digits
   * ASCII conversion for output

### 5. Memory Usage
- Check that variables don't overflow
- Verify temporary storage is sufficient
- Ensure constants remain unchanged

This comprehensive testing approach will help ensure the program works correctly for all valid inputs and handles invalid inputs appropriately.

## Conclusion

### code outline
Here's the rough pseudo code outline of what I think the entire program will be:

```
Start Program:
    Set up memory locations for:
        - sum (start at 0)
        - counter (will hold input number)
        - temporary storage
        - first digit
        - second digit

Input Processing:
    Get first character from input
    Convert from ASCII to number by subtracting 48
    Multiply by 10 to put in tens place
    Store as first digit

    Get second character from input
    Convert from ASCII to number by subtracting 48
    Store as second digit

    Add first and second digits together
    Store result in counter

Sum Calculation:
    While counter is greater than or equal to 1:
        Add counter to sum
        Subtract 2 from counter
        Check if counter is still valid
        If valid, repeat loop

Octal Conversion:
    Copy sum to temporary storage
    Set up storage for octal digits

    While temporary storage is greater than 0:
        Repeatedly subtract 8 until we can't anymore
        Count how many times we subtracted
        Store the count as an octal digit
        What's left is the remainder
        Store the remainder as next octal digit
        Continue with the count as new number

Output:
    For each octal digit (starting from last one stored):
        Convert digit to ASCII by adding 48
        Output the ASCII character

End Program
```

Key points about the implementation:
1. All arithmetic operations (multiplication, division, modulo) will be implemented using repeated addition/subtraction
2. The octal conversion will store digits in memory in reverse order
3. The output will need to handle multiple digits by converting each to ASCII
4. Memory management will be crucial for storing intermediate values
5. The program will need to handle edge cases like single-digit inputs

### Outlook
After working through all the pieces of this project, I can see how breaking it down makes it much less overwhelming. Each part has its own challenges - like figuring out how to multiply by 10 without a multiply instruction, or converting to octal without division - but by solving one small problem at a time, the whole thing becomes doable.

The trickiest parts will probably be the ASCII conversion and the octal display, since they involve a lot of careful memory management and bit manipulation. I'll need to test these parts thoroughly to make sure they work correctly. Even though assembly is much more basic than the high-level languages I'm used to, it's interesting to see how we can build complex operations from simple instructions.

I think my testing plan will help catch any issues early, especially with edge cases like large numbers or invalid inputs. The key will be making sure each part works perfectly before moving on to the next, since debugging assembly code can be pretty challenging. 