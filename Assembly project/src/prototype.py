# Variables we'll need in assembly (using DEC pseudo-instruction)
first_digit = 0   # DEC 0
second_digit = 0  # DEC 0
number = 0        # DEC 0
sum = 0          # DEC 0
counter = 1      # DEC 1
temp = 0         # DEC 0 (for storing temporary values)

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
    # LDA ONE        ; Load 1
    # STA counter    ; Initialize counter
    sum = 0
    counter = 1
    
    # Loop implementation using BUN for branching
    while True:
        # Add current odd number
        # LDA sum
        # ADD counter
        # STA sum
        sum = sum + counter
        
        # Increment counter by 2
        # LDA counter
        # ADD TWO        ; TWO is stored as constant 2
        # STA counter
        counter = counter + 2
        
        # Check loop condition using SPA (Skip if Positive)
        # LDA counter
        # ADD NEG_N      ; Add negative of input (for comparison)
        # SPA            ; Skip next instruction if counter > n
        # BUN LOOP       ; Branch back to loop start if counter <= n
        if counter > n:
            break
    
    return sum

def convert_to_octal(decimal):
    # We'll implement octal conversion using repeated subtraction
    quotient = decimal
    octal = ""
    
    while quotient > 0:
        # Get remainder using repeated subtraction
        # Uses: LDA, ADD (with negative 8), SPA, BUN
        remainder = quotient
        count = 0
        
        # Subtraction loop
        # SUB8, LDA remainder
        # ADD NEG8        ; Subtract 8 using ADD with -8
        # SPA            ; Skip if result positive
        # BUN DONE       ; If negative, we're done
        # STA remainder  ; Store remaining value
        # LDA count
        # INC            ; Increment quotient count
        # STA count
        # BUN SUB8       ; Continue subtraction loop
        while remainder >= 8:
            remainder = remainder - 8
            count = count + 1
        
        # Convert to ASCII using ADD
        # LDA remainder
        # ADD ASCII0      ; Add 48 to get ASCII value
        # OUT            ; Output the character
        octal = str(remainder) + octal
        quotient = count
    
    return octal

# Main program flow
def main():
    # Program will start with ORG to set starting address
    # ORG 100
    
    n = get_input()
    print(f"Input number: {n}")
    
    result = calculate_sum(n)
    print(f"Sum: {result}")
    
    octal = convert_to_octal(result)
    print(f"Result in octal: {octal}")
    
    # Program ends with HLT
    # HLT            ; Stop execution

if __name__ == "__main__":
    main() 