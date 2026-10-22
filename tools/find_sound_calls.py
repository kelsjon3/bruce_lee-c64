#!/usr/bin/env python3
"""
find_sound_calls.py - Find all invocations of the under-KERNAL sound driver.
"""

def find_calls():
    with open("dumps/ram_game_start_0400.bin", "rb") as f:
        ram = f.read()

    targets = {
        0xE000: "SOUND_INIT / RESET",
        0xE003: "SOUND_PLAY_SFX",
        0xE006: "SOUND_FRAME_TICK"
    }

    for i in range(len(ram)-2):
        if ram[i] == 0x20: # JSR
            addr = ram[i+1] | (ram[i+2] << 8)
            if addr in targets:
                print(f"JSR ${addr:04X} ({targets[addr]}) at ${i:04X} (prev bytes: {' '.join(f'${ram[i-3+j]:02X}' for j in range(3))})")

if __name__ == "__main__":
    find_calls()
