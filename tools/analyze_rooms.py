#!/usr/bin/env python3
"""
analyze_rooms.py - Inspect and decode room definitions, tilemaps, and spawn data.
"""

def analyze():
    with open("dumps/ram_game_start_0400.bin", "rb") as f:
        ram = f.read()

    print("=== ROOM POINTER TABLES ===")
    table1 = []
    for i in range(20):
        ptr = ram[0x4EA0 + i*2] | (ram[0x4EA1 + i*2] << 8)
        table1.append(ptr)

    table2 = []
    for i in range(18):
        ptr = ram[0x4EC8 + i*2] | (ram[0x4EC9 + i*2] << 8)
        table2.append(ptr)

    print(f"Table 1 at $4EA0 ({len(table1)} entries):")
    for r, p in enumerate(table1):
        print(f"  Room {r:2d}: ${p:04X} -> bytes: {' '.join(f'{ram[p+j]:02X}' for j in range(16))}")

    print(f"\nTable 2 at $4EC8 ({len(table2)} entries):")
    for r, p in enumerate(table2):
        print(f"  Room {r:2d}: ${p:04X} -> bytes: {' '.join(f'{ram[p+j]:02X}' for j in range(16))}")

    print("\n=== ROOM ATTRIBUTES ($47A0) ===")
    colors = ram[0x47A0:0x47B4]
    for r, c in enumerate(colors):
        print(f"  Room {r:2d}: Color ${c:02X} (Color Index: {c & 0x0F})")

    print("\n=== ENEMY SPAWN PER ROOM ===")
    for r in range(20):
        yamo = ram[0x131F + r]
        ninja = ram[0x135B + r]
        print(f"  Room {r:2d}: Green Yamo=${yamo:02X}, Ninja=${ninja:02X}")

if __name__ == "__main__":
    analyze()
