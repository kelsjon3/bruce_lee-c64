#!/usr/bin/env python3
"""
prg_tool.py - Commodore 64 PRG and memory analysis tool.
Capabilities:
- PRG header and layout parsing
- Hex dump with ASCII and PETSCII decoding
- String scanner (ASCII and PETSCII)
- Memory/PRG comparison
- Block extraction
"""

import sys
import os
import argparse

def petscii_to_ascii(byte_val):
    """Convert C64 PETSCII screen/un-shifted code to printable ASCII."""
    # Standard PETSCII conversions
    if 0x20 <= byte_val <= 0x5A:
        return chr(byte_val)
    elif 0x41 <= byte_val <= 0x5A:
        return chr(byte_val)
    elif 0x61 <= byte_val <= 0x7A:
        return chr(byte_val)
    elif 0xC1 <= byte_val <= 0xDA: # PETSCII uppercase in lower/upper mode
        return chr(byte_val - 0x80)
    elif byte_val == 0x0D:
        return '\n'
    return '.'

def dump_hex(data, start_addr=0x0000, length=None):
    if length is None:
        length = len(data)
    else:
        length = min(length, len(data))
    
    for i in range(0, length, 16):
        chunk = data[i:i+16]
        hex_str = " ".join(f"{b:02X}" for b in chunk).ljust(48)
        asc_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        pet_str = "".join(petscii_to_ascii(b) for b in chunk)
        print(f"${start_addr + i:04X}  {hex_str} |{asc_str}| |{pet_str}|")

def scan_strings(data, start_addr=0x0000, min_len=4):
    """Scan for ASCII and PETSCII strings."""
    results = []
    current_asc = []
    current_start = 0

    for idx, b in enumerate(data):
        # Printable ASCII or PETSCII alphanumeric
        if (32 <= b < 127):
            if not current_asc:
                current_start = start_addr + idx
            current_asc.append(chr(b))
        else:
            if len(current_asc) >= min_len:
                results.append((current_start, "".join(current_asc)))
            current_asc = []

    if len(current_asc) >= min_len:
        results.append((current_start, "".join(current_asc)))

    return results

def cmd_info(args):
    with open(args.file, "rb") as f:
        data = f.read()
    if len(data) < 2:
        print("Error: File too small for PRG header.")
        return
    load_addr = data[0] | (data[1] << 8)
    size = len(data) - 2
    end_addr = load_addr + size - 1
    print(f"File: {args.file}")
    print(f"Total size: {len(data)} bytes")
    print(f"Load Address: ${load_addr:04X} ({load_addr})")
    print(f"End Address:  ${end_addr:04X} (${end_addr + 1:04X} exclusive)")
    print(f"Payload Size: {size} bytes (${size:04X})")

def cmd_strings(args):
    with open(args.file, "rb") as f:
        data = f.read()
    if not args.raw:
        load_addr = data[0] | (data[1] << 8)
        payload = data[2:]
    else:
        load_addr = int(args.base_addr, 16) if args.base_addr.startswith("0x") or args.base_addr.startswith("$") else int(args.base_addr)
        payload = data
    
    strings = scan_strings(payload, load_addr, args.min_len)
    print(f"Found {len(strings)} strings (min_len={args.min_len}):")
    for addr, s in strings:
        print(f"${addr:04X}: {s}")

def cmd_hexdump(args):
    with open(args.file, "rb") as f:
        data = f.read()
    start_offset = 0
    start_addr = 0
    if args.is_prg:
        load_addr = data[0] | (data[1] << 8)
        start_offset = 2
        start_addr = load_addr
    if args.offset:
        start_offset = int(args.offset, 16) if args.offset.startswith("0x") or args.offset.startswith("$") else int(args.offset)
    if args.addr:
        start_addr = int(args.addr, 16) if args.addr.startswith("0x") or args.addr.startswith("$") else int(args.addr)
    
    length = int(args.length, 16) if args.length and (args.length.startswith("0x") or args.length.startswith("$")) else (int(args.length) if args.length else None)
    
    dump_hex(data[start_offset:], start_addr, length)

def cmd_diff(args):
    with open(args.file1, "rb") as f1, open(args.file2, "rb") as f2:
        d1 = f1.read()
        d2 = f2.read()
    print(f"File 1: {args.file1} ({len(d1)} bytes)")
    print(f"File 2: {args.file2} ({len(d2)} bytes)")
    min_len = min(len(d1), len(d2))
    diffs = 0
    diff_blocks = []
    in_diff = False
    diff_start = 0

    for i in range(min_len):
        if d1[i] != d2[i]:
            diffs += 1
            if not in_diff:
                in_diff = True
                diff_start = i
        else:
            if in_diff:
                in_diff = False
                diff_blocks.append((diff_start, i - 1))
    if in_diff:
        diff_blocks.append((diff_start, min_len - 1))

    print(f"Differences in common length ({min_len} bytes): {diffs} bytes differed.")
    print(f"Diff blocks ({len(diff_blocks)}):")
    for s, e in diff_blocks[:20]:
        print(f"  Offset ${s:04X} - ${e:04X} (len {e - s + 1})")
    if len(diff_blocks) > 20:
        print(f"  ... and {len(diff_blocks) - 20} more blocks.")

def main():
    parser = argparse.ArgumentParser(description="Commodore 64 PRG/memory tool")
    subparsers = parser.add_subparsers(dest="cmd")

    info_p = subparsers.add_parser("info", help="Show PRG information")
    info_p.add_argument("file")

    str_p = subparsers.add_parser("strings", help="Find strings")
    str_p.add_argument("file")
    str_p.add_argument("--raw", action="store_true", help="Treat input as raw binary (not PRG)")
    str_p.add_argument("--base-addr", default="0")
    str_p.add_argument("--min-len", type=int, default=4)

    hex_p = subparsers.add_parser("hexdump", help="Hex dump")
    hex_p.add_argument("file")
    hex_p.add_argument("--is-prg", action="store_true", default=False)
    hex_p.add_argument("--offset", default=None)
    hex_p.add_argument("--addr", default=None)
    hex_p.add_argument("--length", default=None)

    diff_p = subparsers.add_parser("diff", help="Compare two binary files")
    diff_p.add_argument("file1")
    diff_p.add_argument("file2")

    args = parser.parse_args()
    if args.cmd == "info":
        cmd_info(args)
    elif args.cmd == "strings":
        cmd_strings(args)
    elif args.cmd == "hexdump":
        cmd_hexdump(args)
    elif args.cmd == "diff":
        cmd_diff(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
