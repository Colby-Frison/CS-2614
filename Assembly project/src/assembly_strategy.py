# This program follows the same strategy as the assembly code
# It takes a two-digit odd number, sums all odd numbers from it down to 1,
# and converts the result to octal

def divide_by_8(number):
    """
    Division by 8 using repeated subtraction
    Assembly equivalent:
    DIVIDE_BY_8, DEC 0
    STA VALTEMP
    CLA
    STA QUOTTEMP
    """
    valtemp = number  # Assembly: STA VALTEMP
    quotient = 0      # Assembly: CLA / STA QUOTTEMP
    
    print(f"\nDivision by 8 subroutine:")
    print(f"Starting with number: {valtemp}")
    print(f"Initial quotient: {quotient}")
    
    while True:
        # Assembly: DIV_LOOP, LDA VALTEMP
        # Assembly: ADD NEG8
        valtemp -= 8  # Subtract 8 (Assembly: ADD NEG8)
        print(f"Subtracting 8: {valtemp + 8} - 8 = {valtemp}")
        
        # Assembly: SPA
        # Assembly: BUN DIV_DONE
        if valtemp < 0:  # If negative, division is done
            print("Result is negative, division complete")
            break
        
        # Assembly: LDA QUOTTEMP
        # Assembly: INC
        # Assembly: STA QUOTTEMP
        quotient += 1  # Increment quotient
        print(f"Incrementing quotient: {quotient}")
    
    # Assembly: DIV_DONE, LDA VALTEMP
    # Assembly: ADD POS8
    # Assembly: STA REMTEMP
    remainder = valtemp + 8  # Add 8 back to get positive remainder
    print(f"Final remainder: {remainder}")
    print(f"Final quotient: {quotient}")
    
    return quotient, remainder

def main():
    # === Input Processing ===
    # Assembly equivalent: LOOPA, SKI / BUN LOOPA
    print("Enter a two-digit odd number:")
    tens = int(input("Enter tens digit: "))  # Assembly: INP
    ones = int(input("Enter ones digit: "))  # Assembly: INP
    
    # Convert ASCII to decimal (Assembly: ADD CON_TO_DEC)
    # In assembly, we subtract 48 from ASCII value
    # Here we just use the integer directly since Python handles the conversion
    
    # Multiply tens digit by 10 (Assembly: repeated ADD NUM)
    # In assembly, we add the number to itself 9 times
    # Here we just multiply by 10 directly
    number = tens * 10 + ones
    
    print(f"\nInput number: {number}")
    
    # === Odd Number Summation ===
    # Assembly equivalent: SUMLOOP
    sum_odd = 0  # Assembly: CLA / STA SUM
    current = number  # Assembly: LDA NUM
    
    print("\n=== Calculating Sum of Odd Numbers ===")
    print("Starting with number:", current)
    print("Initial sum:", sum_odd)
    print("\nAddition Process:")
    
    while current > 0:  # Assembly: SNA / BUN SUMLOOP
        print(f"Adding {current} to sum")
        sum_odd += current  # Assembly: LDA SUM / ADD NUM / STA SUM
        print(f"New sum: {sum_odd}")
        current -= 2  # Assembly: LDA NUM / ADD DECREMENT / STA NUM
        print(f"Next odd number: {current}")
        print("---")
    
    print(f"\nFinal sum of odd numbers: {sum_odd}")
    
    # === Decimal to Octal Conversion ===
    # Assembly equivalent: DIVIDE_BY_8 subroutine
    decimal = sum_odd  # Assembly: LDA SUM / STA DECIMAL
    octal_digits = []  # Will store digits in reverse order (LSB first)
    
    print("\n=== Converting to Octal ===")
    print(f"Starting with decimal value: {decimal}")
    
    # Get first digit (LSB)
    # Assembly: LDA DECIMAL / BSA DIVIDE_BY_8 / LDA REMTEMP / STA OCTALRES0
    print("\nCalculating first digit (LSB):")
    quotient, remainder = divide_by_8(decimal)
    octal_digits.append(remainder)
    decimal = quotient  # Assembly: LDA QUOTTEMP / STA DECIMAL
    
    # Get second digit
    # Assembly: LDA DECIMAL / BSA DIVIDE_BY_8 / LDA REMTEMP / STA OCTALRES1
    print("\nCalculating second digit:")
    quotient, remainder = divide_by_8(decimal)
    octal_digits.append(remainder)
    decimal = quotient
    
    # Get third digit
    # Assembly: LDA DECIMAL / BSA DIVIDE_BY_8 / LDA REMTEMP / STA OCTALRES2
    print("\nCalculating third digit:")
    quotient, remainder = divide_by_8(decimal)
    octal_digits.append(remainder)
    decimal = quotient
    
    # Get fourth digit (MSB)
    # Assembly: LDA DECIMAL / STA OCTALRES3
    print("\nCalculating fourth digit (MSB):")
    print(f"Final quotient: {decimal}")
    octal_digits.append(decimal)
    
    # Reverse the digits to get MSB first (as in assembly output)
    octal_digits.reverse()
    
    print("\nOctal digits (MSB to LSB):", octal_digits)
    
    # === Output ===
    # Assembly equivalent: OUTPUT_DONE section
    print("\n=== Final Output ===")
    print("Octal result: ", end="")
    for digit in octal_digits:
        # Assembly: LDA OCTALRESx / ADD CON_TO_ASCII / OUT
        # In assembly, we add 48 to convert to ASCII
        # Here we just print the digit directly
        print(digit, end="")
    print()  # Newline at end

if __name__ == "__main__":
    main() 