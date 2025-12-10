import register



funct3 = {"add":"000", "sub":"000", "slt":"010", "srl":"101", "or":"110", "and":"111"}

def r_type(instruction):
    """
    Docstring for r_type

    -> ENCODING

         ______________________________________________________________________________________
        |   [31:25]     |  [24:20] | [19:15] |  [14:12]  |  [11:7]  |   [6:0]   |  Instruction | 
        |    funct7     |    rs2   |   rs1   |  funct3   |    rd    |  opcode   |              |  
        |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        |   0000000     |    rs2   |   rs1   |    000    |    rd    |  0110011  |     add      |
        |   0100000     |    rs2   |   rs1   |    000    |    rd    |  0110011  |     sub      |                           
        |   0000000     |    rs2   |   rs1   |    010    |    rd    |  0110011  |     slt      |                           
        |   0000000     |    rs2   |   rs1   |    101    |    rd    |  0110011  |     srl      |                           
        |   0000000     |    rs2   |   rs1   |    110    |    rd    |  0110011  |     or       |                           
        |   0000000     |    rs2   |   rs1   |    111    |    rd    |  0110011  |     and      |                           
        |_______________|__________|_________|___________|__________|___________|______________|

        - opcode = 0110011

        -    INSTRUCTIONS
            
            add rd, rs1, rs2
            sub rd, rs1, rs2
            slt rd, rs1, rs2
            srl rd, rs1, rs2
            or rd, rs1, rs2
            and rd, rs1, rs2

    """

    if len(instruction) != 4:
        print("Invalid instruction format")
        return ""
    
    _type, rd, rs1, rs2 = instruction

    encoding = ["-"] * 6

    # opcode
    encoding[5] = "0110011"

    # funct7
    if _type == "sub":
        encoding[0] = "0100000"
    else:
        encoding[0] = "0000000"

    # funct3
    if _type in funct3:
        encoding[3] = funct3[_type]

    if rd not in register.mapping or rs1 not in register.mapping or rs2 not in register.mapping:
        print("Invalid register arguments")
        return ""
    
    # registers
    encoding[1] = register.mapping[rs2]
    encoding[2] = register.mapping[rs1]
    encoding[4] = register.mapping[rd]

    return ''.join(encoding)


def i_type(instruction):
    """
    Docstring for i_type

    -> ENCODING

         ______________________________________________________________________________
        |   [31:20]     |  [19:15] |   [14:12]  |   [11:7]  |   [6:0]   |  Instruction | 
        |   imm[11:0]   |    rs1   |   funct3   |     rd    |  opcode   |              |  
        |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        |   imm[11:0]   |    rs1   |    010     |     rd    |  0000011  |      lw      |
        |   imm[11:0]   |    rs1   |    000     |     rd    |  0010011  |     addi     |                           
        |   imm[11:0]   |    rs1   |    000     |     rd    |  1100111  |     jalr     |                         
        |_______________|__________|____________|___________|___________|______________|

        -    INSTRUCTIONS
            
            lw rd, imm[11:0](rs1)
            addi rd, rs, imm[11:0]
            jalr rd, x6, offset[11:0]

    """

    # ENCODING LEFT RN
    