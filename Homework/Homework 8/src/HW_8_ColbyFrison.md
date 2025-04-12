# Homework 8

**Name**: Colby Frison
**OUID**: 113568816
**Date**: 4/11/2025
**Class**: CS-2614

# Questions

## 1. Problem 5-2 ~ 

**What is the difference between a direct and an indirect address instruction? How many references to memory are needed for each type of instruction to bring an operand into a processor register?**

**Answer:**
- **Direct Addressing:** The address field contains the effective address of the operand. Only one memory reference is needed to access the operand.
- **Indirect Addressing:** The address field points to a memory location that contains the effective address of the operand. Two memory references are needed: one to get the effective address and another to access the operand.

## 2. Problem 5-4 ~ 

**For each transfer, specify: (1) the binary value for bus select inputs \( S_2, S_1, \) and \( S_{0i} \); (2) the register whose LD control input must be active; (3) a memory read or write operation (if needed); and (4) the operation in the adder and logic circuit (if any).**

- **a. \( AR \leftarrow PC \)**
  1. Binary value: S₂S₁S₀ = 010 (selects PC which is connected to bus input 2)
  2. LD control: AR
  3. Memory operation: None
  4. Adder/Logic: None

- **b. \( IR \leftarrow M[AR] \)**
  1. Binary value: S₂S₁S₀ = 111 (selects Memory data output which is connected to bus input 7)
  2. LD control: IR
  3. Memory operation: Read
  4. Adder/Logic: None

- **c. \( M[AR] \leftarrow TR \)**
  1. Binary value: S₂S₁S₀ = 110 (selects TR which is connected to bus input 6)
  2. LD control: None
  3. Memory operation: Write
  4. Adder/Logic: None

- **d. \( AC \leftarrow DR, DR \leftarrow AC \) (done simultaneously)**
  1. Binary value: For AC←DR: S₂S₁S₀ = 011 (selects DR which is connected to bus input 3)
                   For DR←AC: S₂S₁S₀ = 100 (selects AC which is connected to bus input 4)
  2. LD control: AC, DR
  3. Memory operation: None
  4. Adder/Logic: None

## 3. Problem 5-7 ~ 

**What are the two instructions needed in the basic computer to set the E flip-flop to 1?**

**Answer:**
1. **CLA (Clear Accumulator):** Clears the accumulator.
2. **CME (Complement E):** Complements the E flip-flop, setting it to 1.

## 4. Problem 5-8 ~ 

**Draw a timing diagram similar to Fig. 5-7 assuming that SC is cleared to 0 at time \( T_3 \) if control signal \( C_7 \) is active.**

**Answer:**
The timing diagram would show the following signals (from top to bottom):
1. Clock: Continuous square wave pulses through T₀ → T₄
2. T₀: Active during first time slot, then repeats after T₃ (due to early clear)
3. T₁: Active during second time slot
4. T₂: Active during third time slot
5. T₃: Active briefly, then terminates due to C₇
6. T₄: Would not become active due to SC being cleared at T₃
7. D₃: Follows the same pattern as shown in Fig. 5-7 until T₃
8. CLR SC: Would show a pulse at T₃ when C₇ is active

Key differences from Fig. 5-7:
- The sequence terminates at T₃ instead of continuing to T₄
- A new cycle begins immediately after T₃ (shown by T₀ becoming active)
- The timing sequence becomes: T₀ → T₁ → T₂ → T₃ → T₀ (skipping T₄)
- Total cycle length is shortened by one time unit 