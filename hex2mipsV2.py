'''
Kyle Timmermans
hex2mips
python 3.9.2
March 14, 2021

"Entirety of program revolves around converting hex or MIPS instruction
to binary (op, rs, rt, rd, shamt, funct) and then how to order
the binary strings into one final piece so we can get either type"

            h2m()                           m2h()
         0x12345678                      add $t12 $t14
         /    |   \                      /    |    \
      01010 01011 10110               01010 01011 10110
      \      |      /                   \     |     /
      add   $t12  $a14                   0x12345678

'''

from string import ascii_letters as letters  # a-zA-Z
from string import printable as symbols
import re

# For R-Types
functcode_dict = {"100000":"add", "100001":"addu", "100010":"sub", "100011":"subu", "100100":"and", "100101":"or", "100111":"nor",
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


# For m2h()
normalRFormat = ["add", "addu", "sub", "subu", "and", "or", "nor", "slt", "sltu", "mult", "multu", "div", "divu", "xor"]
normalIFormat = ["addi", "addiu", "andi", "ori", "slti", "sltiu", "xori"]


# Input string, check if hex or mips, sanitize, return binary string
def inputSanitize():
    global letters, symbols
    check = ["neither", "content"]   # Init check, check[0] is typ, check[1] is the binary
    while True:
        print(" ")  # Prettify output
        check[1] = input("Enter Hex Code or MIPS Instruction: ")
        if check[1] == 'n' or check[1] == 'N':  # Allow for exit on retry
            exit()
        if len(check[1]) == 0:  # If entry is empty
            print("Nothing entered, Try Again")
            continue  # Return to top of loop
        if check[1][0:2] == "0x":  # If hex, remove 0x if present and non hex code
            check[0] = "hex"
            check[1] = check[1][2:]
            letters = list(letters)  # Make iterable and sliceable
            nonHexCheck = [item for item in (letters[6:25] or letters[32:52] or symbols[62:93]) if(item in check[1])]  #  Check for non-hex chars in 'hex' string (lowercase and uppercase and symbols)
            if nonHexCheck or len(check[1]) != 8:  # if letterCheck is true or length too long
                print("Non-Hexadecimal Character(s) found or Hex-Code too long/short")
                print("Try Again or Type 'n' or 'N' to exit")
                continue  # Go back to top of loop to try again
            else:
                check[1] = bin(int(check[1], 16))[2:].zfill(32)  # 16 for hex base-16 system, zfill is zerofill to make it 32 chars total
                return check  # Return the final binary string for h2m() to take
                break
        else:  # If not hex, then must be mips instruction
            check[0] = "mips"
            nonInstructionCheck = [item for item in (symbols[62:64] or symbols[66:71] or symbols[71:72] or symbols[74:99]) if(item in check[1])]  # Check for symbols that is not '(' ')' ',' '$'
            if nonInstructionCheck:
                print("Invalid symbol found in Instruction string, Try Again")
                continue
            else:
                return check



# Check instruction type and make hex into mips
def h2m(bin):   # returns instruction
    if bin[0:6] == "000000":  # R-Formats always start with an op-code of "000000"
        rs, rt, rd, shamt, funct = bin[6:11], bin[11:16], bin[16:21], bin[21:26], bin[26:32]
        if funct == "001101":  # Break case
            try:
                print("This is an R-Format MIPS Instruction")
                instruction = str(functcode_dict[funct])+" "+str(int(bin[6:25], 2) * 2 )  # int(binary,2) to make decimal, 2nd parameter is the base we are converting from
            except KeyError:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction  # Needs the *2 in this case only, b/c always splits a break instruction code by 2
        elif rs and rt and rd and shamt == "00000" and funct == "001100":  # Create special case for syscall
            try:
                print("This is an R-Format MIPS Instruction")
                instruction = str(functcode_dict[funct])
            except KeyError:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction
        elif rt and rd and shamt == "00000" and funct == "001000":  # Create special case for jr instruction b/c it has special instructions
            try:
                print("This is an R-Format MIPS Instruction")
                instruction = str(functcode_dict[funct])+" "+str(register_dict[rs])
            except KeyError:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction
        elif shamt == "00000":  # Normal case
            try:
                print("This is an R-Format MIPS Instruction")
                instruction = str(functcode_dict[funct])+" "+str(register_dict[rd])+", "+str(register_dict[rs])+", "+str(register_dict[rt])
            except KeyError:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction
        elif funct == "000000" or funct == "000010":  # For sll and srl
            try:
                print("This is an R-Format MIPS Instruction")
                instruction = str(functcode_dict[funct])+" "+str(register_dict[rd])+", "+str(register_dict[rt])+", "+str(int(shamt, 2))
            except KeyError:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction                                          # int(binary,2) to make decimal, 2nd parameter is the base we are converting from
    elif bin[0:6] == "000010" or bin[0:6] == "000011":  # J-Formats are always these two opcodes, needs to wrap boolean statement with parenthesis to work properly
        op, address = bin[0:6], bin[6:31]
        try:
            print("This is a J-Format MIPS Instruction")
            instruction = str(opcode_dict[op])+" "+str(hex(int(address, 2)))  # 'bin' here refers to the binary string array e.g. bin[1:2], not bin() function
        except KeyError:
            print("Not a valid Hex code, Try Again")
            return 1
        return instruction
    else:  # I-Formats are everything else
        op, rs, rt, immediate = bin[0:6], bin[6:11], bin[11:16], bin[16:32]
        if op == "000101" or op == "000100":  # Special Instructions for bne and beq, they take an offset instead of a number at the end
            try:
                print("This is an I-Format Instruction")
                instruction = str(opcode_dict[op])+" "+str(register_dict[rs])+", "+str(register_dict[rt])+", "+str(hex(int(immediate, 2)))
            except KeyError:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction
        elif op == "100011" or op == "101011" or op == "100000" or op == "100100":   # Special Instructions for lw, sw, lb, lbu
            try:
                print("This is an I-Format Instruction")
                instruction = str(opcode_dict[op])+" "+str(register_dict[rt])+", "+str(int(immediate, 2))+"("+str(register_dict[rs])+")"
            except KeyError:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction
        elif op == "001111":   # Special Instructions for lui
            try:
                print("This is an I-Format Instruction")
                instruction = str(opcode_dict[op])+" "+str(register_dict[rt])+", "+str(int(immediate, 2))
            except:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction
        else:  # Normal Case
            try:
                print("This is an I-Format Instruction")
                instruction = str(opcode_dict[op])+" "+str(register_dict[rs])+", "+str(register_dict[rt])+", "+str(int(immediate, 2))
            except KeyError:
                print("Not a valid Hex code, Try Again")
                return 1
            return instruction



# Used with m2h
def getRegisters(registersList):
    reg1, reg2, reg3 = "err", "err", "err"  # If these never get changed, register was not found
    for i in range(len(registersList)):
        for key, value in register_dict.items():
            if i == 0 and registersList[i] == value:
                reg1 = key
            elif i == 1 and registersList[i] == value:
                reg2 = key
            elif i == 2 and registersList[i] == value:
                reg3 = key
        if i == 0 and registersList[i].isdigit():  # Register can also just be an int for I format instructions
            reg1 = bin(registersList[i])[2:]  # Then convert to binary
        elif i == 1 and registersList[i].isdigit():
            reg2 = bin(registersList[i])[2:]
        elif i == 2 and registersList[i].isdigit():
            reg3 = bin(registersList[i])[2:]
        if i == 0 and 'x' in registersList[i]:  # Register can also just be hex for I format instructions
            reg1 = bin(int(registersList[i], 16))[2:]
        elif i == 1 and 'x' in registersList[i]:
            reg2 = bin(int(registersList[i], 16))[2:]
        elif i == 2 and 'x' in registersList[i]:
            reg3 = bin(int(registersList[i], 16))[2:]
    if (len(registersList)) == 3:   # Some codes have 3
        if reg1 == "err" or reg2 == "err" or reg3 == "err":
            print("Invalid register(s), Try Again")
            return 1
    else:
        return reg1, reg2, reg3
    if (len(registersList)) == 2:  # Some codes have 2
        if reg1 == "err" or reg2 == "err":
            print("Invalid register(s), Try Again")
            return 1
    else:
        return reg1, reg2



# Mips instruction to hex
def m2h(instruction):
    shamt = "00000"  # Need to be added in for R format instructions, always the same
    funct = "100000"
    newInstruction = instruction.replace(" ", "")  # Remove spaces
    if ',' in newInstruction: # Split string up by comma if R format or I format
        splitString = newInstruction.replace(")", "")  # Get rid of trailing )
        splitString = re.split('[\,\(]', splitString)  # Split everything by comma and parenthesis, put in a list
        splitString[0] = re.split('([\$])', splitString[0])  # Split first item e.g. add$t5 becomes ['add', '$', 't5']
        splitString[0][1:3] = [''.join(splitString[0][1:3])] # Join $ and t5 in the substring, so now we have [['add', '$t5'], '$t4', '$t3']
        temp = [item for sublists in splitString for item in sublists if isinstance(sublists, list)]  # Flatten first list
        temp2 = splitString  # Hold onto old values while we reassign splitString
        splitString = temp   # Assign the flattened values of index 1, e.g. 'add' and '$t5'
        splitString.extend([temp2[1], temp2[2]])  # Put it all together e.g. ['add', '$t5'] + ['$t4'] + ['$t3'] = ['add', '$t5', '$t4', 't3']
        if len(splitString) > 4 or len(splitString) < 2:  # If too many or two few arguments
            print("Too many/few arguments for MIPS instruction, Try Again")
            return 1
        # Check first list item, the instruction, if its in
        for key, value in functcode_dict.items():  # Check if it's in functcode dictionary first
            if splitString[0] == value:   # If funct code matches one of the values, then append binary
                op = key, op_value = value
        for key, value in opcode_dict.items():  # Check opcodes next if we didn't find the command in functcodes_dict
            if splitString[0] == value:  # If funct code matches one of the values, then append binary
                op = key, op_value = value
        try:
            op
        except NameError:
            print("Invalid or unrecognized op code, Try Again")
            return 1
        # Depending on the op code, have to do certain things with the registers
        registers = splitString[1:]  # From index 1, because index 0 was handled already as the instruction code
        registerList = list(getRegisters(registers))
        if registerList == 1:  # Invalid register somewhere
            return 1
        else:     # finalHex is the binary string to be converted to hex
            if op_value == "syscall":   # R and I formats that don't follow the normal format
                finalHex = op + shamt + funct
            elif op_value == "break":
                finalHex = op + splitString[1] + shamt + funct   # Break + breakpoint which is only other field
            elif op_value == "lw" or op_value == "sw" or op_value == "lb" or op_value == "lbu":
                finalHex = op
            elif op_value == "lui":
                finalHex = op
            elif op_value in normalRFormat:  # Normal R instruction
                finalHex = op + registerList[0] + registerList[1] + registerList[2] + shamt + funct
            elif op_value in normalIFormat:  # Normal I instruction
                finalHex = op + registerList[0] + registerList[2] + registerList[1]
    else:  # If not R or I instruction, then treat differently bc it's J format, except for jr
        # Check op code
        if newInstruction[0] == 'j' and newInstruction[1] != 'r' and newInstruction[1] != 'a':  # Check if it's only j, not jr or jal
            op_value = "j"
        elif newInstruction[0] == 'j' and newInstruction[1] == 'r':  # Check if its jr
            op_value = "jr"
        elif newInstruction[0] == 'j' and newInstruction[1] == 'a' and newInstruction[2] == 'l':  # Check if it's jal
            op_value = "jal"
        else:
            print("Invalid or unrecognized op code, Try Again")  # None of the j codes recognized either, try again
            return 1
        if len(newInstruction) > 4 or len(newInstruction) < 2:  # If too many or too few arguments
            print("Too many/few arguments for MIPS instruction, Try Again")
            return 1
        # Only three op codes, dont need to search through functcode_dict or opcode_dict
        if op_value == "jr":
            try:
                finalHex = list(functcode_dict.keys())[list(functcode_dict.values()).index(op_value)] + list(register_dict.keys())[list(register_dict.values()).index(instruction[2:])]    # One liner for dict value -> key from G4G
            except KeyError:
                print("Invalid register(s), Try Again")
                return 1
        elif op_value == "j":  # Normal cases
            try:
                finalHex = list(functcode_dict.keys())[list(opcode_dict.values()).index(op_value)] + list(register_dict.keys())[list(register_dict.values()).index(instruction[1:])]  # String splice is just the one register used
            except KeyError:
                print("Invalid register(s), Try Again")
                return 1
        elif op_value == "jal":
            try:
                finalHex = list(functcode_dict.keys())[list(opcode_dict.values()).index(op_value)] + list(register_dict.keys())[list(register_dict.values()).index(instruction[3:])]
            except:
                print("Invalid register(s), Try Again")
                return 1
    return hex(bin(int(finalHex, 2)).zfill(32))    # Return as Binary String -> Binary Literal -> Hex

# Driver
print("\nhex2mips by @KyleTimmermans")
print("Notice: Labels must be entered as hexadecimal")
repeat = 'Y'
while repeat == 'Y' or repeat == 'y':
   firstInput = inputSanitize()
   if firstInput[0] == "hex":
        binary = firstInput[1]
        instruction = h2m(binary)
        if instruction == 1:
            continue
        else:
            print(instruction+"\n")
   elif firstInput[0] == "mips":
        instruction = firstInput[1]
        hex = m2h(instruction)
        if hex == 1:  # If m2h() returned 1, it was an error
            continue
        else:    # Otherwise it's normal hex and we can print
            print(hex+"\n")
   repeat = input("Convert another hex or instruction value? (Y/n): ")