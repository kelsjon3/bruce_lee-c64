; ==============================================================================
; Bruce Lee - HUD & String Printing Routine ($17E2-$1817)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $17E2 - $1817 ---

print_string:
        PHA
        JSR     $1A67
        PLA
        ASL
        TAX
        STY     PTR_STRING_LO
        LDA     tbl_string_pointers,X
        SEC
        SBC     PTR_STRING_LO
        STA     PTR_STRING_LO
        LDA     $43BF,X
        SBC     #$00
        STA     PTR_STRING_HI
        LDA     (PTR_STRING_LO),Y
        SEC
        SBC     #$20
        CMP     #$80
        BEQ     $1817
        AND     #$7F
        STA     (PTR_SCREEN_LO),Y
        ORA     #$80
        STA     (PTR_COLOR_LO),Y
        INY
        BNE     $17FA
        INC     PTR_SCREEN_HI
        INC     PTR_STRING_HI
        INC     PTR_COLOR_HI
        JMP     $17FA
        RTS
