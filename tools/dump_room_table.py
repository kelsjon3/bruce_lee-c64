#!/usr/bin/env python3
"""
dump_room_table.py - Dump the Master Room Layout Pointer Table at $4AA8.
"""

def dump():
    with open("dumps/ram_game_start_0400.bin", "rb") as f:
        ram = f.read()

    print("=== MASTER ROOM LAYOUT POINTER TABLE ($4AA8) ===")
    for r in range(20):
        ptr = ram[0x4AA8 + r*2] | (ram[0x4AA9 + r*2] << 8)
        header = [ram[ptr + i] for i in range(20)]
        header_hex = " ".join(f"{b:02X}" for b in header)
        print(f"Room {r:2d} (${r:02X}): Pointer=${ptr:04X} -> Header: {header_hex}")

if __name__ == "__main__":
    dump()
