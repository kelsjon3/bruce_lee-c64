#!/usr/bin/env python3
"""
build_clean_game.py - Extract raw memory segments from ram_game_start_0400.bin
and construct a clean, standalone, cracktro-free Bruce Lee PRG.
"""

import sys
import os
import struct

def build():
    with open("dumps/ram_game_start_0400.bin", "rb") as f:
        ram = f.read()

    # 1. Extract raw binary chunks
    main_0400_c6ff = ram[0x0400:0xC700]
    with open("dumps/brucelee_main_0400_c6ff.bin", "wb") as f:
        f.write(main_0400_c6ff)
    print(f"Extracted main game code: {len(main_0400_c6ff)} bytes ($0400-$C6FF)")

    kernal_e000_f1ff = ram[0xE000:0xF200]
    with open("dumps/brucelee_under_kernal_e000_f1ff.bin", "wb") as f:
        f.write(kernal_e000_f1ff)
    print(f"Extracted under-KERNAL RAM: {len(kernal_e000_f1ff)} bytes ($E000-$F1FF)")

    vectors = ram[0xFFFA:0x10000]
    with open("dumps/brucelee_vectors_fffa_ffff.bin", "wb") as f:
        f.write(vectors)
    print(f"Extracted RAM vectors: {len(vectors)} bytes ($FFFA-$FFFF)")

    # 2. Build standalone clean PRG:
    # Memory layout when loading at $0801:
    # $0801: BASIC stub: 10 SYS 2061 ($080D)
    # At $080D: Bootstrap code to copy installer to $0340 and run it.
    # From $0850 to $C6FF: Genuine unpacked game RAM.
    # At $C700: Appended buffers:
    #   - Buffer 1: $0400-$07FF (1024 bytes)
    #   - Buffer 2: $0800-$084F (80 bytes to restore original $0800-$084F)
    #   - Buffer 3: $E000-$F1FF (4608 bytes)
    #   - Buffer 4: $FFFA-$FFFF (6 bytes)

    # Let's craft the installer routine to run in tape buffer ($0340):
    # Addresses of buffers appended after $C700:
    buf_0400 = 0xC700
    buf_0800 = buf_0400 + 0x0400 # $CB00
    buf_e000 = buf_0800 + 0x0050 # $CB50
    buf_vec  = buf_e000 + 0x1200 # $DD50

    # Assembly for $0340 installer:
    # SEI
    # LDA #$34
    # STA $01         ; All RAM mode
    #
    # ; 1. Copy $0400-$07FF (4 pages) from buf_0400 ($CB00 is actually buf_0800, buf_0400 is $C700)
    # LDX #$00
    # loop1:
    # LDA $C700,X
    # STA $0400,X
    # LDA $C800,X
    # STA $0500,X
    # LDA $C900,X
    # STA $0600,X
    # LDA $CA00,X
    # STA $0700,X
    # INX
    # BNE loop1
    #
    # ; 2. Copy $0800-$084F (80 bytes) from buf_0800 ($CB00)
    # LDX #$4F
    # loop2:
    # LDA $CB00,X
    # STA $0800,X
    # DEX
    # BPL loop2
    #
    # ; 3. Copy $E000-$F1FF (18 pages = $12 pages) from buf_e000 ($CB50)
    # ; We can use 16-bit pointers in zero page $FA/$FB (src) and $FC/$FD (dest)
    # LDA #$50
    # STA $FA
    # LDA #$CB
    # STA $FB
    # LDA #$00
    # STA $FC
    # LDA #$E0
    # STA $FD
    # LDY #$00
    # loop3:
    # LDA ($FA),Y
    # STA ($FC),Y
    # INY
    # BNE loop3
    # INC $FB
    # INC $FD
    # LDA $FD
    # CMP #$F2
    # BNE loop3
    #
    # ; 4. Copy 6 bytes of vectors to $FFFA
    # LDX #$05
    # loop4:
    # LDA $DD50,X
    # STA $FFFA,X
    # DEX
    # BPL loop4
    #
    # ; 5. Set $01 = $36 (KERNAL + I/O, BASIC off), JMP $0400
    # LDA #$36
    # STA $01
    # CLI
    # JMP $0400

    installer_code = bytearray([
        0x78,             # SEI
        0xA9, 0x34,       # LDA #$34
        0x85, 0x01,       # STA $01

        # 1. Copy 4 pages to $0400-$07FF
        0xA2, 0x00,       # LDX #$00
        # loop1 ($0347):
        0xBD, 0x00, 0xC7, # LDA $C700,X
        0x9D, 0x00, 0x04, # STA $0400,X
        0xBD, 0x00, 0xC8, # LDA $C800,X
        0x9D, 0x00, 0x05, # STA $0500,X
        0xBD, 0x00, 0xC9, # LDA $C900,X
        0x9D, 0x00, 0x06, # STA $0600,X
        0xBD, 0x00, 0xCA, # LDA $CA00,X
        0x9D, 0x00, 0x07, # STA $0700,X
        0xE8,             # INX
        0xD0, 0xE7,       # BNE loop1

        # 2. Copy 80 bytes ($0800-$084F)
        0xA2, 0x4F,       # LDX #$4F
        # loop2:
        0xBD, 0x00, 0xCB, # LDA $CB00,X
        0x9D, 0x00, 0x08, # STA $0800,X
        0xCA,             # DEX
        0x10, 0xF7,       # BPL loop2

        # 3. Copy $E000-$F1FF ($1200 bytes = 18 pages)
        0xA9, 0x50,       # LDA #$50 (low byte of $CB50)
        0x85, 0xFA,       # STA $FA
        0xA9, 0xCB,       # LDA #$CB (high byte of $CB50)
        0x85, 0xFB,       # STA $FB
        0xA9, 0x00,       # LDA #$00
        0x85, 0xFC,       # STA $FC
        0xA9, 0xE0,       # LDA #$E0
        0x85, 0xFD,       # STA $FD
        0xA0, 0x00,       # LDY #$00
        # loop3 ($0384):
        0xB1, 0xFA,       # LDA ($FA),Y
        0x91, 0xFC,       # STA ($FC),Y
        0xC8,             # INY
        0xD0, 0xF9,       # BNE loop3
        0xE6, 0xFB,       # INC $FB
        0xE6, 0xFD,       # INC $FD
        0xA5, 0xFD,       # LDA $FD
        0xC9, 0xF2,       # CMP #$F2
        0xD0, 0xEE,       # BNE loop3

        # 4. Copy vectors ($DD50 -> $FFFA)
        0xA2, 0x05,       # LDX #$05
        # loop4:
        0xBD, 0x50, 0xDD, # LDA $DD50,X
        0x9D, 0xFA, 0xFF, # STA $FFFA,X
        0xCA,             # DEX
        0x10, 0xF7,       # BPL loop4

        # 5. Switch to $36 and jump to game
        0xA9, 0x36,       # LDA #$36
        0x85, 0x01,       # STA $01
        0x58,             # CLI
        0x4C, 0x00, 0x04  # JMP $0400
    ])

    print(f"Installer size: {len(installer_code)} bytes")
    assert len(installer_code) <= 0xC0 # fits comfortably in $0340-$03FF

    # Bootstrap code at $080D:
    # Copies installer_code to $0340 and jumps to $0340.
    # $080D:
    #   SEI
    #   LDX #len(installer_code)-1
    # copy_inst:
    #   LDA $0817,X
    #   STA $0340,X
    #   DEX
    #   BPL copy_inst
    #   JMP $0340
    # $0817: <installer_code>
    # This total size is ~10 + len(installer_code) = ~120 bytes (fits well within $080D-$084F = 67 bytes? wait!)
    # Let's check: $084F - $080D = 66 bytes!
    # If len(installer_code) is 108 bytes, it won't fit between $080D and $084F!
    # Where can the installer be stored?
    # At $C700!
    # If the installer is stored in the buffer at $C700, then $080D only needs:
    #   SEI
    #   LDX #len(installer_code)-1
    # copy:
    #   LDA <addr>,X
    #   STA $0340,X
    #   DEX
    #   BPL copy
    #   JMP $0340
    # That is only 15 BYTES! 15 bytes easily fits in $080D-$084F!

    # Let's organize the appended buffer at $C700:
    # $C700: installer_code (e.g. 110 bytes) -> padded to 128 bytes ($80)
    # $C780: Buffer for $0400-$07FF (1024 bytes = $0400) -> ends at $CB80
    # $CB80: Buffer for $0800-$084F (80 bytes = $0050) -> ends at $CBD0
    # $CBD0: Buffer for $E000-$F1FF (4608 bytes = $1200) -> ends at $DDD0
    # $DDD0: Buffer for $FFFA-$FFFF (6 bytes) -> ends at $DDD6

    buf_installer = 0xC700
    buf_0400 = 0xC780
    buf_0800 = 0xCB80
    buf_e000 = 0xCBD0
    buf_vec  = 0xDDD0

    # Let's adjust installer_code addresses to match these new buffers:
    installer_code = bytearray([
        0x78,             # SEI
        0xA9, 0x34,       # LDA #$34
        0x85, 0x01,       # STA $01

        # 1. Copy 4 pages to $0400-$07FF from $C780
        0xA2, 0x00,       # LDX #$00
        # loop1:
        0xBD, 0x80, 0xC7, # LDA $C780,X
        0x9D, 0x00, 0x04, # STA $0400,X
        0xBD, 0x80, 0xC8, # LDA $C880,X
        0x9D, 0x00, 0x05, # STA $0500,X
        0xBD, 0x80, 0xC9, # LDA $C980,X
        0x9D, 0x00, 0x06, # STA $0600,X
        0xBD, 0x80, 0xCA, # LDA $CA80,X
        0x9D, 0x00, 0x07, # STA $0700,X
        0xE8,             # INX
        0xD0, 0xE7,       # BNE loop1

        # 2. Copy 80 bytes ($0800-$084F) from $CB80
        0xA2, 0x4F,       # LDX #$4F
        # loop2:
        0xBD, 0x80, 0xCB, # LDA $CB80,X
        0x9D, 0x00, 0x08, # STA $0800,X
        0xCA,             # DEX
        0x10, 0xF7,       # BPL loop2

        # 3. Copy $E000-$F1FF ($1200 bytes) from $CBD0
        0xA9, 0xD0,       # LDA #$D0 (low byte of $CBD0)
        0x85, 0xFA,       # STA $FA
        0xA9, 0xCB,       # LDA #$CB (high byte of $CBD0)
        0x85, 0xFB,       # STA $FB
        0xA9, 0x00,       # LDA #$00
        0x85, 0xFC,       # STA $FC
        0xA9, 0xE0,       # LDA #$E0
        0x85, 0xFD,       # STA $FD
        0xA0, 0x00,       # LDY #$00
        # loop3:
        0xB1, 0xFA,       # LDA ($FA),Y
        0x91, 0xFC,       # STA ($FC),Y
        0xC8,             # INY
        0xD0, 0xF9,       # BNE loop3
        0xE6, 0xFB,       # INC $FB
        0xE6, 0xFD,       # INC $FD
        0xA5, 0xFD,       # LDA $FD
        0xC9, 0xF2,       # CMP #$F2
        0xD0, 0xEE,       # BNE loop3

        # 4. Copy vectors ($DDD0 -> $FFFA)
        0xA2, 0x05,       # LDX #$05
        # loop4:
        0xBD, 0xD0, 0xDD, # LDA $DDD0,X
        0x9D, 0xFA, 0xFF, # STA $FFFA,X
        0xCA,             # DEX
        0x10, 0xF7,       # BPL loop4

        # 5. Switch to $36 and jump to game
        0xA9, 0x36,       # LDA #$36
        0x85, 0x01,       # STA $01
        0x58,             # CLI
        0x4C, 0x00, 0x04  # JMP $0400
    ])

    inst_len = len(installer_code)
    print(f"Final installer length: {inst_len} bytes")

    # Bootstrap code at $080D:
    # 78                SEI
    # A2 <len-1>        LDX #<len-1>
    # BD 00 C7          LDA $C700,X
    # 9D 40 03          STA $0340,X
    # CA                DEX
    # 10 F7             BPL -9
    # 4C 40 03          JMP $0340
    boot_code = bytearray([
        0x78,                   # SEI
        0xA2, inst_len - 1,     # LDX #len-1
        0xBD, 0x00, 0xC7,       # LDA $C700,X
        0x9D, 0x40, 0x03,       # STA $0340,X
        0xCA,                   # DEX
        0x10, 0xF7,             # BPL copy
        0x4C, 0x40, 0x03        # JMP $0340
    ])

    # Construct the PRG:
    # Header: Load Address $0801
    prg = bytearray([0x01, 0x08])

    # BASIC stub:
    # $0801: 0B 08 CA 07 9E 32 30 36 31 00 00 00
    # 1994 SYS 2061 ($080D)
    basic_stub = bytearray([
        0x0B, 0x08,             # Pointer to next line ($080B)
        0xCA, 0x07,             # Line number 1994
        0x9E,                   # SYS token
        0x32, 0x30, 0x36, 0x31, # "2061"
        0x00,                   # End of line
        0x00, 0x00              # End of BASIC program
    ])
    assert len(basic_stub) == 12 # $0801 to $080C

    # Add bootstrap code at $080D
    stub_and_boot = basic_stub + boot_code
    print(f"Stub + boot size: {len(stub_and_boot)} bytes ($0801-${0x0801 + len(stub_and_boot) - 1:04X})")

    # Fill up to $0850 with NOPs
    if len(stub_and_boot) < 0x50 - 1:
        stub_and_boot += bytearray([0xEA] * (0x50 - 1 - len(stub_and_boot)))

    prg += stub_and_boot

    # Add main game body from $0850 up to $C6FF
    prg += ram[0x0850:0xC700]

    # Now we are at offset corresponding to address $C700:
    # 1. Padded installer at $C700 (128 bytes)
    inst_padded = installer_code + bytearray(128 - len(installer_code))
    prg += inst_padded

    # 2. Buffer for $0400-$07FF (1024 bytes) at $C780
    prg += ram[0x0400:0x0800]

    # 3. Buffer for $0800-$084F (80 bytes) at $CB80
    prg += ram[0x0800:0x0850]

    # 4. Buffer for $E000-$F1FF (4608 bytes) at $CBD0
    prg += ram[0xE000:0xF200]

    # 5. Buffer for $FFFA-$FFFF (6 bytes) at $DDD0
    prg += ram[0xFFFA:0x10000]

    with open("brucelee_clean.prg", "wb") as f:
        f.write(prg)

    total_len = len(prg)
    load_addr = prg[0] | (prg[1] << 8)
    end_addr = load_addr + total_len - 3
    print(f"SUCCESS: Created brucelee_clean.prg: {total_len} bytes")
    print(f"Load Address: ${load_addr:04X}, End Address: ${end_addr:04X}")

if __name__ == "__main__":
    build()
