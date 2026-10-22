#!/usr/bin/env python3
"""
create_startup_part.py - Create startup trampoline at $0200 to initialize C64 registers and page 3.
"""

def create():
    # Trampoline at $0200:
    # 78          SEI
    # A9 2F       LDA #$2F
    # 85 00       STA $00
    # A9 36       LDA #$36
    # 85 01       STA $01
    # A9 32       LDA #$32
    # 85 02       STA $02
    # A9 40       LDA #$40
    # 8D 01 03    STA $0301
    # A9 03       LDA #$03
    # 8D 19 03    STA $0319
    # A9 01       LDA #$01
    # 8D 18 03    STA $0318
    # A2 00       LDX #$00
    # 8A          TXA
    # loop:
    # 9D 34 03    STA $0334,X
    # E8          INX
    # E0 CC       CPX #$CC
    # D0 F8       BNE loop
    # 4C 00 04    JMP $0400

    code = bytearray([
        0x78,
        0xA9, 0x2F, 0x85, 0x00,
        0xA9, 0x36, 0x85, 0x01,
        0xA9, 0x32, 0x85, 0x02,
        0xA9, 0x40, 0x8D, 0x01, 0x03,
        0xA9, 0x03, 0x8D, 0x19, 0x03,
        0xA9, 0x01, 0x8D, 0x18, 0x03,
        0xA2, 0x00, 0x8A,
        0x9D, 0x34, 0x03,
        0xE8,
        0xE0, 0xCC,
        0xD0, 0xF8,
        0x4C, 0x00, 0x04
    ])

    # PRG header: $00, $02 (load address $0200)
    prg = bytearray([0x00, 0x02]) + code
    with open("dumps/part_startup.prg", "wb") as f:
        f.write(prg)
    print(f"Created dumps/part_startup.prg: {len(prg)} bytes ($0200-${0x0200 + len(code) - 1:04X})")

if __name__ == "__main__":
    create()
