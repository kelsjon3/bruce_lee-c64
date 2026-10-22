; ==============================================================================
; zeropage.inc - Bruce Lee Zero-Page Memory Map & Variables ($0000-$00FF)
; ==============================================================================

VAR_CURRENT_PLAYER      = $03   ; Active player index (0 = Player 1, 1 = Player 2)
PTR_SCREEN_LO           = $04   ; Pointer to screen RAM row low byte
PTR_SCREEN_HI           = $05   ; Pointer to screen RAM row high byte
PTR_STRING_LO           = $06   ; Pointer to string/text source low byte
PTR_STRING_HI           = $07   ; Pointer to string/text source high byte
PTR_COLOR_LO            = $08   ; Pointer to color RAM row low byte
PTR_COLOR_HI            = $09   ; Pointer to color RAM row high byte
PTR_SPRITE_SHAPE_LO     = $0E   ; Pointer to dynamic sprite shape buffer low byte
PTR_SPRITE_SHAPE_HI     = $0F   ; Pointer to dynamic sprite shape buffer high byte

VAR_CHAR_SUBPIXEL_X     = $1B   ; Horizontal sub-pixel offset (0-3)
VAR_CHAR_SUBPIXEL_Y     = $1C   ; Vertical sub-pixel offset (0-7)

VAR_PLAYER_LIVES        = $28   ; Remaining lives counter (decremented at $1826, inc at $2FE5)
VAR_CURRENT_ROOM        = $29   ; Current active room/screen ID (0-19)

VAR_FRAME_DELAY_COUNTER = $48   ; Main loop frame pacing delay counter (decremented by IRQ)
VAR_TIMER_LO            = $49   ; Countdown timer low byte (decremented by IRQ)
VAR_TIMER_HI            = $4A   ; Countdown timer high byte
VAR_COLLISION_TEMP      = $4C   ; Temporary collision storage register
VAR_ACTIVE_CHAR_IDX     = $50   ; Current character being updated (0=Bruce, 1=Ninja, 2=Yamo)

VAR_NINJA_SPAWN_TIMER   = $5D   ; Spawn / activation countdown for Ninja
VAR_YAMO_SPAWN_TIMER    = $5E   ; Spawn / activation countdown for Green Yamo

VAR_SPSPCL_SHADOW       = $67   ; Shadow register for sprite collision ($D01E)
VAR_ROOM_HAZARD_FLAG    = $7A   ; Flag indicating active hazards in room
VAR_PUNCH_COOLDOWN      = $7B   ; Cooldown timer for punches / attacks

; Character state tables (indexed by X: 0=Bruce, 1=Ninja, 2=Green Yamo)
TAB_CHAR_ACTIVE         = $95   ; Active / state flags per character
TAB_CHAR_POS_X          = $9E   ; Horizontal pixel position (X-coord)
TAB_CHAR_POS_Y          = $A1   ; Vertical pixel position (Y-coord)
TAB_BRUCE_COLLISION     = $B3   ; Collision hit flags on Bruce Lee
TAB_NINJA_COLLISION     = $B4   ; Collision hit flags on Ninja
TAB_YAMO_COLLISION      = $B5   ; Collision hit flags on Green Yamo
TAB_CHAR_TILE_COL       = $E6   ; Current tile column per character
TAB_CHAR_TILE_ROW       = $E9   ; Current tile row per character

VAR_VMCSB_SHADOW        = $F2   ; Shadow of $D018 (screen and charset base)
VAR_ATTR_COUNTER        = $F3   ; Attribute / color countdown
