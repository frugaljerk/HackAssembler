import re

# dest to binary conversion table
dest_dic = {
    "null" : "000",
    "M" : "001",
    "D" : "010",
    "MD" : "011",
    "A" : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD" : "111",
}

comp_dic = {
    # a = 0
    "0" : "0 1 0 1 0 1 0",
    "1" : "0 1 1 1 1 1 1",
    "-1" : "0 1 1 1 0 1 0",
    "D" : "0 0 0 1 1 0 0",
    "A" : "0 1 1 0 0 0 0",
    "!D" : "0 0 0 1 1 0 1",
    "!A" : "0 1 1 0 0 0 1",
    "-D" : "0 0 0 1 1 1 1",
    "-A" : "0 1 1 0 0 1 1",
    "D+1" : "0 0 1 1 1 1 1",
    "A+1" : "0 1 1 0 1 1 1",
    "D-1" : "0 0 0 1 1 1 0",
    "A-1" : "0 1 1 0 0 1 0",
    "D+A" : "0 0 0 0 0 1 0",
    "D-A" : "0 0 1 0 0 1 1",
    "A-D" : "0 0 0 0 1 1 1",
    "D&A" : "0 0 0 0 0 0 0",
    "D|A" : "0 0 1 0 1 0 1",
    # a = 1
    "M" : "1 1 1 0 0 0 0",
    "!M" : "1 1 1 0 0 0 1",
    "-M" : "1 1 1 0 0 1 1",
    "M+1" : "1 1 1 0 1 1 1",
    "M-1" : "1 1 1 0 0 1 0",
    "D+M" : "1 0 0 0 0 1 0",
    "D-M" : "1 0 1 0 0 1 1",
    "M-D" : "1 0 0 0 1 1 1",
    "D&M" : "1 0 0 0 0 0 0",
    "D|M" : "1 0 1 0 1 0 1",
}

jump_dic = {
    "null" : "0 0 0",
    "JGT" : "0 0 1",
    "JEQ" : "0 1 0",
    "JGE" : "0 1 1",
    "JLT" : "1 0 0",
    "JNE" : "1 0 1",
    "JLE" : "1 1 0",
    "JMP" : "1 1 1",
}

symbol_dic = {
    "R0" : "0",
    "R1" : "1",
    "R2" : "2",
    "R3" : "3",
    "R4" : "4",
    "R5" : "5",
    "R6" : "6",
    "R7" : "7",
    "R8" : "8",
    "R9" : "9",
    "R10" : "10",
    "R11" : "11",
    "R12" : "12",
    "R13" : "13",
    "R14" : "14",
    "R15" : "15",
    "SCREEN" : "16384",
    "KBD" : "24576",
    "SP" : "0",
    "LCL" : "1",
    "ARG" : "2",
    "THIS" : "3",
    "THAT" : "4",

}

def instructionType(line):
    """
    :param line: one line of assembly language instruction
    :return: type of instruction in string if valid instruction, else None
    """
    for char in line:
        if re.findall('\s', char):
            continue
        elif re.findall('/', char):
            return None
        elif re.findall('@', char):
            return 'A_INSTRUCTION'
        elif re.findall('\(', char):
            return 'L_INSTRUCTION'
        else:
            return 'C_INSTRUCTION'
    return None

def a_coder(address):
    """
    :param address: integer address excluding @ from A_instruction
    :return: binary representation in string
    """
    # convert address to integer then to binary
    return f'{address:016b}'

def dest_coder(dest):
    """
    convert dest to binary representation
    :param dest: destination in string
    :return: binary representation of dest in string
    """
    return dest_dic[dest]

def comp_coder(comp):
    """
    convert comp to binary representation
    :param comp: comp instruction in string
    :return: binary representation of comp in string
    """
    return comp_dic[comp].replace(" ", "")

def jump_coder(jump):
    """
    conver jump instruction to binary
    :param jump: jump instruction in string
    :return: binary representation of jump in string
    """
    return jump_dic[jump].replace(" ", "")

# INITIALIZE
# open input file and get ready to process.
OUTPUTPATH = r'C:\Users\HSapi\Documents\Computer Science\Nand2Tetris\projects\06\rect\rectpython.hack'
INPUTPATH = r'C:\Users\HSapi\Documents\Computer Science\Nand2Tetris\projects\06\rect\rect.asm'
outputfile = open(OUTPUTPATH, 'w')
# FIRST PASS
# Reads the program line by line and construct symbol table
with open(INPUTPATH) as f:
    line = f.readline()
    # Construct symbol table and add predefined symbols.
    count = 0 #track the ROM instruction count

    while line:
        instruction = instructionType(line)
        if instruction == None:
            line = f.readline()
            continue
        if instruction == 'L_INSTRUCTION':
            label = re.findall('(?<=\()[\w!|+&$.]+', line)[0]
            symbol_dic.setdefault(label, str(count))
            count -= 1 #move back one line because label is pseudo instruction.

        count += 1
        line = f.readline()


# SECOND PASS
# While there are more line to process:
with open(INPUTPATH) as f:
    line = f.readline()
    variable_count = 16 # per Hack program specification
    while line:

        if instructionType(line) == None:
            line = f.readline()
            continue

        elif instructionType(line) == 'A_INSTRUCTION':
            address = re.findall('(?<=@)[\w!|+&.$]+', line)[0]
            try:
                address = int(address)
                binary = a_coder(address)
            except ValueError:
                # If the instruction is @symbol:
                if address in symbol_dic:
                    # else: translate the symbol to binary value
                    address = symbol_dic.get(address)
                else:
                    # If new symbol, add to symbol table
                    address = symbol_dic.setdefault(address, variable_count)
                    variable_count += 1
                binary = a_coder(int(address))

        elif instructionType(line) == 'C_INSTRUCTION':  # If the instruction is dest = comp ; jmp:
            # If jump is empty, the ‘‘;’’ is omitted: matching for '='
            if re.findall('=', line):
                comp = re.findall('(?<==)[\w!-|+$&]+', line)[0]
                dest = re.findall('\w+(?==)', line)[0]
                # Assemble the instruction into a string of sixteen 0 and 1s
                binary = '111' + comp_coder(comp) + dest_coder(dest) + jump_coder('null')
            # If dest is empty, the ‘‘=’’ is omitted: matching for ';'
            else:
                comp = re.findall('[\w!-|+&]+(?=;)', line)[0]
                jump = re.findall('(?<=;)\w+', line)[0]
                # Assemble the instruction into a string of sixteen 0 and 1s
                binary = '111' + comp_coder(comp) + dest_coder('null') + jump_coder(jump)

        else: #skip writing binary if L_INSTRUCTION
            line = f.readline()
            continue

        # Write the string to output file.
        outputfile.write(binary + '\n')
        # Parse the next instruction
        line = f.readline()
    # close the written file
    outputfile.close()
