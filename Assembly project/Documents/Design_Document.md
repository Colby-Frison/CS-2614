# Assembly Project Design Document

## Introduction
For this project, I'm going to write an assembly program that does a few things: first, it takes a two-digit odd number from the user, then it adds up all the odd numbers from 1 up to that number, and finally shows the answer in octal. I know this would be pretty straightforward in a high-level language like Python or Java, but doing it in assembly is trickier since we don't have all those built-in functions and features.

To make this manageable, I'm breaking it down into smaller pieces that I can tackle one at a time. This document explains my plan for how to handle each part of the problem. Since we're limited to basic assembly instructions, I'll need to figure out ways to do things like multiplication and division using just the basic operations we have available.

## Breaking Down the Problem
The main problem can be split into four main parts:
1. Getting and processing the input
2. Converting ASCII input to actual numbers
3. Calculating the sum of odd numbers
4. Converting the result to octal and displaying it

## 1. Problem-Solving Approach Using Assembly Instructions

To solve this problem, I'll need to use several types of assembly instructions:

For handling memory and data:
- Load and Store instructions to move data between memory and the accumulator
  * Using LDA to load values and STA to store them
- Add instructions for arithmetic
  * ADD for addition, and adding negative numbers for subtraction
- Branch instructions to control program flow
  * BUN for unconditional jumps, BSA for subroutines

For processing:
- Clear instructions to reset registers
  * CLA to clear accumulator, CLE for E bit
- Increment instructions for counting
  * INC to add 1, ISZ for loop control
- Skip instructions for making decisions
  * SPA, SNA, SZA for condition checking
- Input/Output instructions for user interaction
  * INP for getting input, OUT for display

## 2. Input Processing and ASCII Conversion

### Getting the Input
The program needs to:
1. Get the first digit from input
   * Using INP to read character
   * Checking input flag if needed
2. Store it somewhere in memory
   * Using STA to save in memory
3. Get the second digit
4. Store it in a different memory location

### Converting from ASCII to Numbers
When we get input characters, they're in ASCII. For example, if someone types "5", we actually get the ASCII value 53 (which is "5" in ASCII). To convert this to the actual number 5:
1. Take the ASCII character value
   * Using LDA to get stored value
2. Subtract 48 (ASCII value for "0")
   * Add -48 since we only have ADD
3. For the first digit, multiply by 10 (will explain how in the assembly)
   * Using CIL for multiplication
    * Shift left three times for ×8
    * Then add 2 times for to finish x10
4. Add the second digit's value
   * Using ADD after conversion

For example:
If input is "25":
- First digit "2": (50 - 48) × 10 = 20
- Second digit "5": (53 - 48) = 5
- Final number: 20 + 5 = 25

## 3. Loop Implementation and Conditions

### How to Do Loops in Assembly
Since assembly doesn't have while or for loops, we have to make our own using:
1. A counter variable in memory
   * Store using STA, update with ADD
2. A way to change the counter (add or increment)
   * Using ADD or INC instructions
3. A way to check if it should continue looping
   * Using skip instructions (SPA, SNA, SZA)
4. A way to jump back to the start of the loop
   * Using BUN instruction

### Loop Conditions for Sum Calculation
For calculating the sum of odd numbers:

Initial setup:
- Counter starts at 1 (first odd number)
  * Initialize using CLA and INC
- Sum starts at 0
  * Initialize using CLA
- Input number is our end point
  * Store in memory with STA

Each loop iteration:
1. Add current counter to sum
2. Add 2 to counter (to get next odd number)
3. Check if counter is bigger than input
   * Add negative of input number
   * Use SPA to check if result is positive
4. If not bigger, go back to step 1
   * Use BUN to return to loop start
5. If bigger, break

Example: If input is 7
- First iteration: sum = 0 + 1 = 1, counter = 3
- Second iteration: sum = 1 + 3 = 4, counter = 5
- Third iteration: sum = 4 + 5 = 9, counter = 7
- Fourth iteration: sum = 9 + 7 = 16, counter = 9
- Counter > 7, so stop. Result is 16

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
   * Increment counter with INC
3. The remainder is what we couldn't subtract
   * Check using SNA for negative
4. Convert each digit to ASCII before output
   * Add 48 to get ASCII value
   * Use OUT to display

### Outputting Multi-Digit Numbers
When we need to display a number that's more than one digit, we need to:
1. Split the number into its digits
   - For a two-digit number:
     * Keep subtracting 10 until we can't anymore
     * Count how many times we subtracted (this is the tens digit)
     * What's left is the ones digit
2. Convert each digit to ASCII
   - Add 48 (ASCII '0') to each digit
3. Output the digits in order
   - First output the tens digit
   - Then output the ones digit

Example for number 25:
1. Split into digits:
   - Subtract 10 twice (tens digit = 2)
   - Remainder is 5 (ones digit)
2. Convert to ASCII:
   - 2 + 48 = 50 (ASCII '2')
   - 5 + 48 = 53 (ASCII '5')
3. Output:
   - First OUT displays '2'
   - Second OUT displays '5'

This same approach can be extended for larger numbers by subtracting 100 for hundreds digit, etc.

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
After working through all the pieces of this project, I can see how breaking it down makes it much less overwhelming. Each part has its own challenges - like figuring out how to multiply by 10 without a multiply instruction, or converting to octal without division - but by solving one small problem at a time, the whole thing becomes doable.

The trickiest parts will probably be the ASCII conversion and the octal display, since they involve a lot of careful memory management and bit manipulation. I'll need to test these parts thoroughly to make sure they work correctly. Even though assembly is much more basic than the high-level languages I'm used to, it's interesting to see how we can build complex operations from simple instructions.

I think my testing plan will help catch any issues early, especially with edge cases like large numbers or invalid inputs. The key will be making sure each part works perfectly before moving on to the next, since debugging assembly code can be pretty challenging. 