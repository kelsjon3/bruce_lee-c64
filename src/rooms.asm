; ==============================================================================
; Bruce Lee - Room Transition & Screen Tile Rendering ($09BC-$0B30, $2D55-$2D80, $2FA0-$2FD5)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $09BC - $0B30 ---

render_room_screen:
        LDA     SCROLY
        AND     #$EF
        STA     SCROLY
        LDA     SPENA
        AND     #$1F
        STA     $47
        LDA     #$00
        STA     SPENA
        LDX     #$27
        LDA     #$20
        STA     $8C00,X
        DEX
        BPL     $09D4
        LDX     VAR_CURRENT_ROOM
        LDA     tbl_room_bg_colors,X
        LDX     #$00
        STA     $D878,X
        STA     $D900,X
        STA     $DA00,X
        STA     $DB00,X
        INX
        BNE     $09E1
        JSR     $423F
        JSR     $255E
        LDA     VAR_CURRENT_ROOM
        CMP     #$0B
        BNE     $0A0E
        LDA     $36
        ORA     $38
        ORA     $3A
        BNE     $0A0E
        LDA     $47
        STA     SPENA
        LDX     #$0D
        JMP     $3217
        LDA     VAR_CURRENT_ROOM
        ASL
        ADC     VAR_CURRENT_PLAYER
        TAX
        LDA     $0300,X
        BEQ     $0A2A
        LSR     $0300,X
        LDA     #$07
        LDX     #$01
        JSR     $3175
        LDA     #$D0
        LDX     #$02
        JSR     $3175
        LDA     #$00
        LDY     #$83
        STA     $4F57,Y
        DEY
        BPL     $0A2E
        STA     $87
        STA     $88
        STA     $65
        LDA     #$07
        STA     $4321
        LDX     VAR_CURRENT_ROOM
        LDA     $4C9E,X
        STA     VAR_ROOM_HAZARD_FLAG
        BEQ     $0A4E
        LDA     #$00
        STA     $8B
        STA     $8C
        LDA     $130B,X
        STA     VAR_NINJA_SPAWN_TIMER
        LDA     $1347,X
        STA     VAR_YAMO_SPAWN_TIMER
        LDA     $40
        BEQ     $0A62
        LDA     #$03
        STA     VAR_NINJA_SPAWN_TIMER
        STA     VAR_YAMO_SPAWN_TIMER
        LDA     var_selected_player_mode
        BEQ     $0A6B
        LDA     #$08
        STA     VAR_YAMO_SPAWN_TIMER
        LDA     #$01
        STA     $B6
        LDA     #$04
        STA     $CE
        LDA     #$00
        STA     $4FDE
        STA     $4FDF
        STA     $4FE0
        STA     $BF
        STA     $0106
        LDA     VAR_CURRENT_ROOM
        ASL
        TAX
        LDA     tbl_master_room_pointers,X
        STA     PTR_STRING_LO
        LDA     $4AA9,X
        STA     PTR_STRING_HI
        LDY     #$13
        LDA     (PTR_STRING_LO),Y
        STA     $0153,Y
        DEY
        BPL     $0A93
        LDA     #$38
        LDX     VAR_CURRENT_ROOM
        CPX     #$0A
        BCC     $0AAD
        CPX     #$12
        BEQ     $0AAB
        LDA     #$3A
        BNE     $0AAD
        LDA     #$3C
        STA     VAR_VMCSB_SHADOW
        LDA     tbl_room_tiles_lo,X
        STA     PTR_STRING_LO
        LDA     tbl_room_tiles_hi,X
        STA     PTR_STRING_HI
        LDA     #$78
        STA     PTR_SCREEN_LO
        STA     $10
        LDA     #$A0
        STA     PTR_COLOR_LO
        STA     $12
        LDA     #$8C
        STA     PTR_SCREEN_HI
        STA     PTR_COLOR_HI
        LDA     #$D8
        STA     $11
        STA     $13
        LDA     #$27
        STA     VAR_ATTR_COUNTER
        LDY     #$00
        LDA     (PTR_STRING_LO),Y
        BPL     $0B07
        AND     #$7F
        BEQ     $0B30
        TAX
        JSR     $478D
        LDA     (PTR_STRING_LO),Y
        BPL     $0AEA
        JSR     $0B5F
        STA     (PTR_SCREEN_LO),Y
        ORA     #$80
        STA     (PTR_COLOR_LO),Y
        JSR     $4786
        JSR     $478D
        JSR     $4794
        JSR     $0B51
        JSR     $0B58
        JSR     $485B
        DEX
        BNE     $0AE3
        BEQ     $0AD7
        TAX
        JSR     $478D
        LDA     (PTR_STRING_LO),Y
        BPL     $0B12
        JSR     $0B5F
        STA     (PTR_SCREEN_LO),Y
        ORA     #$80
        STA     (PTR_COLOR_LO),Y
        JSR     $4786
        JSR     $4794
        JSR     $0B51
        JSR     $0B58
        JSR     $485B
        DEX
        BNE     $0B0B
        JSR     $478D
        JMP     $0AD7
        JSR     $336E

; --- Range: $2D55 - $2D80 ---

check_room_transition:
        LDX     #$02
        LDA     TAB_CHAR_ACTIVE,X
        AND     #$01
        BEQ     $2D75
        LDA     $BF,X
        CMP     #$13
        BEQ     $2D67
        CMP     #$19
        BNE     $2D6B
        LDA     $CE,X
        BNE     $2D75
        LDA     $D1,X
        BPL     $2D75
        TXA
        BEQ     $2D79
        JSR     reset_enemy_position
        DEX
        BPL     $2D57
        RTS
        JMP     player_death
        LDX     #$02
        LDA     $D1,X
        BMI     $2DBC

; --- Range: $2FA0 - $2FD5 ---

room_transition_handler:
        LSR     $2985
        LDX     #$02
        LDA     TAB_CHAR_ACTIVE,X
        AND     #$01
        BEQ     $2FB9
        LDA     $D1,X
        STA     $8E,X
        LDA     TAB_CHAR_POS_X
        STA     $8A,X
        LDA     TAB_CHAR_POS_Y
        STA     $8C,X
        BNE     $2FBF
        LDA     #$00
        STA     $8A,X
        STA     $8C,X
        JSR     reset_enemy_position
        DEX
        BNE     $2FA5
        SEI
        JSR     $0D42
        LDX     #$FF
        TXS
        JSR     render_room_screen
        JSR     sound_effects_dispatcher
        CLI
        JMP     main_game_loop
