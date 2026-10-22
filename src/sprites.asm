; ==============================================================================
; Bruce Lee - Sprite Multiplexer & Animation Blitter ($5212-$52A5, $26A0-$2700)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $5212 - $52A5 ---

update_sprite_multiplexer:
        LDX     #$02
        STX     VAR_ACTIVE_CHAR_IDX
        LDA     TAB_CHAR_ACTIVE,X
        AND     #$01
        BNE     $521F
        JMP     $52A4
        LDA     TAB_CHAR_POS_X,X
        SEC
        SBC     #$0C
        STA     TAB_CHAR_TILE_COL,X
        AND     #$03
        STA     VAR_CHAR_SUBPIXEL_X
        LDA     TAB_CHAR_POS_Y,X
        SEC
        SBC     #$1D
        STA     TAB_CHAR_TILE_ROW,X
        AND     #$07
        STA     VAR_CHAR_SUBPIXEL_Y
        LDA     tab_char_anim_frame,X
        TAX
        LDA     tbl_sprite_frame_lo,X
        STA     $52CC
        LDA     tbl_sprite_frame_hi,X
        STA     $52CD
        JSR     $52AD
        LDA     VAR_CHAR_SUBPIXEL_Y
        CLC
        ADC     #$15
        STA     $4F39
        SEC
        SBC     #$06
        STA     $4F38
        JSR     $55AB
        LDX     VAR_ACTIVE_CHAR_IDX
        LDA     TAB_CHAR_TILE_COL,X
        LSR
        LSR
        STA     TAB_CHAR_TILE_COL,X
        LDA     TAB_CHAR_TILE_ROW,X
        LSR
        LSR
        LSR
        STA     TAB_CHAR_TILE_ROW,X
        LDY     #$00
        STY     $52
        LDA     #$08
        STA     $4F3A
        JSR     $530A
        JSR     $537E
        LDX     VAR_ACTIVE_CHAR_IDX
        INC     TAB_CHAR_TILE_ROW,X
        LDA     #$10
        STA     $4F3A
        JSR     $530A
        JSR     $537E
        LDX     VAR_ACTIVE_CHAR_IDX
        INC     TAB_CHAR_TILE_ROW,X
        LDA     #$18
        STA     $4F3A
        JSR     $530A
        JSR     $537E
        LDX     VAR_ACTIVE_CHAR_IDX
        INC     TAB_CHAR_TILE_ROW,X
        LDA     #$20
        STA     $4F3A
        JSR     $530A
        JSR     $537E
        LDX     VAR_ACTIVE_CHAR_IDX

; --- Range: $26A0 - $2700 ---

blit_sprite_shape:
        BNE     $26D7
        LDA     #$3F
        STA     $277F
        LDA     $E0,X
        TAX
        LDA     SOUND_DRIVER_INIT,X
        STA     (PTR_SPRITE_SHAPE_LO),Y
        DEC     $277F
        DEX
        BMI     $26C6
        DEY
        LDA     #$00
        STA     (PTR_SPRITE_SHAPE_LO),Y
        DEC     $277F
        DEY
        STA     (PTR_SPRITE_SHAPE_LO),Y
        DEC     $277F
        DEY
        BPL     $26AA
        LDA     $277F
        EOR     #$3F
        TAY
        LDA     #$00
        STA     (PTR_SPRITE_SHAPE_LO),Y
        INY
        DEC     $277F
        BPL     $26CE
        RTS
        LDA     #$3F
        STA     $277F
        LDA     $E0,X
        ASL
        TAX
        DEX
        DEY
        DEY
        LDA     SOUND_DRIVER_INIT,X
        STA     (PTR_SPRITE_SHAPE_LO),Y
        DEC     $277F
        DEX
        DEY
        LDA     SOUND_DRIVER_INIT,X
        STA     (PTR_SPRITE_SHAPE_LO),Y
        DEC     $277F
        DEX
        BMI     $26C6
        DEY
        LDA     #$00
        STA     (PTR_SPRITE_SHAPE_LO),Y
        DEC     $277F
        DEY
