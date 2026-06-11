import sys

memory_keys = [
    "0x00010000", "0x00010004", "0x00010008", "0x0001000C",
    "0x00010010", "0x00010014", "0x00010018", "0x0001001C",
    "0x00010020", "0x00010024", "0x00010028", "0x0001002C",
    "0x00010030", "0x00010034", "0x00010038", "0x0001003C",
    "0x00010040", "0x00010044", "0x00010048", "0x0001004C",
    "0x00010050", "0x00010054", "0x00010058", "0x0001005C",
    "0x00010060", "0x00010064", "0x00010068", "0x0001006C",
    "0x00010070", "0x00010074", "0x00010078", "0x0001007C"
]


def parse_instruction(binary_str):
    opcode = binary_str[25:32]

    if opcode == "0110011":
        funct7 = binary_str[0:7]
        rs2 = binary_str[7:12]
        rs1 = binary_str[12:17]
        funct3 = binary_str[17:20]
        rd = binary_str[20:25]
        f7f3 = funct7 + funct3
        ops = {
            "0000000000": "add", "0100000000": "sub", "0000000111": "and",
            "0000000110": "or", "0000000010": "slt", "0000000101": "srl",
            "0000000100": "xor", "0000000001": "sll"
        }
        return {"type": "R", "rd": rd, "rs1": rs1, "rs2": rs2, "operation": ops.get(f7f3, "unknown")}

    elif opcode in ["0010011", "0000011", "1100111"]:
        imm = binary_str[0:12]
        rs1 = binary_str[12:17]
        funct3 = binary_str[17:20]
        rd = binary_str[20:25]
        key = opcode + funct3
        ops = {"0010011000": "addi", "0000011010": "lw", "1100111000": "jalr"}
        return {"type": "I", "rd": rd, "rs1": rs1, "imm": imm, "operation": ops.get(key, "unknown"), "opcode": opcode}

    elif opcode == "0100011":
        imm11_5 = binary_str[0:7]
        rs2 = binary_str[7:12]
        rs1 = binary_str[12:17]
        funct3 = binary_str[17:20]
        imm4_0 = binary_str[20:25]
        return {"type": "S", "rs1": rs1, "rs2": rs2, "imm": imm11_5 + imm4_0, "funct3": funct3, "operation": "sw" if funct3 == "010" else "unknown"}

    elif opcode == "1100011":
        imm12 = binary_str[0:1]
        imm10_5 = binary_str[1:7]
        rs2 = binary_str[7:12]
        rs1 = binary_str[12:17]
        funct3 = binary_str[17:20]
        imm4_1 = binary_str[20:24]
        imm11 = binary_str[24:25]
        imm_str = imm12 + imm11 + imm10_5 + imm4_1 + "0"
        ops = {"000": "beq", "001": "bne", "100": "blt", "101": "bge", "110": "bltu"}
        return {"type": "B", "rs1": rs1, "rs2": rs2, "imm": imm_str, "funct3": funct3, "operation": ops.get(funct3, "unknown")}

    elif opcode == "1101111":
        imm20 = binary_str[0:1]
        imm10_1 = binary_str[1:11]
        imm11 = binary_str[11:12]
        imm19_12 = binary_str[12:20]
        rd = binary_str[20:25]
        imm_str = imm20 + imm19_12 + imm11 + imm10_1 + "0"
        return {"type": "J", "rd": rd, "imm": imm_str, "operation": "jal"}

    return {"type": "unknown", "operation": "unknown"}


def sign_extend(val, bits):
    sign_bit = 1 << (bits - 1)
    return (val & (sign_bit - 1)) - (val & sign_bit)


def to_signed(val, bits=32):
    if val >= (1 << (bits - 1)):
        return val - (1 << bits)
    return val


def bin32(val):
    return "0b" + format(val & 0xFFFFFFFF, '032b')


def execute_r_type(inst, regs):
    rs1_v = regs[int(inst["rs1"], 2)] if inst["rs1"] != "00000" else 0
    rs2_v = regs[int(inst["rs2"], 2)] if inst["rs2"] != "00000" else 0
    rd = int(inst["rd"], 2)
    op = inst["operation"]
    if op == "add":
        result = rs1_v + rs2_v
    elif op == "sub":
        result = rs1_v - rs2_v
    elif op == "and":
        result = rs1_v & rs2_v
    elif op == "or":
        result = rs1_v | rs2_v
    elif op == "xor":
        result = rs1_v ^ rs2_v
    elif op == "slt":
        result = 1 if to_signed(rs1_v) < to_signed(rs2_v) else 0
    elif op == "srl":
        result = rs1_v >> (rs2_v & 0x1F)
    elif op == "sll":
        result = rs1_v << (rs2_v & 0x1F)
    else:
        return
    if rd != 0:
        regs[rd] = result & 0xFFFFFFFF


def execute_i_type(inst, regs, pc, memory):
    rs1_v = regs[int(inst["rs1"], 2)] if inst["rs1"] != "00000" else 0
    rd = int(inst["rd"], 2)
    imm = sign_extend(int(inst["imm"], 2), 12)
    op = inst["operation"]
    if op == "addi":
        result = rs1_v + imm
        if rd != 0:
            regs[rd] = result & 0xFFFFFFFF
        return pc + 4
    elif op == "lw":
        address = (rs1_v + imm) & 0xFFFFFFFF
        result = memory.get(address, 0)
        if rd != 0:
            regs[rd] = result & 0xFFFFFFFF
        return pc + 4
    elif op == "jalr":
        if rd != 0:
            regs[rd] = pc + 4
        return ((rs1_v + imm) & ~1)
    return pc + 4


def execute_s_type(inst, regs, memory):
    rs1_v = regs[int(inst["rs1"], 2)] if inst["rs1"] != "00000" else 0
    rs2_v = regs[int(inst["rs2"], 2)] if inst["rs2"] != "00000" else 0
    imm = sign_extend(int(inst["imm"], 2), 12)
    op = inst["operation"]
    if op == "sw":
        address = (rs1_v + imm) & 0xFFFFFFFF
        memory[address] = rs2_v & 0xFFFFFFFF


def execute_b_type(inst, regs, pc):
    rs1_v = regs[int(inst["rs1"], 2)] if inst["rs1"] != "00000" else 0
    rs2_v = regs[int(inst["rs2"], 2)] if inst["rs2"] != "00000" else 0
    imm = sign_extend(int(inst["imm"], 2), 13)
    op = inst["operation"]
    taken = False
    if op == "beq":
        taken = (rs1_v == rs2_v)
    elif op == "bne":
        taken = (rs1_v != rs2_v)
    elif op == "blt":
        taken = (to_signed(rs1_v) < to_signed(rs2_v))
    elif op == "bge":
        taken = (to_signed(rs1_v) >= to_signed(rs2_v))
    elif op == "bltu":
        taken = (rs1_v < rs2_v)
    if taken:
        return pc + imm
    return pc + 4


def execute_j_type(inst, regs, pc):
    rd = int(inst["rd"], 2)
    imm = sign_extend(int(inst["imm"], 2), 21)
    if rd != 0:
        regs[rd] = pc + 4
    return pc + imm


def run_simulator(input_file, output_file):
    regs = [0] * 32
    regs[2] = 380
    memory = {}
    instructions = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                instructions.append(line)

    parsed = [parse_instruction(instr) for instr in instructions]
    pc = 0
    trace_lines = []
    max_steps = 10000

    for _ in range(max_steps):
        idx = pc // 4
        if idx < 0 or idx >= len(instructions):
            break

        inst = parsed[idx]
        old_pc = pc
        next_pc = pc + 4

        if inst["type"] == "R":
            execute_r_type(inst, regs)
        elif inst["type"] == "I":
            next_pc = execute_i_type(inst, regs, pc, memory)
        elif inst["type"] == "S":
            execute_s_type(inst, regs, memory)
        elif inst["type"] == "B":
            next_pc = execute_b_type(inst, regs, pc)
        elif inst["type"] == "J":
            next_pc = execute_j_type(inst, regs, pc)

        trace_line = bin32(next_pc)
        for r in regs:
            trace_line += " " + bin32(r)
        trace_lines.append(trace_line)

        pc = next_pc
        if pc == old_pc:
            break

    memory_trace = {}
    for addr in memory_keys:
        memory_trace[addr] = 0
    for addr, val in memory.items():
        key = "0x" + format(addr, '08X')
        if key in memory_trace:
            memory_trace[key] = val

    with open(output_file, "w") as f:
        for line in trace_lines:
            f.write(line + "\n")
        for addr in memory_keys:
            val = memory_trace[addr]
            f.write(f"{addr}:0b{format(val & 0xFFFFFFFF, '032b')}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 Simulator.py <input_bin_file> <output_trace_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    run_simulator(input_file, output_file)
