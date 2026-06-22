# Kanban Execution System (KES)

## Purpose

Kanban Execution System (KES) is a local-first Markdown Kanban analysis system.

The system treats Markdown Kanban boards as the single source of truth and provides:

- deterministic parsing of Kanban boards
- structured domain models
- board analytics
- board health evaluation
- analytical reporting foundations

KES is designed to evolve into a complete execution analysis platform while preserving Markdown as the canonical data format.

---

# Current Repository Status

This section describes the actual implementation state of the repository.

## Implemented

### Domain Layer

- Board model
- Section model
- Task model
- Task status model

### Parser Layer

- Markdown board parsing
- Section detection
- Task extraction
- Metadata extraction
- Due date parsing
- Score parsing
- Tag parsing
- Duration parsing

### Analytics Foundation

- Board metrics
- Section metrics
- Task metrics
- WIP metrics
- Board health metrics
- Score corridor metrics
- Overload detection foundations

### Reporting Foundation

- Analytics report models
- Review/report infrastructure foundations

### Test Infrastructure

- Parser tests
- Analytics tests
- Golden tests
- Invariant tests

---

## Partially Implemented

### Analytics Model V2 Migration

Some structures defined in Analytics_Model_v2 are present.

The complete analytics pipeline has not yet been implemented.

---

## Not Implemented

### Recommendation Engine

The repository does not currently generate recommendations.

### Safe Automation Layer

The repository does not modify boards automatically.

### Autonomous Execution Workflows

No autonomous task management or execution logic currently exists.

---

# Specification Hierarchy

All contributors and LLM agents must follow this hierarchy.

When conflicts exist between documents, the higher-priority document wins.

---

## Priority 1 — Canonical System Specification

### KANBAN_EXECUTION_SYSTEM.md

Defines:

- system philosophy
- architectural boundaries
- system goals
- roadmap
- long-term architecture

This document is the primary source of truth.

---

## Priority 2 — Domain Specifications

### Task_Model.md

Defines:

- task schema
- task lifecycle
- task invariants
- board structure expectations

### METADATA_STANDARDS.md

Defines:

- metadata syntax
- metadata typing
- metadata validation rules
- metadata interpretation

---

## Priority 3 — Analytics Specification

### Analytics_Model_v2.md

Defines:

- analytics contracts
- analytics outputs
- analytics pipeline
- report structure
- executive summary structure

---

## Priority 4 — System Boundaries

### SYSTEM BOUNDARIES.md

Defines:

- forbidden behaviors
- mutation restrictions
- safety requirements
- automation limits

---

## Priority 5 — Implementation

Source code reflects the current implementation state.

Implementation may lag behind specifications.

When implementation conflicts with specifications:

**Specifications are authoritative.**

---

# Operating Principles

All contributors and LLM agents must follow these principles.

## Principle 1 — Markdown is the Source of Truth

Markdown files are authoritative.

Generated artifacts are derived data.

No generated artifact may become the primary source of truth.

---

## Principle 2 — Deterministic First

Before introducing AI behavior:

1. Parse deterministically.
2. Analyze deterministically.
3. Validate deterministically.

AI layers must consume deterministic outputs.

---

## Principle 3 — Analysis Before Recommendation

The system roadmap is:

```text
Markdown
↓
Parser
↓
Domain Model
↓
Analytics
↓
Executive Summary
↓
Recommendations
↓
Automation
```

A later layer must never be implemented before the previous layer is stable.

---

## Principle 4 — Safety Before Automation

Automation is the final stage of the roadmap.

No automatic board modification should be introduced before:

- parser compliance
- analytics stability
- recommendation validation

have been completed.

---

# Repository Structure

Current high-level structure:

```text
repository/
│
├── src/
│   ├── parser/
│   ├── analytics/
│   └── ...
│
├── tests/
│
├── README.md
│
├── KANBAN_EXECUTION_SYSTEM.md
├── TASK_MODEL.md
├── METADATA_STANDARDS.md
├── ANALYTICS_MODEL_V2.md
└── SYSTEM BOUNDARIES.md
```

---

# Current Domain Model

Current implementation is centered on three primary entities.

```text
Board
 └── Section
      └── Task
```

## Board

Represents an entire Kanban board.

Contains:

- sections
- board metadata

---

## Section

Represents a logical board section.

Examples:

- Inbox
- Today
- Doing
- Waiting
- Archive

Contains:

- tasks
- section metadata

---

## Task

Represents a single actionable item.

Current implementation supports:

- title
- status
- score
- due date
- tags
- duration
- metadata

---

# Current Parser Capabilities

## Supported

The parser currently supports:

- task status parsing
- section parsing
- metadata extraction



Supported metadata:

- score
- due
- time_estimate (task duration estimate)
- start
- scheduled
- completion
- priority
- repeat
- category
- finance
- cost
- currency
- analytics
- tags

---

# Current Analytics Capabilities

## Implemented

### Board Analytics

- board metrics
- board health metrics
- score aggregation

### Task Analytics

- task metrics
- score metrics

### Execution Analytics

- WIP metrics
- overload detection

### Corridor Analytics

- score corridor evaluation

---

## Planned

Analytics_Model_v2 defines future analytics domains:

### Focus Analytics

Examples:

- overdue analysis
- due-today analysis
- attention analysis

### Tactical Analytics

Examples:

- workload analysis
- execution pressure
- waiting analysis

### Strategic Analytics

Examples:

- value concentration
- execution debt
- long-term board health

### Executive Summary

Human-readable analytical synthesis.

---

# Development Roadmap

This roadmap is intended to guide both human developers and LLM agents.

Each phase should be completed before the next phase begins.

---

## Phase 0 — Documentation Alignment

Goal:

Align repository documentation with actual implementation.

Deliverables:

- updated README
- updated roadmap
- documented specification hierarchy

Success Criteria:

A new contributor can understand repository state without external context.

---

## Phase 1 — Parser Compliance (completed)

Goal:

Achieve compliance with Task_Model and Metadata_Standards.

Success Criteria:

All canonical metadata fields are parsed into domain models.

---

## Phase 2 — Analytics Model V2 Foundation (in progress)

Goal:

Introduce analytics snapshots and analytics context.

Target Pipeline:

```text
Tasks
↓
AnalyticsTaskSnapshot
↓
Analytics Context
↓
Analytics Report
```

Success Criteria:

Analytics no longer operate directly on raw task collections.

---

## Phase 3 — Focus Analytics

Implement:

- overdue analysis
- due today analysis
- upcoming analysis
- attention scoring
- focus scoring

Source:

Analytics_Model_v2.md

---

## Phase 4 — Tactical Analytics

Implement:

- workload analysis
- WIP pressure analysis
- execution pressure
- waiting analysis
- velocity analysis

Source:

Analytics_Model_v2.md

---

## Phase 5 — Strategic Analytics

Implement:

- value concentration
- score distribution
- execution debt
- strategic board health

Source:

Analytics_Model_v2.md

---

## Phase 6 — Executive Summary

Goal:

Generate deterministic analytical summaries.

Pipeline:

```text
Analytics
↓
Executive Summary
```

Recommendations are explicitly out of scope.

---

## Phase 7 — Recommendation Engine

Goal:

Generate recommendations from analytics outputs.

Pipeline:

```text
Analytics
↓
Executive Summary
↓
Recommendations
```

Recommendations must consume analytics outputs rather than raw tasks.

---

## Phase 8 — Safe Automation Layer

Goal:

Introduce controlled board modifications.

Must comply with:

- KANBAN_EXECUTION_SYSTEM.md
- SYSTEM BOUNDARIES.md

Automation is not allowed before earlier phases are complete.

---

# Rules for LLM Agents

When working in this repository:

1. Read the specification hierarchy first.
2. Determine current implementation state before proposing changes.
3. Do not assume planned features already exist.
4. Prefer deterministic implementations over AI-driven implementations.
5. Do not introduce automation before roadmap completion.
6. Treat Markdown as the canonical data source.
7. Update tests alongside implementation changes.
8. Preserve backward compatibility unless specifications explicitly require otherwise.

If uncertain:

- trust specifications over implementation;
- trust higher-priority specifications over lower-priority specifications.