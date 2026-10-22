; ==============================================================================
; Bruce Lee - Player Input & Character Physics ($19B8-$1B20)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $19B8 - $1B20 ---

read_player_input:
        LDA     $0104
        BNE     $19EB
        LDA     CIAPRB
        AND     #$10
        BEQ     $19DD
        LDA     #$01
        STA     $010E
        JSR     $139E
        LDA     $010C
        BEQ     $19EB
        LDA     #$00
        STA     $010C
        LDA     $0109
        CMP     #$04
        BNE     $19EB
        JSR     wait_joystick_release
        LDA     #$06
        STA     VAR_FRAME_DELAY_COUNTER
        LDA     VAR_FRAME_DELAY_COUNTER
        BNE     $19E4
        JMP     game_start_play
        RTS
        LDA     $0105
        PHA
        AND     #$80
        STA     $0105
        PLA
        AND     #$06
        BEQ     $1A07
        SEC
        SBC     #$01
        ORA     $0105
        STA     $0105
        LDA     #$FF
        STA     $4B
        RTS
        LDA     $0105
        AND     #$06
        BNE     $1A51
        LDA     $0105
        BPL     $1A51
        LDA     VAR_CURRENT_PLAYER
        EOR     #$01
        AND     #$01
        TAX
        LDA     CIAPRA,X
        AND     #$10
        BNE     $1A51
        LDA     $0105
        EOR     #$80
        ORA     #$06
        STA     $0105
        BMI     $1A42
        JSR     $1BB6
        LDA     $82
        BPL     $1A38
        JSR     $103B
        LDA     #$00
        STA     $82
        JSR     $1ABB
        JMP     $31C2
        LDA     #$11
        STA     $43BD
        JSR     player_physics_update
        LDA     #$51
        STA     $82
        JMP     $1BA4
        RTS
        LDX     #$02
        BNE     $1A5B
        LDX     #$00
        STX     $0100
        JSR     $1A67
        JSR     $1A8A
        INX
        CPX     #$0D
        BCC     $1A5B
        RTS
        LDA     $4338,X
        STA     PTR_SCREEN_LO
        LDA     $434C,X
        STA     PTR_SCREEN_HI
        LDA     $4360,X
        STA     PTR_COLOR_LO
        LDA     $4374,X
        STA     PTR_COLOR_HI
        LDA     $0100
        BNE     $1A81
        RTS
        LDA     #$00
        STA     PTR_COLOR_LO
        LDA     #$CE
        STA     PTR_COLOR_HI
        RTS
        LDY     #$27
        LDA     #$00
        STA     (PTR_SCREEN_LO),Y
        STA     (PTR_COLOR_LO),Y
        DEY
        BPL     $1A8E
        RTS

player_physics_update:
        DEC     $43BD
        BNE     $1AA8
        LDA     #$20
        STA     $43BD
        LDA     #$00
        TAX
        LDY     #$2C
        JMP     print_string
        LDA     $43BD
        CMP     #$10
        BNE     $1ABA
        LDX     VAR_CURRENT_PLAYER
        INX
        TXA
        LDX     #$00
        LDY     #$2C
        JMP     print_string
        RTS
        LDA     #$03
        STA     $0100
        LDX     #$00
        LDY     #$38
        JMP     $1BAD
        LDA     #$05
        LDX     #$00
        LDY     #$44
        JMP     print_string
        RTS
        LDA     TAB_CHAR_TILE_COL
        LDY     #$43
        JSR     $1B84
        LDA     TAB_CHAR_TILE_ROW
        LDY     #$45
        JSR     $1B84
        LDA     $5A
        LDY     #$47
        JSR     $1B84
        LDA     $5B
        LDY     #$4E
        JMP     $1B84
        LDA     #$00
        STA     $439B
        LDA     VAR_PLAYER_LIVES
        STA     $4398
        SEC
        SBC     #$0A
        BCC     $1B02
        INC     $439B
        JMP     $1AF7
        CLC
        ADC     #$0A
        STA     $4398
        LDA     $439B
        ASL
        ASL
        ASL
        ASL
        ORA     $4398
        LDY     #$4A
        JMP     $1B84
        PHA
        JSR     $320E
        ORA     #$10
        STA     $8C00,Y
        PLA
