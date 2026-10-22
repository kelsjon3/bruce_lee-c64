#!/usr/bin/env python3
"""
render_screen.py - Render C64 text/multicolour screen from memory dump to PNG.
"""

import sys
import os

# Standard C64 RGB Palette (VICE Pepto / Colodore)
C64_PALETTE = [
    (0x00, 0x00, 0x00), # 0: Black
    (0xFF, 0xFF, 0xFF), # 1: White
    (0x88, 0x00, 0x00), # 2: Red
    (0xAA, 0xFF, 0xEE), # 3: Cyan
    (0xCC, 0x44, 0xCC), # 4: Purple
    (0x00, 0xCC, 0x55), # 5: Green
    (0x00, 0x00, 0xAA), # 6: Blue
    (0xEE, 0xEE, 0x77), # 7: Yellow
    (0xDD, 0x88, 0x55), # 8: Orange
    (0x66, 0x44, 0x00), # 9: Brown
    (0xFF, 0x77, 0x77), # 10: Light Red
    (0x33, 0x33, 0x33), # 11: Dark Grey
    (0x77, 0x77, 0x77), # 12: Grey
    (0xAA, 0xFF, 0x66), # 13: Light Green
    (0x00, 0x88, 0xFF), # 14: Light Blue
    (0xBB, 0xBB, 0xBB), # 15: Light Grey
]

def render_title_screen(ram_file, output_png):
    with open(ram_file, "rb") as f:
        ram = f.read()

    width = 320
    height = 200
    pixels = bytearray(width * height * 3)

    # In Bruce Lee title screen:
    # Screen RAM: $8C00
    # Top rows (0-11): Multicolour with font at $8000
    # Bottom rows (12-24): Standard text with font at $8800
    # Background: Blue (6)
    # Multicolour 1 ($D022): $FF & 0x0F = 15 (Light Grey)
    # Multicolour 2 ($D023): $FF & 0x0F = 15 (Light Grey)

    bg_color = C64_PALETTE[6]
    mc1_color = C64_PALETTE[15]
    mc2_color = C64_PALETTE[15]
    fg_color = C64_PALETTE[1] # White

    screen_base = 0x8C00

    for row in range(25):
        font_base = 0x8000 if row < 12 else 0x8800
        is_multicolor = (row < 12)

        for col in range(40):
            char_code = ram[screen_base + row * 40 + col]
            char_data = ram[font_base + char_code * 8 : font_base + char_code * 8 + 8]

            for y_char in range(8):
                byte = char_data[y_char]
                y_pos = row * 8 + y_char

                if is_multicolor:
                    # Multicolour: 4 double-width pixels
                    for x_pair in range(4):
                        bits = (byte >> ((3 - x_pair) * 2)) & 0x03
                        if bits == 0:
                            rgb = bg_color
                        elif bits == 1:
                            rgb = mc1_color
                        elif bits == 2:
                            rgb = mc2_color
                        else:
                            rgb = fg_color

                        # 2 horizontal pixels
                        for dx in range(2):
                            x_pos = col * 8 + x_pair * 2 + dx
                            idx = (y_pos * width + x_pos) * 3
                            pixels[idx] = rgb[0]
                            pixels[idx + 1] = rgb[1]
                            pixels[idx + 2] = rgb[2]
                else:
                    # Hi-res standard text: 8 pixels
                    for x_bit in range(8):
                        bit = (byte >> (7 - x_bit)) & 1
                        rgb = fg_color if bit else bg_color
                        x_pos = col * 8 + x_bit
                        idx = (y_pos * width + x_pos) * 3
                        pixels[idx] = rgb[0]
                        pixels[idx + 1] = rgb[1]
                        pixels[idx + 2] = rgb[2]

    # Write uncompressed PPM then convert to PNG
    ppm_file = output_png + ".ppm"
    with open(ppm_file, "wb") as f:
        f.write(f"P6\n{width} {height}\n255\n".encode())
        f.write(pixels)

    os.system(f"convert '{ppm_file}' '{output_png}' && rm -f '{ppm_file}'")
    print(f"Rendered screen to {output_png}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: render_screen.py <ram_dump> <output_png>")
        sys.exit(1)
    render_title_screen(sys.argv[1], sys.argv[2])
