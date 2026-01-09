import encode, sys

if len(sys.argv) < 3:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

instructions = {"add":"R", "sub":"R", "slt":"R", "srl":"R", "or":"R", "and":"R",
                "lw":"I", "addi":"I", "jalr":"I",
                "sw":"S",
                "beq":"B", "bne":"B",
                "jal":"J"
                }

# ------------------------------------------------------- #
# STORING LABELS                                          #
# ------------------------------------------------------- #
                                                            
fr = open(input_file, "r")
                                                        
line = fr.readline()

labels = {}
pc = 0

while line:
    instruct = line.replace(',', ' ')
    if ':' in instruct:
        instruct = line.replace(':', ' ')
        instruct = instruct.split()
        labels[instruct[0]] = pc
    pc += 4
    line = fr.readline()

fr.close()



# ------------------------------------------------------- #
# PARSING INSTRUCTIONS                                    #
# ------------------------------------------------------- #
fr = open(input_file, "r")
fw = open(output_file, "w")

line = fr.readline()

pc = 0

while line:
    instruct = line.replace(',', ' ')
    if ':' in instruct:
        instruct = instruct.replace(':', ' ')
        instruct = instruct.split()[1:]
    else:
        instruct = instruct.split()
    # print(instruct)
        
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

