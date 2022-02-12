#!/usr/bin/env python3

'''
Kyle Timmermans
Compiled in Python 3.9.7
Feb 11, 2022
hex2mips v2.1

"Entirety of program revolves around converting hex or MIPS instruction
to binary (op, rs, rt, rd, shamt, funct) and then how to order
the binary strings into one final piece so we can get either type"

            h2m()                            m2h()
         0x12345678                      add $t12 $t14
         /    |   \                      /    |    \
      01010 01011 10110               01010 01011 10110
       \      |      /                   \    |     /
       add  $t12  $a14                    0x12345678
'''


from string import ascii_letters as letters  # a-zA-Z
from string import printable as symbols  # !@#%^&*(){}[] etc
import re  # regex
import sys  # Get command line args


# Input string, check if hex or mips, sanitize, return binary string
def inputSanitize():
    global letters, symbols
    check = ["neither", "content"]   # Init check, check[0] is typ, check[1] is the binary
    while True:
        print(" ")  # Space between intro text and other input prompts
        if len(sys.argv) == 2:  # If there are command line args, don't prompt user to enter again
            check[1] = sys.argv[1]   # Hex command line mode
        elif len(sys.argv) > 2:
            check[1] = ' '.join(sys.argv[1:])   # MIPS Instruction command line
            print(check[1])
        elif len(sys.argv) == 1:  # GUI Mode
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
                print("Invalid symbol found in instruction string, Try Again")
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
            instruction = str(opcode_dict[op])+" "+str(hex(int(address, 2)*2))  # 'bin' here refers to the binary string array e.g. bin[1:2], not bin() function
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


# Used with m2h, looks for register names, otherwise sanitizes integers and hex code parameters for op command
def getRegisters(registersList):
    reg1, reg2, reg3 = "err", "err", "err"  # If these never get changed, register was not found
    for i in range(len(registersList)):
        for key, value in register_dict.items():    # If it's a register in functcode_dict or opcode_dict
            if i == 0 and registersList[i] == value:    # Otherwise it is an integer or hex code which needs zfill(16)
                reg1 = key
            elif i == 1 and registersList[i] == value:
                reg2 = key
            elif i == 2 and registersList[i] == value:   # May not be evaluated if only two registers
                reg3 = key
        if i == 0 and registersList[i].isdigit():  # Register can also just be an int for I format instructions
            reg1 = bin(int(registersList[i], 10))[2:].zfill(16)  # Then convert to binary with zfill and re-integer it
        elif i == 1 and registersList[i].isdigit():
            reg2 = bin(int(registersList[i], 10))[2:].zfill(16)
        elif i == 2 and registersList[i].isdigit():
            reg3 = bin(int(registersList[i], 10))[2:].zfill(16)
        if i == 0 and 'x' in registersList[i]:  # Register can also just be hex for I format instructions (return as binary string)
            reg1 = bin(int(registersList[i], 16))[2:].zfill(16)
        elif i == 1 and 'x' in registersList[i]:
            reg2 = bin(int(registersList[i], 16))[2:].zfill(16)
        elif i == 2 and 'x' in registersList[i]:
            reg3 = bin(int(registersList[i], 16))[2:].zfill(16)
    if (len(registersList)) == 3:   # Some codes have 3 registers
        if reg1 == "err" or reg2 == "err" or reg3 == "err":  # If len == 3 and there are errors
            print("Invalid register(s), make sure any labels are in hexadecimal, Try Again")  # Possibile they used a label not in hex
            return 1
        else:  # If len == 3 and no errors
            return reg1, reg2, reg3
    if (len(registersList)) == 2:  # Some codes have only 2 registers
        if reg1 == "err" or reg2 == "err":  # If len == 2 and there are errors
            print("Invalid register(s), make sure any labels are in hexadecimal, Try Again")
            return 1
        else:   # If len == 2 and no errors
            return reg1, reg2


# Mips instruction to hex
def m2h(instruction):
    shamt = "00000"  # Need to be added in for R format instructions, always the same
    funct = "100000"
    special = "000000"
    newInstruction = instruction.replace(" ", "")  # Remove spaces
    if ',' in newInstruction or "syscall" in newInstruction or "break" in newInstruction:  # Split string up by comma if R format or I format and syscall/break
        splitString = newInstruction.replace(")", "")  # Get rid of trailing )
        splitString = re.split('[\,\(]', splitString)  # Split everything by comma and parenthesis, put in a list
        splitString[0] = re.split('([\$])', splitString[0])  # Split first item e.g. add$t5 becomes ['add', '$', 't5']
        if splitString[0][0] == "syscall":  # List of lists
            return "0x0000000C"
        elif splitString[0][0] == "break":
            return "0x0000000D"
        splitString[0][1:3] = [''.join(splitString[0][1:3])] # Join $ and t5 in the substring, so now we have [['add', '$t5'], '$t4', '$t3']
        temp = [item for sublists in splitString for item in sublists if isinstance(sublists, list)]  # Flatten first list
        temp2 = splitString  # Hold onto old values while we reassign splitString
        splitString = temp   # Assign the flattened values of index 1, e.g. 'add' and '$t5'
        if len(temp2) == 3:
            splitString.extend([temp2[1], temp2[2]])  # Put it all together e.g. ['add', '$t5'] + ['$t4'] + ['$t3'] = ['add', '$t5', '$t4', 't3']
        elif len(temp2) == 2:
            splitString.append(temp2[1])  # Append instead of extend if only adding an extra
        if (len(splitString) > 4 or len(splitString) < 2):  # If too many or two few arguments
            print("Too many/few arguments for MIPS instruction, Try Again")
            return 1
        # Check first list item, the instruction, if its in
        for key, value in functcode_dict.items():  # Check if it's in functcode dictionary first
            if splitString[0] == value:   # If funct code matches one of the values, then append binary
                op, op_value = key, value  # Save values if found
        for key, value in opcode_dict.items():  # Check opcodes next if we didn't find the command in functcodes_dict
            if splitString[0] == value:  # If funct code matches one of the values, then append binary
                op, op_value = key, value
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
            if op_value == "lw" or op_value == "sw" or op_value == "lb" or op_value == "lbu":
                finalHex = op + registerList[2] + registerList[0] + registerList[1]
            elif op_value == "lui":
                finalHex = op + 5*'0' + registerList[0] + registerList[1]
            elif op_value == "srl" or op_value == "sll":
                finalHex = special + 5*'0' + registerList[1] + registerList[0] + registerList[2][11:16] + op
                finalHex = hex(int(finalHex, 2))
                if len(finalHex) == 7:
                    return finalHex[0:2] + "000" + finalHex[2:].upper()  # If 5 chars, add 3 0's
                elif len(finalHex) == 8:
                    return finalHex[0:2] + "00" + finalHex[2:].upper()  # If 6 chars, add 2 0's
            elif op_value in normalRFormat:  # Normal R instruction
                finalHex = special + registerList[1] + registerList[2] + registerList[0] + shamt + op  # rs, rt, rd: in that order
                finalHex = hex(int(finalHex, 2))
                return finalHex[0:2] + "0" + finalHex[2:].upper()  # R Format needs extra 0 in the front
            elif op_value in normalIFormat:  # Normal I instruction
                finalHex = op + registerList[1] + registerList[0] + registerList[2]
    else:  # If not R or I instruction, then treat differently bc it's J format, except for jr (All hardcoded)
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
        if '0x' in newInstruction:  # Split at 0x or $
            sizeCheck = re.split('0x|[^0-9a-zA-Z]+', newInstruction)
        elif '$' in newInstruction:
            sizeCheck = re.split('[\$]', newInstruction)
        if len(sizeCheck) != 2:  # If too many or too few arguments
            print("Too many/few arguments for MIPS instruction, Try Again")
            return 1
        # Only three op codes, dont need to search through functcode_dict or opcode_dict
        if op_value == "jr":
            try:    # Special + register + 15 0s + special
                finalHex = "00000" + list(register_dict.keys())[list(register_dict.values()).index("$" + sizeCheck[1])] + 15*'0' + "001000"  # One liner for dict value -> key from G4G
                finalHex = hex(int(finalHex, 2))
                if len(finalHex) <= 8:
                    return finalHex[0:2] + "00" + finalHex[2:].upper()  # If 6 chars, add 2 0's
                elif len(finalHex) > 8:
                    return finalHex[0:2] + "0" + finalHex[2:].upper()   # If 7 chars, add 1 0
            except KeyError:
                print("Invalid register(s), Try Again")
                return 1
        elif op_value == "j":  # Normal cases, take hex labelss, not registers
            if '0x' in newInstruction:
                finalHex = "000010" + bin(int("0x" + sizeCheck[1], 16))[2:].zfill(26)  # j opcode + target with 26 zfill
                finalHex = hex(int(finalHex, 2))
                return finalHex[0:2] + "0" + finalHex[2:].upper()
            else:
                print("Invalid hex label, Try Again")
                return 1
        elif op_value == "jal":
            if '0x' in newInstruction:
                finalHex = "000011" + bin(int("0x" + sizeCheck[1], 16))[2:].zfill(26)  # jal opcode + target with 26 zfill
                finalHex = hex(int(finalHex, 2))
                return finalHex[0:2] + "0" + finalHex[2:].upper()
            else:
                print("Invalid hex label, Try Again")
                return 1
    # int should be '2' base because its binary, don't need zfill, already perfect length
    finalHex = hex(int(finalHex, 2))  # Return as Binary String -> Binary Literal -> Hex
    return finalHex[0:2] + finalHex[2:].upper()  # Return with capital letters besides the x in '0x'


def main():
    if '--version' in sys.argv or '-v' in sys.argv:
        print("\nhex2mips v2.1\n")
        quit()
        
    if len(sys.argv) == 1:  # Normal "Y/N" loop when not using
        print("\nhex2mips by @KyleTimmermans")
        print("Notice: -Labels must be entered as hexadecimal")
        print("        -Registers must have $ and be separated by commas")
        repeat = 'Y'
        while repeat == 'Y' or repeat == 'y':
           firstInput = inputSanitize()
           if firstInput[0] == "hex":
                binary = firstInput[1]
                instruction = h2m(binary)
                if instruction == 1:
                    continue
                else:
                    print("\n"+instruction+"\n")
           elif firstInput[0] == "mips":
                instruction = firstInput[1]
                hexOutput = m2h(instruction)   # hex() is built in, do not name variables "hex"
                if hexOutput == 1:  # If m2h() returned 1, it was an error
                    continue
                else:    # Otherwise it's normal hex and we can print
                    print("\n"+hexOutput+"\n")
           repeat = input("Convert another hex or instruction value? (Y/n): ")
    elif len(sys.argv) > 1 and "-h" not in sys.argv:  # If hex or mips given
        while True:  # Keep allowing for retries, and then on correct, end it
           firstInput = inputSanitize()
           if firstInput[0] == "hex":
                binary = firstInput[1]
                instruction = h2m(binary)
                if instruction == 1:
                    continue
                else:
                    print("\n"+instruction+"\n")
                    quit()  # On correct, end, no more retries
           elif firstInput[0] == "mips":
                instruction = firstInput[1]
                hexOutput = m2h(instruction)   # hex() is built in, do not name variables "hex"
                if hexOutput == 1:  # If m2h() returned 1, it was an error
                    continue
                else:    # Otherwise it's normal hex and we can print
                    print(hexOutput+"\n")
                    quit()  # On correct, end, no more retries
    elif "-h" in sys.argv:  # If usage/help requested
        print("\nUsage 1: \"hex2mips.py\" (w/o arguments) for a \"Y/n\" GUI Mode")
        print("Usage 2: \"hex2mips.py (hex or mips instruction)\" for Command Line Mode")
        print("Usage 3: \"hex2mips.py -h\"  To print this message again")
        print("Example 1: \"hex2mips.py\" with no arguments will bring you to the GUI menu")
        print("Example 2: \"hex2mips.py 0x018B6820\" will return \"add $t5, $t4, $t3\"")
        print("Example 3: \"hex2mips.py sw \\$t1, 32\\(\\$s7\\)\" will return \"0xAEE90020\"")
        print("    -Backslashes needed for the command line mips instruction to hex for any dollar signs or parethesis")
        print("    -Backslashes not needed for the GUI version\n")


if __name__ == "__main__":

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
    
    main()
