# Variables we'll need in assembly (using DEC pseudo-instruction)
first_digit = 0   # DEC 0
second_digit = 0  # DEC 0
number = 0        # DEC 0
sum = 0          # DEC 0
counter = 1      # DEC 1
temp = 0         # DEC 0 (for storing temporary values)

def split_number(n):
    """
    Splits a number into its individual digits using repeated subtraction.
    This simulates how we'll do it in assembly without division.
    
    In assembly:
    - We'll use LDA to load the number
    - Repeatedly subtract 10 using ADD with -10
    - Count how many times we can subtract (tens digit)
    - What's left is the ones digit
    """
    # Initialize variables
    tens = 0
    ones = n
    
    # Keep subtracting 10 until we can't anymore
    # In assembly:
    # SUB10, LDA ones
    # ADD NEG10      ; Subtract 10 using ADD with -10
    # SPA            ; Skip if result is positive
    # BUN DONE       ; If negative, we're done
    # STA ones       ; Store remaining value
    # LDA tens
    # INC            ; Increment tens count
    # STA tens
    # BUN SUB10      ; Continue subtraction loop
    while ones >= 10:
        ones = ones - 10
        tens = tens + 1
    
    return tens, ones

def multiply_by_10(n):
    # In assembly, multiplication by 10 using CIL (Circular shift left)
    # number × 10 = (number × 8) + (number × 2)
    
    # First get number × 2
    # LDA n     ; Load number to AC
    # CIL       ; Shift left (×2)
    # STA TEMP  ; Store ×2 result
    times2 = n + n
    
    # Now get number × 8
    # LDA TEMP  ; Load ×2 value
    # CIL       ; Shift left (×4)
    # CIL       ; Shift left (×8)
    # STA times8
    times8 = times2 + times2  # ×4
    times8 = times8 + times8  # ×8
    
    # Add them together
    # LDA times8
    # ADD TEMP  ; Add ×2 to get ×10
    return times8 + times2

def get_input():
    # Input handling using INP and checking with SKI
    # INLOOP, SKI      ; Check for input
    # BUN INLOOP       ; If no input, keep checking
    # INP             ; Get character into AC
    digit = input("Enter first digit: ")
    
    # Convert ASCII using ADD with negative constant
    # ADD NEG48       ; Subtract 48 (stored as negative for ADD)
    first_digit = ord(digit) - ord('0')
    
    # Multiply by 10 (see multiply_by_10 function)
    first_digit = multiply_by_10(first_digit)
    
    # Get second digit (same process with INP and SKI)
    digit = input("Enter second digit: ")
    second_digit = ord(digit) - ord('0')
    
    # Combine digits with ADD
    # LDA first_digit
    # ADD second_digit
    # STA number
    number = first_digit + second_digit
    return number

def calculate_sum(n):
    # Initialize using CLA and STA
    # CLA            ; Clear AC
    # STA sum        ; Initialize sum to 0
    # LDA n          ; Load input number
    # STA counter    ; Initialize counter
    sum = 0
    counter = n
    
    # Loop implementation using ISZ for countdown
    while True:
        # Add current odd number
        # LDA sum
        # ADD counter
        # STA sum
        sum = sum + counter
        
        # Decrement counter by 2
        # LDA counter
        # ADD NEG_TWO    ; NEG_TWO is stored as constant -2
        # STA counter
        counter = counter - 2
        
        # Check loop condition using ISZ (Increment and Skip if Zero)
        # ISZ counter    ; Decrement counter and skip if zero or negative
        # BUN LOOP       ; Branch back to loop start if counter > 0
        if counter < 1:
            break
    
    return sum

def convert_to_octal(decimal):
    """
    Converts a decimal number to octal using repeated subtraction.
    In assembly, we'll use these memory locations:
    - AC (Accumulator): Main working register
    - Memory locations:
      * decimal: Input number to convert (also used as quotient)
      * remainder: Remainder after division
      * count: How many times we subtracted 8
      * octal_digits: Array to store octal digits
    """
    # Initialize variables
    # CLA            ; Clear AC
    # STA count      ; Initialize count to 0
    count = 0
    octal_digits = []
    
    # Main conversion loop
    # LOOP, LDA decimal
    # SZA            ; Skip if decimal is zero
    # BUN CONVERT    ; If not zero, continue conversion
    # BUN END        ; If zero, we're done
    while decimal > 0:
        # Reset remainder and count for this digit
        # LDA decimal
        # STA remainder
        # CLA
        # STA count
        remainder = decimal
        count = 0
        
        # Division by 8 using repeated subtraction
        # DIV8, LDA remainder
        # ADD NEG8     ; NEG8 is -8 stored in memory
        # SPA          ; Skip if result positive
        # BUN DONE     ; If negative, we're done
        # STA remainder; Store new remainder
        # LDA count
        # INC          ; Increment count
        # STA count
        # BUN DIV8     ; Continue subtraction
        while remainder >= 8:
            remainder = remainder - 8
            count = count + 1
        
        # Store the remainder (current octal digit)
        # LDA remainder
        # STA octal_digits,I  ; Store at current digit pointer
        octal_digits.append(remainder)
        
        # Prepare for next digit
        # LDA count
        # STA decimal         ; New decimal is the count
        decimal = count
    
    return octal_digits

# Main program flow
def main():
    # Program will start with ORG to set starting address
    # ORG 100
    
    n = get_input()
    print(f"Input number: {n}")
    
    # Split the number to demonstrate the digit extraction
    tens, ones = split_number(n)
    print(f"Split into digits: {tens} and {ones}")
    
    result = calculate_sum(n)
    print(f"Sum: {result}")
    
    # Split the result to show how we'll display it
    result_tens, result_ones = split_number(result)
    print(f"Result split into digits: {result_tens} and {result_ones}")
    
    octal = convert_to_octal(result)
    print(f"Result in octal: {octal}")
    
    # Program ends with HLT
    # HLT            ; Stop execution

if __name__ == "__main__":
    main() 