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

## Environment and Execution

**Python Version:** 3.14+

**Virtual Environment:**
This project uses a virtual environment in the `venv` folder.

**Setup (first time only):**

Step 1: Create virtual environment
py -3.14 -m venv venv

Step 2: Activate virtual environment
.\venv\Scripts\Activate.ps1

Step 3: Install dependencies
pip install -r requirements.txt

**Activation (every new terminal session):**

.\venv\Scripts\Activate.ps1

**After activation, use these commands:**

Run tests:
pytest

Install packages:
pip install <package>

Install all dependencies:
pip install -r requirements.txt

**Never use:**

- `py -3.14 -m pytest` (use `pytest` after venv activation)
- Bare `pip` without activating venv first

---
# Development Environment

## Current configured workflow

KES is a Python repository. The only configured test runner is `pytest`:

- `pytest.ini` sets `testpaths = tests` and `pythonpath = .`;
- `.vscode/settings.json` enables `pytest` and disables `unittest`;
- tests and source are imported from the repository root.

Run all commands from the repository root and invoke tools through the Python interpreter selected for the project:

```powershell
python -m pytest
```

This is the intended full-suite command **once a supported Python environment and dependencies have been configured**.

## Configuration currently missing

The repository does not currently define a reproducible development setup. In particular, it has no:

- supported Python version (`.python-version`, `pyproject.toml`, or equivalent);
- packaging or environment configuration (`pyproject.toml`, `setup.py`, `setup.cfg`, Pipenv, Poetry, uv, tox, or nox configuration);
- declared test dependency (`pytest` is absent from `requirements.txt`);
- declared YAML dependency, although `src/config/scoring_loader.py` imports `yaml` (`PyYAML` is absent from `requirements.txt`);
- lockfile or documented dependency-install command;
- configured formatter, linter, type checker, or coverage command.

Do not claim that `pip install -r requirements.txt` creates a complete development environment, and do not invent lint, format, or type-check commands. Before this section can describe a canonical setup procedure, the project must declare its supported Python version and all runtime and development dependencies, including the test runner and YAML provider.

## Validation steps and limitations

After the missing environment configuration has been added and installed, run the full suite with:

```powershell
python -m pytest
```

The full suite is not portable as currently written. `tests/reporting/test_real_board_snapshot.py` requires a real board provided by `KANBAN_REAL_BOARD_PATH`, a local `O:\Проекты\Kanban\Doing (KB).md` fallback, or a fixture named `tests/fixtures/Doing (KB).md`. It also writes `report.md` in the repository root. For a full validation run outside the original developer machine, set the environment variable explicitly:

```powershell
$env:KANBAN_REAL_BOARD_PATH = "C:\path\to\board.md"
python -m pytest
```

Until that board is available, the following command is a useful portable subset check, but it is **not** a complete validation of the repository:

```powershell
python -m pytest --ignore=tests/reporting/test_real_board_snapshot.py
```

Formatting, linting, static typing, coverage, packaging, and application/CLI validation have no repository-defined commands at present. Report them as unconfigured rather than marking them as passed. Do not add a tool or command solely to satisfy this checklist unless the task explicitly includes configuring it.

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
