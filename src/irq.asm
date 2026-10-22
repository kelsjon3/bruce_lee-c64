; ==============================================================================
; Bruce Lee - Raster IRQ Dispatcher & Screen Splits ($1103-$1165, $152C-$15A8)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $1103 - $1165 ---

irq_dispatcher:
        PHA
        TXA
        PHA
        TYA
        PHA
        TSX
        LDA     $0104,X
        AND     #$00
        BEQ     $1113
        JMP     ($0408)
        JMP     ($0408)
        RTI
        JMP     ($FFFC)
        JMP     (D6510_DIR)
        PHA
        TXA
        PHA
        LDA     #$00
        LDX     #$7F
        STA     $8180,X
        STA     $82C0,X
        DEX
        BPL     $1124
        PLA
        TAX
        PLA
        RTS
        PHA
        TXA
        PHA
        LDA     #$00
        LDX     #$7F
        STA     $8200,X
        STA     $8340,X
        DEX
        BPL     $1138
        PLA
        TAX
        PLA
        RTS
        PHA
        TXA
        PHA
        LDA     #$00
        LDX     #$3F
        STA     $8280,X
        STA     $83C0,X
        DEX
        BPL     $114C
        PLA
        TAX
        PLA
        RTS
        LDA     $0104
        BNE     $1161
        LDA     #$01
        RTS
        INC     $16
        LDA     ($16),Y
        RTS

; --- Range: $152C - $15A8 ---

irq_raster_split_top:
        LDA     VAR_FRAME_DELAY_COUNTER
        BEQ     $1532
        DEC     VAR_FRAME_DELAY_COUNTER
        LDA     VAR_TIMER_LO
        BEQ     $1542
        DEC     VAR_TIMER_LO
        BNE     $1542
        LDA     VAR_TIMER_HI
        BEQ     $1542
        DEC     VAR_TIMER_HI
        DEC     VAR_TIMER_LO
        LDA     #$30
        STA     VMCSB
        LDA     #$18
        STA     SCROLX
        JSR     SOUND_DRIVER_FRAME_TICK
        LDA     #$74
        STA     $0408
        LDA     #$15
        STA     $0409
        LDA     #$01
        STA     IRQMSK
        STA     VICIRQ
        LDA     SCROLY
        AND     #$7F
        STA     SCROLY
        LDA     #$82
        STA     RASTER
        PLA
        TAY
        PLA
        TAX
        PLA
        RTI

irq_raster_split_bottom:
        LDX     #$04
        DEX
        BNE     $1576
        LDA     #$32
        STA     VMCSB
        LDA     #$16
        STA     SCROLX
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
        PLA
        TAY
        PLA
        TAX
        PLA
        RTI
        CLD
