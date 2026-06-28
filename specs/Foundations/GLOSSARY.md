# GLOSSARY

## Purpose

This glossary defines the canonical vocabulary of the Kanban Execution System (KES).

The purpose of the glossary is to ensure that specifications, documentation, analytics, automations, and future agents use the same terms with the same meanings.

If a term is defined here, all other documents should use that definition consistently.

In case of ambiguity, the definitions in this document prevail unless overridden by SYSTEM BOUNDARIES.md.

---

# Core Concepts

## Kanban Execution System (KES)

A specification-driven execution system built around a Kanban board.

KES combines:

- task management;
- execution workflows;
- metadata standards;
- analytics;
- review protocols;
- automation.

The primary goal of KES is effective execution rather than organization.

---

## Execution

The process of converting commitments into completed outcomes.

Execution is the central concern of KES.

The system exists to improve execution quality, consistency, and predictability.

---

## Commitment

Anything the user has implicitly or explicitly agreed to do, maintain, decide, monitor, or achieve.

Commitments may exist as tasks, projects, responsibilities, routines, or obligations.

---

## Work

Any activity that consumes time, energy, attention, or resources.

Work may or may not contribute to meaningful outcomes.

---

## Outcome

A completed result that creates value or fulfills a commitment.

Tasks exist to contribute to outcomes.

---

# Board Concepts

## Board

The operational workspace used to manage execution.

The board provides a structured representation of commitments and work in progress.

---

## Column

A workflow state represented on the board.

Columns define where work currently exists in the execution process.

Examples:

- Inbox
- Next
- Doing
- Waiting
- Done

Specific column names may vary.

---

## Workflow

The set of rules governing how work moves through the board.

Workflow defines valid transitions between states.

---

## State

A specific stage within the lifecycle of a task.

A state represents the current execution status of the task.

---

## Work In Progress (WIP)

All tasks that currently consume attention, effort, or resources.

WIP should be actively managed to reduce overload and context switching.

---

# Task Concepts

## Task

The smallest executable unit of work managed within KES.

A task should represent a meaningful action that can be executed and evaluated.

Tasks are the primary operational entities of the system.

---

## Project

A collection of related tasks intended to achieve a specific outcome.

Projects organize work that cannot be completed through a single task.

---

## Subtask

A task derived from another task.

Subtasks exist to simplify execution of larger tasks.

---

## Action

A concrete activity that can be performed.

Actions are the operational content of tasks.

---

## Next Action

The next executable step required to move work forward.

A task should ideally have a clearly identifiable next action.

---
# Modeling Concepts

## Parser Model

A **Parser Model** defines how information is represented in source files and how it is parsed into structured data.

Parser Models specify syntax, formatting rules, metadata conventions, and parsing behavior. They do not define business logic or analytical behavior.

Parser Models are the boundary between external representations (such as Markdown) and the internal models used by the Kanban Execution System.

---

## Domain Model

A **Domain Model** defines the canonical business entities of the Kanban Execution System, together with their properties, relationships, and invariants.

Domain Models represent the persistent state of the system independently of storage format, analytics, or presentation.

They serve as the single source of truth for all higher-level system components.

---

## Analytics Model

An **Analytics Model** defines deterministic analytical objects that derive measurements from the Domain Model.

Analytics Models specify analytical inputs, calculation rules, metrics, and interpretation without modifying the underlying Domain Model.

They transform domain state into measurable insights that can be consumed by reports and recommendation engines.

---

## Report Model

A **Report Model** defines the structure of analytical output presented to the user.

Report Models organize analytical results into human-readable sections such as Executive Summary, Findings, Recommendations, statistics, and supporting evidence.

They represent the presentation layer of analytics and are derived entirely from Analytics Models without introducing additional business logic.

---

## Service Contract

A **Service Contract** defines the structure and semantics of data exchanged between system components or services.

Service Contracts specify the expected input and output of a component while remaining independent of implementation details.

They enable stable communication between parsers, validators, analytics, automation, and reporting components.

---

## Snapshot

A **Snapshot** is an immutable representation of the Domain Model captured at a specific point in time.

Snapshots provide a stable input for analytical processing, ensuring that all calculations operate on a consistent system state regardless of subsequent changes.

Snapshots are transient analytical artifacts and are not part of the persistent Domain Model.


---
# Organizational Concepts

## Area

A long-term responsibility that requires ongoing maintenance.

Areas do not have completion dates.

Examples:

- Health
- Career
- Finance
- Relationships

---

## Domain

A conceptual part of the system with a specific responsibility.

Examples:

- Task Management
- Metadata
- Analytics
- Automation

Domains help structure specifications.

---

## Context

Relevant information required to understand or execute work.

Context may include:

- projects;
- responsibilities;
- history;
- constraints;
- priorities.

---

# Metadata Concepts

## Metadata

Structured information attached to a task.

Metadata describes a task but is not the task itself.

Examples:

- priority;
- effort;
- due date;
- project;
- area.

---

## Required Metadata

Metadata fields that must exist for a task to comply with system standards.

---

## Optional Metadata

Metadata that may improve execution quality but is not mandatory.

---

## Validation

The process of determining whether a task complies with defined standards.

---

# Analytics Concepts

## Analytics

The process of evaluating execution using structured observations and metrics.

Analytics exist to improve decision making.

---

## Metric

A measurable property used to evaluate system performance.

Examples:

- completion rate;
- throughput;
- WIP level.

---

## Insight

A meaningful observation derived from analytics.

Insights explain what is happening.

---

## Recommendation

A suggested action generated from an insight.

Recommendations suggest what should happen next.

---

## Bottleneck

A constraint that limits execution effectiveness.

Bottlenecks may exist in workflow, priorities, resources, or attention.

---

# Review Concepts

## Review

A structured process used to evaluate commitments, work, and execution quality.

Reviews are one of the primary feedback mechanisms within KES.

---

## Morning Review

A review focused on planning and prioritization for the current day.

---

## Evening Review

A review focused on evaluating completed work and execution quality.

---

## Weekly Review

A review focused on strategic alignment and system maintenance.

---

## Monthly Review

A review focused on long-term direction, trends, and outcomes.

---

# Automation Concepts

## Automation

A process performed automatically according to predefined rules.

Automation executes specifications but does not define them.

---

## Agent

A software entity capable of performing actions within defined boundaries.

Agents operate under KES rules and constraints.

---

## Autonomous Assistance

Agent behavior that supports execution without replacing human decision-making authority.

---

## Human Authority

The principle that the user remains the final decision maker.

No automation or agent may override human judgment.

---

# Specification Concepts

## Specification

A formal description of system behavior, structure, or constraints.

Specifications define how KES operates.

---

## Canonical Source

The authoritative document for a specific topic.

When multiple documents conflict, the canonical source prevails.

---

## Implementation

A practical realization of one or more specifications.

Implementations may include:

- prompts;
- scripts;
- software;
- automations;
- agents.

Implementations must conform to specifications.

---

## Compliance

The degree to which an implementation follows the specifications.

Compliance is required for all components of KES.

---

# Guiding Principle

Every concept within KES ultimately exists to support one objective:

**Convert commitments into completed outcomes with the minimum possible cognitive overhead while preserving clarity, control, and intentionality.**