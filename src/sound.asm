; ==============================================================================
; Bruce Lee - Under-KERNAL Micropearl Sound Driver ($E000-$E030, $E300-$E3B8, $E49E-$E4E0)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $E000 - $E030 ---

SOUND_DRIVER_INIT:
        JMP     snd_init_engine

SOUND_DRIVER_PLAY_SFX:
        JMP     snd_start_track

SOUND_DRIVER_FRAME_TICK:
        JMP     snd_frame_update
        ROL     $D7
        TAX
        INC     $26
        .byte   $D7
        TAX
        .byte   $BF
        .byte   $BF
        .byte   $B3
        .byte   $B2
        .byte   $BF
        .byte   $BF
        .byte   $B3
        .byte   $B2
        .byte   $BF
        .byte   $BF
        .byte   $F3
        .byte   $B2
        .byte   $BF
        .byte   $BF
        .byte   $F3
        .byte   $B2
        INC     $9326
        TAX
        INC     $9326
        TAX
        INC     $26
        .byte   $D3
        TAX
        INC     $26
        .byte   $D3
        TAX
        .byte   $BF

; --- Range: $E300 - $E3B8 ---

snd_init_engine:
        JMP     $E434
        JMP     $E352

snd_start_track:
        JMP     $E479
        BRK
        .byte   $A7
        .byte   $BF
        LDX     $02,Y
        .byte   $A7
        .byte   $BF
        .byte   $1F
        LDX     $0016,Y
        .byte   $1F
        JSR     $494D
        .byte   $43
        .byte   $52
        .byte   $4F
        BVC     $E362
        EOR     ($52,X)
        JMP     $4D20
        EOR     $53,X
        EOR     #$43
        JSR     $4C50
        EOR     ($59,X)
        EOR     $52
        JSR     $4320
        .byte   $4F
        BVC     $E38C
        .byte   $52
        EOR     #$47
        PHA
        .byte   $54
        JSR     $3931
        SEC
        .byte   $33
        JSR     $4F4A
        PHA
        LSR     $4120
        ROL     $4620
        EOR     #$54
        .byte   $5A
        BVC     $E38D
        .byte   $54
        .byte   $52
        EOR     #$43
        .byte   $4B
        JSR     $00A9
        STA     $E30C
        JSR     $E38C
        LDA     #$01
        STA     $E30C
        RTS
        LDA     $E309
        CMP     $E86B
        BCC     $E36B
        LDA     $E86B
        ASL
        ASL
        ASL
        TAY
        LDX     #$FE
        INX
        INX
        LDA     $E8C0,Y
        STA     $E3DF,X
        INY
        INX
        LDA     $E8C0,Y
        STA     $E3DF,X
        INY
        INX
        CPX     #$0A
        BCC     $E371
        RTS
        LDA     $E8C0,Y
        RTS
        JSR     $E360
        JSR     $E3A8
        LDX     #$00
        STX     $E12E
        LDA     #$FF
        STA     $E130
        JSR     $E5BB
        LDX     $E12E
        INX
        CPX     #$03
        BNE     $E394
        RTS
        LDA     #$00
        STA     $E30F
        STA     $E2E8
        LDX     #$2E
        LDA     $E2A7,X
        STA     $E0FF,X
        DEX

; --- Range: $E49E - $E4E0 ---

snd_frame_update:
        LDA     $E30A
        BNE     $E4BB
        LDA     $E30C
        BNE     $E4A9
        RTS
        LDX     $E30E
        CPX     #$FF
        BNE     $E4BE
        LDY     $E314
        BEQ     $E4BB
        JSR     $E438
        JMP     snd_frame_update
        JMP     $E3DA
        DEC     $E12F
        BNE     $E4A8
        LDA     $E30D
        STA     $E12F
        DEC     $E104
        BPL     $E4F4
        LDA     $E104
        CMP     $E107
        BNE     $E503
        LDA     $E10A
        STA     $E104
        LDA     $E10D
        STA     $E107
