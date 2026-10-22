# Bruce Lee (C64) - Reverse Engineering Notes

## Executive Summary

The game image on `Bruce Lee.d64` (`"bruce lee+2 /rem"`, extracted as `brucelee.prg`) is a multi-stage packed release cracked by the group **REMEMBER** (dating to ~2001). It contains two full decompression layers, a cracktro/doc reader scroller, an in-memory relocation loop, an RLE graphical expander, a trainer selector, and finally the original uncompressed game engine.

Through VICE monitor tracing and breakpoint automation, the entire execution flow from BASIC start `$0801` to the pristine game entry point at `$0400` was traced and verified. Full memory states at key milestones were dumped to disk.

---

## Binary Overview

- **Source Disk**: `Bruce Lee.d64` (174,848 bytes, 35 tracks D64)
- **Extracted File**: `brucelee.prg` (40,472 bytes)
- **Load Address**: `$0801` (standard C64 BASIC load address)
- **End Address**: `$A617`
- **BASIC Stub**:
  ```text
  $0801: 0B 08 CA 07 9E 32 30 35 39 00
  Decoded: 1994 SYS 2059
  ```
  `2059` decimal = `$080B`.

---

## Detailed Execution Pipeline

### Stage 1: Cracker Outer Bootloader & Unpacker
- **Entry**: `$080B`
- **Code**:
  ```asm
  $080B  A2 00       LDX #$00
  $080D  78          SEI
  $080E  E6 01       INC $01        ; Bank switching: switches out BASIC ROM ($01 becomes $38)
  $0810  BD 48 A5    LDA $A548,X    ; Copies 256 bytes from $A548-$A647
  $0813  9D F0 00    STA $00F0,X    ; into Zero Page / Stack ($00F0-$01EF)
  $0816  E8          INX
  $0817  D0 F7       BNE $0810
  $0819  4C 4E 01    JMP $014E      ; Jumps to unpacker entry
  ```
- **Relocated Unpacker (`$00F0-$01EF`)**:
  - Classic Commodore backward-expanding LZ/Huffman decruncher.
  - Source end pointer: `$A448` (`$FA, $FB`).
  - Destination end pointer: `$CF78` (`$FE, $FF`).
  - Unpacks backward from `$CF78` down to `$07FF` (expanding into `$0800-$CF78`).
  - Upon completion:
    ```asm
    $0146  A9 37      LDA #$37
    $0148  85 01      STA $01
    $014A  58         CLI
    $014B  4C 00 28   JMP $2800
    ```

### Stage 2: Remember Cracktro & Doc Reader
- **Entry**: `$2800`
- **Function**:
  - Initializes SID music at `$1006` (composed by Reyn Ouwehand, credits at `$1FE4`).
  - Sets up VIC-II sprite multiplexing and raster bars (`$2800-$28D0`).
  - Raster IRQ set to `$29A7`.
  - Checks joystick/spacebar at `$28E9`:
    ```asm
    $28E9  AD 01 DC   LDA $DC01
    $28EC  2D 00 DC   AND $DC00
    $28EF  29 10      AND #$10      ; Fire / space check
    $28F1  D0 F6      BNE $28E9
    ```
  - When pressed, cleans up VIC/SID (`$28F3-$292F`), copies 32 bytes from `$2987` to `$0340` (tape buffer), and presents doc scroller at `$2F40` ("DOCUMENTS TO BRUCE LEE", stored at `$3000-$5EE0`).
  - Stored behind the doc reader in memory (`$5EE0-$FFFF`) is the crunched Stage 2 payload.
  - Pressing space in the doc reader jumps to `$2FEE`, which executes `JMP $0340`.

### Stage 3: Relocation of Inner Payload
- **Entry**: `$0340` (tape buffer free area)
- **Code**:
  ```asm
  $0340  78          SEI
  $0341  A9 34       LDA #$34
  $0343  85 01       STA $01       ; All-RAM mode ($34: switches out BASIC, KERNAL, and I/O)
  $0345  A2 00       LDX #$00
  $0347  BD E0 5E    LDA $5EE0,X   ; Source starting at $5EE0
  $034A  9D 01 08    STA $0801,X   ; Destination starting at $0801
  $034D  E8          INX
  $034E  D0 F7       BNE $0347
  $0350  EE 4C 03    INC $034C     ; Increments dest high byte
  $0353  EE 49 03    INC $0349     ; Increments source high byte
  $0356  D0 ED       BNE $0347     ; Loops 162 pages (41,472 bytes) until source high byte wraps $FF->$00
  $0358  A9 37       LDA #$37
  $035A  85 01       STA $01       ; Re-enables ROMs
  $035C  58          CLI
  $035D  4C 0B 08    JMP $080B     ; Re-enters $080B (now holding Stage 2 bootstrap!)
  ```

### Stage 4: Stage 2 Inner Decruncher
- **Entry**: `$080B` (new contents relocated from `$5EEA`)
- **Code**:
  ```asm
  $080B  A2 00       LDX #$00
  $080D  78          SEI
  $080E  E6 01       INC $01
  $0810  BD CB 77    LDA $77CB,X   ; Copies inner unpacker from $77CB
  $0813  9D F0 00    STA $00F0,X   ; to $00F0-$01EF
  $0816  E8          INX
  $0817  D0 F7       BNE $0810
  $0819  4C 4E 01    JMP $014E
  ```
- **Relocated Unpacker (`$00F0-$01EF`)**:
  - Source pointer: `$76CB` (`$FA, $FB`).
  - Destination pointer: `$B472` (`$FE, $FF`).
  - Unpacks backward into `$0800-$B472`.
  - Upon completion:
    ```asm
    $0146  A9 37      LDA #$37
    $0148  85 01      STA $01
    $014A  58         CLI
    $014B  4C 02 08   JMP $0802
    ```

### Stage 5: In-Memory Relocator & RLE Expander
- **Entry**: `$0802`
- **Code**:
  ```asm
  $0802  A9 00       LDA #$00
  $0804  8D 20 D0    STA $D020     ; Border black
  $0807  8D 21 D0    STA $D021     ; Background black
  $080A  20 36 E5    JSR $E536     ; Clear screen
  $080D  78          SEI
  $080E  A2 FF       LDX #$FF
  $0810  9A          TXS
  $0811  A2 49       LDX #$49
  $0813  BD 1E 08    LDA $081E,X   ; Copies $49 bytes from $081F to $0001-$0049
  $0816  95 00       STA $00,X
  $0818  CA          DEX
  $0819  D0 F8       BNE $0813
  $081B  A0 F5       LDY #$F5
  $081D  4C 35 00    JMP $0035     ; Jumps into zero page
  ```
- **Zero Page Copier (`$0035`)**:
  - Relocates memory backward: copies `$B373` down to `$0700` up to `$FF00` down to `$5300`.
  - When source high byte decrements to `$06`, branches to `$0002`.
- **Zero Page RLE Expander (`$0002`)**:
  - Reads RLE-compressed data from `$5300` using escape byte `$D6`.
  - Expands into `$0800...`.
  - When finished:
    ```asm
    $002E  A9 37      LDA #$37
    $0030  85 01      STA $01
    $0032  58         CLI
    $0033  4C 00 C5   JMP $C500
    ```

### Stage 6: Remember Title Screen & Trainer Options
- **Entry**: `$C500`
- **Function**:
  - Sets bitmap graphics mode (`$D011 = $3B`), displays title image, waits for fire/space.
  - Relocates text/charset: `$A000` to `$2000` (`$C56C-$C582`).
  - Prompts for Trainer Options via `$C633`:
    1. `"UNLIMITED LIVES ??"` ('Y'/'N'): if 'Y', writes `$A5` to `$1826`, `$2FE5`, `$3155`.
    2. `"OPPONENTS CAN'T HIT ??"` ('Y'/'N'): if 'Y', writes `$09` to `$29E2`, `$29F7`.
  - Cleans zero page (`$C5AF-$C5B4`).
  - Sets `$00 = $2F`, `$01 = $36` (KERNAL ROM in, BASIC ROM out, I/O in).
  - Copies 5 pages (1,280 bytes) from `$C000-$C4FF` to `$0400-$08FF` (`$C618-$C62E`).
  - Transfers execution to `$0400`:
    ```asm
    $C630  4C 00 04   JMP $0400
    ```

### Stage 7: Pristine Bruce Lee Game Entry
- **Entry**: `$0400`
- **First Instructions**:
  ```asm
  $0400  78          SEI
  $0401  D8          CLD
  $0402  A2 FF       LDX #$FF
  $0404  9A          TXS
  $0405  AD 11 D0    LDA $D011
  $0408  29 EF       AND #$EF
  $040A  8D 11 D0    STA $D011     ; Disable screen during init
  $040D  AD FF 03    LDA $03FF
  $0410  F0 03       BEQ $0415
  $0412  4C D1 04    JMP $04D1
  $0415  A9 00       LDA #$00
  $0417  8D 00 EB    STA $EB00
  $041A  8D 70 EF    STA $EF70
  $041D  8D 70 F0    STA $F070
  $0420  8D 1B D4    STA $D41B     ; SID Voice 3 noise generator setup
  $0423  A9 FF       LDA #$FF
  $0425  8D 0F D4    STA $D40F
  $0428  8D 0E D4    STA $D40E
  $042B  A9 80       LDA #$80
  $042D  8D 12 D4    STA $D412
  $0430  A2 00       LDX #$00
  $0432  A0 60       LDY #$60
  $0434  88          DEY
  $0435  D0 FD       BNE $0434
  $0437  AD 1B D4    LDA $D41B     ; Sample hardware random noise into $0200-$02FF
  $043A  9D 00 02    STA $0200,X
  $043D  E8          INX
  $043E  D0 F2       BNE $0432
  $0443  A9 32       LDA #$32
  $0445  85 01       STA $01       ; Switch in Character ROM ($D000)
  $0447  A2 00       LDX #$00
  $0449  BD 00 D0    LDA $D000,X   ; Copy font to $8800-$8BFF (both normal and inverted)
  $044C  9D 00 89    STA $8900,X
  ...
  $0462  A9 36       LDA #$36
  $0464  85 01       STA $01       ; Switch I/O back in
  ...
  $04F6  A9 35       LDA #$35
  $04F8  85 01       STA $01       ; All-RAM except I/O ($35: RAM at $E000-$FFFF)
  ...
  $051C  20 00 E0    JSR $E000     ; Calls game routines under KERNAL in RAM
  ...
  $0584  78          SEI           ; Game title screen & attract loop setup
  ```

---

## Memory Map at Game Start (`$0400`)

The clean 64KB RAM dump at `$0400` before execution (`dumps/ram_game_start_0400.bin`) reveals the following memory layout:

| Range | Size | Description / Contents |
|---|---|---|
| `$0000-$00FF` | 256 B | Zero page workspace (cleared at `$C5B1`) |
| `$0100-$01FF` | 256 B | 6502 Hardware stack |
| `$0200-$02FF` | 256 B | Random seed buffer initialized from SID noise |
| `$0300-$03FF` | 256 B | System vectors and scratch RAM |
| `$0400-$08FF` | 1,280 B | Game entry & engine startup code (copied from `$C000`) |
| `$0900-$33FF` | 10.75 KB | Main game logic, player movement, physics, combat |
| `$3400-$37FF` | 1 KB | Text strings: `"BRUCE LEE"`, `"DATASOFT PRESENTS"`, player options |
| `$3800-$4EFF` | 5.75 KB | Screen layout data, collision tables, level maps |
| `$5000-$57FF` | 2 KB | Game routines & animation data |
| `$5900-$81FF` | 10.25 KB | Sprite shape data (Bruce Lee, Ninja, Green Yamo, items, hazards) |
| `$8400-$87FF` | 1 KB | Level attribute / tile data |
| `$8800-$8BFF` | 1 KB | Character generator font (populated by `$0447` from CHARGEN) |
| `$9000-$A5FF` | 5.5 KB | Music data and audio sequences |
| `$A600-$B3FF` | 3.5 KB | Micropearl Music Player (c) 1983 John A. Fitzpatrick |
| `$B400-$C6FF` | 4.75 KB | High score tables, screen buffers, loader staging |
| `$E000-$F1FF` | 4.5 KB | Under-KERNAL RAM routines (`JMP $E300`, `$E306`, `$E49E`, level data) |
| `$FFFA-$FFFF` | 6 B | Hardware RAM interrupt vectors (`NMI=$1116, RESET=$1116, IRQ=$1103`) |

---

## Key Hardware Register Settings in Game
- **Processor Port `$01`**: `$35` (All RAM enabled except I/O at `$D000-$DFFF`; KERNAL and BASIC ROMs are banked out).
- **Sprite Colors**:
  - `$D027` (Sprite 0): `$F7` (Yellow - Bruce Lee)
  - `$D028` (Sprite 1): `$F0` (Black - Ninja)
  - `$D029` (Sprite 2): `$F5` (Green - Green Yamo)
  - `$D02A` (Sprite 3): `$F0` (Black)
  - `$D02B` (Sprite 4): `$F0` (Black)
- **Interrupts**: Custom raster IRQ dispatcher at `$1103` jumps through indirect vector `($0408)`. Initial vector is `$152C`.

---

## Engine Subsystems Architecture

### 1. Main Game Loop (`$1BC2-$1C36`)

The core execution loop of Bruce Lee runs at `$1BC2`. Each frame tick processes input, physics, collision, enemy AI, animations, and sound before waiting for the raster IRQ:

```asm
$1BC2  LDA #$03; STA $48       ; Reset frame delay counter ($48)
$1BC6  JSR $19B8               ; Read joystick / player input
$1BC9  LDA $0104; BEQ $1BDF    ; Check pause state
$1BCE  JSR $1B29
$1BD1  JSR $19EC
$1BD4  JSR $1A08
$1BD7  LDA $0105; BPL $1BDF
$1BDC  JMP $1C32               ; Skip frame if paused
$1BDF  LDA $D2; AND #$BF; STA $D2
$1BE5  LDA $D3; AND #$87; STA $D3
$1BEB  JSR $1A96               ; Player physics & motion update
$1BEE  JSR $40BC               ; Background tile collision check
$1BF1  LDA $7A; BNE $1BFE      ; Check room hazard state
$1BF5  JSR $0DA4               ; Update Ninja AI
$1BF8  JSR $0D0F               ; Update Green Yamo AI
$1BFB  JSR $0DB1               ; Update Wizard & environmental hazards
$1BFE  LDA $7B; BNE $1C08      ; Check punch/attack cooldown
$1C02  LDA #$01; STA $7B; BNE $1C0A
$1C08  DEC $7B
$1C0A  JSR $3A6F               ; Lantern collection & door triggers (RTS trick)
$1C0D  JSR $5212               ; Multi-character sprite animation dispatcher
$1C10  JSR $2E39               ; Combat hit detection (punches & kicks)
$1C13  LDA $CF7A; EOR $CF9A; STA $2007
$1C1C  LDX $29                 ; Load current Room ID ($29)
$1C1E  LDA $4C9E,X; BNE $1C26
$1C23  JSR $29C3               ; Room-specific hazard checks
$1C26  JSR $3184               ; Player health & life count check
$1C29  JSR $179E               ; Refresh HUD score & lives
$1C2C  JSR $2584               ; Dispatch character sound effects
$1C2F  JSR $2D55               ; Check room transition boundaries
$1C32  LDA $48; BNE $1C32      ; Frame sync: wait until raster IRQ decrements $48 to 0
$1C36  JMP $1BC2               ; Repeat game loop
```

---

### 2. Dual-Split Raster Interrupt System

Bruce Lee uses a custom dual-split raster interrupt architecture to display both the custom multicolor logo banner at the top of the screen and high-resolution character graphics below:

1. **Top Split (`$152C`) at Raster Line `$FD` (VBLANK)**:
   - Decrements frame synchronization counter (`$48`).
   - Decrements countdown timer (`$49/$4A`).
   - Configures multicolor mode: `$D018 = $30` (Screen at `$8C00`, Charset at `$8000`), `$D016 = $18`.
   - Calls sound frame tick: `JSR $E006` (under KERNAL).
   - Sets next IRQ vector to `$1574` and next raster trigger line to `$82` (130).

2. **Bottom Split (`$1574`) at Raster Line `$82` (Line 130)**:
   - Delay loop to synchronize past bad lines (`LDX #$04; DEX; BNE`).
   - Reverts to standard character mode: `$D018 = $32` (Screen at `$8C00`, Charset at `$8800`), `$D016 = $16`.
   - Sets next IRQ vector back to `$152C` and next raster trigger line to `$FD`.

---

### 3. Audio Driver (Micropearl Music Player)

The audio driver is preserved in RAM under KERNAL at `$E000-$F1FF` (composed/programmed by John A. Fitzpatrick, copyright 1983):
- **`$E000` (`JMP $E300`)**: Sound Engine Initialization / Reset.
- **`$E003` (`JMP $E306`)**: SFX / Music Track Trigger. Playing song `$03` via `STA $E314; JSR $E003` starts the title screen music.
- **`$E006` (`JMP $E49E`)**: Sound Driver Frame Tick (called 60 times/sec from raster IRQ at `$154C`).
- **Pitch Table**: Stored at `$E285` (`!#%'*,/258;?BFKOTY^djpw~`).

---

### 4. Room & Level System

The game world consists of 20 distinct rooms:
- **Room ID Variable**: `$29` (0 to 19).
- **Master Room Layout Pointer Table**: Located at `$4AA8`. Each 2-byte entry points to a 20-byte room attribute and boundary header.
- **Room Background Color Table**: Located at `$47A0` (indexed by Room ID `$29`).
- **Screen Tile Layout Tables**:
  - Low pointers at `$4B34`, High pointers at `$4B49`.
  - Room data spans `$68F9` to `$7FE0`.
  - Uses an RLE tile compression scheme: bytes `< $80` represent literal tile lengths; bytes `>= $80` represent repeat runs.
- **Room Event & Mechanics Tables**:
  - Table 1 at `$4EA0` (per-room action routines).
  - Table 2 at `$4EC4` (per-room action routines). Dispatched every frame via the RTS jump trick at `$3A6F` (`PHA; PHA; RTS`).
- **Enemy Spawn Tables**:
  - Green Yamo spawn location table at `$131F`.
  - Ninja spawn location table at `$135B`.

---

### 5. Collision Detection & Combat Mechanics

- **Sprite-to-Sprite Collision**: Handled by reading `$D01E` (SPSPCL) at `$29CE`.
  - Bits `%00000011` (Sprite 0): Bruce Lee.
  - Bits `%00001100` (Sprite 1): Ninja.
  - Bits `%00110000` (Sprite 2): Green Yamo.
- **Collision Hit Flags**:
  - `$B3`: Bruce Lee collision state.
  - `$B4`: Ninja collision state.
  - `$B5`: Green Yamo collision state.
- **Player Lives**: Stored at Zero Page `$28`.
  - Decremented at `$1826` (`DEC $28`). When negative, branches to Game Over (`$188E`).
  - Incremented at `$2FE5` (`INC $28`) on extra life.
- **Trainer Locations Verified**:
  - Unlimited Lives: Replaces `$1826` (`C6 28` `DEC $28`) with `A5 28` (`LDA $28`).
  - Opponents Can't Hit: Alters branch offsets at `$29E2` and `$29F7` from `$03` to `$09` to bypass hit registration.

---

### 6. Sprite Animation Engine

- **Characters**:
  - Index 0: Bruce Lee (yellow, multicolor).
  - Index 1: Ninja (black/dark grey).
  - Index 2: Green Yamo (green, multicolor).
- **Sprite Animation Tables**:
  - Low byte pointers at `$1167` (64 frames).
  - High byte pointers at `$1239` (64 frames).
  - Frame shapes are 96 bytes each (`3 * 32 = $60` bytes) at `$9000, $9060, $90C0, $9120...`
- **Dynamic Blitter**: Routine `$26A0` copies and shifts 64-byte sprite shapes dynamically into VIC-II bank buffers.

---

### 7. Reconstructed Source Code Map

All reverse-engineered code has been reconstructed into modular, commented 6502 assembly files under [`src/`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src):

| File | Purpose / Coverage |
|---|---|
| [`src/c64.inc`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/c64.inc) | Hardware registers (VIC-II, SID, CIA1, CIA2, Color RAM) |
| [`src/zeropage.inc`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/zeropage.inc) | Reverse-engineered zero page variables & character tables |
| [`src/main.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/main.asm) | Entry point (`$0400`), initialization, and main game loop (`$1BC2-$1C36`) |
| [`src/title.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/title.asm) | Title screen setup (`$0584`), attract mode & option selectors |
| [`src/irq.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/irq.asm) | Raster IRQ dispatcher (`$1103`) & dual-split handlers (`$152C`, `$1574`) |
| [`src/player.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/player.asm) | Joystick input reader (`$19B8`) & player physics (`$1A96`) |
| [`src/enemies.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/enemies.asm) | Ninja AI (`$0DA4`), Green Yamo AI (`$0D0F`), hazards (`$0DB1`) |
| [`src/combat.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/combat.asm) | Sprite collision (`$29C3`), hit registration (`$2E39`), lives & death |
| [`src/rooms.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/rooms.asm) | Room transition (`$2FA0`), screen tile renderer (`$09BC`), room tables |
| [`src/sprites.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/sprites.asm) | Sprite multiplexer (`$5212`) & dynamic shape blitter (`$26A0`) |
| [`src/strings.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/strings.asm) | Screen string printer (`$17E2`) & string table |
| [`src/sound.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/sound.asm) | Micropearl music player interface (`$E000-$F1FF`) under KERNAL |
| [`src/brucelee.asm`](file:///home/kelsjon3/Downloads/C64/ROMS/bruce_lee/src/brucelee.asm) | Master top-level source file linking all modules |
