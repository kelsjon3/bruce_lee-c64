; ==============================================================================
; Bruce Lee - Enemy AI (Ninja, Green Yamo) & Hazards ($0D0F-$0DF0)
; Reconstructed from pristine Commodore 64 binary
; ==============================================================================

; --- Range: $0D0F - $0DF0 ---

enemy_ai_green_yamo:
        LDA     VAR_YAMO_SPAWN_TIMER
        BNE     $0D3C
        LDX     #$01
        LDA     TAB_CHAR_ACTIVE,X
        AND     #$01
        BNE     $0D3C
        JSR     $0CD5
        LDX     VAR_CURRENT_ROOM
        LDA     tbl_ninja_spawn_per_room,X
        STA     VAR_YAMO_SPAWN_TIMER
        LDA     var_selected_player_mode
        BEQ     $0D2E
        LDA     #$30
        STA     VAR_YAMO_SPAWN_TIMER
        JSR     $10D0
        BVS     $0D3D
        BCS     $0D3A
        LDA     $40
        BNE     $0D3D
        RTS
        LSR     VAR_YAMO_SPAWN_TIMER
        RTS
        LDA     #$03
        STA     VAR_YAMO_SPAWN_TIMER
        RTS
        CPX     #$01
        BNE     $0D72
        LDA     #$5B
        CLC
        ADC     VAR_CURRENT_ROOM
        STA     $0D56
        LDA     #$13
        ADC     #$00
        STA     $0D57
        LDA     SOUND_DRIVER_INIT
        STA     VAR_YAMO_SPAWN_TIMER
        LDA     var_selected_player_mode
        BEQ     $0D63
        LDA     #$30
        STA     VAR_YAMO_SPAWN_TIMER
        JSR     $10D0
        BVS     $0D3D
        BCS     $0D6F
        LDA     $40
        BNE     $0D3D
        RTS
        LSR     VAR_YAMO_SPAWN_TIMER
        RTS
        CPX     #$02
        BNE     $0D9E
        LDA     #$1F
        CLC
        ADC     VAR_CURRENT_ROOM
        STA     $0D86
        LDA     #$13
        ADC     #$00
        STA     $0D87
        LDA     SOUND_DRIVER_INIT
        STA     VAR_NINJA_SPAWN_TIMER
        JSR     $10D0
        BVS     $0D99
        BCS     $0D96
        LDA     $40
        BNE     $0D99
        RTS
        LSR     VAR_NINJA_SPAWN_TIMER
        RTS
        LDA     #$03
        STA     VAR_NINJA_SPAWN_TIMER
        RTS
        JSR     $0D46
        JMP     $0D76

enemy_ai_ninja:
        LDA     VAR_NINJA_SPAWN_TIMER
        BEQ     $0DAA
        DEC     VAR_NINJA_SPAWN_TIMER
        LDA     VAR_YAMO_SPAWN_TIMER
        BEQ     $0DB0
        DEC     VAR_YAMO_SPAWN_TIMER
        RTS

hazard_update:
        LDA     VAR_NINJA_SPAWN_TIMER
        BNE     $0DF7
        LDA     $96
        AND     #$01
        BEQ     $0DD7
        LDA     $40
        BNE     $0DD7
        LDA     var_selected_player_mode
        BNE     $0DD7
        JSR     $10D0
        BVS     $0DD7
        BCS     $0DD7
        JSR     $1159
        CMP     #$19
        BCC     $0DD7
        LDA     #$10
        STA     VAR_NINJA_SPAWN_TIMER
        RTS
        LDX     #$02
        LDA     TAB_CHAR_ACTIVE,X
        AND     #$01
        BNE     $0DF7
        JSR     $0DF8
        LDX     VAR_CURRENT_ROOM
        LDA     tbl_yamo_spawn_per_room,X
        STA     VAR_NINJA_SPAWN_TIMER
        JSR     $10D0
        BVS     $0D99
        BCS     $0DF5
        LDA     $40
