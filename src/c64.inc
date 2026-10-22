; ==============================================================================
; c64.inc - Commodore 64 Hardware Registers & System Memory Equates
; ==============================================================================

; 6510 On-Chip I/O Port
D6510_DIR       = $0000 ; Data Direction Register
D6510_DATA      = $0001 ; 6510 Processor Port (Bank Switching)

; VIC-II Video Controller ($D000-$D02E)
SP0X            = $D000 ; Sprite 0 X-Coordinate
SP0Y            = $D001 ; Sprite 0 Y-Coordinate
SP1X            = $D002 ; Sprite 1 X-Coordinate
SP1Y            = $D003 ; Sprite 1 Y-Coordinate
SP2X            = $D004 ; Sprite 2 X-Coordinate
SP2Y            = $D005 ; Sprite 2 Y-Coordinate
SP3X            = $D006 ; Sprite 3 X-Coordinate
SP3Y            = $D007 ; Sprite 3 Y-Coordinate
SP4X            = $D008 ; Sprite 4 X-Coordinate
SP4Y            = $D009 ; Sprite 4 Y-Coordinate
SP5X            = $D00A ; Sprite 5 X-Coordinate
SP5Y            = $D00B ; Sprite 5 Y-Coordinate
SP6X            = $D00C ; Sprite 6 X-Coordinate
SP6Y            = $D00D ; Sprite 6 Y-Coordinate
SP7X            = $D00E ; Sprite 7 X-Coordinate
SP7Y            = $D00F ; Sprite 7 Y-Coordinate
MSIGX           = $D010 ; Sprite 0-7 Most Significant X-Bits
SCROLY          = $D011 ; Control Register 1 (Vertical Scroll & Screen Enable)
RASTER          = $D012 ; Current Raster Line (Bits 0-7)
LPX             = $D013 ; Light Pen X-Coordinate
LPY             = $D014 ; Light Pen Y-Coordinate
SPENA           = $D015 ; Sprite Enable Register
SCROLX          = $D016 ; Control Register 2 (Horizontal Scroll & Multicolor)
YXPAND          = $D017 ; Sprite Y Vertical Expansion
VMCSB           = $D018 ; Memory Setup Register (Screen & Charset Base)
VICIRQ          = $D019 ; VIC Interrupt Flag Register
IRQMSK          = $D01A ; VIC Interrupt Mask / Enable Register
SPBGPR          = $D01B ; Sprite-to-Background Priority
SPMC            = $D01C ; Sprite Multicolor Mode Select
XXPAND          = $D01D ; Sprite X Horizontal Expansion
SPSPCL          = $D01E ; Sprite-to-Sprite Collision Register
SPBGCL          = $D01F ; Sprite-to-Background Collision Register
EXTCOL          = $D020 ; Border Color
BGCOL0          = $D021 ; Background Color 0
BGCOL1          = $D022 ; Background Color 1
BGCOL2          = $D023 ; Background Color 2
BGCOL3          = $D024 ; Background Color 3
SPMC0           = $D025 ; Sprite Multicolor 0
SPMC1           = $D026 ; Sprite Multicolor 1
SP0COL          = $D027 ; Sprite 0 Color
SP1COL          = $D028 ; Sprite 1 Color
SP2COL          = $D029 ; Sprite 2 Color
SP3COL          = $D02A ; Sprite 3 Color
SP4COL          = $D02B ; Sprite 4 Color
SP5COL          = $D02C ; Sprite 5 Color
SP6COL          = $D02D ; Sprite 6 Color
SP7COL          = $D02E ; Sprite 7 Color

; SID Sound Interface Device ($D400-$D41C)
FRELO1          = $D400 ; Voice 1 Frequency Low
FREHI1          = $D401 ; Voice 1 Frequency High
PWLO1           = $D402 ; Voice 1 Pulse Width Low
PWHI1           = $D403 ; Voice 1 Pulse Width High
VCREG1          = $D404 ; Voice 1 Control Register
ATDCY1          = $D405 ; Voice 1 Attack / Decay
SUREL1          = $D406 ; Voice 1 Sustain / Release
FRELO2          = $D407 ; Voice 2 Frequency Low
FREHI2          = $D408 ; Voice 2 Frequency High
PWLO2           = $D409 ; Voice 2 Pulse Width Low
PWHI2           = $D40A ; Voice 2 Pulse Width High
VCREG2          = $D40B ; Voice 2 Control Register
ATDCY2          = $D40C ; Voice 2 Attack / Decay
SUREL2          = $D40D ; Voice 2 Sustain / Release
FRELO3          = $D40E ; Voice 3 Frequency Low
FREHI3          = $D40F ; Voice 3 Frequency High
PWLO3           = $D410 ; Voice 3 Pulse Width Low
PWHI3           = $D411 ; Voice 3 Pulse Width High
VCREG3          = $D412 ; Voice 3 Control Register
ATDCY3          = $D413 ; Voice 3 Attack / Decay
SUREL3          = $D414 ; Voice 3 Sustain / Release
CUTLO           = $D415 ; Filter Cutoff Frequency Low
CUTHI           = $D416 ; Filter Cutoff Frequency High
RESON           = $D417 ; Filter Resonance and Routing
SIGVOL          = $D418 ; Master Volume and Filter Modes
RANDOM_GEN      = $D41B ; Voice 3 Waveform Output / Hardware Noise Generator

; CIA 1 Complex Interface Adapter ($DC00-$DC0F)
CIAPRA          = $DC00 ; Port A (Keyboard Matrix Columns & Joystick 2)
CIAPRB          = $DC01 ; Port B (Keyboard Matrix Rows & Joystick 1)
CIDDRA          = $DC02 ; Data Direction Port A
CIDDRB          = $DC03 ; Data Direction Port B
TIMALO          = $DC04 ; Timer A Low
TIMAHI          = $DC05 ; Timer A High
TIMBLO          = $DC06 ; Timer B Low
TIMBHI          = $DC07 ; Timer B High
ICR             = $DC0D ; Interrupt Control Register

; CIA 2 Complex Interface Adapter ($DD00-$DD0F)
CI2PRA          = $DD00 ; Port A (Serial Bus & VIC-II Bank Select)
CI2PRB          = $DD01 ; Port B (User Port)
CI2ICR          = $DD0D ; Interrupt Control Register

; Color RAM Base
COLOR_RAM       = $D800 ; 1000 Bytes of Color Nybbles ($D800-$DBE7)
