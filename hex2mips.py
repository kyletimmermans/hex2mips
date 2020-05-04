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
                 "11000":"$t8", "11001":"$t9", "11010":"$k0", "11011":"$k1", "11100":"$gp", "11101":"$sp", "11110":"fp", "11111":"$ra"}

# Fix the order of the input while loop below
def sanitize():
    global letters
    while True:  # Keep going until true
        print(" ")  # Prettify output
        hex = input("Enter Hex Code: ")
        if hex == 'n' or hex == 'N':  # Allow for exit on retry
            exit()
        if hex[0:2] == "0x":  # Remove 0x if present and non hex code
            hex = hex[2:]
        letters = list(letters)  # Make iterable and sliceable
        check = [item for item in (letters[6:25] or letters[32:52]) if(item in hex)]  #  Check for non-hex chars in 'hex' string
        if check or len(hex) != 8:  # if check is true or length too long
            print("Non-Hexadecimal Character(s) Found or Hex-Code too long")
            print("Try Again or Type 'n' or 'N' to exit")
        else:
            break
    # Convert hexadecimal to binary by converting to int
    binary = bin(int(hex, 16))[2:].zfill(32)  # 16 for hex base-16 system, zfill is zerofill to make it 32 chars total
    return binary  # Return the final binary string for h2m() to take


# Check instruction type
def h2m(bin):   # returns instruction
    if bin[0:6] == "000000":  # R-Formats always start with an op-code of "000000"
        rs, rt, rd, shamt, funct = bin[6:11], bin[11:16], bin[16:21], bin[21:26], bin[26:32]
        if funct == "001101":  # Break case
            print("This is an R-Format MIPS Instruction")
            instruction = str(functcode_dict[funct])+" "+str(int(bin[6:25], 2) * 2 )  # int(binary,2) to make decimal, 2nd parameter is the base we are converting from
            return instruction  # Needs the *2 in this case only, b/c always splits a break insturction code by 2
        elif rs and rt and rd and shamt == "00000" and funct == "001100":  # Create special case for syscall
            print("This is an R-Format MIPS Instruction")
            instruction = str(functcode_dict[funct])
            return instruction
        elif rt and rd and shamt == "00000" and funct == "001000":  # Create special case for jr instruction b/c it has special instructions
            print("This is an R-Format MIPS Instruction")
            instruction = str(functcode_dict[funct])+" "+str(register_dict[rs])
            return instruction
        elif shamt == "00000":  # Normal case
            print("This is an R-Format MIPS Instruction")
            instruction = str(functcode_dict[funct])+" "+str(register_dict[rd])+", "+str(register_dict[rs])+", "+str(register_dict[rt])
            return instruction
        elif funct == "000000" or funct == "000010":  # For sll and srl
            print("This is an R-Format MIPS Instruction")
            instruction = str(functcode_dict[funct])+" "+str(register_dict[rd])+", "+str(register_dict[rt])+", "+str(int(shamt, 2))
            return instruction                                          # int(binary,2) to make decimal, 2nd parameter is the base we are converting from
    elif bin[0:6] == ("000010" or "000011"):  # J-Formats are always these two opcodes, needs to wrap boolean statement with parenthesis to work properly
        op, address = bin[0:6], bin[6:31]
        print("This is a J-Format MIPS Instruction")
        instruction = str(opcode_dict[op])+" "+str(hex(int(address, 2)))  # 'bin' here refers to the binary string array e.g. bin[1:2], not bin() function
        return instruction
    else:  # I-Formats are everything else
        op, rs, rt, immediate = bin[0:6], bin[6:11], bin[11:16], bin[16:32]
        if op == "000101" or op == "000100":  # Special Instructions for bne and beq, they take an offset instead of a number at the end
            print("This is an I-Format Instruction")
            instruction = str(opcode_dict[op])+" "+str(register_dict[rs])+", "+str(register_dict[rt])+", "+str(hex(int(immediate, 2)))
            return instruction
        elif op == "100011" or op == "101011":   # Special Instructions for lw and sw
            print("This is an I-Format Instruction")
            instruction = str(opcode_dict[op])+" "+str(register_dict[rt])+", "+str(int(immediate, 2))+"("+str(register_dict[rs])+")"
            return instruction
        elif op == "001111":   # Special Instructions for lui
            print("This is an I-Format Instruction")
            instruction = str(opcode_dict[op])+" "+str(register_dict[rt])+", "+str(int(immediate, 2))
            return instruction
        else:  # Normal Case
            print("This is an I-Format Instruction")
            instruction = str(opcode_dict[op])+" "+str(register_dict[rs])+", "+str(register_dict[rt])+", "+str(int(immediate, 2))
            return instruction

# Driver
print("\nhex2mips by @KyleTimmermans")
repeat = 'Y'
while repeat == 'Y' or repeat == 'y':   # Needs second repeat == statement or boolean logic messes up ('n' won't cause an escape)
    binary = sanitize()
    instruction = h2m(binary)
    print(instruction+"\n")
    repeat = input("Convert more hex values? (Y/n): ")
