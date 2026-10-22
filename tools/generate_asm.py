#!/usr/bin/env python3
"""
generate_asm.py - Disassemble and reconstruct structured, commented 6502 assembly source modules.
"""

import os
from disasm6502 import OPCODES, C64_SYMBOLS, disassemble_raw

# Domain-specific symbols discovered during reverse engineering
GAME_SYMBOLS = {
    # Zero page variables
    0x0000: "D6510_DIR",
    0x0001: "D6510_DATA",
    0x0003: "VAR_CURRENT_PLAYER",
    0x0004: "PTR_SCREEN_LO",
    0x0005: "PTR_SCREEN_HI",
    0x0006: "PTR_STRING_LO",
    0x0007: "PTR_STRING_HI",
    0x0008: "PTR_COLOR_LO",
    0x0009: "PTR_COLOR_HI",
    0x000E: "PTR_SPRITE_SHAPE_LO",
    0x000F: "PTR_SPRITE_SHAPE_HI",
    0x001B: "VAR_CHAR_SUBPIXEL_X",
    0x001C: "VAR_CHAR_SUBPIXEL_Y",
    0x0028: "VAR_PLAYER_LIVES",
    0x0029: "VAR_CURRENT_ROOM",
    0x0048: "VAR_FRAME_DELAY_COUNTER",
    0x0049: "VAR_TIMER_LO",
    0x004A: "VAR_TIMER_HI",
    0x004C: "VAR_COLLISION_TEMP",
    0x0050: "VAR_ACTIVE_CHAR_IDX",
    0x005D: "VAR_NINJA_SPAWN_TIMER",
    0x005E: "VAR_YAMO_SPAWN_TIMER",
    0x0067: "VAR_SPSPCL_SHADOW",
    0x007A: "VAR_ROOM_HAZARD_FLAG",
    0x007B: "VAR_PUNCH_COOLDOWN",
    0x0095: "TAB_CHAR_ACTIVE",
    0x009E: "TAB_CHAR_POS_X",
    0x00A1: "TAB_CHAR_POS_Y",
    0x00B3: "TAB_BRUCE_COLLISION",
    0x00B4: "TAB_NINJA_COLLISION",
    0x00B5: "TAB_YAMO_COLLISION",
    0x00E6: "TAB_CHAR_TILE_COL",
    0x00E9: "TAB_CHAR_TILE_ROW",
    0x00F2: "VAR_VMCSB_SHADOW",
    0x00F3: "VAR_ATTR_COUNTER",

    # Important game routines & vectors
    0x0400: "game_entry",
    0x04D1: "game_init_continue",
    0x050F: "game_start_play",
    0x0584: "title_setup",
    0x070B: "title_input_loop",
    0x0760: "title_start_game",
    0x0763: "screen_clear_and_init",
    0x08B1: "title_wait_input",
    0x094B: "wait_joystick_release",
    0x09BC: "render_room_screen",
    0x0D0F: "enemy_ai_green_yamo",
    0x0DA4: "enemy_ai_ninja",
    0x0DB1: "hazard_update",
    0x0E4C: "title_render_player_mode",
    0x0E65: "title_render_game_mode",
    0x1103: "irq_dispatcher",
    0x152C: "irq_raster_split_top",
    0x1574: "irq_raster_split_bottom",
    0x17E2: "print_string",
    0x1818: "player_death",
    0x19B8: "read_player_input",
    0x1A96: "player_physics_update",
    0x1BC2: "main_game_loop",
    0x2584: "sound_effects_dispatcher",
    0x26A0: "blit_sprite_shape",
    0x29C3: "collision_detect_sprites",
    0x2D55: "check_room_transition",
    0x2E39: "combat_hit_detection",
    0x2FA0: "room_transition_handler",
    0x3001: "reset_enemy_position",
    0x3184: "check_player_health",
    0x3A6F: "check_lanterns_and_doors",
    0x40BC: "check_tile_collision",
    0x5212: "update_sprite_multiplexer",

    # Tables & data
    0x1167: "tbl_sprite_frame_lo",
    0x1239: "tbl_sprite_frame_hi",
    0x131F: "tbl_yamo_spawn_per_room",
    0x135B: "tbl_ninja_spawn_per_room",
    0x42C9: "var_selected_game_mode",
    0x42CA: "var_selected_player_mode",
    0x43BE: "tbl_string_pointers",
    0x47A0: "tbl_room_bg_colors",
    0x4AA8: "tbl_master_room_pointers",
    0x4B34: "tbl_room_tiles_lo",
    0x4B49: "tbl_room_tiles_hi",
    0x4EA0: "tbl_room_events_1",
    0x4EC4: "tbl_room_events_2",
    0x4F4E: "tab_char_anim_frame",

    # Under-KERNAL sound driver routines
    0xE000: "SOUND_DRIVER_INIT",
    0xE003: "SOUND_DRIVER_PLAY_SFX",
    0xE006: "SOUND_DRIVER_FRAME_TICK",
    0xE300: "snd_init_engine",
    0xE306: "snd_start_track",
    0xE49E: "snd_frame_update",
}

def get_merged_symbols():
    syms = dict(C64_SYMBOLS)
    syms.update(GAME_SYMBOLS)
    return syms

def disassemble_range(ram, start_addr, end_addr, symbols, labels):
    lines = []
    pc = start_addr
    while pc <= end_addr and pc < len(ram):
        offset = pc
        if pc in labels:
            lines.append(f"\n{labels[pc]}:")
        
        mnemonic, operand_str, comment, length = disassemble_raw(ram, offset, pc, symbols)
        if length == 0:
            lines.append(f"        .byte   ${ram[offset]:02X}")
            pc += 1
            continue
        
        instr_str = f"{mnemonic:<7} {operand_str}".rstrip()
        if comment:
            lines.append(f"        {instr_str:<32} ; {comment}")
        else:
            lines.append(f"        {instr_str}")
        pc += length
    return "\n".join(lines)

def generate_module(filename, title, ram, ranges, symbols):
    # Collect all jump/branch targets inside ranges to create local labels
    labels = {}
    for sym_addr, sym_name in GAME_SYMBOLS.items():
        for r_start, r_end in ranges:
            if r_start <= sym_addr <= r_end:
                labels[sym_addr] = sym_name

    header = f"""; ==============================================================================
; {title}
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

"""
    body = []
    for r_start, r_end in ranges:
        body.append(f"; --- Range: ${r_start:04X} - ${r_end:04X} ---")
        dis = disassemble_range(ram, r_start, r_end, symbols, labels)
        body.append(dis)
        body.append("")

    content = header + "\n".join(body)
    with open(filename, "w") as f:
        f.write(content)
    print(f"Generated {filename} ({len(content)} bytes)")

def build_all():
    os.makedirs("src", exist_ok=True)
    with open("dumps/ram_game_start_0400.bin", "rb") as f:
        ram = f.read()

    symbols = get_merged_symbols()

    # 1. Main entry, startup, and game loop
    generate_module(
        "src/main.asm",
        "Bruce Lee - Main Entry, Startup & Core Loop ($0400-$0580, $1BC2-$1C80)",
        ram,
        [(0x0400, 0x0583), (0x1BC2, 0x1C80)],
        symbols
    )

    # 2. Title screen & Attract Mode
    generate_module(
        "src/title.asm",
        "Bruce Lee - Title Screen, Attract Mode & Options ($0584-$0762, $08B1-$0970, $0E4C-$0EA6)",
        ram,
        [(0x0584, 0x0762), (0x08B1, 0x0970), (0x0E4C, 0x0EA6)],
        symbols
    )

    # 3. Raster IRQ & Interrupt Dispatcher
    generate_module(
        "src/irq.asm",
        "Bruce Lee - Raster IRQ Dispatcher & Screen Splits ($1103-$1165, $152C-$15A8)",
        ram,
        [(0x1103, 0x1165), (0x152C, 0x15A8)],
        symbols
    )

    # 4. Player Input, Physics & Motion
    generate_module(
        "src/player.asm",
        "Bruce Lee - Player Input & Character Physics ($19B8-$1B20)",
        ram,
        [(0x19B8, 0x1B20)],
        symbols
    )

    # 5. Enemies & Hazards AI
    generate_module(
        "src/enemies.asm",
        "Bruce Lee - Enemy AI (Ninja, Green Yamo) & Hazards ($0D0F-$0DF0)",
        ram,
        [(0x0D0F, 0x0DF0)],
        symbols
    )

    # 6. Combat & Collision Detection
    generate_module(
        "src/combat.asm",
        "Bruce Lee - Sprite-to-Sprite Collision & Combat ($29C0-$2A30, $2E39-$2E90, $1818-$1850)",
        ram,
        [(0x29C0, 0x2A30), (0x2E39, 0x2E90), (0x1818, 0x1850)],
        symbols
    )

    # 7. Room Transition & Screen Tile Renderer
    generate_module(
        "src/rooms.asm",
        "Bruce Lee - Room Transition & Screen Tile Rendering ($09BC-$0B30, $2D55-$2D80, $2FA0-$2FD5)",
        ram,
        [(0x09BC, 0x0B30), (0x2D55, 0x2D80), (0x2FA0, 0x2FD5)],
        symbols
    )

    # 8. Sprite Multiplexer & Animation Dispatcher
    generate_module(
        "src/sprites.asm",
        "Bruce Lee - Sprite Multiplexer & Animation Blitter ($5212-$52A5, $26A0-$2700)",
        ram,
        [(0x5212, 0x52A5), (0x26A0, 0x2700)],
        symbols
    )

    # 9. In-Game Text & String Printing
    generate_module(
        "src/strings.asm",
        "Bruce Lee - HUD & String Printing Routine ($17E2-$1817)",
        ram,
        [(0x17E2, 0x1817)],
        symbols
    )

    # 10. Under-KERNAL Sound Driver Interface
    with open("dumps/brucelee_under_kernal_e000_f1ff.bin", "rb") as f_k:
        ram_kernal = bytearray(0x10000)
        ram_kernal[0xE000:0xF200] = f_k.read()

    generate_module(
        "src/sound.asm",
        "Bruce Lee - Under-KERNAL Micropearl Sound Driver ($E000-$E030, $E300-$E3B8, $E49E-$E4E0)",
        ram_kernal,
        [(0xE000, 0xE030), (0xE300, 0xE3B8), (0xE49E, 0xE4E0)],
        symbols
    )

if __name__ == "__main__":
    build_all()
