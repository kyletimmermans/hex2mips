from string import ascii_letters as letters  # a-zA-Z

# For R-Types
functcode_dict = {"100000":"add", "100001":"addu", "100010":"sub", "100011":"subu", "100100":"and", "100100":"or", "100111":"nor",
                  "101010":"slt", "101011":"sltu", "000000":"sll", "000010":"srl", "011000":"mult", "011001":"multu", "011010":"div",
                  "011011":"divu", "100110":"xor", "001000":"jr", "001100":"syscall", "001101":"break"}

# For I/J-Type
opcode_dict = {"000100":"beq", "000101":"bne", "001000":"addi", "001001":"addiu", "001100":"andi", "001101":"ori", "001010":"slti",
               "001011":"sltiu", "001111":"lui", "100011":"lw", "101011":"sw", "001110":"xori", "100000":"lb", "100100":"lbu",
               "000010":"j", "000011":"jal"}

# For register naming
register_dict = {"00000":"$zero", "00001":"$at", "00010":"$v0", "00011":"$v1", "00100":"$a0", "00101":"$a1", "00110":"$a2", "00111":"$a3",
                 "01000":"$t0", "01001":"$t1", "01010":"$t2", "01011":"$t3", "01100":"$t4", "01101":"$t5", "01110":"$t6", "01111":"$t7",
                 "10000":"$s0", "10001":"$s1", "10010":"$s2", "10011":"$s3", "10100":"$s4", "10101":"$s5", "10110":"$s6", "10111":"$s7",
                 "11000":"$t8", "11001":"$t9", "11010":"$k0", "11011":"$k1", "11100":"$gp", "11101":"$sp", "11110":"fp", "11110":"$ra"}

# Fix the order of the input while loop below
def sanitize():
    global letters
    while True:  # Keep going until true
        hex = input("Enter Hex Code: ")
        if hex[0:2] == "0x":  # Remove 0x if present and non hex code
            hex = hex[2:]
        letters = list(letters)  # Make iterable and sliceable
        check = [item for item in (letters[6:25] or letters[32:52]) if(item in hex)]  #  Check for non-hex chars in 'hex' string
        if check or len(hex) > 8:  # if check is true or length too long
            print("Non-Hexadecimal Character(s) Found or Hex-Code too long")
            print("Try Again")
        else:
            break
    # Convert hexadecimal to binary by converting to int
    binary = bin(int(hex, 16))[2:].zfill(32)  # 16 for hex base-16 system, 32 bits for output, zfill is zerofill to make it 32 chars total
    return binary  # Return the final binary string for h2m() to take


# Check instruction type
def h2m(bin):   # returns instruction
    if bin[0:6] == "000000":  # R-Formats always start with an op-code of "000000"
        rs, rt, rd, shamt, funct = bin[6:11], bin[11:16], bin[16:21], bin[21:26], bin[26:32]
        if funct == "001101":  # Break case
            print("This is a non-format system instruction")
        if shamt == "00000":  # Normal case
            print("This is an R-Format MIPS Instruction")
            instruction = str(functcode_dict[funct])+" "+str(register_dict[rd])+", "+str(register_dict[rs])+", "+str(register_dict[rt])
            return instruction
        else:  # For sll and srl
            print("This is an R-Format MIPS Instruction")
            #return instruction
        if rt and rd and shamt == "00000" and funct == "001000":  # Create special case for jr instruction b/c it has special instructions
            print("This is an R-Format MIPS Instruction")
            #return instruction
        if rs and rt and rd and shamt == "00000" and funct == "001100":  # Create special case for syscall
            print("This is non-format system instruction")
            #return instruction
    elif bin[0:6] == "000010" or "000011":  # J-Formats are always these two opcodes
        #op, rs, rt, immediate =
        print("This is a J-Format MIPS Instruction")
        #return instruction
    else:  # I-Formats are everything else
        #op, address =
        print("This is an I-Format MIPS Instruction")
        #return instruction

# Driver
print("\nhex2mips by @KyleTimmermans\n")
repeat = 'Y'
while repeat == 'Y' or repeat == 'y':   # Needs second repeat == statement or boolean logic messes up ('n' won't cause an escape)
    binary = sanitize()                 # Otherwise "if 'y'" just checks if 'n' is a string, which it is
    instruction = h2m(binary)
    print(instruction+"\n")
    repeat = input("Convert more hex values? (Y/n): ")
