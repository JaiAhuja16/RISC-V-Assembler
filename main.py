import encode, register

instructions = {"add":"R", "sub":"R", "slt":"R", "srl":"R", "or":"R", "and":"R",
                "lw":"I", "addi":"I", "jalr":"I",
                "sw":"S",
                "beq":"B", "bne":"B",
                "jal":"J"
                }

fr = open("input.txt", "r")
fw = open("output.txt", "w")

line = fr.readline()

while line:
    instruct = line
    if instructions[instruct[0]] == "R":
        fw.write(encode.r_type(instruct))
    elif instructions[instruct[0]] == "I":
        fw.write(encode.i_type(instruct))

    line = fr.readline()