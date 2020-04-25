from string import ascii_letters as letters  # a-zA-Z

# For R-Types
functcode_dict = {}

# For I/J-Type
opcode_dict = {"000100":"beq", "000101":"bne", "001000":"addi", "001001":"addiu", "001100":"andi", "001101":"ori", "001010":"slti",
               "001011":"sltiu", "001111":"lui", "100011":"lw", "101011":"sw", "000010":"j", "000011":"jal"}

print("hex2mips by @KyleTimmermans\n")
hex = input("Enter Hex Code: ")

if hex[0:2] == "0x":  # Remove 0x if present and non hex code
    hex = hex[2:]

letters = list(letters)  # Make iterable and sliceable
check = [item for item in (letters[6:25] or letters[32:52]) if(item in hex)]  #  Check for non-hex chars in 'hex' string

if check:  # if check is true
    print("Non-Hexadecimal Character(s) Found, Exiting Program...")
    exit(0)

# Convert hexadecimal to binary by converting to int
bin = "{0:08b}".format(int(hex, 16))

# Check instruction type
if bin[0:6] == "000000":  # R-Formats always start with an op-code of "000000"
    print("This is an R-Format MIPS Instruction")
elif bin[0:6] == "000010" or "000011":  # J-Formats are always these two opcodes
    print("This is a J-Format MIPS Instruction")
else:  # I-Formats are everything else
    print("This is an I-Format MIPS Instruction")
