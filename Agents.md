# AGENTS.md

# Kanban Execution System (KES)

## Mission

KES is an execution intelligence system for Kanban boards stored in Obsidian Markdown.

The purpose of the project is not to manage tasks, but to improve execution quality by transforming board state into actionable recommendations.

Every change should make the system more deterministic, understandable, and maintainable.

---

# Architecture Principles

The project follows a layered architecture.

```text
Board
    ↓
Parser
    ↓
Domain Model
    ↓
Analytics
    ↓
ExecutionReport
    ↓
Presentation Layer
```

Each layer has a single responsibility.

Higher layers must never bypass lower-layer contracts.

---

# Source of Truth

Every component has exactly one source of truth.

Examples:

- Parser is the only source of Board parsing.
- ExecutionReport is the only source for presentation artifacts.
- Presentation layers never access analytical models directly.

Do not introduce duplicate sources of truth.

---

# Design Principles

Prefer:

- deterministic behavior;
- explicit contracts;
- immutable data models where practical;
- small composable functions;
- pure analytical logic.

Avoid:

- hidden side effects;
- duplicated business rules;
- implicit coupling between modules.

---

# Invariants

Never violate documented invariants.

If an implementation conflicts with an invariant, the implementation is wrong.

When uncertain, preserve correctness over convenience.

---

# Documentation

Architecture decisions belong in `docs/`.

Do not infer architecture from implementation if documentation already defines the behavior.

Implementation should follow documentation, not the opposite.

---

# Testing

Every behavioral change requires appropriate tests.

At minimum:

- unit tests for isolated logic;
- integration tests for parser interactions when applicable.

Existing tests should continue to pass unless intentionally updated.

---

# Refactoring

Prefer improving existing architecture over introducing parallel implementations.

Avoid temporary compatibility layers unless explicitly requested.

Keep changes focused.

---

# Code Style

Write clear code.

Optimize for readability before optimization.

Remove dead code rather than leaving commented implementations.

Use meaningful names.

---

# Before Completing a Task

Verify that:

- architecture remains consistent;
- documented contracts are preserved;
- tests pass;
- formatting and linting pass;
- no unrelated files were modified.

If requirements are ambiguous, stop and explain the ambiguity instead of guessing.