import encode, register

instructions = {"add":"R", "sub":"R", "slt":"R", "srl":"R", "or":"R", "and":"R",
                "lw":"I", "addi":"I", "jalr":"I",
                "sw":"S",
                "beq":"B", "bne":"B",
                "jal":"J"
                }

# ------------------------------------------------------- #
# STORING LABELS                                          #
# ------------------------------------------------------- #
                                                            
fr = open("input.txt", "r")
                                                        
line = fr.readline()

labels = {}
pc = 0

while line:
    instruct = (line.replace(',', ' ')).split()
    if instruct[0][-1] == ':':
        labels[instruct[0][:len(instruct[0]) - 1]] = pc
    pc += 4
    line = fr.readline()

fr.close()



# ------------------------------------------------------- #
# PARSING INSTRUCTIONS                                    #
# ------------------------------------------------------- #
fr = open("input.txt", "r")
fw = open("output.txt", "w")

line = fr.readline()

pc = 0

while line:
    instruct = line.replace(',', ' ').split()
    if instruct[0][-1] == ':':
        instruct = instruct[1:]
        
    if instructions[instruct[0]] == "R":
        fw.write(encode.r_type(instruct))
        fw.write('\n')

    elif instructions[instruct[0]] == "I":
        fw.write(encode.i_type(instruct))
        fw.write('\n')

    elif instructions[instruct[0]] == "S":
        fw.write(encode.s_type(instruct))
        fw.write('\n')

    elif instructions[instruct[0]] == "B":
        fw.write(encode.b_type(instruct, labels, pc))
        fw.write('\n')
        
    elif instructions[instruct[0]] == "J":
        fw.write(encode.j_type(instruct, labels, pc))
        fw.write('\n')
        
    pc += 4
    line = fr.readline()

