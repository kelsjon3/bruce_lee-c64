#!/usr/bin/env python3
"""
find_tilemaps.py - Locate screen tile data and room rendering routines.
"""

def find_tilemaps():
    with open("dumps/ram_game_start_0400.bin", "rb") as f:
        ram = f.read()

    # In $09BC (screen drawer), it cleared screen and then what did it call?
    # Let's inspect $09F0-$0AB0 to see how $09BC renders the room tiles.
    print("Screen drawer $09F0-$0A80 disassembly flow:")
    import subprocess
    cmd = ["python3", "tools/disasm6502.py", "dumps/ram_game_start_0400.bin", "0A20", "0A20", "60"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)

if __name__ == "__main__":
    find_tilemaps()
