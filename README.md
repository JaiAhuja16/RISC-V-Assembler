<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F2027,50:203A43,100:2C5364&height=220&section=header&text=RISC-V%20Toolkit&fontSize=55&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Assembler%20%7C%20Simulator%20%7C%20RV32I&descAlignY=60"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/RV32I-Supported-blue"/>
  <img src="https://img.shields.io/badge/Python-3.10+-green"/>
  <img src="https://img.shields.io/badge/Assembler-Implemented-orange"/>
  <img src="https://img.shields.io/badge/Simulator-Implemented-red"/>
</p>

# RISC-V Toolkit

A Python-based assembler and simulator for the RV32I instruction set architecture. The project converts RISC-V assembly programs into machine code and executes them while generating detailed execution traces.

## Features

- ✅ Two-pass assembler with label resolution
- ✅ RV32I instruction set support
- ✅ Binary machine code generation
- ✅ Execution simulator with register tracing
- ✅ Memory emulation and management
- ✅ Branch and jump instruction support
- ✅ Automated test case framework
- ✅ Execution trace generation

## Supported Instructions

### R-Type (Register Operations)
- `add` - Add two registers
- `sub` - Subtract registers
- `and` - Bitwise AND
- `or` - Bitwise OR
- `xor` - Bitwise XOR
- `srl` - Shift right logical
- `slt` - Set less than

### I-Type (Immediate Operations)
- `addi` - Add immediate
- `lw` - Load word
- `jalr` - Jump and link register

### S-Type (Store Operations)
- `sw` - Store word

### B-Type (Branch Operations)
- `beq` - Branch if equal
- `bne` - Branch if not equal
- `blt` - Branch if less than
- `bge` - Branch if greater than or equal
- `bltu` - Branch if less than (unsigned)

### J-Type (Jump Operations)
- `jal` - Jump and link

## Architecture

```
Assembly Program (.asm)
        │
        ▼
   ┌─────────────┐
   │  Assembler  │
   └─────────────┘
        │
        ▼
Machine Code (.bin)
        │
        ▼
   ┌─────────────┐
   │  Simulator  │
   └─────────────┘
        │
        ▼
Execution Trace (.txt)
```

## Quick Start

### Assembler

```bash
cd SimpleAssembler
python3 Assembler.py input.asm output.bin
```

### Simulator

```bash
cd SimpleSimulator
python3 Simulator.py machine_code.bin output_trace.txt
```

### Automated Testing

```bash
cd automatedTesting
python3 src/main.py --no-sim --windows    # Test assembler only
python3 src/main.py --no-asm --windows    # Test simulator only
python3 src/main.py --verbose --windows   # Test both and mentions the output difference (if exists)
```

## Example

### Input Assembly (simple.asm)

```assembly
addi x5, x0, 10
addi x6, x0, 20
add  x7, x5, x6
sw   x7, 0(x2)
```

### Generated Machine Code

```text
00000000101000000000001010010011
00000001010000000000001100010011
00000000011000101000001110110011
00000000011000101010000000100011
```

### Execution Trace Output

```text
0b00000000000000000000000000000100 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000101111100 ...
0b00000000000000000000000000001000 0b00000000000000000000000000000000 0b00000000000000000000000000001010 0b00000000000000000000000101111100 ...
0b00000000000000000000000000001100 0b00000000000000000000000000000000 0b00000000000000000000000000001010 0b00000000000000000000000000010100 ...
...
```

## Repository Structure

```
RISC-V-Toolkit/
├── SimpleAssembler/
│   ├── Assembler.py          # Main assembler implementation
│   ├── encode.py             # Instruction encoding
│   └── register.py           # Register definitions
├── SimpleSimulator/
│   └── Simulator.py          # CPU simulator
├── automatedTesting/
│   ├── src/
│   │   ├── main.py           # Test runner
│   │   ├── Grader.py         # Base grader class
│   │   ├── AsmGrader.py      # Assembler grading
│   │   ├── SimGrader.py      # Simulator grading
│   │   └── colors.py         # Terminal colors
│   ├── tests/
│   │   ├── assembly/         # Test assembly files
│   │   ├── bin/              # Expected machine code
│   │   └── traces/           # Expected execution traces
│   └── results/              # Test results
└── README.md
```

## Testing

The project includes comprehensive automated tests:

- **Simple Tests**: Basic instruction operations
- **Hard Tests**: Complex control flow and memory operations
- **Assembly Tests**: Assembler output validation
- **Simulation Tests**: Execution trace validation

Run tests:

```bash
cd automatedTesting
python3 src/main.py --no-sim --windows
python3 src/main.py --no-asm --windows
python3 src/main.py --verbose --windows
```

## Implementation Details

### Assembler

- **First Pass**: Parse labels and calculate addresses
- **Second Pass**: Generate machine code with resolved addresses
- **Instruction Encoding**: RV32I format compliance
- **Label Resolution**: Support for forward and backward references

### Simulator

- **Register Set**: 32 × 32-bit registers (x0-x31)
- **Memory**: Dynamic memory allocation
- **Program Counter**: Instruction pointer management
- **Execution**: Sequential execution with branch support
- **Tracing**: Per-cycle register state capture

## Features Showcase

### Label Support
```assembly
loop:
    addi x5, x5, 1
    bne  x5, x6, loop
```

### Memory Operations
```assembly
lw   x5, 0(x2)      # Load from address in x2
sw   x5, 4(x2)      # Store to address x2 + 4
```

### Branch & Jump
```assembly
beq  x5, x6, equal
addi x7, x0, 1
jal  x0, end
equal:
    addi x7, x0, 0
end:
```

## License

MIT License

---