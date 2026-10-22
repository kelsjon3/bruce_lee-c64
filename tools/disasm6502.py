#!/usr/bin/env python3
"""
disasm6502.py - Lightweight, clean 6502 disassembler with C64 symbol annotations.
"""

import sys

# Official 6502 instruction table
# Format: (mnemonic, addressing_mode, length)
# Addressing modes:
#   'imp': implied / accumulator
#   'imm': #$xx
#   'zp':  $xx
#   'zpx': $xx,X
#   'zpy': $xx,Y
#   'rel': relative (branch)
#   'abs': $xxxx
#   'abx': $xxxx,X
#   'aby': $xxxx,Y
#   'ind': ($xxxx)
#   'izx': ($xx,X)
#   'izy': ($xx),Y

OPCODES = {
    0x00: ("BRK", "imp", 1), 0x01: ("ORA", "izx", 2), 0x05: ("ORA", "zp", 2),  0x06: ("ASL", "zp", 2),
    0x08: ("PHP", "imp", 1), 0x09: ("ORA", "imm", 2), 0x0A: ("ASL", "imp", 1), 0x0D: ("ORA", "abs", 3),
    0x0E: ("ASL", "abs", 3), 0x10: ("BPL", "rel", 2), 0x11: ("ORA", "izy", 2), 0x15: ("ORA", "zpx", 2),
    0x16: ("ASL", "zpx", 2), 0x18: ("CLC", "imp", 1), 0x19: ("ORA", "aby", 3), 0x1D: ("ORA", "abx", 3),
    0x1E: ("ASL", "abx", 3), 0x20: ("JSR", "abs", 3), 0x21: ("AND", "izx", 2), 0x24: ("BIT", "zp", 2),
    0x25: ("AND", "zp", 2),  0x26: ("ROL", "zp", 2),  0x28: ("PLP", "imp", 1), 0x29: ("AND", "imm", 2),
    0x2A: ("ROL", "imp", 1), 0x2C: ("BIT", "abs", 3), 0x2D: ("AND", "abs", 3), 0x2E: ("ROL", "abs", 3),
    0x30: ("BMI", "rel", 2), 0x31: ("AND", "izy", 2), 0x35: ("AND", "zpx", 2), 0x36: ("ROL", "zpx", 2),
    0x38: ("SEC", "imp", 1), 0x39: ("AND", "aby", 3), 0x3D: ("AND", "abx", 3), 0x3E: ("ROL", "abx", 3),
    0x40: ("RTI", "imp", 1), 0x41: ("EOR", "izx", 2), 0x45: ("EOR", "zp", 2),  0x46: ("LSR", "zp", 2),
    0x48: ("PHA", "imp", 1), 0x49: ("EOR", "imm", 2), 0x4A: ("LSR", "imp", 1), 0x4C: ("JMP", "abs", 3),
    0x4D: ("EOR", "abs", 3), 0x4E: ("LSR", "abs", 3), 0x50: ("BVC", "rel", 2), 0x51: ("EOR", "izy", 2),
    0x55: ("EOR", "zpx", 2), 0x56: ("LSR", "zpx", 2), 0x58: ("CLI", "imp", 1), 0x59: ("EOR", "aby", 3),
    0x5D: ("EOR", "abx", 3), 0x5E: ("LSR", "abx", 3), 0x60: ("RTS", "imp", 1), 0x61: ("ADC", "izx", 2),
    0x65: ("ADC", "zp", 2),  0x66: ("ROR", "zp", 2),  0x68: ("PLA", "imp", 1), 0x69: ("ADC", "imm", 2),
    0x6A: ("ROR", "imp", 1), 0x6C: ("JMP", "ind", 3), 0x6D: ("ADC", "abs", 3), 0x6E: ("ROR", "abs", 3),
    0x70: ("BVS", "rel", 2), 0x71: ("ADC", "izy", 2), 0x75: ("ADC", "zpx", 2), 0x76: ("ROR", "zpx", 2),
    0x78: ("SEI", "imp", 1), 0x79: ("ADC", "aby", 3), 0x7D: ("ADC", "abx", 3), 0x7E: ("ROR", "abx", 3),
    0x81: ("STA", "izx", 2), 0x84: ("STY", "zp", 2),  0x85: ("STA", "zp", 2),  0x86: ("STX", "zp", 2),
    0x88: ("DEY", "imp", 1), 0x8A: ("TXA", "imp", 1), 0x8C: ("STY", "abs", 3), 0x8D: ("STA", "abs", 3),
    0x8E: ("STX", "abs", 3), 0x90: ("BCC", "rel", 2), 0x91: ("STA", "izy", 2), 0x94: ("STY", "zpx", 2),
    0x95: ("STA", "zpx", 2), 0x96: ("STX", "zpy", 2), 0x98: ("TYA", "imp", 1), 0x99: ("STA", "aby", 3),
    0x9A: ("TXS", "imp", 1), 0x9D: ("STA", "abx", 3), 0xA0: ("LDY", "imm", 2), 0xA1: ("LDA", "izx", 2),
    0xA2: ("LDX", "imm", 2), 0xA4: ("LDY", "zp", 2),  0xA5: ("LDA", "zp", 2),  0xA6: ("LDX", "zp", 2),
    0xA8: ("TAY", "imp", 1), 0xA9: ("LDA", "imm", 2), 0xAA: ("TAX", "imp", 1), 0xAC: ("LDY", "abs", 3),
    0xAD: ("LDA", "abs", 3), 0xAE: ("LDX", "abs", 3), 0xB0: ("BCS", "rel", 2), 0xB1: ("LDA", "izy", 2),
    0xB4: ("LDY", "zpx", 2), 0xB5: ("LDA", "zpx", 2), 0xB6: ("LDX", "zpy", 2), 0xB8: ("CLV", "imp", 1),
    0xB9: ("LDA", "aby", 3), 0xBA: ("TSX", "imp", 1), 0xBC: ("LDY", "abx", 3), 0xBD: ("LDA", "abx", 3),
    0xBE: ("LDX", "aby", 3), 0xC0: ("CPY", "imm", 2), 0xC1: ("CMP", "izx", 2), 0xC4: ("CPY", "zp", 2),
    0xC5: ("CMP", "zp", 2),  0xC6: ("DEC", "zp", 2),  0xC8: ("INY", "imp", 1), 0xC9: ("CMP", "imm", 2),
    0xCA: ("DEX", "imp", 1), 0xCC: ("CPY", "abs", 3), 0xCD: ("CMP", "abs", 3), 0xCE: ("DEC", "abs", 3),
    0xD0: ("BNE", "rel", 2), 0xD1: ("CMP", "izy", 2), 0xD5: ("CMP", "zpx", 2), 0xD6: ("DEC", "zpx", 2),
    0xD8: ("CLD", "imp", 1), 0xD9: ("CMP", "aby", 3), 0xDD: ("CMP", "abx", 3), 0xDE: ("DEC", "abx", 3),
    0xE0: ("CPX", "imm", 2), 0xE1: ("SBC", "izx", 2), 0xE4: ("CPX", "zp", 2),  0xE5: ("SBC", "zp", 2),
    0xE6: ("INC", "zp", 2),  0xE8: ("INX", "imp", 1), 0xE9: ("SBC", "imm", 2), 0xEA: ("NOP", "imp", 1),
    0xEC: ("CPX", "abs", 3), 0xED: ("SBC", "abs", 3), 0xEE: ("INC", "abs", 3), 0xF0: ("BEQ", "rel", 2),
    0xF1: ("SBC", "izy", 2), 0xF5: ("SBC", "zpx", 2), 0xF6: ("INC", "zpx", 2), 0xF8: ("SED", "imp", 1),
    0xF9: ("SBC", "aby", 3), 0xFD: ("SBC", "abx", 3), 0xFE: ("INC", "abx", 3),
}

# Standard C64 hardware symbols
C64_SYMBOLS = {
    0x0000: "D6510",
    0x0001: "R6510",
    0x0314: "CINV_L",
    0x0315: "CINV_H",
    0x0318: "NMINV_L",
    0x0319: "NMINV_H",
    0xD000: "SP0X", 0xD001: "SP0Y", 0xD002: "SP1X", 0xD003: "SP1Y",
    0xD004: "SP2X", 0xD005: "SP2Y", 0xD006: "SP3X", 0xD007: "SP3Y",
    0xD008: "SP4X", 0xD009: "SP4Y", 0xD00A: "SP5X", 0xD00B: "SP5Y",
    0xD00C: "SP6X", 0xD00D: "SP6Y", 0xD00E: "SP7X", 0xD00F: "SP7Y",
    0xD010: "MSIGX", 0xD011: "SCROLY", 0xD012: "RASTER", 0xD013: "LPX",
    0xD014: "LPY", 0xD015: "SPENA", 0xD016: "SCROLX", 0xD017: "YXPAND",
    0xD018: "VMCSB", 0xD019: "VICIRQ", 0xD01A: "IRQMSK", 0xD01B: "SPBGPR",
    0xD01C: "SPMC", 0xD01D: "XXPAND", 0xD01E: "SPSPCL", 0xD01F: "SPBGCL",
    0xD020: "EXTCOL", 0xD021: "BGCOL0", 0xD022: "BGCOL1", 0xD023: "BGCOL2",
    0xD024: "BGCOL3", 0xD025: "SPMC0", 0xD026: "SPMC1", 0xD027: "SP0COL",
    0xD028: "SP1COL", 0xD029: "SP2COL", 0xD02A: "SP3COL", 0xD02B: "SP4COL",
    0xD02C: "SP5COL", 0xD02D: "SP6COL", 0xD02E: "SP7COL",
    0xD400: "FRELO1", 0xD401: "FREHI1", 0xD402: "PWLO1", 0xD403: "PWHI1",
    0xD404: "VCREG1", 0xD405: "ATDCY1", 0xD406: "SUREL1",
    0xD407: "FRELO2", 0xD408: "FREHI2", 0xD409: "PWLO2", 0xD40A: "PWHI2",
    0xD40B: "VCREG2", 0xD40C: "ATDCY2", 0xD40D: "SUREL2",
    0xD40E: "FRELO3", 0xD40F: "FREHI3", 0xD410: "PWLO3", 0xD411: "PWHI3",
    0xD412: "VCREG3", 0xD413: "ATDCY3", 0xD414: "SUREL3",
    0xD415: "CUTLO",  0xD416: "CUTHI",  0xD417: "RESON",  0xD418: "SIGVOL",
    0xDC00: "CIAPRA", 0xDC01: "CIAPRB", 0xDC02: "CIDDRA", 0xDC03: "CIDDRB",
    0xDC04: "TIMALO", 0xDC05: "TIMAHI", 0xDC06: "TIMBLO", 0xDC07: "TIMBHI",
    0xDC08: "TOD10",  0xDC09: "TODSEC", 0xDC0A: "TODMIN", 0xDC0B: "TODHR",
    0xDC0C: "SDR",    0xDC0D: "ICR",    0xDC0E: "CRA",    0xDC0F: "CRB",
    0xDD00: "CI2PRA", 0xDD01: "CI2PRB", 0xDD02: "CI2DRA", 0xDD03: "CI2DRB",
    0xDD04: "TI2ALO", 0xDD05: "TI2AHI", 0xDD06: "TI2BLO", 0xDD07: "TI2BHI",
    0xDD0D: "CI2ICR", 0xDD0E: "CI2CRA", 0xDD0F: "CI2CRB",
}

def disassemble_instruction(data, offset, pc, symbols=None):
    if symbols is None:
        symbols = C64_SYMBOLS
    else:
        # Merge symbols
        merged = dict(C64_SYMBOLS)
        merged.update(symbols)
        symbols = merged

    if offset >= len(data):
        return None, 0

    opcode = data[offset]
    if opcode not in OPCODES:
        # Undocumented / illegal opcode or data byte
        return f".byte ${opcode:02X}", 1

    mnemonic, mode, length = OPCODES[opcode]
    if offset + length > len(data):
        return f".byte ${opcode:02X}", 1

    raw_bytes = data[offset:offset+length]

    operand_str = ""
    comment = ""

    if mode == "imp":
        operand_str = ""
    elif mode == "imm":
        val = raw_bytes[1]
        operand_str = f"#${val:02X}"
    elif mode == "zp":
        val = raw_bytes[1]
        sym = symbols.get(val)
        if sym:
            operand_str = f"${val:02X}"
            comment = f"; {sym}"
        else:
            operand_str = f"${val:02X}"
    elif mode == "zpx":
        val = raw_bytes[1]
        operand_str = f"${val:02X},X"
    elif mode == "zpy":
        val = raw_bytes[1]
        operand_str = f"${val:02X},Y"
    elif mode == "rel":
        rel = raw_bytes[1]
        if rel >= 0x80:
            rel -= 0x100
        target = (pc + 2 + rel) & 0xFFFF
        operand_str = f"${target:04X}"
    elif mode == "abs":
        val = raw_bytes[1] | (raw_bytes[2] << 8)
        sym = symbols.get(val)
        if sym:
            operand_str = f"${val:04X}"
            comment = f"; {sym}"
        else:
            operand_str = f"${val:04X}"
    elif mode == "abx":
        val = raw_bytes[1] | (raw_bytes[2] << 8)
        sym = symbols.get(val)
        if sym:
            operand_str = f"${val:04X},X"
            comment = f"; {sym}"
        else:
            operand_str = f"${val:04X},X"
    elif mode == "aby":
        val = raw_bytes[1] | (raw_bytes[2] << 8)
        sym = symbols.get(val)
        if sym:
            operand_str = f"${val:04X},Y"
            comment = f"; {sym}"
        else:
            operand_str = f"${val:04X},Y"
    elif mode == "ind":
        val = raw_bytes[1] | (raw_bytes[2] << 8)
        operand_str = f"(${val:04X})"
    elif mode == "izx":
        val = raw_bytes[1]
        operand_str = f"(${val:02X},X)"
    elif mode == "izy":
        val = raw_bytes[1]
        operand_str = f"(${val:02X}),Y"

    bytes_hex = " ".join(f"{b:02X}" for b in raw_bytes).ljust(9)
    asm = f"{mnemonic.ljust(4)} {operand_str}".strip()
    line = f"${pc:04X}  {bytes_hex}  {asm.ljust(18)} {comment}".rstrip()
    return line, length

def disassemble_raw(data, offset, pc, symbols=None):
    if symbols is None:
        symbols = C64_SYMBOLS
    else:
        merged = dict(C64_SYMBOLS)
        merged.update(symbols)
        symbols = merged

    if offset >= len(data):
        return None, "", "", 0

    opcode = data[offset]
    if opcode not in OPCODES:
        return f".byte", f"${opcode:02X}", "", 1

    mnemonic, mode, length = OPCODES[opcode]
    if offset + length > len(data):
        return f".byte", f"${opcode:02X}", "", 1

    raw_bytes = data[offset:offset+length]
    operand_str = ""
    comment = ""

    if mode == "imp":
        operand_str = ""
    elif mode == "imm":
        val = raw_bytes[1]
        operand_str = f"#${val:02X}"
    elif mode == "zp":
        val = raw_bytes[1]
        sym = symbols.get(val)
        if sym:
            operand_str = f"{sym}"
        else:
            operand_str = f"${val:02X}"
    elif mode == "zpx":
        val = raw_bytes[1]
        sym = symbols.get(val)
        if sym:
            operand_str = f"{sym},X"
        else:
            operand_str = f"${val:02X},X"
    elif mode == "zpy":
        val = raw_bytes[1]
        sym = symbols.get(val)
        if sym:
            operand_str = f"{sym},Y"
        else:
            operand_str = f"${val:02X},Y"
    elif mode == "rel":
        rel = raw_bytes[1]
        if rel >= 0x80:
            rel -= 0x100
        target = (pc + 2 + rel) & 0xFFFF
        sym = symbols.get(target)
        if sym:
            operand_str = f"{sym}"
        else:
            operand_str = f"${target:04X}"
    elif mode == "abs":
        val = raw_bytes[1] | (raw_bytes[2] << 8)
        sym = symbols.get(val)
        if sym:
            operand_str = f"{sym}"
        else:
            operand_str = f"${val:04X}"
    elif mode == "abx":
        val = raw_bytes[1] | (raw_bytes[2] << 8)
        sym = symbols.get(val)
        if sym:
            operand_str = f"{sym},X"
        else:
            operand_str = f"${val:04X},X"
    elif mode == "aby":
        val = raw_bytes[1] | (raw_bytes[2] << 8)
        sym = symbols.get(val)
        if sym:
            operand_str = f"{sym},Y"
        else:
            operand_str = f"${val:04X},Y"
    elif mode == "ind":
        val = raw_bytes[1] | (raw_bytes[2] << 8)
        sym = symbols.get(val)
        if sym:
            operand_str = f"({sym})"
        else:
            operand_str = f"(${val:04X})"
    elif mode == "izx":
        val = raw_bytes[1]
        sym = symbols.get(val)
        if sym:
            operand_str = f"({sym},X)"
        else:
            operand_str = f"(${val:02X},X)"
    elif mode == "izy":
        val = raw_bytes[1]
        sym = symbols.get(val)
        if sym:
            operand_str = f"({sym}),Y"
        else:
            operand_str = f"(${val:02X}),Y"

    return mnemonic, operand_str, comment, length

    lines = []
    offset = 0
    pc = start_pc
    instr_count = 0
    total_bytes = len(data) if max_bytes is None else min(len(data), max_bytes)

    while offset < total_bytes:
        if count is not None and instr_count >= count:
            break
        line, length = disassemble_instruction(data, offset, pc, symbols)
        if length == 0:
            break
        lines.append(line)
        offset += length
        pc += length
        instr_count += 1
    return lines

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: disasm6502.py <file> <hex_start_pc> [hex_offset] [length_or_count]")
        sys.exit(1)
    filename = sys.argv[1]
    start_pc = int(sys.argv[2], 16)
    offset = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0
    count = int(sys.argv[4]) if len(sys.argv) > 4 else None

    with open(filename, "rb") as f:
        data = f.read()

    lines = disassemble_block(data[offset:], start_pc, count=count)
    for l in lines:
        print(l)
