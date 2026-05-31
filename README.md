# Kanban Execution System

A local-first Kanban analysis and execution system designed for personal productivity, strategic execution, and AI-assisted reviews.

The system treats a Markdown Kanban board as the single source of truth and builds a structured domain model, analytics layer, and review workflows on top of it.

## Current Status

The project is in active development.

Implemented:

* Domain model for Board, Section, and Task
* Markdown parser with metadata support
* Duration parsing
* Task status model
* Analytics engine
* Review service
* Golden tests and domain invariant tests

Current test status:

* 92 passing tests

## Core Principles

### Local-First

All data is stored in plain Markdown files.

No database is required.

### Human-Readable Source of Truth

The Kanban board remains editable by both humans and AI systems.

### Strong Domain Model

The system uses explicit domain entities:

* Board
* Section
* Task

instead of manipulating raw Markdown structures.

### Deterministic Analytics

Analytics are calculated from board data using deterministic rules.

The system avoids hidden state and opaque calculations.

## Repository Structure

```text
src/
├── parser/
│   ├── models.py
│   └── parser.py
│
├── analytics/
│   ├── models.py
│   ├── service.py
│   └── calculators/
│       ├── status_metrics.py
│       ├── time_metrics.py
│       └── score_metrics.py
│
├── review/
│
└── ...
```

## Domain Model

### Task

A task contains:

* title
* status
* section
* score
* due date
* scheduled date
* completion date
* time estimate
* tags
* metadata
* archive state

Domain helpers:

* is_active
* is_actionable
* is_completed
* is_done
* score_value

### Section

Logical grouping of tasks.

### Board

Top-level domain object representing the entire Kanban board.

## Analytics

The analytics layer is organized into independent calculators.

### Status Metrics

* active_tasks
* completed_tasks
* cancelled_tasks
* delegated_tasks
* scheduled_tasks
* archived_tasks

### Time Metrics

* overdue_tasks
* due_today_tasks
* due_next_3_days_tasks

### Score Metrics

* tasks_without_score
* total_score
* active_score

## Testing

The project uses pytest.

Test categories include:

* parser tests
* golden tests
* analytics tests
* domain invariant tests
* review tests

The goal is to maintain a highly testable and deterministic core.

## Development Roadmap

### 1. Board-Centric Analytics

Move analytics from task collections toward board-level analysis.

Target direction:

```python
calculate_board_metrics(board: Board)
```

This will allow analytics to leverage board metadata, sections, and future board-level signals.

### 2. Execution Metrics

Add execution-focused analytics such as:

* completed_score
* completion_rate
* completion_velocity

These metrics will support daily and weekly execution reviews.

### 3. Analytics Architecture Consolidation

Review and consolidate legacy analytics modules.

Goal:

* one analytics architecture
* calculators as the primary extension mechanism
* reduced duplication

### 4. Review Intelligence

Expand review workflows using deterministic metrics produced by the analytics layer.

Focus areas:

* daily review
* weekly review
* execution bottlenecks
* overload detection

### 5. Analytics Signal Model

Implement the canonical analytics signals defined in the project documentation.

Examples:

* workload signals
* execution signals
* score signals
* health indicators

## Long-Term Vision

Kanban Execution System aims to become a local-first execution operating system that combines:

* structured task management
* deterministic analytics
* review workflows
* AI-assisted decision support

while keeping Markdown as the primary source of truth.