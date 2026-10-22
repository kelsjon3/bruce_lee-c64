; ==============================================================================
; BRUCE LEE (Commodore 64) - Master Reconstructed Source Code
; Original Game (c) 1984 Datasoft, Inc.
; Programmed by Ron J. Fortier
; Micropearl Music Player by John A. Fitzpatrick
; ==============================================================================

; --- Include Hardware & Zero-Page Equates ---
.include "c64.inc"
.include "zeropage.inc"

; --- Core Engine & Startup ---
.include "main.asm"

; --- Title Screen & Attract Loop ---
.include "title.asm"

; --- Interrupts & Video Splits ---
.include "irq.asm"

; --- Player Control & Physics ---
.include "player.asm"

; --- Enemies & Hazards AI ---
.include "enemies.asm"

; --- Combat, Collision & Health ---
.include "combat.asm"

; --- Room Logic & Tile Renderer ---
.include "rooms.asm"

; --- Sprite Animation & Multiplexing ---
.include "sprites.asm"

; --- Text & HUD Routines ---
.include "strings.asm"

; --- Under-KERNAL Audio Driver ---
.include "sound.asm"
