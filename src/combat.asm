; ==============================================================================
; Bruce Lee - Sprite-to-Sprite Collision & Combat ($29C0-$2A30, $2E39-$2E90, $1818-$1850)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $29C0 - $2A30 ---
        EOR     ($4F),Y
        RTS

collision_detect_sprites:
        LDA     #$00
        LDX     #$02
        STA     TAB_BRUCE_COLLISION,X
        STA     $BC,X
        DEX
        BPL     $29C7
        LDA     SPSPCL
        BNE     $29D4
        RTS
        STA     VAR_SPSPCL_SHADOW
        AND     #$03
        BNE     $29DD
        JMP     $2A07
        LDA     VAR_SPSPCL_SHADOW
        AND     #$0C
        BNE     $29E6
        JMP     $29F2
        LDA     TAB_BRUCE_COLLISION
        ORA     #$08
        STA     TAB_BRUCE_COLLISION
        LDA     TAB_NINJA_COLLISION
        ORA     #$02
        STA     TAB_NINJA_COLLISION
        LDA     VAR_SPSPCL_SHADOW
        AND     #$30
        BNE     $29FB
        JMP     $2A07
        LDA     TAB_BRUCE_COLLISION
        ORA     #$10
        STA     TAB_BRUCE_COLLISION
        LDA     TAB_YAMO_COLLISION
        ORA     #$02
        STA     TAB_YAMO_COLLISION
        LDA     VAR_SPSPCL_SHADOW
        AND     #$0C
        BEQ     $2A1F
        LDA     VAR_SPSPCL_SHADOW
        AND     #$30
        BEQ     $2A1F
        LDA     TAB_NINJA_COLLISION
        ORA     #$10
        STA     TAB_NINJA_COLLISION
        LDA     TAB_YAMO_COLLISION
        ORA     #$08
        STA     TAB_YAMO_COLLISION
        LDX     #$02
        LDA     TAB_BRUCE_COLLISION,X
        STA     VAR_COLLISION_TEMP
        LDY     #$00
        LSR     VAR_COLLISION_TEMP
        BCS     $2A36
        INY
        CPY     #$05
        BCC     $2A27
        DEX

; --- Range: $2E39 - $2E90 ---

combat_hit_detection:
        LDA     #$00
        STA     $0100
        LDX     #$02
        STX     $51
        LDA     TAB_CHAR_ACTIVE,X
        AND     #$01
        BEQ     $2E68
        LDA     $BF,X
        CMP     #$19
        BEQ     $2E68
        CMP     #$17
        BNE     $2E55
        JSR     $2E10
        LDA     $B6,X
        AND     #$02
        STA     $53
        JSR     $1C39
        JSR     $2E6E
        LDX     $51
        INC     TAB_CHAR_TILE_ROW,X
        JSR     $2E6E
        LDX     $51
        DEX
        BPL     $2E40
        RTS
        LDA     TAB_CHAR_TILE_ROW,X
        TAX
        JSR     $1A67
        LDX     $51
        LDY     TAB_CHAR_TILE_COL,X
        LDA     #$02
        STA     VAR_COLLISION_TEMP
        LDA     (PTR_SCREEN_LO),Y
        AND     #$7F
        JSR     $2E89
        INY
        DEC     VAR_COLLISION_TEMP
        BPL     $2E7C
        RTS
        CMP     #$05
        BNE     $2E90
        JMP     $2F7B
        CMP     #$02

; --- Range: $1818 - $1850 ---

player_death:
        JSR     $255E
        LDA     $0104
        BNE     $1826
        STA     $09BB
        JMP     title_setup
        DEC     VAR_PLAYER_LIVES
        BMI     $188E
        LDA     #$24
        STA     $D1
        STA     $D2
        STA     $D3
        LDA     #$00
        STA     $8B
        STA     $8C
        JSR     $423F
        LDA     var_selected_game_mode
        BEQ     $184B
        LDA     $439F
        BMI     $184B
        LDA     VAR_CURRENT_PLAYER
        EOR     #$01
        STA     VAR_CURRENT_PLAYER
        JSR     $0EA7
        LDA     SCROLY
