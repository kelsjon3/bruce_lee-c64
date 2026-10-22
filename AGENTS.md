# OpenCode Guide — Bruce Lee C64 Static Recompiler

## Mission

Build a **native static-recompilation path** for the reconstructed Commodore 64 version of *Bruce Lee*.

Preserve the original reconstructed 6502/6510 game logic wherever practical. Do not turn this into a handwritten remake and do not make a full C64 emulator the final runtime.

The detailed architecture, milestones, and completion criteria are in `STATIC_RECOMPILER_PLAN.md`. Read that file before implementation work.

## Source of Truth

Treat the existing reverse-engineering work as authoritative:

- `src/` — reconstructed assembly source.
- `README.md` and `notes/` — technical findings and game architecture.
- `dumps/` — reference memory captures.
- `tools/` — reverse-engineering/build utilities.
- `brucelee_clean.prg` / `brucelee_clean.d64` — known-working clean C64 builds.

Treat `src/` as read-only unless correcting a demonstrable reconstruction error. Any such correction must be documented separately.

## Non-Negotiable Rules

1. Prefer static translation of reconstructed game logic over handwritten replacement logic.
2. Do not build a full C64 emulator as the final solution. A small 6502 reference core may be used as a test oracle.
3. Correctness and automated equivalence testing come before graphics, SDL, SID output, or polish.
4. Do not modify files outside this repository or install system packages automatically.
5. Do not push, force-push, rewrite Git history, delete branches, or use destructive Git operations such as `git reset --hard` or `git clean -fd`.
6. Never delete or overwrite original disk images, PRGs, dumps, or reconstructed source.
7. Unsupported or ambiguous translation constructs must be reported explicitly; never silently guess.

## Autonomous Working Style

Work with minimal user supervision.

Proceed without asking for routine confirmation when actions are reversible and repository-local. You may:

- read repository files;
- create/edit static-recompiler code, tests, build files, and documentation;
- run repository-local tools, compilers, and tests already installed;
- use read-only Git commands;
- create local Git commits after meaningful passing milestones.

If one implementation approach fails, diagnose it and try reasonable alternatives before stopping.

Stop only when:

- an external dependency must be installed and there is no reasonable repository-local alternative;
- required source information is genuinely missing;
- a destructive/irreversible action would be required;
- continuing would require materially altering the reconstructed original source;
- third-party licensing would require a user decision.

## Required Process

At the beginning of work:

1. run `git status`;
2. read `STATIC_RECOMPILER_PLAN.md`;
3. read `PROGRESS.md` if it exists;
4. resume the first incomplete milestone.

Before architectural decisions, read the relevant `README.md`, `notes/`, and `src/` material rather than assuming behavior.

After a meaningful milestone:

1. run relevant tests;
2. inspect `git diff`;
3. update `PROGRESS.md`;
4. create a local commit with a descriptive message;
5. continue to the next milestone if its prerequisites are satisfied.

Never commit failing generated output merely to make progress appear complete.

## First Milestone

For a fresh project session, begin with **Milestone 0 — Reconnaissance** from `STATIC_RECOMPILER_PLAN.md`.

The required Milestone 0 deliverable is:

`recompiler/RECONNAISSANCE.md`

It must document the actual reconstructed assembly syntax, used opcodes/addressing modes, directives/data forms, and difficult static-translation constructs found in this repository.

Do not start writing the parser from assumptions before reconnaissance is complete.

## Core Technical Direction

The intended pipeline is:

```text
reconstructed 6502 assembly
        -> parser / normalized representation
        -> native code generator
        -> generated C/C++
        -> small CPU/memory runtime + C64 compatibility layer
        -> native host presentation
```

Maintain exact 6502 semantics until correctness is proven. Use a 64 KiB logical address space initially. Treat C64 memory-mapped hardware as an explicit compatibility boundary.

The central proof mechanism is **reference-vs-native equivalence testing**: execute the same real Bruce Lee routine from identical state in a reference 6502 core and in generated/native code, then compare registers, flags, stack state, modified RAM, and relevant mapped hardware state.

The first real routine that passes automated equivalence testing is the project's first major proof of concept.
