; ==============================================================================
; Bruce Lee - Title Screen, Attract Mode & Options ($0584-$0762, $08B1-$0970, $0E4C-$0EA6)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $0584 - $0762 ---

title_setup:
        SEI
        LDA     SCROLY
        AND     #$EF
        STA     SCROLY
        JSR     $255E
        LDA     #$00
        STA     $0100
        JSR     $1A56
        JSR     $0E2E
        LDX     #$3F
        LDA     #$00
        STA     $83C0,X
        DEX
        BPL     $059F
        LDA     #$01
        STA     SPENA
        STA     XXPAND
        STA     MSIGX
        LDA     #$00
        STA     YXPAND
        STA     SPBGPR
        STA     SPMC
        LDA     #$0A
        STA     SP0X
        LDA     #$56
        STA     SP0Y
        LDA     #$FF
        STA     SP0COL
        LDA     #$0F
        STA     $8FF8
        LDX     #$0B
        LDA     $0E40,X
        STA     $83CC,X
        DEX
        BPL     $05D1
        LDA     #$2C
        STA     $0408
        LDA     #$15
        STA     $0409
        LDA     #$01
        STA     IRQMSK
        STA     VICIRQ
        LDA     SCROLY
        AND     #$7F
        STA     SCROLY
        LDA     #$FD
        STA     RASTER
        LDA     #$F6
        STA     EXTCOL
        STA     BGCOL0
        LDA     #$FF
        STA     BGCOL1
        STA     BGCOL2
        LDX     #$08
        STX     SCROLX
        JSR     $09A9
        LDX     #$00
        LDA     #$F1
        STA     $D9E0,X
        STA     $DAE0,X
        LDA     #$DC
        STA     $8C00,X
        STA     $8C68,X
        DEX
        BNE     $0613
        LDX     #$27
        LDA     $4A0D,X
        ORA     #$80
        STA     $8C50,X
        LDA     $49BD,X
        ORA     #$80
        STA     $8CC8,X
        LDA     $49E5,X
        ORA     #$80
        STA     $8CF0,X
        LDA     $4A35,X
        ORA     #$80
        STA     $8D68,X
        DEX
        BPL     $0628
        LDA     #$FF
        STA     $0100
        LDA     #$4F
        LDX     #$06
        LDY     #$31
        JSR     print_string
        LDA     #$50
        LDX     #$07
        LDY     #$2B
        JSR     print_string
        LDA     #$51
        LDX     #$08
        LDY     #$31
        JSR     print_string
        LDX     #$09
        LDA     $8DF0,X
        CLC
        ADC     #$40
        STA     $8DF0,X
        LDA     $8E40,X
        CLC
        ADC     #$40
        STA     $8E40,X
        CPX     #$02
        BCS     $069E
        LDA     $8DEB,X
        CLC
        ADC     #$40
        STA     $8DEB,X
        LDA     $8E3B,X
        CLC
        ADC     #$40
        STA     $8E3B,X
        LDA     $8E8B,X
        CLC
        ADC     #$40
        STA     $8E8B,X
        DEX
        BPL     $066D
        LDA     $42CB
        STA     var_selected_game_mode
        LDA     $42CC
        STA     var_selected_player_mode
        LDA     var_selected_game_mode
        BEQ     $06B5
        JSR     title_render_game_mode
        LDA     var_selected_player_mode
        BEQ     $06BD
        JSR     title_render_player_mode
        LDA     $1385
        BNE     $06DD
        DEC     $09BB
        BPL     $06DD
        LDA     #$04
        STA     $09BB
        LDA     #$03
        STA     $E314
        LDX     #$00
        STX     $E870
        DEX
        STX     $E871
        JSR     SOUND_DRIVER_PLAY_SFX
        LDX     #$00
        LDA     $CF8F,X
        EOR     $CFB1,X
        EOR     $CF90,X
        EOR     $CFAF,X
        EOR     $CF91,X
        EOR     $CFB0,X
        BEQ     $06FA
        STA     ($1D),Y
        INC     $1E
        JMP     $06F3
        LDA     #$09
        STA     VAR_TIMER_HI
        LDA     #$60
        STA     VAR_TIMER_LO
        JSR     $50DB
        NOP
        NOP
        NOP
        NOP
        NOP
        CLI

title_input_loop:
        JSR     title_wait_input
        SEI
        LDA     SCROLY
        AND     #$EF
        STA     SCROLY
        LDA     #$00
        STA     SPENA
        STA     SP0X
        STA     SP0Y
        STA     VAR_CURRENT_PLAYER
        LDA     #$01
        STA     $E30A
        JSR     SOUND_DRIVER_INIT
        LDA     var_selected_game_mode
        STA     $42CB
        LDA     var_selected_player_mode
        STA     $42CC
        JSR     $0EA7
        LDA     SCROLY
        AND     #$EF
        STA     SCROLY
        LDX     #$FD
        TXS
        JSR     $0F72
        JSR     screen_clear_and_init
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

title_start_game:
        JMP     main_game_loop

; --- Range: $08B1 - $0970 ---

title_wait_input:
        LDA     VAR_TIMER_LO
        ORA     VAR_TIMER_HI
        BNE     $08BA
        JMP     $0531
        LDA     #$00
        STA     $010E
        JSR     $139E
        LDA     $010C
        BEQ     $08E0
        LDA     #$00
        STA     $010C
        LDA     $0109
        JMP     $0956
        AND     #$7F
        CMP     #$03
        BEQ     $08FC
        CMP     #$06
        BEQ     $0908
        CMP     #$05
        BEQ     $092C
        LDA     VAR_TIMER_HI
        CMP     #$08
        BNE     $08F5
        LDA     VAR_TIMER_LO
        CMP     #$02
        BCS     $08F5
        LDA     #$0E
        LDX     #$0A
        LDY     #$02
        JSR     print_string
        LDA     CIAPRB
        AND     #$10
        BNE     title_wait_input
        JSR     wait_joystick_release
        LDA     #$10
        STA     VAR_FRAME_DELAY_COUNTER
        LDA     VAR_FRAME_DELAY_COUNTER
        BNE     $0903
        RTS
        LDA     var_selected_player_mode
        EOR     #$01
        STA     var_selected_player_mode
        STA     $42CC
        JSR     title_render_player_mode
        JSR     wait_joystick_release
        LDA     #$09
        STA     VAR_TIMER_HI
        LDA     #$60
        STA     VAR_TIMER_LO
        LDA     #$04
        STA     VAR_FRAME_DELAY_COUNTER
        LDA     VAR_FRAME_DELAY_COUNTER
        BNE     $0925
        JMP     title_wait_input
        LDA     var_selected_game_mode
        EOR     #$01
        STA     var_selected_game_mode
        STA     $42CB
        JSR     title_render_game_mode
        JSR     wait_joystick_release
        LDA     #$09
        STA     VAR_TIMER_HI
        LDA     #$60
        STA     VAR_TIMER_LO
        LDA     #$04
        STA     VAR_FRAME_DELAY_COUNTER
        BNE     $0925

wait_joystick_release:
        LDA     CIAPRA
        AND     CIAPRB
        AND     #$10
        BEQ     wait_joystick_release
        RTS
        CMP     #$2A
        BEQ     $0969
        CMP     #$AA
        BEQ     $0979
        CMP     #$11
        BEQ     $0988
        CMP     #$91
        BEQ     $0998
        JMP     $08D2
        LDA     #$08
        LDX     #$0A
        LDY     #$02
        JSR     print_string

; --- Range: $0E4C - $0EA6 ---

title_render_player_mode:
        LDX     #$13
        LDA     $8E40,X
        CMP     #$4D
        BEQ     $0E5A
        EOR     #$40
        STA     $8E40,X
        DEX
        BPL     $0E4E
        LDX     #$50
        LDA     var_selected_player_mode
        JMP     $0E7B

title_render_game_mode:
        LDX     #$13
        LDA     $8DF0,X
        CMP     #$4D
        BEQ     $0E73
        EOR     #$40
        STA     $8DF0,X
        DEX
        BPL     $0E67
        LDX     #$00
        LDA     var_selected_game_mode
        BNE     $0E92
        LDA     #$42
        STA     $8DEF,X
        LDA     #$40
        STA     $8DF8,X
        LDA     #$56
        STA     $8DFA,X
        LDA     #$00
        STA     $8E04,X
        RTS
        LDA     #$00
        STA     $8DEF,X
        LDA     #$42
        STA     $8DF8,X
        LDA     #$40
        STA     $8DFA,X
        LDA     #$56
        STA     $8E04,X
        RTS
