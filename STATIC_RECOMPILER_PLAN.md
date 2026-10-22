# Static Recompiler Plan — Bruce Lee C64

## Goal

Create a native static-recompilation path for the reconstructed Commodore 64 version of *Bruce Lee*.

The project should preserve as much original 6502/6510 game logic as practical, translate that logic into native code, and isolate C64-specific behavior behind a small compatibility/runtime layer.

This is **not** a handwritten remake and **not** a full C64 emulator. Linux/x86-64 is the first host target; keep the design portable enough for Windows, macOS, and ARM later.

## Existing Authoritative Material

Treat the completed reverse-engineering work as the source of truth:

- `src/` — reconstructed 6502/6510 assembly.
- `src/brucelee.asm` — master source.
- `src/main.asm` — startup and main loop.
- `src/player.asm` — joystick input and player physics.
- `src/enemies.asm` — Ninja and Green Yamo AI.
- `src/combat.asm` — collision, hit detection, death/lives.
- `src/rooms.asm` — room transitions, room data, tile rendering.
- `src/sprites.asm` — sprite logic and multiplexer.
- `src/irq.asm` — raster interrupt logic.
- `src/sound.asm` — Micropearl interface.
- `src/c64.inc` — C64 hardware equates.
- `src/zeropage.inc` — reconstructed zero-page mappings.
- `notes/` — reverse-engineering notes.
- `dumps/` — reference RAM dumps and extracted binary regions.
- `tools/` — reverse-engineering/build utilities.
- `brucelee_clean.prg` / `brucelee_clean.d64` — known-working clean C64 builds.

Read `README.md` and relevant `notes/` before architectural decisions.

## Preferred Layout

```text
recompiler/
├── parser/          # parse reconstructed assembly
├── ir/              # optional normalized/control-flow representation
├── translator/      # convert parsed 6502 to native C/C++
├── runtime/         # CPU state, flags, memory, stack/call helpers
└── generated/       # generated native source

native/
├── c64/             # minimal VIC/CIA/SID-facing compatibility layer
└── platform/        # host integration; SDL later

tests/
├── cpu/             # 6502 semantics
├── parser/          # parser behavior
├── routines/        # original-vs-native routine equivalence
└── integration/     # larger execution tests
```

Generated files must be marked as generated and reproducible.

## Architecture

```text
Reconstructed Bruce Lee assembly
              |
              v
       assembly parser
              |
              v
    normalized representation
              |
              v
      native code generator
              |
              v
      generated C/C++
              |
      +-------+-------+
      |               |
      v               v
 CPU/register/flag   C64 compatibility
      runtime             layer
                            |
                            v
                 graphics/input/audio
```

Start with a faithful architectural model. A minimal CPU state may resemble:

```cpp
struct Cpu6502State {
    uint8_t a;
    uint8_t x;
    uint8_t y;
    uint8_t sp;
    uint8_t p;
    uint16_t pc;
};
```

Provide a 64 KiB logical address space until correctness is established.

Preserve exact 6502 behavior for:

- Carry, Zero, Negative, Overflow;
- 8-bit wrapping arithmetic;
- `ADC` / `SBC`;
- compare instructions;
- branch conditions;
- stack behavior;
- `JSR` / `RTS` where relevant;
- zero-page addressing;
- indirect addressing and any 6502 quirks the game uses;
- memory-mapped I/O interception.

Do not optimize away the architectural model prematurely.

## C64 Hardware Boundary

Treat these as explicit compatibility boundaries:

- `$D000-$D3FF` — VIC-II.
- `$D400-$D7FF` — SID.
- `$D800-$DBFF` — color RAM.
- `$DC00-$DCFF` — CIA 1.
- `$DD00-$DDFF` — CIA 2.
- `$0001` — processor port / banking behavior.

Initially these may be simple memory-backed state objects with hooks. Add behavior only as Bruce Lee requires it. Do not implement a general-purpose VIC-II, SID, CIA, or C64 emulator unless narrowly required.

## Reference-vs-Native Equivalence

Automated equivalence testing is central to the project.

A small trustworthy 6502 core may be used as a **test oracle only**. It is not part of the final native runtime.

For a selected original routine:

1. initialize identical registers and memory;
2. execute the original routine in the reference 6502 core;
3. execute the generated/native translation;
4. compare final state;
5. report exact differences.

Compare when applicable:

- A, X, Y;
- status flags;
- stack pointer;
- changed zero-page locations;
- changed RAM;
- relevant memory-mapped register state;
- return/continuation behavior.

After deterministic fixtures pass, add randomized/property-style inputs where useful.

The first real Bruce Lee routine proven equivalent is the first major proof of concept.

## Milestone 0 — Reconnaissance

- Read `README.md`, `src/`, and reverse-engineering notes.
- Identify the exact assembler syntax used by the reconstructed source.
- Inventory the 6502/6510 opcodes and addressing modes actually used.
- Identify directives, data declarations, aliases, expressions, and macros the parser must support.
- Identify self-modifying code, computed jumps, indirect dispatch, RTS jump-table tricks, banking, runtime relocation, code/data overlap, and other difficult constructs.
- Write findings to `recompiler/RECONNAISSANCE.md`.

Do not modify the reconstructed source during reconnaissance.

## Milestone 1 — Minimal Parser

Build a parser for the subset of assembly actually needed by this project.

Recognize at minimum:

- labels;
- instructions;
- operands;
- addressing modes;
- constants/equates;
- source locations;
- basic data directives used by the source.

Add parser tests using real excerpts from `src/`.

Unsupported constructs must fail loudly and explicitly; never silently guess.

## Milestone 2 — CPU/Memory Runtime

Implement:

- register state;
- status flags;
- 64 KiB logical address space;
- read/write helpers;
- stack helpers;
- exact arithmetic/flag helpers.

Add unit tests for all 6502 semantics used by Bruce Lee.

## Milestone 3 — First Code Generation

Generate compilable native code for a deliberately small, uncomplicated subset of instructions/control flow.

Choose one real Bruce Lee routine that:

- does not depend heavily on raster timing;
- does not require SID playback;
- has simple inputs/outputs;
- exercises enough CPU semantics to prove the approach.

Document why it was selected.

## Milestone 4 — First Routine Equivalence

Create the reference execution harness and prove the selected routine produces equivalent results in original 6502 execution and generated/native execution.

Completion requires automated passing tests.

At completion:

- update `PROGRESS.md`;
- document the routine and test cases;
- create a local commit.

## Milestone 5 — Instruction Coverage Expansion

Inventory unsupported instructions/addressing modes encountered by additional routines and implement them incrementally.

Track opcode/addressing-mode coverage. Do not implement unused CPU functionality merely for completeness unless it materially simplifies the runtime.

## Milestone 6 — Module-Level Translation

Progress from individual routines to coherent subsystems, roughly in this order:

1. pure utility/string/math routines;
2. input abstraction;
3. player state/physics;
4. enemy AI;
5. combat/collision;
6. room/game-state logic;
7. main-loop orchestration;
8. IRQ-sensitive behavior;
9. audio-facing behavior.

Maintain regression tests throughout.

## Milestone 7 — Hardware Compatibility Layer

Introduce explicit abstractions for only the C64 hardware behavior Bruce Lee needs.

Begin with deterministic register/state behavior. Avoid SDL at first.

The goal is deterministic game logic that records/exposes graphics, input, raster, and sound state through clean interfaces.

## Milestone 8 — Headless Native Game Loop

Run translated game logic for multiple frames without VICE or a full C64 emulator.

Success requires:

- deterministic startup;
- repeatable frame progression;
- no unexpected fallback into untranslated code;
- stable memory/state evolution;
- automated integration tests.

## Milestone 9 — Host Presentation Layer

Only after the headless path is stable:

- add SDL3 or another justified cross-platform host layer;
- map keyboard/controller input to the C64 input abstraction;
- render playfield/sprites from compatibility-layer state;
- add host timing/frame pacing.

## Milestone 10 — Audio and Difficult Timing

Handle SID/music and raster-sensitive behavior last.

Evaluate alternatives instead of assuming a solution. A narrowly scoped SID/6502 component for the original music driver is acceptable if substantially cleaner and more faithful than rewriting the music engine.

## Translation Strategy

Prefer routine/basic-block/control-flow translation rather than mechanically generating one giant CPU-instruction switch unless analysis proves otherwise.

Preserve original labels and source addresses in generated names/comments when practical. Maintain source-location metadata so native failures can be traced back to reconstructed assembly.

Be especially cautious with:

- self-modifying code;
- code/data overlap;
- indirect jumps;
- RTS jump-table techniques;
- memory banking;
- runtime code relocation/copying;
- interrupt entry/exit assumptions;
- hardware registers with read side effects;
- cycle-sensitive raster behavior.

When static translation cannot safely resolve a construct, detect and report it. Never silently invent behavior.

## Generated-Code Quality

Correctness and traceability outrank elegance.

Retain useful source information such as:

```cpp
// Original $19B8: joystick input
```

Avoid transformations that make debugging against the 6502 source difficult. Handwritten runtime code should remain clear and testable.

## Build System and Dependencies

Choose a simple, widely available build system after inspecting what is already installed.

Do not install system dependencies automatically.

Keep the proof of concept dependency-light. Standard C++ and Python are preferred where practical. If a third-party 6502 test core is needed, prefer a small permissively licensed implementation and record its license/provenance.

## Progress Tracking

Create and maintain `PROGRESS.md` once implementation begins.

For every milestone record:

- status: `not started`, `in progress`, `blocked`, or `complete`;
- what was implemented;
- tests added;
- known limitations;
- next concrete task.

Keep it concise enough for a future agent to resume quickly.

## Definition of Done

The static-recompiler project is successful when:

- core game behavior derives from translated reconstructed 6502/6510 logic;
- a full C64 emulator is not required at runtime;
- C64-specific dependencies are isolated behind a compatibility layer;
- translation is reproducible from repository source;
- automated tests demonstrate equivalence for substantial original logic;
- the native executable can eventually present graphics/input/audio on the host platform.

Fidelity to the original game is more important than enhancements.
