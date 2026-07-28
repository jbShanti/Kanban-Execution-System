# Canonical Operating Principles

## Purpose

Kanban Execution System (KES) is a personal execution system that turns a Kanban board into an operational aid for clarity, continuity, and deliberate action. It exists to reduce cognitive overload, preserve momentum, externalize operational complexity, and prevent chaos from accumulating.

This document defines the operating principles, safety boundaries, and human protocols of KES. It is deliberately separate from [ARCHITECTURE.md](ARCHITECTURE.md): architecture defines ownership and data flow; this document defines why the system exists and how it must behave.

## Core objectives

KES optimizes for:

- clarity;
- execution continuity;
- leverage;
- cognitive sustainability;
- operational stability; and
- low-chaos workflows.

KES is an execution co-pilot and operational assistant. It is not an autonomous governor, a replacement for human judgment, an AGI system, or a generic task manager.

## Operating principles

- Clarity over complexity.
- Execution over endless planning.
- Leverage over raw effort.
- Stability over intensity.
- Simplicity over feature count.
- Completion over perfection.
- Automation only after the process is understood.

Every capability must reduce friction, cognitive load, unnecessary decisions, or operational chaos. If it does not provide measurable execution value, simplify, remove, or reject it.

## Human authority and AI boundaries

Humans retain authority for strategic direction, priorities, irreversible life decisions, task deletion, project-structure changes, architecture changes, and automation escalation.

AI or deterministic assistance may analyse, structure information, identify overload, suggest simplifications, generate reports, and support execution. It must not override human judgment, redefine strategy autonomously, create uncontrolled automation, create dependency loops, or add complexity without execution value.

An approved automation may generate reports, update derived metrics, create summaries, or archive completed recurring tasks only under explicit safety controls. Any material mutation outside these rules requires human approval.

## Execution doctrine

- One completed task is more valuable than many open loops.
- The smallest executable step comes first.
- Visible progress matters.
- Action generates clarity.
- Systems support execution; they never replace it.

The active-context rule is one primary direction and at most two or three secondary contexts. A new context requires completion, pause, or explicit replacement of an existing one.

## Cognitive protocols

### Cognitive overload

When fragmentation, paralysis, excessive open loops, or chaos accumulation appear:

1. capture everything into the inbox;
2. structure the situation;
3. identify the primary direction;
4. remove secondary complexity; and
5. return to the smallest executable action.

### Context collapse

When too many directions or constant switching prevent completion:

1. stop intake;
2. freeze secondary contexts;
3. retain one primary direction and one or two secondary contexts;
4. identify the smallest executable step; and
5. resume single-task execution.

### Analysis paralysis

1. Determine whether the decision is reversible.
2. Reduce the required certainty.
3. Choose the smallest viable action.
4. Limit analysis time.
5. Move into execution.

### Recovery mode

During burnout symptoms, exhaustion, sustained overload, or energy crashes, avoid optimization, major decisions, new systems, and unnecessary intake. Focus on baseline restoration, essential execution, reduced commitments, and lower complexity.

### Focus reset

1. Clear the active context.
2. Define the current priority.
3. Define the next executable step.
4. Remove unnecessary inputs.
5. Return to focused execution.

## Review practices

### Daily review

The daily review recalibrates execution and reduces chaos. It asks what created progress or friction, what caused overload, which open loops remain, what can be simplified, and what matters next. Before ending the day, unload loose thoughts, close unnecessary contexts, update the board, define the next-day priority, and clear cognitive residue.

### Weekly review

The weekly review provides strategic recalibration. It examines leverage, noise, complexity accumulation, bottlenecks, energy drains, and candidates for operationalization, archiving, or removal. Its outputs are priorities, active contexts, paused directions, simplifications, and strategic adjustments.

## Operational board rules

The Obsidian board is the system source of truth for tasks, projects, knowledge, and machine-readable metadata. Task syntax, metadata semantics, statuses, archive handling, and parser constraints are defined exclusively by:

- `docs/Models/Task_Model.md`; and
- `docs/Models/METADATA_STANDARDS.md`.

At a policy level, subtasks are excluded from high-level analytics, archive sections are excluded from active metrics, and metadata must remain machine-readable. The board should favour stable hierarchy, consistent task formatting, predictable metadata placement, and minimal decorative syntax.

## Knowledge flow

```text
Capture -> Processing -> Structuring -> Operationalization -> Execution -> Review -> Archive
```

Capture first and organize later. Operational value is more important than information quantity. Knowledge should support execution, and low-value information may be archived or removed rather than accumulated.

## Safety, failure modes, and default action

KES must remain understandable and maintainable. Warning signs include endless optimization, automation bloat, context fragmentation, maintenance overload, excessive abstraction, AI dependency, and execution displacement. When they appear, reduce scope, simplify aggressively, and return to execution.

If the appropriate next action is unclear:

1. reduce chaos;
2. simplify;
3. identify the primary direction;
4. define the smallest executable step; and
5. return to execution.

The system succeeds when it reduces cognitive load and operational friction, improves execution continuity, prevents chaos accumulation, supports sustained execution, and remains maintainable and understandable.
