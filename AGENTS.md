# OpenCode Project Guide — Bruce Lee C64 Static Recompiler

## Mission

Extend this repository with a **native static-recompilation path** for the reconstructed Commodore 64 version of *Bruce Lee*.

The goal is **not** to rewrite the game from scratch and **not** to embed a full C64 emulator. The goal is to preserve as much of the reconstructed original 6502/6510 game logic as practical, translate it into native code, and provide a small compatibility/runtime layer for the C64 hardware behavior the game depends on.

Target development platform: Linux (x86-64 first). The design should remain portable enough for Windows, macOS, and ARM later.

## Important Existing Work

The repository already contains a completed reverse-engineering effort. Treat that work as the authoritative description of the original game.

Important existing areas include:

- `src/` — reconstructed 6502/6510 assembly source.
- `src/brucelee.asm` — master assembly source.
- `src/main.asm` — startup and main game loop.
- `src/player.asm` — joystick input and player physics.
- `src/enemies.asm` — Ninja and Green Yamo AI.
- `src/combat.asm` — collision, hit detection, death/lives logic.
- `src/rooms.asm` — room transitions, room data, tile rendering.
- `src/sprites.asm` — sprite logic and multiplexer.
- `src/irq.asm` — raster interrupt logic.
- `src/sound.asm` — interface to the original Micropearl music driver.
- `src/c64.inc` — C64 hardware equates.
- `src/zeropage.inc` — reconstructed zero-page mappings.
- `notes/` — reverse-engineering notes.
- `dumps/` — reference RAM dumps and extracted binary regions.
- `tools/` — reverse-engineering and build utilities.
- `brucelee_clean.prg` / `brucelee_clean.d64` — known-working clean C64 builds.

Read the existing `README.md` and relevant files under `notes/` before making architectural decisions.

## Non-Negotiable Rules

1. **Preserve the reconstructed original source.**
   - Do not rewrite or "clean up" `src/` merely to make translation easier.
   - Treat `src/` as read-only reference material unless a change is required to correct a demonstrable reconstruction error.
   - If such a correction is necessary, document why and keep it separate from native-port work.

2. **Do not replace original game logic with a handwritten remake when static translation is practical.**
   - Prefer generated/native representations derived from the reconstructed assembly.
   - Hardware adaptation belongs in a compatibility/runtime layer.

3. **Do not build a full C64 emulator as the final solution.**
   - A small 6502 core may be used as a development/reference oracle for equivalence tests.
   - A small interpreter fallback for genuinely difficult/self-modifying regions may be considered only if documented and justified.

4. **Correctness before graphics.**
   - Do not begin SDL rendering, controller support, SID output, or visual polish until translation and equivalence testing work for real game routines.

5. **Automate verification.**
   - Every translated routine should eventually be testable against a reference execution path.
   - Prefer machine-verifiable results over visual inspection or assumptions.

6. **Do not modify files outside this repository.**
   - Do not install system packages automatically.
   - If a missing system dependency is required, document the exact package and continue with work that does not require it.

7. **Do not push, force-push, rewrite Git history, or delete branches.**
   - Local commits are allowed and encouraged.
   - Never use destructive Git operations such as `git reset --hard`, `git clean -fd`, or force checkout to discard user work.

8. **Never delete or overwrite original disk images, PRGs, dumps, or reconstructed source files.**

## Autonomous Working Style

This project is intended to run with minimal user supervision.

Do not repeatedly ask for confirmation before ordinary repository-local development actions. Proceed autonomously when the action is reversible and confined to this repository.

You may, without asking:

- read any file in this repository;
- create and edit files for the static recompiler;
- create build scripts and tests;
- run compilers and tests already available on the system;
- run repository-local Python tools;
- use `git status`, `git diff`, `git log`, and similar read-only Git commands;
- create local Git commits after a milestone passes;
- create test fixtures derived from repository-owned data;
- refactor code created as part of the static-recompiler effort.

Stop and explain the blocker only when:

- an external dependency must be installed and no reasonable repository-local alternative exists;
- required source information is genuinely missing;
- a destructive or irreversible action would be required;
- the next step would materially alter the reconstructed original source rather than the new recompiler/runtime work;
- legal/licensing ambiguity would require redistribution of third-party code not already present in the repository.

When one approach fails, investigate the failure, try another reasonable approach, and document the result rather than immediately asking the user what to do.

## Preferred New Repository Layout

Create new work under this structure unless a clearly better organization emerges:

```text
recompiler/
├── parser/          # Parse reconstructed assembly into an internal representation
├── ir/              # Optional intermediate representation / control-flow representation
├── translator/      # Convert parsed 6502 constructs to native C/C++
├── runtime/         # CPU state, flags, memory, call/branch helpers
└── generated/       # Generated native source; do not hand-maintain generated files

native/
├── c64/             # Minimal C64 compatibility layer (VIC/CIA/SID-facing APIs)
└── platform/        # Host platform integration; SDL later

tests/
├── cpu/             # Instruction/flag semantics
├── parser/          # Assembly parser tests
├── routines/        # Original-vs-generated Bruce Lee routine equivalence tests
└── integration/     # Larger translated execution tests
```

If generated files are committed, clearly mark them as generated and provide a deterministic regeneration command.

## Architectural Direction

The expected architecture is:

```text
Reconstructed Bruce Lee 6502 assembly
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
       generated C/C++ code
                |
        +-------+-------+
        |               |
        v               v
 CPU/register/flag   C64 compatibility
      runtime             layer
                            |
                            v
                 host graphics/input/audio
```

The native runtime should model only the CPU state and C64 behavior actually required by this game.

A reasonable initial CPU state representation is conceptually:

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

and a 64 KiB logical address space should be available to translated code, even if later optimized.

Preserve 6502 semantics precisely, especially:

- Carry, Zero, Negative, and Overflow flags;
- wrapping 8-bit arithmetic;
- `ADC` / `SBC` behavior;
- compare instructions;
- branch conditions;
- stack behavior;
- `JSR` / `RTS` semantics where relevant;
- zero-page addressing;
- indirect addressing and 6502 quirks if used by the game;
- memory-mapped I/O interception.

Do not optimize away the architectural model until correctness has been established.

## C64 Hardware Boundary

Treat memory-mapped hardware accesses as an explicit boundary.

Important ranges include:

- `$D000-$D3FF` — VIC-II registers;
- `$D400-$D7FF` — SID registers;
- `$D800-$DBFF` — color RAM;
- `$DC00-$DCFF` — CIA 1;
- `$DD00-$DDFF` — CIA 2;
- processor port `$0001` — ROM/RAM banking behavior relevant to the original game.

Initially, these ranges may be backed by simple state objects or memory with hooks. Add behavioral emulation only as required by Bruce Lee.

Do not implement a general-purpose VIC-II, SID, CIA, or C64 emulator unless required for a narrowly scoped compatibility behavior.

## Reference Execution / Equivalence Testing

A central requirement is an automated **reference-vs-native equivalence harness**.

Use a small, trustworthy 6502 execution core for tests if practical. This core is a test oracle, not part of the final native runtime.

For a selected original routine:

1. initialize identical registers and memory;
2. execute the original routine with the reference 6502 core;
3. execute the generated/native translation;
4. compare relevant final state;
5. report precise differences.

Compare at minimum when applicable:

- A, X, Y;
- processor status flags;
- stack pointer;
- changed zero-page locations;
- changed RAM locations;
- relevant memory-mapped register state;
- return/continuation behavior.

Use randomized/property-style inputs where safe and useful after deterministic fixtures pass.

The first successful equivalence test against a real Bruce Lee routine is the first major proof-of-concept milestone.

## Milestones

Work through these in order. Do not jump directly to rendering the game.

### Milestone 0 — Reconnaissance

- Read `README.md`, `src/`, and reverse-engineering notes.
- Identify assembler syntax used in the reconstructed source.
- Inventory the 6502/6510 opcodes and addressing modes actually used by Bruce Lee.
- Identify obvious assembler directives, data declarations, aliases, expressions, and macros that the parser must support.
- Identify self-modifying code, computed jumps, RTS jump-table tricks, indirect dispatch, banking, and other constructs that may complicate static translation.
- Write findings to `recompiler/RECONNAISSANCE.md`.

Do not modify original reconstructed source during reconnaissance.

### Milestone 1 — Minimal Parser

Build a parser for the subset of reconstructed assembly needed by the project.

It should recognize at least:

- labels;
- instructions;
- operands;
- addressing modes;
- constants/equates;
- source locations;
- basic data directives needed by the existing source.

Add parser tests using real excerpts from `src/`.

The parser should fail loudly and clearly on unsupported constructs rather than silently misinterpreting them.

### Milestone 2 — CPU/Memory Runtime

Implement the minimum native runtime required for translated code:

- register state;
- status flags;
- 64 KiB logical address space;
- read/write helpers;
- stack helpers;
- exact arithmetic/flag helpers.

Add unit tests for 6502 semantics used by the game.

### Milestone 3 — First Code Generation

Generate compilable native code for a deliberately small, uncomplicated subset of instructions and control flow.

Do not target the whole game yet.

Select one small real Bruce Lee routine that:

- does not depend heavily on raster timing;
- does not require SID playback;
- has simple inputs/outputs;
- exercises enough CPU semantics to prove the approach.

Document why it was selected.

### Milestone 4 — First Routine Equivalence

Create the reference execution harness and prove that the selected real Bruce Lee routine produces equivalent results in original 6502 execution and generated/native execution.

This milestone is complete only when automated tests pass.

At completion:

- update `PROGRESS.md`;
- document the routine and test cases;
- commit the working state.

### Milestone 5 — Instruction Coverage Expansion

Inventory unsupported instructions/addressing modes encountered by additional game routines and implement them incrementally.

Track opcode/addressing-mode support in a generated or maintained coverage document.

Do not implement unused CPU functionality merely for completeness unless it materially simplifies the runtime.

### Milestone 6 — Module-Level Translation

Progress from individual routines toward coherent subsystems, preferably in roughly this order:

1. pure utility/string/math routines;
2. input abstraction;
3. player state/physics;
4. enemy AI;
5. combat/collision;
6. room/game-state logic;
7. main loop orchestration;
8. IRQ-sensitive behavior;
9. audio-facing behavior.

Maintain regression tests throughout.

### Milestone 7 — Hardware Compatibility Layer

Introduce explicit abstractions for the C64 hardware behavior Bruce Lee needs.

Start with deterministic register/state behavior. Avoid SDL at first.

The goal is to make game logic execute deterministically while recording or exposing graphics, input, raster, and sound state through clean interfaces.

### Milestone 8 — Headless Native Game Loop

Run translated game logic for multiple frames without VICE or a full C64 emulator.

Success means:

- deterministic startup;
- repeatable frame progression;
- no unexpected fallback into untranslated code;
- stable memory/state evolution;
- automated integration tests.

### Milestone 9 — Host Presentation Layer

Only after the headless path is stable:

- add SDL3 or another justified cross-platform host layer;
- map keyboard/controller input to the C64 input abstraction;
- render the playfield/sprites from compatibility-layer state;
- add timing/frame pacing.

### Milestone 10 — Audio and Difficult Timing

Handle SID/music and raster-sensitive behavior last.

Possible approaches should be evaluated and documented rather than assumed. It is acceptable to use a narrowly scoped SID/6502 component for the original music driver if that produces a substantially cleaner and more faithful design than rewriting the music engine.

## Static-Translation Strategy

Prefer translation at the routine/basic-block/control-flow level rather than mechanically generating one giant switch per CPU instruction unless analysis proves that a different approach is necessary.

Preserve original labels in generated names/comments whenever practical. Maintain source-location metadata so generated/native failures can be traced back to reconstructed assembly.

Be especially cautious with:

- self-modifying code;
- code/data overlap;
- indirect jumps;
- the game's RTS jump-table technique;
- memory banking;
- code copied or relocated at runtime;
- interrupt entry/exit assumptions;
- hardware registers with read side effects;
- cycle-sensitive raster behavior.

When static translation cannot safely resolve a construct, detect and report it explicitly. Do not silently guess.

## Generated Code Quality

Generated code should prioritize correctness and traceability over elegance.

Prefer code that makes the relationship to the original routine obvious. For example, retain comments/source addresses such as:

```cpp
// Original $19B8: joystick input
```

Avoid premature transformations that make debugging against the 6502 source difficult.

Handwritten runtime code should be clear, idiomatic, documented, and testable.

## Build System

Choose a simple, widely available build system after inspecting what is already installed and what best fits the implementation language.

Do not install dependencies automatically.

Keep the first proof of concept dependency-light. Standard C++ and Python are preferred where practical because Python already exists in the repository toolchain and C++ is suitable for the eventual native runtime.

If a third-party 6502 test core is needed, prefer a small, permissively licensed implementation that can be vendored or fetched reproducibly. Record its license and provenance.

## Progress Tracking

Create and maintain `PROGRESS.md` once implementation begins.

For each milestone record:

- status (`not started`, `in progress`, `blocked`, `complete`);
- what was implemented;
- tests added;
- known limitations;
- next concrete task.

Keep it concise enough that a future agent can recover project state quickly.

## Git Discipline

Before beginning a task:

```bash
git status
```

Do not overwrite unrelated uncommitted user changes.

After a meaningful milestone:

1. run relevant tests;
2. inspect `git diff`;
3. update `PROGRESS.md`;
4. create a local commit with a descriptive message.

Examples:

```text
recompiler: add assembly parser skeleton
recompiler: implement 6502 arithmetic flag semantics
recompiler: prove equivalence for first Bruce Lee routine
runtime: add CIA input compatibility state
```

Never commit failing generated output merely to make progress appear complete.

## Definition of "Done" for the Static Recompiler

The project is successful when the Bruce Lee game can run as a native host executable such that:

- core game behavior derives from translated reconstructed 6502/6510 logic;
- a full C64 emulator is not required at runtime;
- C64-specific hardware dependencies are isolated behind a compatibility layer;
- translation is reproducible from repository source;
- automated tests demonstrate equivalence for substantial original game logic;
- the native executable can eventually present graphics/input/audio on the host platform.

Fidelity to the original game is more important than adding enhancements.

## First Task for a Fresh OpenCode Session

When instructed to begin the static-recompiler project, start with **Milestone 0 — Reconnaissance**.

Do not immediately write a translator from assumptions.

Read the repository, identify the exact assembly syntax and difficult control-flow constructs actually present, produce `recompiler/RECONNAISSANCE.md`, and then use those findings to design Milestone 1.

Continue autonomously through repository-local analysis and implementation unless one of the explicit stop conditions in this document is reached.
