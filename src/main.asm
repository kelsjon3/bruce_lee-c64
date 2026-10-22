; ==============================================================================
; Bruce Lee - Main Entry, Startup & Core Loop ($0400-$0580, $1BC2-$1C80)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $0400 - $0583 ---

game_entry:
        SEI
        CLD
        LDX     #$FF
        TXS
        LDA     SCROLY
        AND     #$EF
        STA     SCROLY
        LDA     $03FF
        BEQ     $0415
        JMP     game_init_continue
        LDA     #$00
        STA     $EB00
        STA     $EF70
        STA     $F070
        STA     $D41B
        LDA     #$FF
        STA     FREHI3
        STA     FRELO3
        LDA     #$80
        STA     VCREG3
        LDX     #$00
        LDY     #$60
        DEY
        BNE     $0434
        LDA     $D41B
        STA     $0200,X
        INX
        BNE     $0432
        NOP
        NOP
        NOP
        LDA     #$32
        STA     D6510_DATA
        LDX     #$00
        LDA     SP0X,X
        STA     $8900,X
        EOR     #$FF
        STA     $8B00,X
        LDA     $D100,X
        STA     $8800,X
        EOR     #$FF
        STA     $8A00,X
        INX
        BNE     $0449
        LDA     #$36
        STA     D6510_DATA
        LDX     #$07
        LDA     #$FF
        STA     $8900,X
        LDA     #$03
        STA     $8A10,X
        LDA     #$C0
        STA     $8AB0,X
        DEX
        BPL     $0468
        LDA     #$7F
        STA     VAR_ATTR_COUNTER
        LDA     #$00
        STA     PTR_SCREEN_LO
        LDA     #$90
        STA     PTR_SCREEN_HI
        LDA     #$00
        STA     PTR_STRING_LO
        STA     PTR_COLOR_LO
        LDA     #$A0
        STA     PTR_STRING_HI
        LDA     #$A4
        STA     PTR_COLOR_HI
        JSR     $4892
        LDA     #$7F
        STA     VAR_ATTR_COUNTER
        LDA     #$00
        STA     PTR_SCREEN_LO
        LDA     #$94
        STA     PTR_SCREEN_HI
        LDA     #$00
        STA     PTR_STRING_LO
        STA     PTR_COLOR_LO
        LDA     #$A8
        STA     PTR_STRING_HI
        LDA     #$AC
        STA     PTR_COLOR_HI
        JSR     $4892
        LDA     #$7F
        STA     VAR_ATTR_COUNTER
        LDA     #$00
        STA     PTR_SCREEN_LO
        LDA     #$98
        STA     PTR_SCREEN_HI
        LDA     #$00
        STA     PTR_STRING_LO
        STA     PTR_COLOR_LO
        LDA     #$B0
        STA     PTR_STRING_HI
        LDA     #$B4
        STA     PTR_COLOR_HI
        JSR     $4892

game_init_continue:
        LDA     #$7F
        STA     VAR_ATTR_COUNTER
        LDA     #$00
        STA     PTR_SCREEN_LO
        LDA     #$9C
        STA     PTR_SCREEN_HI
        LDA     #$00
        STA     PTR_STRING_LO
        STA     PTR_COLOR_LO
        LDA     #$B8
        TAX
        TXS
        STA     PTR_STRING_HI
        LDA     #$BC
        STA     PTR_COLOR_HI
        JSR     $4892
        JSR     $512F
        JSR     $10F7
        LDA     #$35
        STA     D6510_DATA
        LDA     #$F0
        STA     SP1COL
        STA     SP3COL
        STA     SP4COL
        LDA     #$F7
        STA     SP0COL
        LDA     #$F5
        STA     SP2COL

game_start_play:
        SEI
        CLD
        LDX     #$FD
        TXS
        LDA     SCROLY
        AND     #$EF
        STA     SCROLY
        JSR     SOUND_DRIVER_INIT
        LDA     #$00
        STA     $16
        LDA     #$02
        STA     $17
        SEI
        JSR     $0F72
        JSR     screen_clear_and_init
        JMP     title_setup
        SEI
        LDA     SCROLY
        AND     #$EF
        STA     SCROLY
        LDA     #$00
        STA     SPENA
        STA     SP0X
        STA     SP0Y
        LDA     #$01
        STA     $E30A
        JSR     SOUND_DRIVER_INIT
        LDX     #$FD
        TXS
        JSR     $0F72
        JSR     screen_clear_and_init
        LSR     $0104
        LDA     var_selected_game_mode
        STA     $42CB
        LDA     var_selected_player_mode
        STA     $42CC
        LDA     #$00
        STA     var_selected_player_mode
        STA     var_selected_game_mode
        JSR     render_room_screen
        LDA     #$00
        STA     $1D
        LDA     #$F3
        STA     $1E
        JSR     $50DB
        NOP
        NOP
        NOP
        NOP
        NOP
        CLI
        JMP     main_game_loop

; --- Range: $1BC2 - $1C80 ---

main_game_loop:
        LDA     #$03
        STA     VAR_FRAME_DELAY_COUNTER
        JSR     read_player_input
        LDA     $0104
        BEQ     $1BDF
        JSR     $1B29
        JSR     $19EC
        JSR     $1A08
        LDA     $0105
        BPL     $1BDF
        JMP     $1C32
        LDA     $D2
        AND     #$BF
        STA     $D2
        LDA     $D3
        AND     #$87
        STA     $D3
        JSR     player_physics_update
        JSR     check_tile_collision
        LDA     VAR_ROOM_HAZARD_FLAG
        BNE     $1BFE
        JSR     enemy_ai_ninja
        JSR     enemy_ai_green_yamo
        JSR     hazard_update
        LDA     VAR_PUNCH_COOLDOWN
        BNE     $1C08
        LDA     #$01
        STA     VAR_PUNCH_COOLDOWN
        BNE     $1C0A
        DEC     VAR_PUNCH_COOLDOWN
        JSR     check_lanterns_and_doors
        JSR     update_sprite_multiplexer
        JSR     combat_hit_detection
        LDA     $CF7A
        EOR     $CF9A
        STA     $2007
        LDX     VAR_CURRENT_ROOM
        LDA     $4C9E,X
        BNE     $1C26
        JSR     collision_detect_sprites
        JSR     check_player_health
        JSR     $179E
        JSR     sound_effects_dispatcher
        JSR     check_room_transition
        LDA     VAR_FRAME_DELAY_COUNTER
        BNE     $1C32
        JMP     main_game_loop
        LDA     TAB_CHAR_POS_X,X
        SEC
        SBC     #$0C
        LSR
        LSR
        STA     TAB_CHAR_TILE_COL,X
        LDA     VAR_CURRENT_ROOM
        CMP     #$0D
        BNE     $1C4F
        LDA     TAB_CHAR_POS_Y,X
        CLC
        ADC     #$04
        BNE     $1C51
        LDA     TAB_CHAR_POS_Y,X
        SEC
        SBC     #$0C
        LSR
        LSR
        LSR
        LSR
        STA     TAB_CHAR_TILE_ROW,X
        RTS
        LDA     #$08
        STA     $86
        LDA     $0106,X
        BEQ     $1C68
        DEC     $0106,X
        RTS
        STA     $4FDB,X
        LDA     $4F57,X
        ORA     $4F5A,X
        ORA     $4F5D,X
        ORA     $4F60,X
        BEQ     $1C8F
        LDA     #$27
        STA     $4E
        TXA
        CLC
        ADC     #$75
