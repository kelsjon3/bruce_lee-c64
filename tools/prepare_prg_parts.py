#!/usr/bin/env python3
"""
prepare_prg_parts.py - Prepare individual PRG segments for exomizer sfx.
"""

def prepare():
    with open("dumps/ram_game_start_0400.bin", "rb") as f:
        ram = f.read()

    # Part 1: Main code $0400-$C6FF
    # PRG header: $00, $04 (load address $0400)
    with open("dumps/part_main.prg", "wb") as f:
        f.write(bytearray([0x00, 0x04]))
        f.write(ram[0x0400:0xC700])
    print("Created dumps/part_main.prg ($0400-$C6FF)")

    # Part 2: Under-KERNAL RAM $E000-$F1FF
    # PRG header: $00, $E0 (load address $E000)
    with open("dumps/part_kernal.prg", "wb") as f:
        f.write(bytearray([0x00, 0xE0]))
        f.write(ram[0xE000:0xF200])
    print("Created dumps/part_kernal.prg ($E000-$F1FF)")

    # Part 3: Vectors $FFFA-$FFFF
    # PRG header: $FA, $FF (load address $FFFA)
    with open("dumps/part_vectors.prg", "wb") as f:
        f.write(bytearray([0xFA, 0xFF]))
        f.write(ram[0xFFFA:0x10000])
    print("Created dumps/part_vectors.prg ($FFFA-$FFFF)")

if __name__ == "__main__":
    prepare()
