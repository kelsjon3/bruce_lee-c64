#!/usr/bin/env python3
"""
inspect_layout_pointers.py - Dump the Room Screen Tile Layout tables ($4B34 / $4B49).
"""

def inspect():
    with open("dumps/ram_game_start_0400.bin", "rb") as f:
        ram = f.read()

    print("=== ROOM SCREEN TILE LAYOUT TABLES ($4B34 / $4B49) ===")
    for r in range(21):
        low = ram[0x4B34 + r]
        high = ram[0x4B49 + r]
        ptr = low | (high << 8)
        bytes_preview = " ".join(f"{ram[ptr+i]:02X}" for i in range(16))
        print(f"Room {r:2d}: Address=${ptr:04X} -> Data: {bytes_preview}")

if __name__ == "__main__":
    inspect()
